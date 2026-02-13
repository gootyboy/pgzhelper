# Pgzhelper

# Run using pgzhelper_run.go(), not pgzrun.go()
as camera and changing the frames per second will fail.

# Do not import Screen as screen
as screen will overload the pgzero-screen making all capabilities fail.

Helper package to pgzero. Has addition capabilities such as showing the camera. Some capabilities can also be used in pygame.

The first line of your draw function must include `init(screen)`

In the draw function, when you pass in the screen parameter for init(screen), this is expecting the pgzero screen or the pygame display surface. For pgzero, just enter screen for the screen parameter. This will have a yellow underline under it, but do not worry because this is what is supposed to happen.

If you do not call the init function, then any function that you run will raise a ScreenError. This is for making sure both the pgzero/pygame screen and the surface that Screen uses are both the same. If Screen makes a new surface, then doing one action in one of them will not affect the other.

Example (assuming that Screen creates its own surface):

```python
def draw():
    Screen.fill("blue") # Makes the screen blue
```

```python
def draw():
    Screen.fill("blue")
    Screen.draw.text("hi", topleft=(100, 100))
    screen.draw.text("bye", topleft=(200, 200)) # You can only see "hi" because Screen is 
    # overloading the screen. With the init(),
    # you would see both the hi and the bye.
```

This means, that, your draw function can have some Screen drawings and some screen drawings, and the output won't be affected. So, an action in one of them affects the other.

# Advantages of using Screen:

All of the Screen functions have the exact same capabilities as the screen functions, just with some more such as drawing lines with 5 thickness.

Also, all of the Screen functions have full documentation, so you do not have to go to the pgzero website to find out what functions and what parameters there are.

# Additional capabilities:

thickness parameter for line drawing and drawing rects.

Drawing polygons

set the window position (on the laptop)

center the window (on the laptop)

Changing the cursor shape (on the screen)

Changing the frames per second in the functions (For the this to work, you must call pgzhelper_run.go(), not pgzrun.go())

Shapes:

HRect (helper rect) class that has .collidecircle()

Circle class that has .colliderect(), .collidecircle(), .collidepoint()

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

# Versions

Version 0.0.1: Base code published
(Latest) Version 0.0.2: Add documentation to all Screen functions and classes.
Version 0.0.3: Add documentation to all Shape classes.
