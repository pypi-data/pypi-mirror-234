"""
Contains everything related to Colors in pgw
"""
from pygame import Color
from typing import Tuple, Union, Sequence

# type hinting stuff
RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]


class CustomColor(Color):
    """
    A class to create custom colors 
    """
    def __init__(self, color: ColorValue, alpha: int = 255) -> None:
        """
        The init class for CustomColor
        :param color: The color you want to set (excluding alpha)
        :param alpha: The alpha value of the color (optional defaults to 255)
        :return: None
        """
        super().__init__(color[0], color[1], color[2], alpha)
        self.color = (*color, alpha)  # a tuple which will look like this: (r, g, b, a)
    
    def darken(self, offset: int) -> tuple:
        """
        A function which returns the darker version of the color
        :param offset: The integer value of how much to darken the color
        :return tuple: The tuple of the new color
        """
        darkColor = [0, 0, 0]
        for i, c in enumerate([self.color[0], self.color[1], self.color[2]]):
            nc = c - offset
            darkColor[i] = nc if nc >= 0 else 0
        
        return (*darkColor, self.color[3])  # returns the new color along with the old alpha
    
    def lighten(self, offset: int) -> tuple:
        """
        A function whcih returns the lighter version of the color
        :param offset: The integer value of how much to darken the color
        :return tuple: The tuple of the new color
        """
        lightColor = [0, 0, 0]
        for i, c in enumerate([self.color[0], self.color[1], self.color[2]]):
            nc = c + offset
            lightColor[i] = nc if nc <= 255 else 255
        
        return (*lightColor, self.color[3])  # returns the new color along with the old alpha
