#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  8/31/2021 9:42 PM
@Desc    :  Tools line.
"""
import base64
import configparser
import datetime
import platform
import re
import smtplib
import socket
import subprocess
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from multiprocessing import Process

import ntplib
import pytest
import pytz
import requests
import urllib3.exceptions
from airtest.core.android.adb import ADB
from airtest.core.android.recorder import Recorder
from airtest.core.api import *
from airtest.core.error import AdbShellError
from loguru import logger
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed
from tqdm import tqdm

from utx.core.css.custom_report import gen_report


adb = ADB.builtin_adb_path()


@retry(wait=wait_fixed(10), stop=stop_after_attempt(3))
def get_net_time(timezone="Asia/Shanghai", formatting="%Y-%m-%d %H:%M:%S"):
    """
    get beijing time
    :param timezone: Asia/Shanghai
    :param formatting: %Y-%m-%d %H:%M:%S
    :return:
    """

    # create a timezone for beijing
    beijing_tz = pytz.timezone(timezone)

    # from ntp server get utc time
    c = ntplib.NTPClient()
    response = c.request("pool.ntp.org")
    utc_dt = datetime.datetime.fromtimestamp(response.tx_time, pytz.utc)

    # convert utc time to beijing time
    beijing_dt = utc_dt.astimezone(beijing_tz)

    # return beijing time
    return beijing_dt.strftime(formatting)


@logwrap
@retry(wait=wait_fixed(10), stop=stop_after_attempt(3))
def customs_install(apk_path, **kwargs):
    """
    Install APK with install_options
    :param apk_path: Path to the APK file
    :param kwargs: Optional parameters
                   - install_options: List of installation options
                   - timeout: Command timeout in seconds, default is 120 seconds
    :return: None
    """
    serialno = device().serialno
    install_options = kwargs.get("install_options", [])
    timeout = kwargs.get("timeout", 120)

    # If install_options is None, set it to an empty list
    if install_options is None:
        install_options = []

    install_options_str = " ".join(install_options)

    command = f"{adb} -s {serialno} install {install_options_str} {apk_path}"
    log(command)

    # Check if timeout is an integer
    if not isinstance(timeout, int):
        raise ValueError("Timeout must be an integer.")

    # Execute the command and capture standard output and error streams
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    try:
        stdout, stderr = process.communicate(timeout=timeout)
        log(stdout)
        log(stderr)
    except subprocess.TimeoutExpired:
        # If the command times out, kill the process and raise an exception
        process.kill()
        log("adb install command timed out")
        raise Exception("adb install command timed out")

    if process.returncode != 0:
        log("adb install command failed")
        raise Exception("adb install command failed")


@logwrap
def set_ime(ime="com.netease.nie.yosemite/.ime.ImeService"):
    """
    Set default none gui ime
    :param ime: com.netease.nie.yosemite/.ime.ImeService
    :return: None
    """
    shell("ime enable " + ime)
    shell("ime set " + ime)


@logwrap
def get_apk(path=None, mark=".apk"):
    """
    Unzip the ZIP file and get the APK file
    :param path: apk_64.zip
    :param mark: .apk
    :return:
    """
    import zipfile
    import os

    # Unzip the ZIP file
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall("unzip_apk")
    # Switch to the unzipped folder
    os.chdir("unzip_apk")
    # Search for files ending in .apk
    import glob

    for file in glob.glob(f"*{mark}"):
        target = os.path.join(os.getcwd(), file)
        return target


@logwrap
def reboot():
    """
    Reboot device
    :return:
    """
    serialno = device().serialno
    ADB(serialno=serialno).cmd(cmds="reboot")
    log(f"Device {serialno} has been restarted!")


def allure_report(report_path, report_html):
    """
    Generate allure Report
    :param report_path:
    :param report_html:
    :return:
    """
    # execution allure generate
    allure_cmd = f"allure generate {report_path} -o {report_html} --clean"
    try:
        subprocess.call(allure_cmd, shell=True)
    except Exception:
        logger.error(
            "The generation of allure report failed. Please check the relevant configuration of the test "
            "environment"
        )
        raise


def plat():
    """
    Check the current script running platform
    :return:'Linux', 'Windows' or 'Darwin'.
    """
    return platform.system()


@logwrap
def check_port(port):
    """
    Detect whether the port is occupied and clean up
    :param port:System port
    :return:None
    """
    if plat() != "Windows":
        os.system("lsof -i:%s| grep LISTEN| awk '{print $2}'|xargs kill -9" % port)
    else:
        port_cmd = f"netstat -ano | findstr {port}"
        r = os.popen(port_cmd)
        if len(r.readlines()) == 0:
            return
        else:
            pid_list = []
            for line in r.readlines():
                line = line.strip()
                pid = re.findall(r"[1-9]\d*", line)
                pid_list.append(pid[-1])
            pid_set = list(set(pid_list))[0]
            pid_cmd = f"taskkill -PID {pid_set} -F"
            os.system(pid_cmd)


def cleanup():
    """
    cleanup device wda process
    :return:
    """
    pid_list = []
    cmd = decryption(b"dGlkZXZpY2U=")
    sub = subprocess.Popen(
        f"{cmd} ps", shell=True, close_fds=True, stdout=subprocess.PIPE
    )
    sub.wait()
    pid_info = sub.stdout.read().decode().splitlines()
    for u in pid_info:
        if "WebDriverAgentRunner" in u:
            pid_list.append(u.strip().split(" ")[0])
    [os.system(f"{cmd} kill {pid}") for pid in pid_list]


def display():
    """
    Gets the length and width of the current device
    :return:
    """
    width, height = device().get_current_resolution()
    return width, height


def device_udid(state, types: str):
    """
    Perform `adb devices` command and return the list of adb devices
    Perform `utx list` command and return the list of iphone devices
    :param types: mobile platform
    :param state: optional parameter to filter devices in specific state
    :return: list od android devices or ios devices
    """
    device_list = []
    if types.lower() == "android":
        patten = re.compile(r"^[\w\d.:-]+\t[\w]+$")
        output = ADB().cmd("devices", device=False)
        for line in output.splitlines():
            line = line.strip()
            if not line or not patten.match(line):
                continue
            serialno, cstate = line.split("\t")
            if state and cstate != state:
                continue
            device_list.append(serialno)
    elif types.lower() == "ios":
        # Get the udid list of the connected mobile phone
        sub = subprocess.Popen(
            "utx list", shell=True, close_fds=True, stdout=subprocess.PIPE
        )
        sub.wait()
        udid = sub.stdout.read().decode().splitlines()
        for u in udid:
            us = u.strip().split(" ")[0]
            if us != "UDID":
                device_list.append(us)
    return device_list


def ios_device_info():
    """
    Gets device_info of the current device

    :return:
    """
    res = subprocess.run(
        "{} info".format(decryption(b"dGlkZXZpY2U=")), shell=True, capture_output=True
    )
    lines = res.stdout.decode("utf-8", "ignore")
    device_info = [info for info in lines.split("\n") if info]
    _device = {}
    if len(device_info) < 2:
        logger.error(f"Read device info line error. {lines}")
    for info in device_info:
        info_kv = info.split(":")
        if info_kv[0] == "ProductVersion":
            _device["ProductVersion"] = info_kv[1].strip()
        if info_kv[0] == "MarketName":
            _device["MarketName"] = info_kv[1].strip()
        if info_kv[0] == "SerialNumber":
            _device["SerialNumber"] = info_kv[1].strip()
    return _device


def get_report(airtest_report_path):
    """
    Get the latest test report path
    :return: report name and path
    """
    file_lists = os.listdir(airtest_report_path)
    file_lists.sort(
        key=lambda fn: os.path.getmtime(airtest_report_path + "/" + fn)
        if not os.path.isdir(airtest_report_path + "/" + fn)
        else 0
    )
    report = os.path.join(airtest_report_path, file_lists[-1])
    print(file_lists[-1])
    return report


def encryption(value):
    """
    encryption
    https://cdn.jsdelivr.net/gh/openutx/static/
    :param value:
    :return:
    """
    bytes_url = value.encode("utf-8")
    str_url = base64.b64encode(bytes_url)
    return str_url


def decryption(value):
    """
    decryption
    https://cdn.jsdelivr.net/gh/openutx/static/
    :param value:
    :return:
    """
    str_url = base64.b64decode(value).decode("utf-8")
    return str_url


def str_to_bool(value):
    """
    str convert bool
    :param value:
    :return:
    """
    return True if value.lower() == "true" else False


def find_all_cases(base, status, mark):
    """
    Find all test cases
    :param base:
    :param status:
    :param mark:
    :return:
    """
    for root, ds, fs in os.walk(base, topdown=True):
        if status in ["0", False]:
            for f in ds:
                if f.endswith(".air") and mark in f:
                    fullname = os.path.join(root, f)
                    yield fullname
        else:
            for f in ds:
                if f.endswith(".air"):
                    fullname = os.path.join(root, f)
                    yield fullname


def get_host_ip():
    """
    Query the local ip address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def proxy(devices, status=True):
    """
    Android proxy
    :param devices:
    :param status: on or off
    :return:
    :platforms: Android
    """
    if status:
        proxy_cmd = f"{adb} -s {devices} {decryption(b'c2hlbGwgc2V0dGluZ3MgcHV0IGdsb2JhbCBodHRwX3Byb3h5')} {get_host_ip()}:8888"
        logger.info(f"Successfully enabled {devices} global proxy！")
        os.system(proxy_cmd)
    else:
        proxy_cmd = f"{adb} -s {devices} {decryption(b'c2hlbGwgc2V0dGluZ3MgcHV0IGdsb2JhbCBodHRwX3Byb3h5IDow')}"
        logger.info(f"Close the {devices} global proxy successfully！")
        os.system(proxy_cmd)


