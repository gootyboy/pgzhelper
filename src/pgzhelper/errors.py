"""All of pgzhelper's errors are found here."""

class ScreenError(Exception):
    """Base error class for all errors in pgzhelper."""
    def __init__(self, *args):
        """
        Base error class for all errors in pgzhelper.
        
        :param args: The messsage to be shown when error is raised.
        """
        super().__init__(*args)

class MouseError(ScreenError):
    """Error for all mouse-related errors (setting the mouse shape)"""
    def __init__(self, *args):
        """
        Error for all mouse-related errors (setting the mouse shape)
        
        :param args: The messsage to be shown when error is raised.
        """
        super().__init__(*args)

class InitError(ScreenError):
    """Error for when you draw before init(screen) is called."""
    def __init__(self, *args):
        """
        Error for when you draw before init(screen) is called.

        :param args: The messsage to be shown when error is raised.
        """
        super().__init__(*args)

class ThicknessError(ScreenError):
    """Error class for when thickness is less than or equal to 0."""
    def __init__(self, *args):
        """
        Error class for when thickness is less than or equal to 0.

        :param args: The messsage to be shown when error is raised.
        """
        super().__init__(*args)

class ShapeError(ScreenError):
    """Error class for any incorrect shapes and for any errors in shapes."""
    def __init__(self, *args):
        """
        Error class for any incorrect shapes and for any errors in shapes.

        :param args: The messsage to be shown when error is raised.
        """
        super().__init__(*args)

class CameraNotLoadedError(ScreenError):
    """Error class for when the camera is drawn before it is loaded."""
    def __init__(self, *args):
        """
        Error class for when the camera is drawn before it is loaded.

        :param args: The messsage to be shown when error is raised.
        """
        super().__init__(*args)

class FPSError(ScreenError):
    """Error class for when the FPS for a function is less than or equal to 0."""
    def __init__(self, *args):
        """
        Error class for when the FPS for a function is less than or equal to 0.

        :param args: The messsage to be shown when error is raised.
        """
        super().__init__(*args)
