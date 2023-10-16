"""
Contains everything related to fonts in the pgw
"""
import pygame.freetype
from pygame import Surface, Color, Vector2
from typing import Union, Tuple, Sequence, Optional
from pathlib import Path

# define vars:
Coordinate = Union[Tuple[float, float], Sequence[float], Vector2]
RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]

STYLE_DEFAULT = pygame.freetype.STYLE_DEFAULT


class Font(pygame.freetype.Font):
    """
    A superior font class that includes some more beneficial features, such as multiline rendering.
    """

    def __init__(self, location: str, fontSize: Union[float, Tuple[float, float]],
                 fgColor: Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]],
                 bgColor: Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]] = None,
                 font_index: int = 0, resolution: int = 0, ucs4: int = False, ColorList: list[
                Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]] = None) -> None:
        """
        The INIT class for Font
        :param location: The location of the font file
        :param fontSize: The size to render the font at
        :param fgColor: The foreground color of the text
        :param bgColor: The background color of the text (optional defaults to None)
        :param font_index: The font index (same as pygame.freetype.font) (defaults to 0)
        :param resolution: The resolution of the font (same as pygame.freetype.font) (defaults to 0)
        :param ucs4: The ucs4 (same as pygame.freetype.font) (defaults to False)
        :param ColorList: The list of colors to use when multiline rendering (very specific use case but can be more efficient/effective) (defaults to None)
        :return: None
        """

        newLoc = Path(location)
        super().__init__(newLoc.absolute(), size=fontSize, font_index=font_index, resolution=resolution, ucs4=ucs4)
        self.fgcolor = fgColor
        if bgColor is not None:
            self.bgcolor = bgColor
        self.ColorList = ColorList

    def multiline_render_to(self, surf: Surface, dest, text: str, fgcolor: Optional[ColorValue] = None,
                            bgcolor: Optional[ColorValue] = None, style: int = STYLE_DEFAULT, rotation: int = 0,
                            size: float = 0) -> list[pygame.rect.Rect]:
        """
        Render to a surface using the multiline render
        :param surf: The pygame.Surface
        :param dest: The position/rect of where to place the text
        :param text: The text the font is rendering (use \n for next line)
        :param fgcolor: The foreground color of the text (optional defaults to the one defined on creation)
        :param bgcolor: The background color of the text (optional defaults to the one defined on creation)
        :param style:
        :param rotation:
        :param size:
        :return: list[pygame.rect.Rect]
        """
        ListText = text.splitlines()
        ListRects = []
        useColorList = True if self.ColorList is not None else False
        for i, line in enumerate(ListText):
            if useColorList:
                self.fgcolor = self.ColorList[i % len(self.ColorList)]
            rect = self.render_to(surf=surf, dest=(dest[0], dest[1] + (i * self.size + 10)), text=line, fgcolor=fgcolor,
                                  bgcolor=bgcolor, style=style, rotation=rotation, size=size)
            ListRects.append(rect)

        return ListRects

    def multiline_render(self, text: str, fgcolor: Optional[ColorValue] = None, bgcolor: Optional[ColorValue] = None,
                         style: int = STYLE_DEFAULT, rotation: int = 0, size: float = 0) -> list[Tuple[Surface, pygame.rect.Rect]]:
        """
        Render using multiline render
        :param text: The text the font is rendering (use \n for next line)
        :param fgcolor: The foreground color of the text (optional defaults to the one defined on creation)
        :param bgcolor: The background color of the text (optional defaults to the one defined on creation)
        :param style:
        :param rotation:
        :param size:
        :return: list[Tuple[Surface, pygame.rect.Rect]]
        """
        ListText = text.splitlines()
        ListSurfs = []
        for i, line in enumerate(ListText):
            surfRect = self.render(text=line, fgcolor=fgcolor, bgcolor=bgcolor, style=style, rotation=rotation,
                                   size=size)
            ListSurfs.append(surfRect)

        return ListSurfs

    def get_center(self, surf: Surface, text: str, style: int = STYLE_DEFAULT, rotation: int = 0, size: float = 0,
                   x: bool = True, y: bool = False) -> pygame.rect.Rect:
        rect = self.get_rect(text=text, style=style, rotation=rotation, size=size)
        if x:
            rect.centerx = surf.get_rect().centerx

        if y:
            rect.centery = surf.get_rect().centery

        return rect

