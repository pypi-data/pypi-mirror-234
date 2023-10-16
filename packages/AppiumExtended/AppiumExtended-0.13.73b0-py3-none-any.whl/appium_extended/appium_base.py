"""
Корневой класс AppiumExtended. Обеспечивает соединение с сервером и инициализацию драйвера.
"""

# coding: utf-8
import logging
import json
import time

from appium import webdriver

from appium_extended_server.appium_server import AppiumServer
from appium_extended_terminal.terminal import Terminal
from appium_extended_terminal.aapt import Aapt
from appium_extended_terminal.adb import Adb
from appium.webdriver.webdriver import WebDriver


class AppiumBase:
    """
    Класс работы с Appium.
    Обеспечивает подключение к устройству
    """

    def __init__(self, logger: logging.Logger = None, log_level=logging.CRITICAL):
        self.server_log_level: str = None
        self.server_port: int = None
        self.server_ip: str = None
        self.server: AppiumServer = None
        self.logger = logger
        self.driver: WebDriver = None
        self.terminal: Terminal = None
        self.session_id: str = None
        self.capabilities = None
        self.keep_alive_server: bool = True
        self.aapt = Aapt()
        self.adb = Adb()
        self.logger.setLevel(log_level)

    def connect(self,
                capabilities: dict,
                server_ip: str = '127.0.0.1',
                server_port: int = 4723,
                server_log_level: str = 'error',
                remote: bool = False,
                keep_alive_server: bool = True) -> None:
        """
        Подключение к устройству через сервер Appium.

        Args:
            capabilities (dict): Словарь с возможностями для подключения к устройству.
            server_ip (str, optional): IP-адрес сервера Appium. По умолчанию '127.0.0.1'.
            server_port (int, optional): Порт сервера Appium. По умолчанию 4723.
            server_log_level (str, optional): Уровень логирования сервера. По умолчанию 'error'.
            remote (bool, optional): Флаг для удаленного подключения. По умолчанию False.
            keep_alive_server (bool, optional): Флаг, оставлять ли сервер работающим после отключения
                (только при remote=False). По умолчанию True.

        Usages:
            app = AppiumExtended(logger=logger, log_level=logging.INFO)

            capabilities = {
                "platformName": "android",
                "appium:automationName": "uiautomator2",
                "appium:deviceName": app.adb.get_device_model(),
                "appium:udid": app.adb.get_device_uuid(),
                }

            app.connect(capabilities=capabilities,
                        server_ip='127.0.0.1',
                        server_port=4723,
                        server_log_level='info',
                        remote=False,
                        keep_alive_server=True)

            # ИЛИ ЕСЛИ СЕРВЕР УДАЛЕННЫЙ:
            app.connect(capabilities=capabilities,
                        server_ip='15.78.145.11',
                        server_port=4723,
                        server_log_level='error',
                        remote=True,
                        keep_alive_server=True)

        Raises:
            AppiumServerNotAliveException: Если сервер Appium не запущен или не отвечает.
            WebDriverException: Если не удается установить соединение с WebDriver.

        Returns:
            None: Функция не возвращает ничего, но инициализирует драйвер и другие компоненты.
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_log_level = server_log_level
        self.keep_alive_server = keep_alive_server
        self.capabilities = capabilities
        self.server = AppiumServer(server_ip=self.server_ip,
                                   server_port=self.server_port,
                                   remote_log_level=self.server_log_level,
                                   logger=self.logger)
        self.logger.debug(
            f"connect(capabilities {capabilities}")
        if not remote:
            # запускаем локальный сервер Аппиум
            if not self.server.is_alive():
                self.server.start()
                time.sleep(10)
                self.server.wait_until_alive()

        url = f'http://{server_ip}:{str(server_port)}/wd/hub'
        self.logger.info(f"Подключение к серверу: {url}")
        self.driver = webdriver.Remote(command_executor=url,
                                       desired_capabilities=capabilities,
                                       keep_alive=True)
        self.session_id = self.driver.session_id
        # Инициализация объектов требующих драйвер
        self.terminal = Terminal(driver=self.driver, logger=self.logger)

        app_capabilities = json.dumps(capabilities)
        self.logger.info(f'Подключение установлено с  параметрами: {str(app_capabilities)}, {url}')
        self.logger.info(f'Сессия №: {self.driver.session_id}')

    def disconnect(self) -> None:
        """
        Отключение от устройства.
        А также остановка сервера Appium, если флаг `keep_alive_server` установлен в False.

        Usages:
            app.disconnect()

        Raises:
            AppiumServerNotAliveException: Если сервер Appium не запущен или не отвечает.
            WebDriverException: Если не удается завершить соединение с WebDriver.

        Returns:
            None: Функция не возвращает ничего, но завершает текущую сессию и останавливает сервер, если необходимо.
        """
        if self.driver:
            self.logger.debug(f"Отключение от сессии №: {self.driver.session_id}")
            self.driver.quit()
            self.driver = None
        if not self.keep_alive_server:
            self.server.stop()

    def is_running(self) -> bool:
        """
        Проверяет, запущен ли сервер Appium и активна ли текущая сессия.

        Usages:
            app.is_running()

        Raises:
            WebDriverException: Если не удается проверить статус сервера или сессии.

        Returns:
            bool: Возвращает True, если сервер и сессия активны, иначе False.
        """
        return self.driver.is_running()

    def reconnect(self):
        self.logger.error("RECONNECT")
        url = f'http://{self.server_ip}:{str(self.server_port)}/wd/hub'
        self.logger.info(f"Подключение к серверу: {url}")
        self.driver = webdriver.Remote(command_executor=url,
                                       desired_capabilities=self.capabilities,
                                       keep_alive=True)
        self.session_id = self.driver.session_id
        # Инициализация объектов требующих драйвер
        self.terminal = Terminal(driver=self.driver, logger=self.logger)

        app_capabilities = json.dumps(self.capabilities)
        self.logger.info(f'Подключение установлено с  параметрами: {str(app_capabilities)}, {url}')
        self.logger.info(f'Сессия №: {self.driver.session_id}')


