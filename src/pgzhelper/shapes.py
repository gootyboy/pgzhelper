from __future__ import annotations
from .utilities import *
from .utilities import Rect, pygame, rect_collides_with_circle, circle_collides_with_circle, Enum, overload, math, Union, Optional

TRIANGLE_CENTER = ("center")
"""Used to indicate the triangle center when pivoting"""

TOP = "top"
"""top direction for EquilateralTriangle"""

DOWN = "down"
"""down direction for EquilateralTriangle"""

class Shape:
    """Base class for all shapes"""

class Polygon(Shape):
    """Base Polygon class."""
    @overload
    def __init__(self, *points: tuple[int, int]) -> None: ...
    @overload
    def __init__(self, points: list[tuple[int, int]]) -> None: ...

    def __init__(self, *args):
        """
        Creates a new Polygon.

        :param points: The points of the polygon. Order matters.
        """
        if isinstance(args[0], list):
            self.points = args[0]
            """The points of the polygon."""
        else:
            self.points = list(args[0])
            """The points of the polygon."""

class Ellipse(Shape):
    """Ellipse class"""
    def __init__(self, rect: Rect) -> None:
        """
        Creates a new Ellipse.
        
        :param rect: The rect within the Ellipse.
        """
        self.rect = rect
        """The rect within the Ellipse. The Ellipse is drawn touching the corners of the Rect."""

class Quadrilateral(Polygon):
    """Quadrilateral Class. Is a Polygon."""
    def __init__(self, point1: tuple[int, int], point2: tuple[int, int], point3: tuple[int, int], point4: tuple[int, int]) -> None:
        """
        Creates a new Quadrilateral.

        :param point1: The first point in the Quadrilateral.
        :param point2: The second point in the Quadrilateral.
        :param point3: The third point in the Quadrilateral.
        :param point4: The fourth/last point in the Quadrilateral.
        """
        self.point1 = point1
        """The first point in the Quadrilateral"""

        self.point2 = point2
        """The second point in the Quadrilateral"""

        self.point3 = point3
        """The third point in the Quadrilateral"""

        self.point4 = point4
        """The fourth/last point in the Quadrilateral"""

        super().__init__([point1, point2, point3, point4])

class Triangle(Polygon):
    """Triangle Class. Is a Polygon"""
    def __init__(self, point1: tuple[int, int], point2: tuple[int, int], point3: tuple[int, int]) -> None:
        """
        Creates a new Triangle.

        :param point1: The first point in the Triangle.
        :param point2: The second point in the Triangle.
        :param point3: The third point in the Triangle.
        """
        self.point1 = point1
        """The first point in the Triangle"""

        self.point2 = point2
        """The second point in the Triangle"""

        self.point3 = point3
        """The third/last point in the Triangle"""

        self.centerx = (self.points[0][0] + self.points[1][0] + self.points[2][0]) / 3
        """The x position of the center of the Triangle."""

        self.centery = (self.points[0][1] + self.points[1][1] + self.points[2][1]) / 3
        """The y position of the center of the Triangle."""

        self.center = (self.centerx, self.centery)
        """The center position of the Triangle."""

        super().__init__(self.point1, self.point2, self.point3)

    def rotate(self, angle: int, pivot: Union[tuple[int, int], str] = TRIANGLE_CENTER) -> Triangle:
        """
        Rotates the Triangle around pivot. Returns a copy.

        :param angle: The angle to rotate.
        :param pivot: The pivot. Defaults to the triangle's center.

        :return Triangle: Copy of the Triangle with the rotation.
        """
        if pivot == TRIANGLE_CENTER:
            pivot = self.center

        pp = pygame.math.Vector2(pivot)
        rotated_points = []
        for x, y in self.points:
            rotated_point = (pygame.math.Vector2(x, y) - pp).rotate(angle) + pp
            rotated_points.append((int(rotated_point.x), int(rotated_point.y)))

        return Triangle(*rotated_points)

    def move_down(self, amount: int) -> Triangle:
        """
        Moves the Triangle down the amount. Returns a copy.

        :param amount: The amount to move down.
        
        :return Triangle: Copy of the Triangle with the moving down.
        """
        new_points = []
        for point in self.points:
            new_points.append((point[0], point[1] + amount))
        return Triangle(*new_points)

    def move_up(self, amount: int) -> Triangle:
        """
        Moves the Triangle up the amount. Returns a copy.

        :param amount: The amount to move up.
        
        :return Triangle: Copy of the Triangle with the moving up.
        """
        return self.move_down(-amount)
    
    def move_right(self, amount: int) -> Triangle:
        """
        Moves the Triangle right the amount. Returns a copy.

        :param amount: The amount to move right.
        
        :return Triangle: Copy of the Triangle with the moving right.
        """
        new_points = []
        for point in self.points:
            new_points.append((point[0] + amount, point[1]))
        return Triangle(*new_points)

    def move_left(self, amount: int) -> Triangle:
        """
        Moves the Triangle left the amount. Returns a copy.

        :param amount: The amount to move left.
        
        :return Triangle: Copy of the Triangle with the moving left.
        """
        return self.move_right(-amount)

