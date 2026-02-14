"""Camera file for pgzhelper. Not meant for user use. Use load_camera() and other functions in pgzscreen instead of _camera."""

from .utilities import *

_camera_loaded = False

def load_camera(camera_number: int = 0) -> None:
    """
    Loads a camera.

    :param camera_number: If you have more than 1 camera, then 0 will be one of the cameras and 1 will be the other one.
    """
    global _cap, _width, _height, _camera_surface, _zoom_factor, _remove_bg, _options, _segmenter, _bg_color, _camera_loaded
    _cap = cv2.VideoCapture(camera_number)
    _width = int(_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    _height = int(_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    _camera_surface = pygame.Surface((_width, _height))

    _zoom_factor = 1

    _remove_bg = False

    _BaseOptions = python.BaseOptions
    _ImageSegmenter = vision.ImageSegmenter
    _VisionRunningMode = vision.RunningMode

    _options = vision.ImageSegmenterOptions(
        base_options=_BaseOptions(model_asset_path="/Users/gootyboy/projects/python__coding/pgz_camera/image_segmenter.tflite"),
        running_mode=_VisionRunningMode.IMAGE
    )

    _segmenter = _ImageSegmenter.create_from_options(_options)

    _bg_color = (255, 255, 255)

    _camera_loaded = True

def set_zoom_factor(factor: float) -> None:
    """
    Sets the camera zoom factor

    :param factor: How zoomed in it should be. 1 means it shows the full camera view. 2 means it zooms into the center of the camera by a factor of 2.
    """
    global _zoom_factor
    _zoom_factor = factor

def camera_update_func() -> None:
    """
    Call this function in your update() function. You do not need to do this if you call pgzhelper_run.go() instead of pgzrun.go()

    :raise CameraNotLoadedError: When the camera is not loaded.
    """
    global _camera_surface, _zoom_factor, _remove_bg
    if not _camera_loaded:
        raise CameraNotLoadedError("camera is not loaded. Load it using load_camera()")

    ret, frame = _cap.read()
    if not ret:
        return

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if _zoom_factor > 1.0:
        cx, cy = _width // 2, _height // 2
        nw = int(_width / _zoom_factor)
        nh = int(_height / _zoom_factor)
        x1 = max(cx - nw // 2, 0)
        y1 = max(cy - nh // 2, 0)
        x2 = min(cx + nw // 2, _width)
        y2 = min(cy + nh // 2, _height)
        frame = frame[y1:y2, x1:x2]

    frame = cv2.resize(frame, (_width, _height))

    if _remove_bg:
        mp_image = Image(image_format=ImageFormat.SRGB, data=frame)
        result = _segmenter.segment(mp_image)
        mask = result.confidence_masks[0].numpy_view().squeeze()

        condition = mask > 0.5
        bg = np.zeros_like(frame)
        bg[:] = _bg_color
        output = np.where(condition[..., None], frame, bg)
    else:
        output = frame

    pygame_frame = pygame.surfarray.make_surface(np.rot90(output))
    _camera_surface = pygame.transform.flip(pygame_frame, True, False)

def remove_background(color = (255, 255, 255)) -> None:
    """
    Removes the camera output's background

    :param color: The color to replace the background with. Defaults to (255, 255, 255).
    """
    global _bg_color, _remove_bg
    _bg_color = color
    _remove_bg = True

def is_camera_loaded() -> bool:
    """
    Checks if the camera is loaded.

    :return True: When the camera is loaded.
    :return False: When the camera is not loaded.
    """
    return _camera_loaded

def camera_draw_func(screen):
    """
    Call this function in your draw() function. You do not need to do this if you call pgzhelper_run.go() instead of pgzrun.go()

    :raise CameraNotLoadedError: When the camera is not loaded.
    """
    if not _camera_loaded:
        raise CameraNotLoadedError("camera is not loaded. Load it using load_camera()")
    if screen:
        screen.blit(_camera_surface, (0, 0))

def camera_on_quit_func():
    """
    Call this function in your on_quit() function. You do not need to do this if you call pgzhelper_run.go() instead of pgzrun.go()

    :raise CameraNotLoadedError: When the camera is not loaded.
    """
    if not _camera_loaded:
        raise CameraNotLoadedError("camera is not loaded. Load it using load_camera()")
    _cap.release()
    cv2.destroyAllWindows()

def get_camera_width() -> int:
    """
    Gets the width of the output of the camera (in pixels).

    :return int: The width of the output of the camera.
    """
    return _width

def get_camera_height():
    """
    Gets the height of the output of the camera (in pixels).

    :return int: The height of the output of the camera.
    """
    return _height