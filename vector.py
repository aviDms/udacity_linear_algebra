from math import sqrt, acos, degrees, pi
from decimal import Decimal
from numbers import Number
from typing import List, Any

DEFAULT_TOLERANCE = 1e-10


'''
ISSUES
* assumes all vectors start from origin 0
'''


class CannotNormalizeZeroVectorError(Exception):
    pass


class NoUniqueParallelComponentError(Exception):
    pass


class NoUniqueOrthogonalComponentError(Exception):
    pass


class Vector(object):

    def __init__(self, coordinates: List) -> None:
        """
        Vector object has a set of coordinates and a length.

        The items of the coordinates list provided by the user
        are transformed to Decimal for consistency and stored in
        a tuple object.

        The length of the vector denotes the number of dimensions.

        :param coordinates: list of real numbers defining
        the vector coordinates
        """
        self.coordinates = tuple(map(Decimal, coordinates))
        self.length = len(coordinates)

    def scale(self, scalar: Number) -> 'Vector':
        """
        Scale itself by a number.

        Scale operation multiplies each coordinate of itself
        by a value belonging to the real numbers.

        :param scalar: real number to scale the vector with
        :return: scaled vector
        """
        try:
            scalar = Decimal(scalar)
        except Exception as err:
            raise err

        return Vector([c * scalar for c in self.coordinates])

    def dot(self, vector: 'Vector') -> Decimal:
        """
        Calculate the dot product of itself with provided vector.

        Multiply each coordinate of itself with the corresponding
        coordinate of the provided vector and sums up the products.

        :param vector: vector to be dotted with
        :return: the magnitude of the projection of one vector onto
        the other
        """
        if not isinstance(vector, Vector):
            raise TypeError('Items must be of type Vector.')

        if self.length != vector.length:
            raise TypeError('Vectors must have equal size.')

        return sum([a * b for a, b in zip(self.coordinates, vector.coordinates)])

    def component_orthogonal_to(self, vector: 'Vector') -> 'Vector':
        """

        :param vector: vector to be projected onto
        :return: projection's orthogonal component
        """
        try:
            projection = self.component_parallel_to(vector)
        except NoUniqueParallelComponentError:
            raise NoUniqueOrthogonalComponentError

        return self - projection

    def component_parallel_to(self, vector: 'Vector') -> 'Vector':
        """

        :param vector:
        :return:
        """
        try:
            basis = vector.normalized
        except CannotNormalizeZeroVectorError:
            raise NoUniqueParallelComponentError

        weight = self.dot(basis)
        return basis.scale(weight)

    @property
    def magnitude(self) -> Decimal:
        """
        Magnitude of itself.

        Calculate the magnitude by taking the square root of the
        sum of its squared coordinates.

        :return: euclidean distance from its origin to its tip
        """
        return Decimal(sqrt(sum([e ** 2 for e in self.coordinates])))

    @property
    def normalized(self) -> 'Vector':
        """
        Normalization is the process of finding the unit vector
        on the same direction as itself.

        Calculate the normalized vector by scaling itself by a
        value equal to 1 divided by its magnitude.

        :return: normalized vector
        """
        try:
            return self.scale(Decimal(1) / self.magnitude)
        except ZeroDivisionError:
            raise CannotNormalizeZeroVectorError

    def is_zero(self, tolerance: Number = DEFAULT_TOLERANCE) -> bool:
        """
        A zero vector is consider to be a vector with a magnitude
        equal to zero (the euclidean distance between its origin
        and its tip is zero).

        :param tolerance: error margin for decimal operations
        :return: True if its magnitude is zero, False otherwise
        """
        return self.magnitude < tolerance

    def is_parallel_with(self, vector: 'Vector') -> bool:
        """
        Two vectors are parallel when they have the same direction
        (the angle between them is 0 or 180 degrees) or at least one
        of them is the zero vector.

        :param vector: vector to be compared with
        :return: True if vectors are parallel, False otherwise
        """
        if not isinstance(vector, Vector):
            raise TypeError('Items must be of type Vector.')

        if self.length != vector.length:
            raise TypeError('Vectors must have equal size.')

        return (
            self.is_zero() or
            vector.is_zero() or
            self.angle_with(vector) == 0 or
            self.angle_with(vector) == pi
        )

    def is_orthogonal_with(self,
                           vector: 'Vector',
                           tolerance: Number = DEFAULT_TOLERANCE) -> bool:
        """
        Two vectors are orthogonal to each other when the projection
        of one onto the other has a magnitude equal to zero (the angle
        between them is 90 degrees).

        :param vector:
        :param tolerance:
        :return:
        """
        if not isinstance(vector, Vector):
            raise TypeError('Items must be of type Vector.')

        if self.length != vector.length:
            raise TypeError('Vectors must have equal size.')

        return abs(self.dot(vector)) < tolerance

    def angle_with(self, vector: 'Vector', radians: bool = True) -> Decimal:
        """
        Angle between two vectors is the result of the dot product between
        their normalized vectors.

        :param vector: vector to be compared with
        :param radians: True will return the the angle value in radians,
        False will return angle value in degrees
        :return: angle between the two vectors in radians (default) or
        degrees
        """
        if not isinstance(vector, Vector):
            raise TypeError('Items must be of type Vector.')

        if self.length != vector.length:
            raise TypeError('Vectors must have equal size.')

        u1 = self.normalized
        u2 = vector.normalized
        p = u1.dot(u2)

        teta = acos(round(p, 3))

        if radians:
            return Decimal(teta)
        else:
            return Decimal(degrees(teta))

    def __add__(self, other: Any) -> 'Vector':
        """
        Addition operator, supports the sum between self and another
        vector or scalar.

        :param other: can be another vector or a scalar
        :return: resulted vector
        """
        if isinstance(other, Vector):
            return Vector([a + b for a, b in zip(self.coordinates, other.coordinates)])
        elif isinstance(other, Number):
            return Vector([e + Decimal(other) for e in self.coordinates])
        else:
            raise TypeError('Addition argument must be a vector or a scalar.')

    def __sub__(self, other: Any) -> 'Vector':
        """
        Subtraction operator, supports the subtraction between self and another
        vector or scalar.

        :param other: can be another vector or a scalar
        :return: resulted vector
        """
        if isinstance(other, Vector):
            return Vector([a - b for a, b in zip(self.coordinates, other.coordinates)])
        elif isinstance(other, Number):
            return Vector([e - Decimal(other) for e in self.coordinates])
        else:
            raise TypeError('Subtraction argument must be a vector or a scalar.')

    def __mul__(self, other: Any) -> Any:
        """
        Multiplication operator, supports dot product with another vector
        or scaling it by a real number.

        :param other: vector or scalar
        :return: return dot product or scaled vector
        """
        if isinstance(other, Number):
            return self.scale(other)
        elif isinstance(other, Vector):
            return self.dot(other)
        else:
            raise TypeError('Operation not supported.')

    def __eq__(self, vector: 'Vector') -> bool:
        """
        Equality operator, checks if the all coordinates of two vectors are
        the same.

        :param vector: vector to compare with
        :return: True if their coordinates are equal, False otherwise
        """
        if not isinstance(vector, Vector) or self.length != vector.length:
            return False

        is_equal = True
        for i in range(self.length):
            if self.coordinates[i] != vector.coordinates[i]:
                is_equal = False
                break

        return is_equal

    def __repr__(self) -> str:
        """
        String representation of the object.

        :return: all coordinates of the vector, comma separated, as string
        """
        return '[{0}]'.format(', '.join(map(str, self.coordinates)))


def cross_product(v1: Vector, v2: Vector) -> Vector:
    """
    Calculate the cross product of 2 3D vectors.

    ! only supports 3D vectors.

    :param v1: first vector
    :param v2: second vector
    :return: resulting vector
    """
    v = v1.coordinates
    w = v2.coordinates

    x = v[1] * w[2] - w[1] * v[2]
    y = -(v[0] * w[2] - w[0] * v[2])
    z = v[0] * w[1] - w[0] * v[1]

    return Vector([x, y, z])
