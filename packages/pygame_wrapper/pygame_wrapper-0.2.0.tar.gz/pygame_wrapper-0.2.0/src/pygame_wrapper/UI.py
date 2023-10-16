"""
Contains everything related to UI in pgw
"""
import pygame
from typing import Union, Tuple, Sequence, List
from .colors import CustomColor
from .fonts import Font

RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[pygame.Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]


def _createCustomColor(color):
    """
    not intended for use outside of this, can change at any time
    """
    if isinstance(color, pygame.Color):
        color = CustomColor([color.r, color.g, color.b], color.a)
    elif isinstance(color, tuple) or isinstance(color, list):
        color = CustomColor([color[0], color[1], color[2]], color[3]) if len(color) == 4 else CustomColor(color)
    elif isinstance(color, str):
        color = CustomColor(color)

    return color


class Button(pygame.Rect):
    """
    A UI button
    """
    def __init__(self, left: float, top: float, width: float, height: float, defaultColor: ColorValue, ClickedColor: ColorValue, font: Font, text: str, darkLightOffset: int = 20, textOffset: Union[Tuple[int, int], list[float, float]] = (0, -30), toggle: bool = False):
        super().__init__(left, top, width, height)
        self.color = _createCustomColor(defaultColor)
        self.clickedColor = _createCustomColor(ClickedColor)
        self.font = font
        self.text = text
        self.offset = darkLightOffset
        self.state = False
        self.hovered = False
        self.surface = pygame.Surface((width, height))
        self.textOffset = textOffset
        self.toggle = toggle

    def render_to(self, surf: pygame.Surface, width: int = 0, border_radius: int = -1, **kwargs):
        if self.state and self.toggle:
            color = self.clickedColor
        elif self.hovered:
            color = self.color.darken(self.offset)
        else:
            color = self.color
        pygame.draw.rect(surf, color, self, width, border_radius, *kwargs)
        pos = self.font.get_center(self.surface, self.text.split("\n")[0])
        pos.x += self.left + self.textOffset[0]
        pos.y += self.top + self.textOffset[1]
        self.font.multiline_render_to(surf, pos, self.text)

    def hook_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if self.collidepoint(mx, my):
                    self.hovered = True
                else:
                    self.hovered = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered:
                    self.state = True
                else:
                    self.state = False


class Checkbox(pygame.Rect):
    def __init__(self, left: float, top: float, width: float, height: float, baseColor: ColorValue, clickedColor: ColorValue, darkLightOffset: int = 20):
        super().__init__(left, top, width, height)
        self.baseColor = _createCustomColor(baseColor)
        self.clickedColor = _createCustomColor(clickedColor)
        self.hoveredColor = self.baseColor.darken(darkLightOffset)
        self.hovered = False
        self.state = False

    def render_to(self, surf: pygame.Surface, width: int = 0, border_radius: int = -1, **kwargs):
        if self.state:
            color = self.clickedColor
        elif self.hovered:
            color = self.hoveredColor
        else:
            color = self.baseColor

        pygame.draw.rect(surf, color, self, width, border_radius, *kwargs)

    def hook_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if self.collidepoint(mx, my):
                    self.hovered = True
                else:
                    self.hovered = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered:
                    self.state = not self.state


