"""
Contains everything related to creating menus using pgw
"""
import pygame
from pygame import Surface


class MenuType:
    """
    A base class when creating Menus, very similar to the game class but without some of the features.
    """
    def __init__(self, screen: Surface, fpsClock: pygame.time.Clock, fps: int = 60) -> None:
        """
        The init function for defining a menu type
        :param screen: The pygame.Surface used for rendering
        :param fpsClock: The pygame.time.Clock used for fps
        :param fps: The actual frames per second (optional defaults to 60)
        :return: None
        """
        self.screen = screen
        self.fpsClock = fpsClock
        self.fps = fps
    
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

    def run(self) -> None:
        """
        A function designed to harbor your actual gameLoop, it is optional to use but definitely recommended
        :return: None
        """
        self.logic()
        self.rendering()
        pass


