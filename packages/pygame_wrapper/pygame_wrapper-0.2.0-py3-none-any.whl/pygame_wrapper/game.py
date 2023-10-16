"""
Contains everything related to the actual game in pgw
"""
import pygame
from pygame import Vector2
from typing import Union, Tuple, Sequence
from .menu import MenuType


Coordinate = Union[Tuple[float, float], Sequence[float], Vector2]


class GameType:
    """
    The base class used when creating a Game class
    """
    def __init__(self, gameName, RES: Coordinate, hwflags: list = None, Icon: pygame.Surface = None, fpsCap: int = 60) -> None:
        """
        The base INIT class for GameType
        :param gameName: The title/name for your game
        :param RES: the resolution of the game
        :param hwflags: the hardware flags for the display (optional)
        :param Icon: the icon for the game (optional)
        :param fpsCap: the fps cap for the game (optional defaults to 60)
        :return: None
        """
        if hwflags is None:
            hwflags = []

        self.screen = pygame.display.set_mode(RES, *hwflags)
        pygame.display.set_caption(gameName)
        if Icon is not None:
            pygame.display.set_icon(Icon)

        self.RES = RES
        self.fpsClock = pygame.time.Clock()
        self.fps = fpsCap

    def rendering(self) -> None:
        """
        A function designed to be used for the rendering aspect of the game, make use as you want
        :return: None
        """
        print(f"Uhh yo man you kinda forgot to do anything in the rendering function my guy (if you put something there, dont call super().rendering()) - {self.__class__}")
        pass

    def logic(self) -> None:
        """
        A function designed to be used for the logic aspect of your game, make use of it as you want
        :return: None
        """
        print(f"You didn't put anything in the logic function (if you did put something there, don't call super().logic()) - {self.__class__}")
        pass

    def router(self) -> MenuType:
        """
        A function designed to help you route where to go in each function, use it how you want and if you want
        :return: MenuType
        """
        pass

    def run(self) -> None:
        """
        A function designed to harbor your actual gameLoop, it is optional to use but definitely recommended
        :return: None
        """
        self.logic()
        self.rendering()
        pass

