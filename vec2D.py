
# vec2D.py
class vec2D:

    '''
    A simple 2D vector class that supports basic arithmetic operations and comparisons.
    '''
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"vec2D({self.x}, {self.y})"

    def __repr__(self):
        return f"vec2D({self.x}, {self.y})"

    # Operator Overloading Methods:

    # Addition: obj1 + obj2
    def __add__(self, other):
        if isinstance(other, vec2D):
            return vec2D(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Unsupported operand type for +: 'vec2D' and '{}'".format(type(other).__name__))

    # Subtraction: obj1 - obj2
    def __sub__(self, other):
        if isinstance(other, vec2D):
            return vec2D(self.x - other.x, self.y - other.y)
        else:
            raise TypeError("Unsupported operand type for -: 'vec2D' and '{}'".format(type(other).__name__))

    # Multiplication (scalar multiplication, assuming you want to multiply a vec2D by a number)
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return vec2D(self.x * scalar, self.y * scalar)
        else:
            raise TypeError("Unsupported operand type for *: 'vec2D' and '{}'".format(type(scalar).__name__))

    # Reverse Multiplication (for when scalar * vec2D)
    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    # Division (scalar division)
    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            if scalar == 0:
                raise ValueError("Cannot divide by zero.")
            return vec2D(self.x / scalar, self.y / scalar)
        else:
            raise TypeError("Unsupported operand type for /: 'vec2D' and '{}'".format(type(scalar).__name__))

    # Equality: obj1 == obj2
    def __eq__(self, other):
        if isinstance(other, vec2D):
            return self.x == other.x and self.y == other.y
        return NotImplemented # Indicate that equality with other types is not supported

    # Inequality: obj1 != obj2 (often implicitly handled if __eq__ is defined)
    def __ne__(self, other):
        return not self.__eq__(other)

    # Greater than: obj1 > obj2 (example for magnitude comparison)
    def __gt__(self, other):
        if isinstance(other, vec2D):
            return (self.x**2 + self.y**2) > (other.x**2 + other.y**2)
        return NotImplemented

    # Less than: obj1 < obj2
    def __lt__(self, other):
        if isinstance(other, vec2D):
            return (self.x**2 + self.y**2) < (other.x**2 + other.y**2)
        return NotImplemented

    # Greater than or equal to: obj1 >= obj2
    def __ge__(self, other):
        if isinstance(other, vec2D):
            return (self.x**2 + self.y**2) >= (other.x**2 + other.y**2)
        return NotImplemented

    # Less than or equal to: obj1 <= obj2
    def __le__(self, other):
        if isinstance(other, vec2D):
            return (self.x**2 + self.y**2) <= (other.x**2 + other.y**2)
        return NotImplemented

    # Unary negation: -obj
    def __neg__(self):
        return vec2D(-self.x, -self.y)

    # Absolute value/magnitude: abs(obj)
    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5

    def __hash__(self):
        """
        Returns a hash value for the vec2D object.
        It's crucial that if v1 == v2, then hash(v1) == hash(v2).
        A common way for simple objects is to hash a tuple of their immutable attributes.
        """
        return hash((self.x, self.y))  # Hash a tuple of the coordinates