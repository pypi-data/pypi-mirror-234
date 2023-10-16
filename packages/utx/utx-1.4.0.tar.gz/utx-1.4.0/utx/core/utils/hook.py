#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  9/14/2021 3:36 PM
@Desc    :  Hook line.
"""
import logging
import random
from logging import getLogger

import allure
import pytest
from airtest.core.api import *
from airtest.core.error import AdbError
from airtest.core.error import DeviceConnectionError
from airtest.core.helper import device_platform
from airtest.core.helper import ST
from popups.dismiss import popup
from popups.dismiss import UT
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tenacity import Retrying
from tenacity import stop_after_attempt
from tenacity import wait_fixed
from wda import WDAError
from webdriver_manager.chrome import ChromeDriverManager

from utx.core.css.custom_report import gen_report
from utx.core.utils.tools import check_network
from utx.core.utils.tools import check_port
from utx.core.utils.tools import cleanup
from utx.core.utils.tools import customs_install
from utx.core.utils.tools import decryption
from utx.core.utils.tools import device_udid
from utx.core.utils.tools import display
from utx.core.utils.tools import download
from utx.core.utils.tools import plat
from utx.core.utils.tools import proxy
from utx.core.utils.tools import str_to_bool

os.environ["WDM_SSL_VERIFY"] = "0"
logger = getLogger(__name__)

ST.THRESHOLD = 0.7
ST.OPDELAY = 0.25
ST.FIND_TIMEOUT = 10
ST.FIND_TIMEOUT_TMP = 2
ST.SNAPSHOT_QUALITY = 10

# todo https://github.com/openutx/utx-pypi/issues/4
# 1.全部都截图，不管成功失败
# 2.只有失败才截图
# 3.配置化
ST.SAVE_IMAGE = True


def app_info(
    cli_platform,
    cli_device,
    cli_wda,
    cli_init,
    ini_platform,
    ini_device,
    ini_wda,
    ini_init,
):
    """

    :param cli_platform:
    :param cli_device:
    :param cli_wda:
    :param cli_init:
    :param ini_platform:
    :param ini_device:
    :param ini_wda:
    :param ini_init:
    :return: iOS:///127.0.0.1:8100
    """
    if cli_init in [None, ""]:
        is_init = str_to_bool(ini_init)
    else:
        is_init = str_to_bool(cli_init)
    if cli_wda in [None, ""]:
        web_driver_agent = ini_wda
        # web_driver_agent = "*WebDriverAgent*"
    else:
        web_driver_agent = cli_wda
        # web_driver_agent = "*WebDriverAgent*"
    # 改为通配符，避免传入错误 bundle_id 启动失败

    if cli_platform in [None, ""]:
        platform = ini_platform.lower()
        if platform in "android":
            device_idx = str(ini_device).split(",")
            device_uri = []
            for idx in device_idx:
                device_uri.append(
                    f"Android:///{idx}?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MAXTOUCH"
                )
            return device_uri, device_idx, is_init
        elif platform in "ios":
            device_idx = []
            device_uri = []
            for u in device_udid(types="ios", state=None):
                proxy_port = str(random.randint(50000, 60000) + 1)
                check_port(port=proxy_port)
                os.system(
                    "{} -u {} wdaproxy -B {} --port {} &".format(
                        decryption(b"dGlkZXZpY2U="), u, web_driver_agent, proxy_port
                    )
                )
                device_idx.append(f"127.0.0.1:{proxy_port}")
                device_uri.append(f"iOS:///127.0.0.1:{proxy_port}")
            return device_uri, device_idx, is_init

    elif cli_platform not in [None, ""]:
        if cli_platform.lower() in "android":
            device_idx = str(cli_device).split(",")
            device_uri = []
            for idx in device_idx:
                device_uri.append(
                    f"Android:///{idx}?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MAXTOUCH"
                )
            return device_uri, device_idx, is_init
        elif cli_platform.lower() in "ios":
            device_idx = []
            device_uri = []
            for u in device_udid(types="ios", state=None):
                proxy_port = str(random.randint(50000, 60000) + 1)
                check_port(port=proxy_port)
                os.system(
                    "{} -u {} wdaproxy -B {} --port {} &".format(
                        decryption(b"dGlkZXZpY2U="), u, web_driver_agent, proxy_port
                    )
                )
                device_idx.append(f"127.0.0.1:{proxy}")
                device_uri.append(f"iOS:///127.0.0.1:{proxy_port}")
            return device_uri, device_idx, is_init


def my_before_sleep(retry_state):
    """

    :param retry_state:
    :return:
    """
    if retry_state.attempt_number < 1:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING

    logging.log(
        loglevel,
        "Retrying %s: attempt %s ended with: %s",
        retry_state.fn,
        retry_state.attempt_number,
        retry_state.outcome,
    )


@allure.step("Try to link the device！")
def my_retry_connect(uri=None, whether_retry=True, sleeps=10, max_attempts=3):
    """

    :param uri:
    :param whether_retry:
    :param sleeps:
    :param max_attempts:
    :return:
    """
    if not whether_retry:
        max_attempts = 1

    r = Retrying(
        wait=wait_fixed(sleeps),
        stop=stop_after_attempt(max_attempts),
        before_sleep=my_before_sleep,
        reraise=True,
    )
    try:
        return r(connect_device, uri)
    except Exception as e:
        if isinstance(e, (WDAError,)):
            logger.info("Can't connect iphone, please check device or wda state!")
        logger.info(f"Try connect device {uri} 3 times per wait 10 sec failed.")
        raise e
    finally:
        logger.info(f"Retry connect statistics: {str(r.statistics)}")


@allure.step("Switch to current device！")
def ensure_current_device(device_idx):
    """

    :param device_idx:
    :return:
    """
    idx = device_idx
    try:
        if device().uuid != idx:
            set_current(idx)
    except IndexError:
        if device().uuid != f"http://{idx}":
            set_current(idx)


@allure.step("Try to wake up the current device！")
def wake_device(current_device):
    """

    :param current_device:
    :return:
    """
    try:
        current_device.wake()
        if current_device.is_locked():
            w, h = display()
            swipe((0.5 * w, 0.8 * h), (0.5 * w, 0.2 * h), duration=0.1)
        current_device.home()
    except AttributeError:
        pass


def app_fixture(
    request, device_uri, app_filepath, app_name, device_idx, init, agent=False
):
    """

    :param request: default param
    :param device_uri: device_uri
    :param app_filepath: app_filepath
    :param app_name: app_name
    :param device_idx: device udid
    :param init: initial install or uninstall
    :param agent: Proxy status is off by default
    :return: app
    """
    with allure.step("Initialize and generate APP object！"):
        logger.info("Session start test.")

        try:
            app = None
            if init:
                logger.info(
                    "Detected that the initialization is True and started installing the application！"
                )
                if str(device_uri[0]).startswith("iOS"):
                    if "http" in app_filepath:
                        app_pkg = download(file_url=app_filepath, types="ipa")
                    else:
                        app_pkg = app_filepath
                else:
                    if "http" in app_filepath:
                        app_pkg = download(file_url=app_filepath, types="apk")
                    else:
                        app_pkg = app_filepath
            for uri, idx in zip(device_uri, device_idx):
                app = my_retry_connect(uri)
                wake_device(G.DEVICE)
                if device_platform().lower() in "android":
                    if not check_network():
                        warning_report = os.path.join(
                            app_filepath.split("packages")[0], "report", "airtest"
                        )
                        gen_report(
                            results=[
                                {
                                    "result": [
                                        "warning_report",
                                        "Warning: The current device network is abnormal, please check it and run it again!",
                                    ]
                                }
                            ],
                            report_path=warning_report,
                        )
                        # todo: xfail is skip ,fail is fail. Lack of multi-device differentiation.
                        pytest.xfail(
                            f"The current device {idx} network is abnormal, please check it and run it again!"
                        )
                    if agent:
                        proxy(devices=idx, status=True)

                if init:
                    if str(uri).startswith("iOS"):
                        os.system(f"utx uninstall {app_name}")
                        os.system(f"utx install {app_pkg}")
                        UT.iOS = True
                    else:
                        try:
                            uninstall(app_name)
                        except AdbError:
                            pass
                        customs_install(app_pkg, install_options=["-g"])
                    stop_app(app_name)
                    sleep(2)
                    start_app(app_name)
                    sleep(2)
                    UT.LOOP = 2
                    UT.SYS = True
                    popup(devices=uri)
                else:
                    stop_app(app_name)
                    sleep(2)
                    start_app(app_name)
                    sleep(2)
        except Exception as e:
            if device_platform().lower() in "ios":
                cleanup()

            if device_platform().lower() in "android" and agent:
                for _ in device_idx:
                    proxy(devices=_, status=False)

            logger.error(f"Create app fail: {e}")
            allure.attach(
                body="",
                name=f"Create app fail: {e}",
                attachment_type=allure.attachment_type.TEXT,
            )
            warning_report = os.path.join(
                app_filepath.split("packages")[0], "report", "airtest"
            )
            gen_report(
                results=[
                    {"result": ["warning_report", f"Warning: Create app fail: {e}"]}
                ],
                report_path=warning_report,
            )
            pytest.xfail(f"Create app fail: {e}")

        assert app is not None

        ensure_current_device(device_idx[0])

        logger.info(f"Current test platform: {device_platform()}")
        logger.info(f"Start app {app_name} in {device_platform()}:{G.DEVICE.uuid}")

    def teardown_test():
        with allure.step("Teardown session"):
            try:
                stop_app(app_name)
            except DeviceConnectionError:
                pass

            # todo: Do not uninstall the installation package at the end of the execution
            #  which is convenient for troubleshooting.

            if device_platform().lower() in "ios":
                check_port(port=str(device_idx[0]).split(":")[1])
                cleanup()
                logger.info("Cleanup device wda process.")
            if device_platform().lower() in "android" and agent:
                for _ in device_idx:
                    proxy(devices=_, status=False)
            try:
                keyevent("26")
            except DeviceConnectionError:
                pass

        logger.info("Session stop test.")

    request.addfinalizer(teardown_test)

    return app


def web_info(cli_headless, ini_headless):
    """

    :param cli_headless:
    :param ini_headless:
    :return:
    """

    if cli_headless is None:
        is_headless = str_to_bool(ini_headless)
    else:
        is_headless = str_to_bool(cli_headless)

    return is_headless


driver = None


def web_fixture(request, **kwargs):
    """

    :param request:
    :return:
    """
    with allure.step("Initialize and generate Web object！"):
        logger.info("Session start test.")
    # chrome://version/
    cache = kwargs.get("cache")
    headless = kwargs.get("headless")

    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        if plat() == "Windows":
            chrome_options.add_argument("--remote-debugging-port=9222")
            if headless:
                chrome_options.add_argument("--headless")
            if cache:
                chrome_options.add_argument(f"--user-data-dir={cache}")

        elif plat() == "Linux":
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            if cache:
                chrome_options.add_argument(f"--user-data-dir={cache}")
        else:
            chrome_options.add_argument("--remote-debugging-port=9222")
            if headless:
                chrome_options.add_argument("--headless")

            if cache:
                chrome_options.add_argument(f"--user-data-dir={cache}")

        driver = webdriver.Chrome(
            options=chrome_options,
            executable_path=ChromeDriverManager(cache_valid_range=3).install(),
        )

        driver.maximize_window()
        # driver.set_window_size(1920, 1080)

    driver.implicitly_wait(30)

    def fn():
        with allure.step("Teardown session"):
            driver.quit()
        logger.info("Session stop test.")

    request.addfinalizer(fn)
    return driver
