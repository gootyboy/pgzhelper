import pgzero.screen as _pgzero_screen
import pygame
from pgzero.rect import Rect, ZRect
from pgzero.clock import clock
from pgzero.actor import Actor
from pgzero.animation import animate
from pgzero.constants import mouse as PGZeroMouse
import os
from typing import overload
from .shapes import *
from .errors import *
from . import _camera as pgz_camera

full_screen_rect = Rect(25, 25, 25, 25)
is_full_screen = False
pgzero_drawer = None
pgzero_screen = None
width_increase = 0
height_increase = 0
resize_mouse_down = False
resize_mouse_down_pos = (0, 0)
window_pos = (200, 200)
draw_frames_per_second = None
update_frames_per_second = None
full_screen_removed = True
resizing_removed = True
inited = False

def load_camera(camera_number = 0):
    pgz_camera.load_camera(camera_number)

def remove_camera_background(color = (255, 255, 255)):
    pgz_camera.remove_background(color)

def set_camera_zoom_factor(factor):
    pgz_camera.set_zoom_factor = factor

def init(surface):
    """
    Function to initilize the screen. Called by using:

        init(screen)

    :param surface: The screen/surface which to initilize to.
    """
    global pgzero_drawer, pgzero_screen, inited
    pgzero_screen = surface
    pgzero_drawer = _pgzero_screen.SurfacePainter(pgzero_screen)
    inited = True

def _init_check():
    """
    Function to make sure Screen is initilized.

    Not meant for user use.

    :raise ScreenError: When the pgzero_surface or the pgzero_screen is None.
    """
    if pgzero_drawer == None or pgzero_screen == None:
        raise ScreenError("Screen must be initilized before drawing. In your draw function add \"init(screen)\" for the first line.")

