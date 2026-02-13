import cv2
import pygame
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import Image, ImageFormat

class CameraError(Exception):
    pass

class CameraNotLoadedError(CameraError):
    pass

camera_loaded = False

def load_camera(camera_number = 0):
    global cap, width, height, camera_surface, zoom_factor, remove_bg, options, segmenter, bg_color, camera_loaded
    cap = cv2.VideoCapture(camera_number)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    camera_surface = pygame.Surface((width, height))

    zoom_factor = 1

    remove_bg = False

    BaseOptions = python.BaseOptions
    ImageSegmenter = vision.ImageSegmenter
    VisionRunningMode = vision.RunningMode

    options = vision.ImageSegmenterOptions(
        base_options=BaseOptions(model_asset_path="/Users/gootyboy/projects/python__coding/pgz_camera/image_segmenter.tflite"),
        running_mode=VisionRunningMode.IMAGE
    )

    segmenter = ImageSegmenter.create_from_options(options)

    bg_color = (255, 255, 255)

    camera_loaded = True

def set_zoom_factor(factor):
    global zoom_factor
    zoom_factor = factor

def camera_update_func():
    global camera_surface, zoom_factor, remove_bg
    if not camera_loaded:
        raise CameraNotLoadedError("camera is not loaded. Load it using load_camera()")

    ret, frame = cap.read()
    if not ret:
        return

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if zoom_factor > 1.0:
        cx, cy = width // 2, height // 2
        nw = int(width / zoom_factor)
        nh = int(height / zoom_factor)
        x1 = max(cx - nw // 2, 0)
        y1 = max(cy - nh // 2, 0)
        x2 = min(cx + nw // 2, width)
        y2 = min(cy + nh // 2, height)
        frame = frame[y1:y2, x1:x2]

    frame = cv2.resize(frame, (width, height))

    if remove_bg:
        mp_image = Image(image_format=ImageFormat.SRGB, data=frame)
        result = segmenter.segment(mp_image)
        mask = result.confidence_masks[0].numpy_view().squeeze()

        condition = mask > 0.5
        bg = np.zeros_like(frame)
        bg[:] = bg_color
        output = np.where(condition[..., None], frame, bg)
    else:
        output = frame

    pygame_frame = pygame.surfarray.make_surface(np.rot90(output))
    camera_surface = pygame.transform.flip(pygame_frame, True, False)

def remove_background(color = (255, 255, 255)):
    global bg_color, remove_bg
    bg_color = color
    remove_bg = True

def is_camera_loaded():
    return camera_loaded

def camera_draw_func(screen):
    if not camera_loaded:
        raise CameraNotLoadedError("camera is not loaded. Load it using load_camera()")
    if screen:
        screen.blit(camera_surface, (0, 0))

def camera_on_quit_func():
    if not camera_loaded:
        raise CameraNotLoadedError("camera is not loaded. Load it using load_camera()")
    cap.release()
    cv2.destroyAllWindows()

def get_camera_width():
    return width

def get_camera_height():
    return height