class ScreenError(Exception):
    pass

class MouseError(ScreenError):
    pass

class InitError(ScreenError):
    pass

class ThicknessError(ScreenError):
    pass

class EllipseThicknessError(ThicknessError):
    pass

class PolygonThicknessError(ThicknessError):
    pass

class CircleThicknessError(EllipseThicknessError):
    pass

class QuadrilateralThicknessError(PolygonThicknessError):
    pass

class RectangleThicknessError(QuadrilateralThicknessError):
    pass

class SquareThicknessError(RectangleThicknessError):
    pass

class ShapeError(ScreenError):
    pass

class EllipseError(ShapeError):
    pass

class PolygonError(ShapeError):
    pass

class CircleError(EllipseError):
    pass

class QuadrilateralError(PolygonError):
    pass

class RectangleError(QuadrilateralError):
    pass

class SquareError(RectangleError):
    pass

class TrapezoidError(RectangleError):
    pass