class Screen:
    """Class for all of the screen drawing, positioning, ..."""
    def __init__(self, surface):
        init(surface)

    @staticmethod
    def set_position(x: float | int, y: float | int) -> None:
        """
        Function to set the start position of the screen. Must be at the top of your code after the imports or else the function will not work.

        :param x: The x coordinate of the position.
        :param y: The y coordinate of the position.
        """
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

    @staticmethod
    def center_window() -> None:
        """
        Function to center the screen. Must be at the top of your code after the imports or else the function will not work.
        """
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    @staticmethod
    def fill(color: tuple[float, float, float] | str) -> None:
        """
        Function to fill the screen with the specified color.

        :param color: The color which to fill the screen with.

        :raise ScreenError: When screen is not initilized with init(screen).
        """
        _init_check()
        pgzero_screen.fill(color)

    @staticmethod
    @property
    def surface() -> pygame.Surface:
        """
        Property to get the surface of the screen for pygame drawing.

        :return pygame.Surface: The surface of screen.

        :raise ScreenError: When screen is not initilized with init(screen).
        """
        _init_check()
        return pgzero_screen.surface
    
    @staticmethod
    @property
    def height() -> float | int:
        """
        Property to get the height of the window. Your HEIGHT constant will automatically change as the window resizes.
        
        :return float: The height of the window in pixels
        :return int: The height of the window in pixels

        :raise ScreenError: When screen is not initilized with init(screen).
        """
        _init_check()
        return pgzero_screen.height
    
    @staticmethod
    @property
    def width() -> float | int:
        """
        Property to get the height of the window. Your WIDTH constant will automatically change as the window resizes.
        
        :return float: The height of the window in pixels
        :return int: The height of the window in pixels

        :raise ScreenError: When screen is not initilized with init(screen).
        """
        _init_check()
        return pgzero_screen.width

    @staticmethod
    def clear() -> None:
        """
        Function to clear the screen. Equivalent to:
            
            Screen.fill("black")
            
        :raise ScreenError: When screen is not initilized with init(screen).
        """
        _init_check()
        pgzero_screen.clear()

    @staticmethod
    def blit(image: str, pos: tuple[float, float] | list[float, float] = (0, 0)) -> None:
        """
        Function to place an image to the Screen.

        :param image: The image name or path. When using image name, image must be saved in an images directory.
        :param pos: The position where to place the image.

        :raise ScreenError: When screen is not initilized with init(screen).
        """
        _init_check()
        pgzero_screen.blit(image, pos)
    
    @staticmethod
    def lerp_color(color1, color2, t):
        r = color1[0] + t * (color2[0] - color1[0])
        g = color1[1] + t * (color2[1] - color1[1])
        b = color1[2] + t * (color2[2] - color1[2])
        return (int(r), int(g), int(b))
    class draw:
        """Class for drawing objects and texts to the Screen."""
        @staticmethod
        def text(text: str, fontname: str | None = None, fontsize: int | float | None = None, sysfontname: str | None = None, antialias: bool = True, bold: bool | None = None, italic: bool | None = None, underline: bool | None = None, 
                 color: tuple | str | None = None, background: tuple | str | None = None, topleft: tuple | None = None, bottomleft: tuple | None = None, topright: tuple | None = None, bottomright: tuple | None = None, midtop: tuple | None = None,
                 midleft: tuple | None = None, midbottom: tuple | None = None, midright: tuple | None = None, center: tuple | None = None, width: float | None = None, widthem: float | None = None, lineheight: float | None = None, 
                 align: str | None = None, owidth: float | None = None, ocolor: tuple | str | None = None, shadow: tuple | None = None, scolor: tuple | str | None =None, gcolor: tuple | str | None = None, alpha: float = 1.0, 
                 anchor: tuple | None = None, angle: int | float = 0) -> None:
            """
            Function to draw text to the Screen.

            :param text: The text to be drawn to the screen.
            :param fontname: The font name for the text. Font names must be in a font directory and in the .ttf format. Defualts to the sysfontname.
            :param fontsize: The size of the font to use, in pixels. Defaults to 24
            :param antialias: Whether to render with antialiasing or not. Defaults to True.
            :param sysfontname: The system font name to use if fontname is omitted. Font names must be in a font directory and in the .ttf format. Defaults to the system font.
            :param bold: Whether to make the text bold or not. Defaults to False.
            :param italic: Whether to make the text italic or not. Defaults to False.
            :param underline: Whether to make the text underlined or not. Defaults to False.
            :param color: The color of the text to use. Defaults to \"white\".
            :param background: The background color of the text. Defaults to None.
            :param topleft: The topleft position of the text. Only use one of the position arguments. If more than one used, then pgzero will choose a random one. Defaults to None.
            :param bottomleft: The bottomleft position of the text. Only use one of the position arguments. If more than one used, then pgzero will choose a random one. Defaults to None.
            :param topright: The topright position of the text. Only use one of the position arguments. If more than one used, then pgzero will choose a random one. Defaults to None.
            :param bottomright: The bottomright position of the text. Only use one of the position arguments. If more than one used, then pgzero will choose a random one. Defaults to None.
            :param midtop: The midtop position of the text. Only use one of the position arguments. If more than one used, then pgzero will choose a random one. Defaults to None.
            :param midleft: The midleft position of the text. Only use one of the position arguments. If more than one used, then pgzero will choose a random one. Defaults to None.
            :param midbottom: The midbottom position of the text. Only use one of the position arguments. If more than one used, then pgzero will choose a random one. Defaults to None.
            :param midright: The midright position of the text. Only use one of the position arguments. If more than one used, then pgzero will choose a random one. Defaults to None.
            :param center: The midtop position of the text. Only use one of the position arguments. If more than one used, then pgzero will choose a random one. Defaults to None.
            :param width: The maximum width of the text, in pixels. If text going past the width, the text will wrap by word. Defaults to None (No limit for the width of text).
            :param widthem: The maximum width of the text, in font-based em units. If text going past the width, the text will wrap by word. Defaults to None (No limit for the width of text).
            :param lineheight: The vertical spacing between the lines, in units of the font's default line height. Defaults to 1.
            :param align: The horizontal positioning of lines with respect to each other. Defaults to None. Valid strings for align are \"left\", \"center\", or \"right\", or a numerical value from 0.0 to 1.0. 0.0 is left and 1.0 is right.
            :param owidth: The outline thickness, in outline units. Defaults to None (no outline).
            :param ocolor: The outline color. As a special case, setting color to a transparent value (e.g. (0,0,0,0)) while using outilnes will cause the text to be invisible, giving a hollow outline. (This feature is not compatible with gcolor). Defaults to \"black\".
            :param shadow: (x,y) values representing the drop shadow offset, in shadow units. Defaults to None (No shadow).
            :param scolor: The shadow color. Defaults to \"black\".
            :param gcolor: The lower gradient stop color. Defaults to None (No gradient).
            :param alpha: Alpha transparency value between 0 and 1. Defaults to 1.0 (No transperency)
            :param anchor: a length-2 sequence of horizontal and vertical anchor fractions. Defaults to (0.0, 0.0).
            :param angle: counterclockwise rotation angle in degrees. Defaults to 0 (No rotation).

            :raise ScreenError: When screen is not initilized with init(screen).
            """
            _init_check()
            if topleft:
                pgzero_drawer.text(text, fontname=fontname, fontsize=fontsize, sysfontname=sysfontname, antialias=antialias, bold=bold, italic=italic, underline=underline, color=color, background=background, topleft=topleft,
                width=width, widthem=widthem, lineheight=lineheight, align=align, owidth=owidth, ocolor=ocolor, shadow=shadow, scolor=scolor, gcolor=gcolor, alpha=alpha, anchor=anchor, angle=angle)
            if bottomleft:
                pgzero_drawer.text(text, fontname=fontname, fontsize=fontsize, sysfontname=sysfontname, antialias=antialias, bold=bold, italic=italic, underline=underline, color=color, background=background, bottomleft=bottomleft,
                width=width, widthem=widthem, lineheight=lineheight, align=align, owidth=owidth, ocolor=ocolor, shadow=shadow, scolor=scolor, gcolor=gcolor, alpha=alpha, anchor=anchor, angle=angle)
            if topright:
                pgzero_drawer.text(text, fontname=fontname, fontsize=fontsize, sysfontname=sysfontname, antialias=antialias, bold=bold, italic=italic, underline=underline, color=color, background=background, topright=topright,
                width=width, widthem=widthem, lineheight=lineheight, align=align, owidth=owidth, ocolor=ocolor, shadow=shadow, scolor=scolor, gcolor=gcolor, alpha=alpha, anchor=anchor, angle=angle)
            if bottomright:
                pgzero_drawer.text(text, fontname=fontname, fontsize=fontsize, sysfontname=sysfontname, antialias=antialias, bold=bold, italic=italic, underline=underline, color=color, background=background, bottomright=bottomright,
                width=width, widthem=widthem, lineheight=lineheight, align=align, owidth=owidth, ocolor=ocolor, shadow=shadow, scolor=scolor, gcolor=gcolor, alpha=alpha, anchor=anchor, angle=angle)
            if midtop:
                pgzero_drawer.text(text, fontname=fontname, fontsize=fontsize, sysfontname=sysfontname, antialias=antialias, bold=bold, italic=italic, underline=underline, color=color, background=background, midtop=midtop,
                width=width, widthem=widthem, lineheight=lineheight, align=align, owidth=owidth, ocolor=ocolor, shadow=shadow, scolor=scolor, gcolor=gcolor, alpha=alpha, anchor=anchor, angle=angle)
            if midleft:
                pgzero_drawer.text(text, fontname=fontname, fontsize=fontsize, sysfontname=sysfontname, antialias=antialias, bold=bold, italic=italic, underline=underline, color=color, background=background, midleft=midleft,
                width=width, widthem=widthem, lineheight=lineheight, align=align, owidth=owidth, ocolor=ocolor, shadow=shadow, scolor=scolor, gcolor=gcolor, alpha=alpha, anchor=anchor, angle=angle)
            if midbottom:
                pgzero_drawer.text(text, fontname=fontname, fontsize=fontsize, sysfontname=sysfontname, antialias=antialias, bold=bold, italic=italic, underline=underline, color=color, background=background, midbottom=midbottom,
                width=width, widthem=widthem, lineheight=lineheight, align=align, owidth=owidth, ocolor=ocolor, shadow=shadow, scolor=scolor, gcolor=gcolor, alpha=alpha, anchor=anchor, angle=angle)
            if midright:
                pgzero_drawer.text(text, fontname=fontname, fontsize=fontsize, sysfontname=sysfontname, antialias=antialias, bold=bold, italic=italic, underline=underline, color=color, background=background, midright=midright,
                width=width, widthem=widthem, lineheight=lineheight, align=align, owidth=owidth, ocolor=ocolor, shadow=shadow, scolor=scolor, gcolor=gcolor, alpha=alpha, anchor=anchor, angle=angle)
            if center:
                pgzero_drawer.text(text, fontname=fontname, fontsize=fontsize, sysfontname=sysfontname, antialias=antialias, bold=bold, italic=italic, underline=underline, color=color, background=background, center=center,
                width=width, widthem=widthem, lineheight=lineheight, align=align, owidth=owidth, ocolor=ocolor, shadow=shadow, scolor=scolor, gcolor=gcolor, alpha=alpha, anchor=anchor, angle=angle)

        @staticmethod
        def textbox(text: str, rect: Rect | pygame.rect.Rect | ZRect, fontname: str | None = None, sysfontname: str | None = None, lineheight: float | None = None, anchor: float | None = None,  bold: bool | None = None, 
                    italic: bool | None = None, underline: bool | None = None,  antialias: bool = True, color: str | tuple | None = None, background: str | tuple | None = None, widthem: float | None = None, align: str | None = None, 
                    owidth: float | None = None, ocolor: tuple | str | None = None, shadow: tuple | None = None, scolor: tuple | str | None = None, gcolor: tuple | str | None = None, alpha: float = 1.0, angle: float = 0) -> None:
            """
            Function to wrap text into a Rect.

            :param text: The text to be wrapped inside a Rect.
            :param rect: The Rect for the text to be wrapped in.
            :param fontname: The font name for the text. Font names must be in a font directory and in the .ttf format. Defualts to the sysfontname.
            :param sysfontname: The system font name to use if fontname is omitted. Font names must be in a font directory and in the .ttf format. Defaults to the system font.
            :param lineheight: The vertical spacing between the lines, in units of the font's default line height. Defaults to 1.
            :param anchor: a length-2 sequence of horizontal and vertical anchor fractions. Defaults to (0.0, 0.0).
            :param bold: Whether to make the text bold or not. Defaults to False.
            :param italic: Whether to make the text italic or not. Defaults to False.
            :param underline: Whether to make the text underlined or not. Defaults to False.
            :param antialias: Whether to render with antialiasing or not. Defaults to True.
            :param color: The color of the text to use. Defaults to \"white\".
            :param background: The background color of the text. Defaults to None.
            :param widthem: The maximum width of the text, in font-based em units. If text going past the width, the text will wrap by word. Defaults to None (No limit for the width of text).
            :param align: The horizontal positioning of lines with respect to each other. Defaults to None. Valid strings for align are \"left\", \"center\", or \"right\", or a numerical value from 0.0 to 1.0. 0.0 is left and 1.0 is right.
            :param owidth: The outline thickness, in outline units. Defaults to None (no outline).
            :param ocolor: The outline color. As a special case, setting color to a transparent value (e.g. (0,0,0,0)) while using outilnes will cause the text to be invisible, giving a hollow outline. (This feature is not compatible with gcolor). Defaults to \"black\".
            :param shadow: (x,y) values representing the drop shadow offset, in shadow units. Defaults to None (No shadow).
            :param scolor: The shadow color. Defaults to \"black\".
            :param gcolor: The lower gradient stop color. Defaults to None (No gradient).
            :param alpha: Alpha transparency value between 0 and 1. Defaults to 1.0 (No transperency)
            :param angle: counterclockwise rotation angle in degrees. Defaults to 0 (No rotation).

            :raise ScreenError: When screen is not initilized with init(screen).
            """
            _init_check()
            pgzero_drawer.textbox(text, rect, fontname=fontname, sysfontname=sysfontname, lineheight=lineheight, anchor=anchor, bold=bold, italic=italic, underline=underline, antialias=antialias,
                                color=color, background=background, widthem=widthem, align=align, owidth=owidth, ocolor=ocolor, shadow=shadow, scolor=scolor, gcolor=gcolor, alpha=alpha, angle=angle)

        @staticmethod
        @overload
        def rect(rect: Rect | pygame.rect.Rect | ZRect, color: tuple[float, float, float] | str, thickness: int | float = 1) -> None:
            """
            Function to draw a rect to the Screen. Draws the outline of the rect. If you want to draw the full, filled in rect, see Screen.draw.filled_rect().

            :param rect: The rect to draw on the screen.
            :param color: The color of the rect.
            :param thickness: The thickness of the outline of the rect.

            :raise ScreenError: When screen is not initilized with init(screen).
            """
            ...

        @staticmethod
        @overload
        def rect(top: int | float, left: int | float, width: int | float, height: int | float, color: tuple[float, float, float] | str, thickness: int | float = 1) -> None:
            """
            Function to draw a rect to the Screen. Draws the outline of the rect. If you want to draw the full, filled in rect, see Screen.draw.filled_rect().

            :param top: The top edge of the rect.
            :param left: The left edge of the rect.
            :param width: The width of the rect.
            :param height: The height of the rect.
            :param color: The color of the rect.
            :param thickness: The thickness of the outline of the rect.

            :raise ScreenError: When screen is not initilized with init(screen).
            """
            ...

        @staticmethod
        def rect(*args):
            _init_check()
            if isinstance(args[0], (Rect, pygame.rect.Rect, ZRect)):
                if len(args) == 2:
                    width = 1
                else:
                    width = args[2]
                if width == 0:
                    raise ScreenError("Cannot draw a circle with 0 thickness")
                elif width <= 0:
                    raise ScreenError("Cannot draw a circle with negative thickness")
                pygame.draw.rect(pgzero_screen.surface, args[1], args[0], width)
            elif isinstance(args[0], (int, float)):
                if len(args) == 2:
                    width = 1
                else:
                    width = args[2]
                if width == 0:
                    raise ScreenError("Cannot draw a circle with 0 thickness")
                elif width <= 0:
                    raise ScreenError("Cannot draw a circle with negative thickness")
                pygame.draw.rect(pgzero_screen.surface, args[4], Rect(args[0], args[1], args[2], args[3]), width)

        @staticmethod
        @overload
        def filled_rect(rect: Rect | pygame.rect.Rect, color: tuple[float, float, float] | str) -> None:
            """
            Function to draw a rect to the Screen. Draws the full, filled in rect. If you want to draw the outline of the rect, see Screen.draw.rect().

            :param rect: The rect to draw on the screen.
            :param color: The color of the rect.

            :raise ScreenError: When screen is not initilized with init(screen).
            """
            ...
        
        @staticmethod
        @overload
        def filled_rect(top: int | float, left: int | float, width: int | float, height: int | float, color: tuple[float, float, float] | str) -> None:
            """
            Function to draw a rect to the Screen. Draws the full, filled in rect. If you want to draw the outline of the rect, see Screen.draw.rect().

            :param top: The top edge of the rect.
            :param left: The left edge of the rect.
            :param width: The width of the rect.
            :param height: The height of the rect.
            :param color: The color of the rect.

            :raise ScreenError: When screen is not initilized with init(screen).
            """
            ...

        @staticmethod
        def filled_rect(*args) -> None:
            _init_check()
            if len(args) == 2:
                pgzero_drawer.filled_rect(args[0], args[1])
            elif len(args) == 5:
                pgzero_drawer.filled_rect(Rect(args[0], args[1], args[2], args[3]), args[4])

        @staticmethod
        def line(start: tuple[float, float], end: tuple[float, float], color: tuple[float, float, float] | str, thickness: float | int = 1) -> Rect:
            """
            Function to draw a line to Screen.

            :param start: The start coordinates for the line.
            :param end: The end coordinates for the line.
            :param color: The color of the line.
            :param thickness: The thickness of the line. Defaults to 1.

            :return Rect: The Rect that the line is drawn within (the circumscribed Rect).

            :raise ScreenError: When the screen is not initialized with init(screen).
            """
            _init_check()
            return pygame.draw.line(pgzero_screen.surface, color, start, end, thickness)
        
        @staticmethod
        def polygon(points: list[tuple[float, float]], color: tuple[float, float, float] | str, thickness: float | int = 1) -> Rect:
            """
            Function to draw a polygon to Screen.

            :param points: The points of the polygon.
            :param color: The color of the line.
            :param thickness: The thickness of the line. Defaults to 1.

            :return Rect: The Rect that the polygon is drawn within (the circumscribed Rect).

            :raise ScreenError: When the screen is not initialized with init(screen).
            """
            _init_check()
            return pygame.draw.polygon(pgzero_screen.surface, color, points, thickness)

        @staticmethod
        @overload
        def circle(center: tuple[float, float], radius: int | float, color: tuple[float, float, float] | str, thickness: float | int = 1) -> None:
            """
            Function to draw a circle to Screen. Draws the outline of the circle. If you want to draw the full, filled in circle, see Screen.draw.filled_circle().

            :param center: The center of the circle.
            :param radius: The radius of the circle.
            :param color: The color of the circle.
            :param thickness: The thickness of the line. Defaults to 1.

            :raise ScreenError: When the screen is not initialized with init(screen) or when the thickness is less than or equal to 0.
            """
            ...
    
        @staticmethod
        @overload
        def circle(circle: Circle, color: tuple[float, float, float] | str, thickness: float | int = 1) -> None:
            """
            Function to draw a circle to Screen. Draws the outline of the circle. If you want to draw the full, filled in circle, see Screen.draw.filled_circle().

            :param circle: the circle to draw on the Screen.
            :param color: The color of the circle.
            :param thickness: The thickness of the line. Defaults to 1.

            :raise ScreenError: When the screen is not initialized with init(screen) or when the thickness is less than or equal to 0.
            """
            ...

        @staticmethod
        def circle(*args):
            _init_check()
            if isinstance(args[0], tuple):
                if len(args) == 4:
                    width = args[3]
                else:
                    width = 1
                if width == 0:
                    raise ScreenError("Cannot draw a circle with 0 thickness")
                elif width <= 0:
                    raise ScreenError("Cannot draw a circle with negative thickness")
                return pygame.draw.circle(pgzero_screen.surface, args[2], args[0], args[1], width)
            elif isinstance(args[0], Circle):
                if len(args) == 3:
                    width = args[2]
                else:
                    width = 1
                if width == 0:
                    raise ScreenError("Cannot draw a circle with 0 thickness")
                elif width <= 0:
                    raise ScreenError("Cannot draw a circle with negative thickness")
                return pygame.draw.circle(pgzero_screen.surface, args[1], args[0].center, args[0].radius, width)

        @staticmethod
        @overload
        def filled_circle(center: tuple[float, float], radius: int | float, color: tuple[float, float, float] | str) -> None:
            """
            Function to draw a circle to Screen.

            :param center: The center of the circle.
            :param radius: The radius of the circle.
            :param color: The color of the circle.

            :raise ScreenError: When the screen is not initialized with init(screen).
            """
            ...
        
        @staticmethod
        @overload
        def filled_circle(circle: Circle, color: tuple[float, float, float] | str) -> None:
            """
            Function to draw a circle to Screen.

            :param circle: The circle.
            :param color: The color of the circle.

            :raise ScreenError: When the screen is not initialized with init(screen).
            """

        @staticmethod
        def filled_circle(*args):
            _init_check()
            if len(args) == 3:
                pygame.draw.circle(pgzero_screen.surface, args[2], args[0], args[1], 0)
            elif len(args) == 2:
                pygame.draw.circle(pgzero_screen.surface, args[1], args[0].center, args[0].radius, 0)

        @staticmethod
        def gradient_line(start_pos, end_pos, start_color, end_color, thickness = 1):
            x1, y1 = start_pos
            x2, y2 = end_pos
            dx = x2 - x1
            dy = y2 - y1
            steps = max(abs(dx), abs(dy))
            if steps == 0:
                return
            for i in range(int(steps) + 1):
                t = i / steps
                current_color = Screen.lerp_color(start_color, end_color, t)
                current_x = int(x1 + t * dx)
                current_y = int(y1 + t * dy)
                Screen.draw.filled_rect(Rect((current_x, current_y), (thickness, thickness)), current_color)


    class cursor:
        """class for changing the cursor shape on the Screen."""
        arrow = pygame.SYSTEM_CURSOR_ARROW
        hand = pygame.SYSTEM_CURSOR_HAND
        cross = pygame.SYSTEM_CURSOR_CROSSHAIR
        text_cursor = pygame.SYSTEM_CURSOR_IBEAM
        unavailable_cursor = pygame.SYSTEM_CURSOR_NO
        cross_with_arrows = pygame.SYSTEM_CURSOR_SIZEALL
        resize_right_diagonal = pygame.SYSTEM_CURSOR_SIZENESW
        resize_left_diagonal = pygame.SYSTEM_CURSOR_SIZENWSE
        resize_vert = pygame.SYSTEM_CURSOR_SIZENS
        resize_horz = pygame.SYSTEM_CURSOR_SIZEWE
        loading = pygame.SYSTEM_CURSOR_WAIT
        ball = pygame.cursors.ball
        broken_x = pygame.cursors.broken_x
        left_arrow = pygame.cursors.tri_left
        diamond = pygame.cursors.diamond
        right_arrow = pygame.cursors.tri_right

        @staticmethod
        def set_cursor(cursor) -> None:
            """
            Sets the cursor shape to a specified cursor.

            :param cursor: The cursor that the mouse should be. Use Screen.mouse. to get the accepted mouse shapes.
            """
            pygame.mouse.set_cursor(cursor)

    class mouse:
        wheel_down = PGZeroMouse.WHEEL_DOWN
        wheel_up = PGZeroMouse.WHEEL_UP
        left_click = PGZeroMouse.LEFT
        right_click = PGZeroMouse.RIGHT

    class change_frames_per_second:
        @staticmethod
        def draw_func(frames_per_second):
            global draw_frames_per_second
            if frames_per_second <= 0:
                raise ScreenError("Frames per second must be greater than 0.")
            draw_frames_per_second = frames_per_second
        
        @staticmethod
        def update_func(frames_per_second):
            global update_frames_per_second
            if frames_per_second <= 0:
                raise ScreenError("Frames per second must be greater than 0.")
            update_frames_per_second = frames_per_second