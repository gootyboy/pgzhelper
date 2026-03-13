# Pgzhelper

Pgzhelper is a helper package for pgzero that adds additional capabilities such as camera support, shape utilities, window controls, and extended drawing features. Some capabilities can also be used in pygame.

---

> ### ⚠️ ***Run using `pgzhelper_run.go()`, not `pgzrun.go()`***
> If you do not run with `pgzhelper_run.go()`, then camera support and changing the frames per second will fail.

> ### ⚠️ ***Do not import Screen as `screen`***
> If you import Screen as `screen`, then the pgzhelper Screen will overload the pgzero Screen, causing all capabilities to fail.

---

## Table of Contents
- Installation
- Why Use Pgzhelper?
- Additional Capabilities
- Shapes
- Advantages of Using Screen
- Camera Capabilities
- Versions
- Coming Soon

## Quick Start

---

### Installation
```
pip install pgzhelper
```

### Usage
```python
from pgzhelper import *

def draw():
    Screen.fill("blue")
    screen.draw.text("Hello!", (100, 100))

pgzhelper_run.go()
```

---

## Why Use Pgzhelper?

Pgzhelper extends pgzero with features that are normally difficult or impossible to do easily, including:

- camera loading, zooming, and background removal
- drawing shapes with thickness and advanced geometry
- window positioning and centering
- cursor customization
- changing FPS dynamically
- a unified Screen object with full documentation

These additions make pgzero more flexible and powerful for game development and educational projects.

---

## Additional Capabilities

- thickness parameter for line drawing and drawing rects
- drawing shapes (polygons, etc. — see shape list below)
- set the window position (on the laptop)
- center the window (on the laptop)
- change the cursor shape (on the screen)
- change the frames per second in functions (requires `pgzhelper_run.go()`)

### Shapes

- HRect (helper rect) class
- Circle class
- Shape class
- Polygon class
- Ellipse class
- Quadrilateral class
- Triangle class
- EquilateralTriangle class
- Square class
- shapes Enum

The Triangle class includes rotate around pivot, move up (moves down visually), move down (moves up visually), move left, and move right.

The EquilateralTriangle class includes a direction (DOWN or UP) parameter and the same methods as the Triangle class ***(moving or rotating will return a Triangle, not an EquilateralTriangle)***.

---

---

## Advantages of Using Screen

Screen functions have the same capabilities as pgzero’s screen functions, plus additional features such as line thickness and shape drawing. All Screen functions include full documentation, so you do not need to reference the pgzero website.

---

## Camera Capabilities

1. Load a camera by number (1 = first camera, 2 = second camera). Returns `None`.
2. Set the zoom factor (1 = full view, 2 = zoom in by factor of 2).
3. Optionally remove the background and replace it with a color.
4. Get camera width and height (in pixels).
5. Camera requires `pgzhelper_run.go()`, not `pgzrun.go()`.

---

## Versions

Version 0.0.1: Base code published.  
Version 0.0.2: Fix errors and bugs.  
Version 0.0.3: Complete documentation.  
Version 0.0.4: Make init() into the injection, so the user does not have to use that. Add changing frames per second for all functions.
**(Latest) Version 0.0.5:** More documentation added.

---

## Coming Soon

Version 0.0.6: Completed Documentation
Version 0.0.7: Add additional `on_mouse_drag(pos, button)` function.
