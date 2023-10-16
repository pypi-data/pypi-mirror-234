# coding: utf-8
import logging
import time
import typing
from typing import Union, Tuple, Dict, Optional

from appium.webdriver import WebElement
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.types import WaitExcTypes

from appium_extended_web_element.web_element_get import WebElementGet


class WebElementScroll(WebElementGet):
    """
    Класс для выполнения действий прокрутки элемента.
    Наследуется от класса WebElementGet.
    """

    def __init__(self, logger: logging.Logger, driver, element_id):
        super().__init__(logger=logger, driver=driver, element_id=element_id)

    def _scroll_down(self,
                     locator: Union[Tuple, 'WebElementExtended', Dict[str, str], str] = None,
                     duration: int = None,
                     timeout_elements: float = 10.0,
                     timeout_method: float = 600.0,
                     elements_range: Union[tuple, list[WebElement], dict[str, str], None] = None,
                     contains: bool = True,
                     poll_frequency: float = 0.5,
                     ignored_exceptions: Optional[typing.Iterable[typing.Type[Exception]]] = None
                     ) -> bool:
        """
        Прокручивает элемент вниз от нижнего дочернего элемента до верхнего дочернего элемента родительского элемента.

        Args:
            locator (Union[Tuple, WebElement, Dict[str, str], str], optional): Локатор или элемент для прокрутки (за что крутить).
            duration (int, optional): Продолжительность прокрутки в миллисекундах (по умолчанию: None).

        Returns:
            bool: True, если прокрутка выполнена успешно.

        """
        try:
            recycler = self

            # Проверка, является ли элемент прокручиваемым
            if recycler.get_attribute('scrollable') != 'true':
                self.logger.error("Элемент не крутиться")
                return False

            # Если локатор для прокрутки не указан, используется локатор первого дочернего элемента
            if not locator:
                locator = {'class': self._get_first_child_class()}

            # Получение верхнего и нижнего дочерних элементов родительского элемента
            top_center_child = self._get_top_center_child_from_parent(locator=locator,
                                                                      timeout_elements=timeout_elements,
                                                                      timeout_method=timeout_method,
                                                                      elements_range=elements_range,
                                                                      contains=contains,
                                                                      poll_frequency=poll_frequency,
                                                                      ignored_exceptions=ignored_exceptions,
                                                                      )
            bottom_child = self._get_bottom_child_from_parent(locator=locator,
                                                              timeout_elements=timeout_elements,
                                                              timeout_method=timeout_method,
                                                              elements_range=elements_range,
                                                              contains=contains,
                                                              poll_frequency=poll_frequency,
                                                              ignored_exceptions=ignored_exceptions,
                                                              )

            # Прокрутка вниз от нижнего дочернего элемента до верхнего дочернего элемента родительского элемента
            self.driver.scroll(origin_el=bottom_child, destination_el=top_center_child, duration=duration)
            return True

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
            self.logger.error("_scroll_down(): Ошибка. {}".format(e))
            return False

    def _scroll_up(self,
                   locator: Union[Tuple, 'WebElementExtended', Dict[str, str], str] = None,
                   duration: int = None,
                   timeout_elements: float = 10.0,
                   timeout_method: float = 600.0,
                   elements_range: Union[tuple, list[WebElement], dict[str, str], None] = None,
                   contains: bool = True,
                   poll_frequency: float = 0.5,
                   ignored_exceptions: Optional[typing.Iterable[typing.Type[Exception]]] = None
                   ) -> bool:
        """
        Прокручивает элемент вверх от верхнего дочернего элемента до нижнего дочернего элемента родительского элемента.

        Args:
            locator (Union[Tuple, WebElement, Dict[str, str], str], optional): Локатор или элемент для прокрутки (за что крутить).
            duration (int, optional): Продолжительность прокрутки в миллисекундах (по умолчанию: None).

        Returns:
            bool: True, если прокрутка выполнена успешно.

        """
        try:
            recycler = self

            # Проверка, является ли элемент прокручиваемым
            if recycler.get_attribute('scrollable') != 'true':
                self.logger.error("Элемент не крутиться")
                return False

            # Если локатор для прокрутки не указан, используется локатор первого дочернего элемента
            if not locator:
                locator = {'class': self._get_first_child_class()}

            # Получение верхнего и нижнего дочерних элементов родительского элемента
            top_child = self._get_top_child_from_parent(locator=locator,
                                                        timeout_elements=timeout_elements,
                                                        timeout_method=timeout_method,
                                                        elements_range=elements_range,
                                                        contains=contains,
                                                        poll_frequency=poll_frequency,
                                                        ignored_exceptions=ignored_exceptions,
                                                        )
            bottom_center_child = self._get_bottom_center_child_from_parent(locator=locator,
                                                                            timeout_elements=timeout_elements,
                                                                            timeout_method=timeout_method,
                                                                            elements_range=elements_range,
                                                                            contains=contains,
                                                                            poll_frequency=poll_frequency,
                                                                            ignored_exceptions=ignored_exceptions,
                                                                            )

            # Прокрутка вверх от верхнего дочернего элемента до нижнего дочернего элемента родительского элемента
            self.driver.scroll(origin_el=top_child, destination_el=bottom_center_child, duration=duration)
            return True

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
            self.logger.error("_scroll_up(): Ошибка. {}".format(e))
            return False

    def _scroll_to_bottom(self,
                          locator: Union[Tuple, WebElement, Dict[str, str], str] = None,
                          timeout_method: int = 120) -> bool:
        """
        Прокручивает элемент вниз до упора.

        Args:
            locator (Union[Tuple, WebElement, Dict[str, str], str], optional): Локатор или элемент для прокрутки (за что крутить).
            timeout_method (int, optional): Время ожидания элемента в секундах (по умолчанию: 120).

        Returns:
            bool: True, если прокрутка выполнена успешно.

        """
        recycler = self

        # Проверка, является ли элемент прокручиваемым
        if recycler.get_attribute('scrollable') != 'true':
            self.logger.error("Элемент не крутиться")
            return False

        # Если локатор для прокрутки не указан, используется локатор первого дочернего элемента
        if not locator:
            locator = {'class': self._get_first_child_class()}

        last_child = None
        start_time = time.time()

        # Прокрутка вниз до упора
        while time.time() - start_time < timeout_method:
            child = self._get_element(locator=locator)
            if child == last_child:
                return True
            last_child = child
            self._scroll_down(locator=locator)
        self.logger.error("_scroll_to_bottom(): Неизвестная ошибка")
        return False

    def _scroll_to_top(self,
                       locator: Union[Tuple, WebElement, Dict[str, str], str],
                       duration: int = 0.5,
                       timeout_method: int = 120,
                       timeout_elem: float = 10.0,
                       timeout_elements: float = 10.0,
                       elements_range: Union[tuple, list[WebElement], dict[str, str], None] = None,
                       contains: bool = True,
                       poll_frequency: float = 0.5,
                       ignored_exceptions: Optional[typing.Iterable[typing.Type[Exception]]] = None
                       ) -> bool:
        """
        Прокручивает элемент вверх до упора.

        Args:
            locator (Union[Tuple, WebElement, Dict[str, str], str]): Локатор или элемент для прокрутки (за что крутить).
            timeout_method (int): Время ожидания элемента в секундах (по умолчанию: 120).

        Returns:
            bool: True, если прокрутка выполнена успешно.

        """
        recycler = self

        # Проверка, является ли элемент прокручиваемым
        if recycler.get_attribute('scrollable') != 'true':
            self.logger.error("Элемент не крутиться")
            return False

        # Если локатор для прокрутки не указан, используется локатор первого дочернего элемента
        if not locator:
            locator = {'class': self._get_first_child_class()}
        last_child = None
        start_time = time.time()

        # Прокрутка вверх до упора
        while time.time() - start_time < timeout_method:
            child = self._get_element(locator=locator,
                                      timeout_elem=timeout_elem,
                                      timeout_method=timeout_method,
                                      elements_range=elements_range,
                                      contains=contains,
                                      poll_frequency=poll_frequency,
                                      ignored_exceptions=ignored_exceptions,
                                      )
            if child == last_child:
                return True
            last_child = child
            self._scroll_up(locator=locator,
                            duration=duration,
                            timeout_elements=timeout_elements,
                            timeout_method=timeout_method,
                            elements_range=elements_range,
                            contains=contains,
                            poll_frequency=poll_frequency,
                            ignored_exceptions=ignored_exceptions,
                            )

        self.logger.error("_scroll_to_top(): Неизвестная ошибка")
        return False

    def _scroll_until_find(self,
                           locator: Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str] = None,
                           timeout_elem: float = 10.0,
                           timeout_method: float = 600.0,
                           elements_range: Union[Tuple, typing.List[WebElement], Dict[str, str], None] = None,
                           contains: bool = True,
                           poll_frequency: float = 0.5,
                           ignored_exceptions: typing.Optional[WaitExcTypes] = None,
                           threshold: float = 0.9) -> bool:
        """
        Крутит элемент вниз, а затем вверх для поиска элемента по заданному локатору.

        Args:
            locator (Union[Tuple, WebElement, Dict[str, str], str]): Локатор или элемент, для которого производится
                поиск.
            timeout_method (int): Время на поиск в одном направлении (по умолчанию: 120 вниз и 120 вверх).

        Returns:
            bool: True, если элемент найден. False, если элемент не найден.

        """
        recycler = self

        # Проверка, является ли элемент scrollable
        if recycler.get_attribute('scrollable') != 'true':
            self.logger.error("Элемент не крутиться")
            return False

        start_time = time.time()

        last_element_image = None

        # Прокрутка вниз до поиска элемента
        while time.time() - start_time < timeout_method:
            try:
                if isinstance(locator, str):
                    if self.is_image_on_the_screen(image=locator, threshold=threshold):
                        return True
                element = self._get_element(locator=locator,
                                            timeout_elem=timeout_elem,
                                            timeout_method=timeout_method,
                                            elements_range=elements_range,
                                            contains=contains,
                                            poll_frequency=poll_frequency,
                                            ignored_exceptions=ignored_exceptions, )
                if element is not None:
                    return True
            except NoSuchElementException:
                continue
            current_element_image = self.screenshot_as_base64
            if current_element_image == last_element_image:
                break
            last_element_image = self.screenshot_as_base64
            recycler._scroll_down()

        # Прокрутка вверх до поиска элемента
        while time.time() - start_time < timeout_method:
            try:
                if isinstance(locator, str):
                    if self.is_image_on_the_screen(image=locator, threshold=threshold):
                        return True
                element = self._get_element(locator=locator,
                                            timeout_elem=timeout_elem,
                                            timeout_method=timeout_method,
                                            elements_range=elements_range,
                                            contains=contains,
                                            poll_frequency=poll_frequency,
                                            ignored_exceptions=ignored_exceptions, )
                if element is not None:
                    return True
            except NoSuchElementException:
                pass
            current_element_image = self.screenshot_as_base64
            if current_element_image == last_element_image:
                break
            last_element_image = self.screenshot_as_base64
            recycler._scroll_up()

        self.logger.error("_scroll_until_find(): Элемент не найден")
        return False

    def _scroll_and_get(self,
                        locator: Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str] = None,
                        timeout_elem: float = 10.0,
                        timeout_method: float = 600.0,
                        elements_range: Union[Tuple, typing.List[WebElement], Dict[str, str], None] = None,
                        contains: bool = True,
                        poll_frequency: float = 0.5,
                        ignored_exceptions: typing.Optional[WaitExcTypes] = None,
                        ) -> Optional[WebElement]:
        """
        Крутит элемент вниз, а затем вверх для поиска элемента по заданному локатору.

        Args:
            locator (Union[Tuple, WebElement, Dict[str, str], str]): Локатор или элемент, для которого производится
                поиск.
            timeout_method (int): Время на поиск в одном направлении (по умолчанию: 120 вниз и 120 вверх).

        Returns:
            bool: True, если элемент найден. False, если элемент не найден.

        """
        recycler = self

        # Проверка, является ли элемент scrollable
        if recycler.get_attribute('scrollable') != 'true':
            self.logger.error("Элемент не крутится")
            return None

        start_time = time.time()

        last_element_image = None

        # Прокрутка вниз до поиска элемента
        while time.time() - start_time < timeout_method:
            try:
                if isinstance(locator, str):
                    if self.is_image_on_the_screen(image=locator):
                        return self._get_element(locator=locator,
                                                 timeout_elem=timeout_elem,
                                                 timeout_method=timeout_method,
                                                 elements_range=elements_range,
                                                 contains=contains,
                                                 poll_frequency=poll_frequency,
                                                 ignored_exceptions=ignored_exceptions, )
                element = self._get_element(locator=locator,
                                            timeout_elem=timeout_elem,
                                            timeout_method=timeout_method,
                                            elements_range=elements_range,
                                            contains=contains,
                                            poll_frequency=poll_frequency,
                                            ignored_exceptions=ignored_exceptions, )
                if element is not None:
                    return element
            except NoSuchElementException:
                continue
            current_element_image = self.screenshot_as_base64
            if current_element_image == last_element_image:
                break
            last_element_image = self.screenshot_as_base64
            recycler._scroll_down()

        # Прокрутка вверх до поиска элемента
        while time.time() - start_time < timeout_method:
            try:
                if isinstance(locator, str):
                    if self.is_image_on_the_screen(image=locator):
                        return self._get_element(locator=locator,
                                                 timeout_elem=timeout_elem,
                                                 timeout_method=timeout_method,
                                                 elements_range=elements_range,
                                                 contains=contains,
                                                 poll_frequency=poll_frequency,
                                                 ignored_exceptions=ignored_exceptions, )
                element = self._get_element(locator=locator,
                                            timeout_elem=timeout_elem,
                                            timeout_method=timeout_method,
                                            elements_range=elements_range,
                                            contains=contains,
                                            poll_frequency=poll_frequency,
                                            ignored_exceptions=ignored_exceptions, )
                if element is not None:
                    return element
            except NoSuchElementException:
                pass
            current_element_image = self.screenshot_as_base64
            if current_element_image == last_element_image:
                break
            last_element_image = self.screenshot_as_base64
            recycler._scroll_up()

        self.logger.error("_scroll_and_get(): Элемент не найден")
        return None