def selector(status, flag, cases_list):
    """
    Find all test cases
    :param status:
    :param flag:
    :param cases_list:
    :return:
    """
    cases = []
    if status in ["0", False]:
        for suite in cases_list:
            if flag in suite:
                if suite.endswith(".air"):
                    cases.append(suite)
    else:
        for suite in cases_list:
            if suite.endswith(".air"):
                cases.append(suite)
    if len(cases) == 0:
        pytest.xfail("No test case found, please check the path!")
        return cases


def selector_v2(path, status, mark):
    """
    Find all test cases
    :param path:
    :param status:
    :param mark:
    :return:
    """
    cases = []
    for i in find_all_cases(path, status, mark):
        print(i)
        cases.append(i)
    if len(cases) == 0:
        warning_report = os.path.join(path.split("suites")[0], "report", "airtest")
        gen_report(
            results=[
                {
                    "result": [
                        "warning_report",
                        "Warning: No test case found, please check the path!",
                    ]
                }
            ],
            report_path=warning_report,
        )
        pytest.xfail("No test case found, please check the path!")
    return sorted(cases)


def selector_v3(path: str, status, mark):
    """
    Find all test cases
    :param path:
    :param status:
    :param mark:
    :return:
    """
    cases = []
    base_path = path.split(path.split("/")[-1])[0]
    path_list = "".join(str(path).split()[0].split("/")[-1]).split(",")
    for item in path_list:
        for i in find_all_cases(base_path + item, status, mark):
            print(i)
            cases.append(i)
    if len(cases) == 0:
        pytest.xfail("No test case found, please check the path!")
    return sorted(cases)


