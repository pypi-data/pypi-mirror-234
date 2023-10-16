# coding: utf-8
import logging
from typing import Union, Tuple, Dict, List, cast

from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By

from appium_extended_web_element.web_element_click import WebElementClick
from appium_extended_web_element.web_element_dom import WebElementDOM
from appium_extended_web_element.web_element_scroll import WebElementScroll
from appium_extended_web_element.web_element_tap import WebElementTap
from appium_extended_web_element.web_element_adb_actions import WebElementTerminalActions


class WebElementExtended(WebElementClick,
                         WebElementTerminalActions,
                         WebElementDOM,
                         WebElementTap,
                         WebElementScroll):
    """
    Основной интерфейс для работы с WebElementExtended
    """

    def __init__(self, logger: logging.Logger, driver, element_id):
        super().__init__(logger=logger, driver=driver, element_id=element_id)

    # GET
    def get_element(self,
                    locator: Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str] = None,
                    by: Union[MobileBy, AppiumBy, By, str] = None,
                    value: Union[str, Dict, None] = None,
                    timeout_elem: int = 10,
                    timeout_method: int = 600,
                    elements_range: Union[Tuple, List[WebElement], Dict[str, str], None] = None,
                    contains: bool = True,
                    ) -> Union['WebElementExtended', None]:
        """
        # TODO fill
        """
        inner_element = self._get_element(locator=locator,
                                          by=by,
                                          value=value,
                                          timeout_elem=timeout_elem,
                                          timeout_method=timeout_method,
                                          elements_range=elements_range,
                                          contains=contains)
        return WebElementExtended(logger=self.logger, driver=inner_element.parent, element_id=inner_element.id)

    def get_attributes(self,
                       desired_attributes: Union[str, List[str]] = None,
                       ) -> Union[str, Dict[str, str], None]:
        """
        # TODO fill
        """
        attributes = self._get_attributes(desired_attributes=desired_attributes)
        return attributes

    # CLICK
    def click(self,
              duration: int = 0,
              decorator_args: dict = None,
              wait: bool = False,
              ) -> 'WebElementExtended':
        """
        Нажимает на элемент.
        Args:
            duration: время в секундах продолжительности нажатия (по умолчанию 0)
            wait: ожидать изменение окна или нет
            decorator_args: параметры для декоратора.
                timeout_window: int время ожидания нового окна (умножается на количество попыток)
                tries: int количество попыток нажатия (по умолчанию 3)
        Usage:
            decorator_args = {"timeout_window": 5,
                              "tries": 5}
            element._tap(duration=0, wait=True, decorator_args=decorator_args)

        Returns:
            True если удалось нажать на элемент, иначе False
        """
        assert self._click(duration=duration,
                           wait=wait,
                           decorator_args=decorator_args)
        return cast('WebElementExtended', self)

    def double_click(self,
                     decorator_args: dict = None,
                     wait: bool = False,
                     ) -> 'WebElementExtended':
        """
        fill me
        # TODO fill
        """
        assert self._double_click(decorator_args=decorator_args,
                                  wait=wait)
        return cast('WebElementExtended', self)

    def click_and_move(self, locator: Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str] = None,
                       x: int = None,
                       y: int = None,
                       direction: int = None,
                       distance: int = None,
                       ) -> 'WebElementExtended':
        """
        fill me
        # TODO fill
        """
        root = self.driver.find_element('xpath', '//*')
        root = WebElementExtended(logger=self.logger, driver=root.parent, element_id=root.id)
        assert super()._click_and_move(root=root, locator=locator, x=x, y=y, direction=direction, distance=distance)
        return cast('WebElementExtended', self)

    # ADB TAP
    def adb_tap(self,
                decorator_args: dict = None,
                wait: bool = False,
                ) -> 'WebElementExtended':
        """
        tap by adb
        # TODO fill
        """
        assert self._terminal_tap(wait=wait,
                                  decorator_args=decorator_args)
        return cast('WebElementExtended', self)

    def adb_swipe(self,
                  locator: Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str] = None,
                  x: int = None,
                  y: int = None,
                  direction: int = None,
                  distance: int = None,
                  duration: int = 1,
                  contains: bool = True,
                  ) -> 'WebElementExtended':
        """
        swipe by adb
        # TODO fill
        """
        root = self.driver.find_element('xpath', '//*')
        root = WebElementExtended(logger=self.logger, driver=root.parent, element_id=root.id)
        element = None
        if locator is not None:
            element = root.get_element(locator=locator, contains=contains)
        assert self._terminal_swipe(root=root, element=element,
                                    x=x, y=y,
                                    direction=direction, distance=distance,
                                    duration=duration)
        return cast('WebElementExtended', self)

    # TAP
    def tap(self,
            duration: int = 0,
            decorator_args: dict = None,
            wait: bool = False,
            ) -> 'WebElementExtended':
        """
        # TODO fill
        """
        positions = self.get_center()
        assert self._tap(positions=[positions],
                         duration=duration,
                         decorator_args=decorator_args,
                         wait=wait)
        return cast('WebElementExtended', self)

    def double_tap(self,
                   decorator_args: dict = None,
                   wait: bool = False,
                   pause: float = 0.2,
                   ) -> 'WebElementExtended':
        """
        # TODO fill
        """
        positions = self.get_center()
        assert self._double_tap(positions=positions,
                                decorator_args=decorator_args,
                                wait=wait,
                                pause=pause)
        return cast('WebElementExtended', self)

    def tap_and_move(self,
                     locator: Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str] = None,
                     x: int = None,
                     y: int = None,
                     direction: int = None,
                     distance: int = None,
                     ) -> 'WebElementExtended':
        """
        # TODO fill
        """
        root = self.driver.find_element('xpath', '//*')
        root = WebElementExtended(logger=self.logger, driver=root.parent, element_id=root.id)
        assert self._tap_and_move(root=root, locator=locator, x=x, y=y, direction=direction, distance=distance)
        return cast('WebElementExtended', self)

    # ELEMENTS
    def get_elements(self,
                     locator: Union[Tuple, List[WebElement], Dict[str, str], str] = None,
                     by: Union[MobileBy, AppiumBy, By, str] = None,
                     value: Union[str, Dict, None] = None,
                     timeout_elements: int = 10,
                     timeout_method: int = 600,
                     elements_range: Union[Tuple, List[WebElement], Dict[str, str], None] = None,
                     contains: bool = True,
                     ) -> Union[List[WebElement], None]:
        """
        # TODO fill
        """
        elements = self._get_elements(locator=locator,
                                      by=by,
                                      value=value,
                                      timeout_elements=timeout_elements,
                                      timeout_method=timeout_method,
                                      elements_range=elements_range,
                                      contains=contains)
        result = []
        for element in elements:
            result.append(WebElementExtended(logger=self.logger,
                                             driver=element.parent,
                                             element_id=element.id))
        return result

    # SCROLL
    def scroll_down(self,
                    locator: Union[Tuple, 'WebElementExtended', Dict[str, str], str] = None,
                    duration: int = None,
                    ) -> 'WebElementExtended':
        """
        Скроллит элемент вниз от нижнего до верхнего элемента.
        :param child_locator: str, имя класса дочернего элемента.
        :param timeout: int, время ожидания элемента, по умолчанию 10 секунд.
        :return: bool, True, если скроллинг выполнен успешно.
        # TODO fill
        """
        assert self._scroll_down(locator=locator,
                                 duration=duration)
        return cast('WebElementExtended', self)

    def scroll_up(self,
                  locator: Union[Tuple, 'WebElementExtended', Dict[str, str], str] = None,
                  duration: int = None,
                  ) -> 'WebElementExtended':
        """
        Скроллит элемент вверх от верхнего дочернего элемента до нижнего дочернего элемента родительского элемента.
        :param locator: Union[tuple, WebElement], локатор или элемент, который нужно проскроллить.
        :param child_locator: str, имя класса дочернего элемента.
        :param timeout: int, время ожидания элемента, по умолчанию 10 секунд.
        :return: bool, True, если скроллинг выполнен успешно.
        # TODO fill
        """
        assert self._scroll_up(locator=locator,
                               duration=duration)

        return cast('WebElementExtended', self)

    def scroll_to_bottom(self,
                         locator: Union[Tuple, 'WebElementExtended', Dict[str, str], str] = None,
                         timeout_method: int = 120,
                         ) -> 'WebElementExtended':
        """
        # TODO fill
        """
        assert self._scroll_to_bottom(locator=locator,
                                      timeout_method=timeout_method)
        return cast('WebElementExtended', self)

    def scroll_to_top(self,
                      locator: Union[Tuple, 'WebElementExtended', Dict[str, str], str] = None,
                      timeout_method: int = 120,
                      ) -> 'WebElementExtended':
        """
        # TODO fill
        """
        assert self._scroll_to_top(locator=locator,
                                   timeout_method=timeout_method)
        return cast('WebElementExtended', self)

    def scroll_until_find(self,
                          locator: Union[Tuple, 'WebElementExtended', Dict[str, str], str],
                          timeout_method: int = 120,
                          contains: bool = True
                          ) -> Union['WebElementExtended', None]:
        """
        # TODO fill
        """
        if not self._scroll_until_find(locator=locator,
                                       timeout_method=timeout_method,
                                       contains=contains):
            return None
        return cast('WebElementExtended', self)

    def scroll_and_get(self,
                       locator: Union[Tuple, 'WebElementExtended', Dict[str, str], str],
                       timeout_method: int = 120,
                       ) -> Union['WebElementExtended', None]:
        """
        # TODO fill
        """
        element = self._scroll_and_get(locator=locator,
                                       timeout_method=timeout_method)
        return WebElementExtended(logger=self.logger,
                                  driver=element.parent,
                                  element_id=element.id)

    # DOM
    def get_parent(self) -> 'WebElementExtended':
        """
        # TODO fill
        """
        element = self._get_parent()
        return WebElementExtended(logger=self.logger, driver=element.parent, element_id=element.id)

    def get_parents(self) -> List['WebElementExtended']:
        """
        # TODO fill
        """
        elements = self._get_parents()
        elements_ext = []
        for element in elements:
            elements_ext.append(WebElementExtended(logger=self.logger, driver=element.parent, element_id=element.id))
        return elements_ext

    def get_sibling(self,
                    attributes: Dict[str, str],
                    contains: bool = True,
                    ) -> 'WebElementExtended':
        """
        # TODO fill
        """
        element = self._get_sibling(attributes=attributes, contains=contains)
        return WebElementExtended(logger=self.logger, driver=element.parent, element_id=element.id)

    def get_siblings(self) -> List['WebElementExtended']:
        """
        # TODO fill
        """
        elements = self._get_siblings()
        elements_ext = []
        for element in elements:
            elements_ext.append(WebElementExtended(logger=self.logger, driver=element.parent, element_id=element.id))
        return elements_ext

    def get_cousin(self,
                   ancestor: Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str],
                   cousin: Dict[str, str],
                   contains: bool = True,
                   ) -> 'WebElementExtended':
        """
        # TODO fill
        """
        root = self.driver.find_element('xpath', '//*')
        root = WebElementExtended(logger=self.logger, driver=root.parent, element_id=root.id)
        ancestor = root.get_element(ancestor)
        ancestor = WebElement(ancestor.parent, ancestor.id)
        element = self._get_cousin(ancestor=ancestor, cousin=cousin, contains=contains)
        return WebElementExtended(logger=self.logger, driver=element.parent, element_id=element.id)

    def get_cousins(self,
                    ancestor: Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str],
                    cousin: Dict[str, str],
                    contains: bool = True,
                    ) -> List['WebElementExtended']:
        """
        # TODO fill
        """
        root = self.driver.find_element('xpath', '//*')
        root = WebElementExtended(logger=self.logger, driver=root.parent, element_id=root.id)
        ancestor = root.get_element(ancestor)
        ancestor = WebElement(ancestor.parent, ancestor.id)
        elements = self._get_cousins(ancestor=ancestor, cousin=cousin, contains=contains)
        elements_ext = []
        for element in elements:
            elements_ext.append(WebElementExtended(logger=self.logger, driver=element.parent, element_id=element.id))
        return elements_ext

    def is_contains(self,
                    locator: Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str],
                    contains: bool = True,
                    ) -> bool:
        """
        # TODO fill
        """
        child_element = self.get_element(locator=locator, contains=contains)
        if child_element is not None:
            return True
        return False

    # ACTIONS
    def zoom(self, hold: bool) -> 'WebElementExtended':
        """
        # TODO fill
        """
        raise NotImplementedError  # TODO implement

    def unzoom(self, hold: bool) -> 'WebElementExtended':
        """
        # TODO fill
        """
        raise NotImplementedError  # TODO implement

    def get_center(self) -> Union[Tuple[int, int], None]:
        """
        Вычисляет координаты центра заданного элемента.

        Аргументы:
            element (WebElement): Веб-элемент.

        Возвращает:
            tuple: Координаты центра в виде (x, y). Возвращает None, если произошла ошибка.
        """
        return self._get_center()

    def get_coordinates(self) -> Union[Tuple[int, int, int, int], None]:
        """
        # TODO fill
        """
        return self._get_coordinates()
