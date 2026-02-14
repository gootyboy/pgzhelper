"""All of pgzhelper's shapes are found here."""

from .utilities import *

TRIANGLE_CENTER = ("center")
TOP = "top"
DOWN = "down"

class Shape:
    pass

class Polygon(Shape):
    def __init__(self, *points):
        self.points = points

class Ellipse(Shape):
    def __init__(self, rect: Rect):
        self.rect = rect

class Quadrilateral(Polygon):
    def __init__(self, point1, point2, point3, point4):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.point4 = point4
        super().__init__([point1, point2, point3, point4])

class Triangle(Polygon):
    def __init__(self, pos1: tuple, pos2: tuple, pos3: tuple):
        self.pos1 = pos1
        self.pos2 = pos2
        self.pos3 = pos3
        self.points = [self.pos1, self.pos2, self.pos3]
        self.centerx = (self.points[0][0] + self.points[1][0] + self.points[2][0]) / 3
        self.centery = (self.points[0][1] + self.points[1][1] + self.points[2][1]) / 3
        self.center = (self.centerx, self.centery)

    def rotate(self, angle, pivot: tuple = TRIANGLE_CENTER) -> Triangle:
        if pivot == TRIANGLE_CENTER:
            pivot = self.center
        pp = pygame.math.Vector2(pivot)
        rotated_points = []
        for x, y in self.points:
            rotated_point = (pygame.math.Vector2(x, y) - pp).rotate(angle) + pp
            rotated_points.append((int(rotated_point.x), int(rotated_point.y)))
        return Triangle(*rotated_points)

    def move_down(self, amount):
        new_points = []
        for point in self.points:
            new_points.append((point[0], point[1] - amount))
        return Triangle(*new_points)

    def move_up(self, amount):
        return self.move_down(-amount)
    
    def move_right(self, amount):
        new_points = []
        for point in self.points:
            new_points.append((point[0] + amount, point[1]))
        return Triangle(*new_points)

    def move_left(self, amount):
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

    def colliderect(self, rect: Rect | pygame.rect.Rect | ZRect | HRect):
        return rect_collides_with_circle(rect, self.center, self.radius)

    def collidecircle(self, circle: Circle):
        return circle_collides_with_circle(*self.center, r1=self.radius, *circle.center, r2=circle.radius)

    def colliderects(self, rects: list[Rect | ZRect | pygame.rect.Rect | HRect]):
        return any([self.colliderect(rect) for rect in rects])
    
    def colliderectsall(self, rects: list[Rect | ZRect | pygame.rect.Rect | HRect]):
        return all([self.colliderect(rect) for rect in rects])
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