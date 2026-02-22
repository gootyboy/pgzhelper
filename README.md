# Pgzhelper

---

## Run using pgzhelper_run.go(), not pgzrun.go()

If you do not run with pgzhelper_run.go(), then camera and changing the frames per second will fail.

---

## Do not import Screen as screen

If you import Screen as screen, then the pgzhelper-screen that you imported will overload the pgzero-screen making all capabilities fail.

## The first line of your draw function must include `init(screen)`

If you do not include this, then pgzhelper will raise an InitError.

---

Helper package to pgzero. Has addition capabilities such as showing the camera. Some capabilities can also be used in pygame.

In the draw function, when you pass in the screen parameter for init(screen), this is expecting the pgzero screen or the pygame display surface. For pgzero, just enter screen for the screen parameter. This will have a yellow underline under it, but do not worry because this is what is supposed to happen.

If you do not call the init function, then any function that you run will raise a ScreenError. This is for making sure both the pgzero/pygame screen and the surface that Screen uses are both the same. If Screen makes a new surface, then doing one action in one of them will not affect the other.

Example (assuming that Screen creates its own surface):

```python
# In a real code file, you must include a init(screen)
def draw():
    Screen.fill("blue") # Makes the screen blue.
```

```python
# In a real code file, you must include a init(screen)
def draw():
    Screen.fill("blue")
    Screen.draw.text("hi", topleft=(100, 100))
    screen.draw.text("bye", topleft=(200, 200)) # You can only see "hi" because Screen is 
    # overloading the screen. With the init(), you would see both the "hi" and the "bye".
```

This means, that, your draw function can have some Screen drawings and some screen drawings, and the output won't be affected. So, an action in one of them affects the other.

---

## Advantages of using Screen

All of the Screen functions have the exact same capabilities as the screen functions, just with some more such as drawing lines with thickness.

Also, all of the Screen functions have full documentation, so you do not have to go to the pgzero website to find out what functions and what parameters there are.

---

## Additional capabilities

thickness parameter for line drawing and drawing rects.

Drawing shapes (polygons, ... (see shape list below))

set the window position (on the laptop)

center the window (on the laptop)

Changing the cursor shape (on the screen)

Changing the frames per second in the functions (For the this to work, you must call pgzhelper_run.go(), not pgzrun.go())

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

The Triangle Class includes rotate around pivot, move up (this is move down to our eyes, because when y increases in pgzero, the shape moves down), move down (this is move up to our eyes, because when y decreases in pgzero, the shape moves up), move left, and move_right.

The EquilateralTriangle class includes a direction (DOWN or UP) parameter and the same methods as the Triangle class **(moving or rotating will return a Triangle, not an EquilateralTriangle)**.

### Camera capabilities

1. loading a camera (with the number which is what camera you want if you have more than 1. 1 will load the first camera and 2 will load the second camera). You do not need to store this in a variable. It will return None.

2. setting the zoom factor. How zoomed in it should be. 1 means it shows the full camera view. 2 means it zooms into the center of the camera by a factor of 2.

3. if you want to remove the background and replace it with a color or not.

4. get camera width and height, the dimentions (in pixels) of how big the camera view is (on screen).

5. For the camera to work, you must call pgzhelper_run.go(), not pgzrun.go()

## Versions

Version 0.0.1: Base code published.

Version 0.0.2: Fix errors and bugs.

Version 0.0.3: Complete Documentation.

(Latest) Version 0.0.4: Add changing frames per second for all functions. Add additional on_mouse_drag(pos, button) function.

## Coming Soon

Version 0.0.5: 