class EquilateralTriangle(Triangle):
    def __init__(self, bottomleft_topleft, length, direction = TOP):
        x, y = bottomleft_topleft
        pos1 = (x, y)
        pos2 = (x + length, y)
        h = (math.sqrt(3) / 2) * length
        if direction == DOWN:
            pos3 = (x + length / 2, y + h)
        else:
            pos3 = (x + length / 2, y - h)
        super().__init__(pos1, pos2, pos3)
        self.length = length
        self.bottomleft_topleft = bottomleft_topleft
        self.direction = direction
        self.is_down = (self.direction == DOWN)

    def rotate(self, angle, pivot: tuple = TRIANGLE_CENTER):
        rotated = super().rotate(angle, pivot)
        return rotated
    
    def change_dir(self):
        if self.is_down:
            return EquilateralTriangle(self.bottomleft_topleft, self.length)
        else:
            return EquilateralTriangle(self.bottomleft_topleft, self.length, DOWN) 

    def move_down(self, amount):
        return super().move_down(amount)

    def move_left(self, amount):
        return super().move_left(amount)
    
    def move_right(self, amount):
        return super().move_right(amount)
    
    def move_up(self, amount):
        return super().move_up(amount)

class Circle(Ellipse):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    @property
    def diameter(self):
        return self.radius * 2

    @overload
    def collidepoint(self, x, y):
        ...

    @overload
    def collidepoint(self, pos):
        ...

    def collidepoint(self, *args):
        if len(args) == 1:
            x = args[0][0]
            y = args[0][1]
        elif len(args) == 2:
            x = args[0]
            y = args[1]
        return (x - self.center[0])**2 + (y - self.center[1])**2 <= self.radius**2

    def colliderect(self, rect: Rect):
        return rect_collides_with_circle(rect, self.center, self.radius)

    def collidecircle(self, circle: Circle):
        return circle_collides_with_circle(*self.center, r1=self.radius, *circle.center, r2=circle.radius)

class HRect(Rect, Quadrilateral):
    def collidecircle(self, circle: Circle):
        return circle.colliderect(self)

class Square(HRect):
    def __init__(self, topleft, length):
        super().__init__(topleft, (length, length))
        self.length = length
        self.points = [self.bottomleft, self.bottomright, self.topright, self.topleft]
        self.corners = self.points

    def get_integer_points_list(self):
        points = [
            (self.left + x, self.top + y)
            for x in range(self.length + 1)
            for y in range(self.length + 1)
        ]
        return sorted(points)

    def get_integer_points_2d_list(self):
        points = self.get_integer_points_list()
        return [
            points[i:i + self.length + 1]
            for i in range(0, len(points), self.length + 1)
        ]

class shapes(Enum):
    polygon = Polygon
    ellipse = Ellipse
    triangle = Triangle
    equilateral_triangle = EquilateralTriangle
    circle = Circle
    rectangle = HRect
    square = Square
    shape = Shape
