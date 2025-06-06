import math

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

    def normalized(self):
        """
        Returns a new vec2D instance representing the normalized (unit) vector.
        The original vector remains unchanged.
        Returns:
            vec2D: A new vector with the same direction but magnitude 1.
                   Returns vec2D(0, 0) if the original vector has zero magnitude.
        """
        magnitude = abs(self)  # Uses the __abs__ method to get magnitude
        if magnitude == 0:
            return vec2D(0, 0)  # Handle zero vector to avoid division by zero
        return vec2D(self.x / magnitude, self.y / magnitude)

    def __hash__(self):
        """
        Returns a hash value for the vec2D object.
        It's crucial that if v1 == v2, then hash(v1) == hash(v2).
        A common way for simple objects is to hash a tuple of their immutable attributes.
        """
        return hash((self.x, self.y))  # Hash a tuple of the coordinates

    @staticmethod
    def dot(v1, v2):
        """
        Computes the dot product of two vec2D vectors.
        Args:
            v1 (vec2D): The first vector.
            v2 (vec2D): The second vector.
        Returns:
            float: The dot product.
        Raises:
            TypeError: If inputs are not vec2D instances.
        """
        if not isinstance(v1, vec2D) or not isinstance(v2, vec2D):
            raise TypeError("dot_product requires two vec2D instances.")
        return v1.x * v2.x + v1.y * v2.y

    @staticmethod
    def distance(v1, v2):
        """
        Computes the Euclidean distance between two vec2D points.
        Args:
            v1 (vec2D): The first point.
            v2 (vec2D): The second point.
        Returns:
            float: The Euclidean distance.
        Raises:
            TypeError: If inputs are not vec2D instances.
        """
        if not isinstance(v1, vec2D) or not isinstance(v2, vec2D):
            raise TypeError("distance requires two vec2D instances.")
        return math.sqrt((v2.x - v1.x) ** 2 + (v2.y - v1.y) ** 2)