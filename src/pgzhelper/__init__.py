"""Helper package for pgzero.
Your draw function must be:

    def draw():
        init(screen)
        ... # The rest of your code

# Do not import Screen as screen
as it would override the pgzero screen.

# Addition Capabilities:

thickness parameter for line drawing and drawing rects.

Drawing shapes (polygons, ... (see shape list below))

set the window position (on the laptop)

center the window (on the laptop)

Changing the cursor shape (on the screen)

Changing the frames per second in the functions (For the this to work, you must call pgzhelper_run.go(), not pgzrun.go())

Shapes:

HRect (helper rect) class

Circle class

Shape class

Polygon class

Ellipse class

Quadrilateral class

Triangle class with rotate around pivot, move up (this is move down to our eyes, because when y increases in pgzero, the shape moves down), move down (this is move up to our eyes, because when y decreases in pgzero, the shape moves up), move left, and move_right

EquilateralTriangle class with direction (DOWN or UP) and the same methods as the Triangle class (moving or rotating will return a Triangle, not an EquilateralTriangle)

Square class

shapes Enum so you can do shapes.rect, shapes.polygon, etc.

Camera capabilities:

loading a camera (with the number which is what camera you want if you have more than 1. 1 will load the first camera and 2 will load the second camera). You do not need to store this in a variable. It will return None.

setting the zoom factor. How zoomed in it should be. 1 means it shows the full camera view. 2 means it zooms into the center of the camera by a factor of 2.

if you want to remove the background and replace it with a color or not.

get camera width and height, the dimentions (in pixels) of how big the camera view is (on screen).

For the camera to work, you must call pgzhelper_run.go(), not pgzrun.go()
"""

from .pyscreen import *
from . import _runner as pgzhelper_run