def download(file_url, types):
    """
    Download file
    :param types:
    :param file_url:
    :return:
    """
    file_url = urllib.parse.unquote(file_url)
    if "http" not in file_url:
        return
    download_url = "http" + file_url.split("http")[-1]
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    r = requests.get(download_url, stream=True, verify=False)
    total = int(r.headers.get("content-length", 0))
    filename = "{}utx_download_{}.{}".format(
        file_url.split("http")[0], int(round(time.time() * 1000)), types
    )

    with open(filename, "wb") as file, tqdm(
        desc=filename,
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in r.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

    return filename


def start_recording(max_time=1800):
    """
    Start recording
    :param max_time:
    :return:
    """
    serialno = device().serialno
    model = ADB(serialno=serialno)
    recorder = Recorder(model)
    recorder.start_recording(max_time=max_time)


def stop_recording(file, name=None):
    """
    Stop recording
    :param file: __file__
    :param name: mp4 name
    :return: video file
    """
    serialno = device().serialno
    model = ADB(serialno=serialno)
    build_version = shell("getprop ro.build.version.release")
    dev = model.get_model() + f" Android {build_version}".replace("\n", "").replace(
        "\r", ""
    )
    recorder = Recorder(model)
    if not name:
        name = str(file).split("/")[-1].split(".")[0]
    output_path = os.path.join(str(file).split(".air")[0] + ".air", "log", dev, name)
    recorder.stop_recording(output=f"{output_path}.mp4")


def go(url):
    """
    Go to the target page
    :param url: app custom short url
    :return: target page
    """
    shell(f"am start -a android.intent.action.VIEW -d '{url}'")
    log(desc="Open the url successfully!", arg=url, snapshot=True)


def check_network():
    """
    Check network connection
    :return:
    """
    try:
        result = shell("ping -c 1 www.baidu.com")
        logger.info(result)
        return True
    except AdbShellError as e:
        logger.error(e)
        return False


def proxy_dump():
    """
    proxy filter url address
    :return:
    """

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"Created file: {path}"
        print(msg)

    content = """#!/usr/bin/python
# encoding=utf-8

\"\"\" Can only be modified by the administrator. Only proxy are provided.
\"\"\"

from garbevents.capture import GetData

addons = [
    GetData()
]
"""
    create_file(os.path.join("proxy.py"), content)
    try:
        from garbevents.cli.main import mitmweb
        from garbevents.settings import Settings as ST

        # Check whether the port is occupied and clean up
        check_port(ST.server_port)
        mitmweb(
            args=[
                "-p",
                f"{ST.server_port}",
                "--ssl-insecure",
                "--web-host",
                f"{ST.web_host}",
                "--web-port",
                f"{ST.web_port}",
                "--no-web-open-browser",
                "-s",
                "proxy.py",
            ]
        )
    except (ImportError, AttributeError):
        logger.error("garbevents not installed, please run: pip install -U garbevents")
        return


def launcher(main, salve):
    """
    Process launcher
    :param main:
    :param salve:
    :return:
    """
    master = Process(target=main)
    salver = Process(target=salve)
    salver.daemon = True
    master.daemon = True
    salver.start()
    master.start()
    master.join()


class ReadConfig:
    """
    configuration file
    """

    def __init__(self, ini_path):
        self.ini_path = ini_path
        if not os.path.exists(ini_path):
            raise FileNotFoundError("Profile %s does not exist！" % ini_path)
        self.config = (
            configparser.RawConfigParser()
        )  # When there are% symbols, use raw to read
        self.config.read(ini_path, encoding="utf-8")

    def _get(self, section, option):
        """

        :param section:
        :param option:
        :return:
        """
        return self.config.get(section, option)

    def _set(self, section, option, value):
        """

        :param section:
        :param option:
        :param value:
        :return:
        """
        try:
            self.config.set(section, option, value)
        except configparser.NoSectionError as e:
            logger.error(e)
        with open(self.ini_path, "w") as f:
            self.config.write(f)

    def getvalue(self, env, name):
        return self._get(env, name)

    def update_value(self, env, name, value):
        return self._set(env, name, str(value).strip())


class SendMail:
    def __init__(
        self,
        report_path,
        receive_address,
        send_address_name,
        send_address_pwd,
        title="",
        receive=None,
    ):
        """

        :param report_path:
        :param receive_address:
        :param send_address_name:
        :param send_address_pwd:
        :param title:
        :param receive:
        """
        if receive is None:
            self.send_to = receive_address
        else:
            self.send_to = receive
        self.report_path = report_path
        self.receive_address = receive_address
        self.send_address_name = send_address_name
        self.send_address_pwd = send_address_pwd
        self.title = title

    def __get_report(self):
        dirs = os.listdir(self.report_path)
        dirs.sort()
        new_report_name = dirs[-1]
        print(f"The new report name: {new_report_name}")
        return new_report_name

    def __take_messages(self):
        new_report = self.__get_report()
        self.msg = MIMEMultipart()
        self.msg["Subject"] = self.title
        self.msg["date"] = time.strftime("%Y-%m-%d_%H-%M")

        with open(os.path.join(self.report_path, new_report), "rb") as f:
            mail_body = f.read()
        html = MIMEText(mail_body, _subtype="html", _charset="utf-8")
        self.msg.attach(html)

        att1 = MIMEText(mail_body, "base64", "gb2312")
        att1["Content-Type"] = "application/octet-stream"
        att1["Content-Disposition"] = 'attachment; filename="utx_summary.html"'
        self.msg.attach(att1)

    def send(self):
        self.__take_messages()
        self.msg["from"] = self.send_address_name
        # ",,,,"
        self.msg["to"] = self.receive_address
        try:
            port = 465
            smtp = smtplib.SMTP_SSL("smtp.exmail.qq.com", port)
            smtp.login(self.send_address_name, self.send_address_pwd)
            smtp.sendmail(
                self.msg["from"], self.msg["to"].split(","), self.msg.as_string()
            )
            smtp.close()
            print("send success")
        except smtplib.SMTPException as e:
            print(e)
            print("send fail")
