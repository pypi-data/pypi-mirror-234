from __future__ import annotations
from typing import Optional, Sequence, Union

import numpy as np

from m3d.common import NumberType, float_eps, number_types


class Vector:
    """
    Represent a vector.
    Takes either x, y, z as argument or a list/array
    """
    def __init__(self, x=0.0, y=0.0, z=0.0, dtype=np.float32, frozen: bool = False):
        self._data: np.ndarray
        if isinstance(x, (list, tuple)):
            if len(x) == 3:
                self._data = np.array(x, dtype=dtype)
            else:
                raise ValueError(f"A list of length 3 is expected, got {x}")
        elif isinstance(x, np.ndarray):
            if x.shape == (3, ):
                self._data = x
            else:
                raise ValueError(f"A array of shape (3,) is expected got {x}")
        else:
            self._data = np.array([float(x), float(y), float(z)], dtype=dtype)
        self._frozen = frozen
        self._data.flags.writeable = not frozen

    def __getitem__(self, idx: int) -> float:
        return self._data[idx]

    def __setitem__(self, idx: int, val: float) -> None:
        self._data[idx] = val

    @property
    def frozen(self) -> bool:
        return self._frozen

    @frozen.setter
    def frozen(self, val: bool) -> None:
        self._frozen = val
        self._data.flags.writeable = not val

    def copy(self) -> Vector:
        return Vector(self._data.copy())

    @property
    def x(self) -> float:
        return float(self._data[0])

    @x.setter
    def x(self, val: float) -> None:
        self._data[0] = val

    @property
    def y(self) -> float:
        return float(self._data[1])

    @y.setter
    def y(self, val: float) -> None:
        self._data[1] = val

    @property
    def z(self) -> float:
        return float(self._data[2])

    @z.setter
    def z(self, val: float) -> None:
        self._data[2] = val

    def __str__(self) -> str:
        return "Vector({}, {}, {})".format(self.x, self.y, self.z)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.data - other.data)

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.data + other.data)

    def __neg__(self) -> Vector:
        return Vector(-self._data)

    __repr__ = __str__

    @property
    def data(self) -> np.ndarray:
        return self._data

    array = data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.similar(other)

    def __mul__(self, other: NumberType) -> Vector:
        if not isinstance(other, number_types):
            raise ValueError()
        return Vector(self._data * other)

    __rmul__ = __mul__

    def __truediv__(self, other: NumberType) -> Vector:
        if not isinstance(other, number_types):
            raise ValueError()
        return Vector(self._data / other)

    def __itruediv__(self, other: NumberType) -> Vector:
        if not isinstance(other, number_types):
            raise ValueError()
        self._data /= other
        return self

    def __imul__(self, other: NumberType) -> Vector:
        if not isinstance(other, number_types):
            raise ValueError()
        self._data *= other
        return self

    @property
    def length(self) -> float:
        return float(np.linalg.norm(self.data))

    def dist(self, other: Vector) -> float:
        """
        return abolute distance to another vector
        """
        v = Vector(other.data - self.data)
        return v.length

    def similar(self, other: Vector, tol: NumberType = float_eps) -> bool:
        """
        Return True if distance to other Vector is less than tol
        return False otherwise
        """
        if not isinstance(other, Vector):
            raise ValueError("Expecting a Vector object, received {} of type {}".format(other, type(other)))
        return bool(self.dist(other) <= tol)

    def normalize(self) -> None:
        """
        Normalize in place vector
        """
        if self.length == 0:
            return
        self._data /= self.length

    def normalized(self) -> Vector:
        """
        Return a normalized copy of vector
        """
        if self.length == 0:
            return Vector(self.data)
        return Vector(self._data / self.length)

    def cross(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            other = Vector(other)
        return Vector(np.cross(self.data, other.data))

    def dot(self, other: Vector) -> float:
        if not isinstance(other, Vector):
            other = Vector(other)
        return np.dot(self.data, other.data)

    __matmul__ = dot

    def project(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            other = Vector(other)
        other = other.normalized()
        return self.dot(other) * other

    def angle(self, other: Vector, normal_vector: Optional[Vector] = None) -> float:
        """
        If provided, normal_vector is a vector defining the reference plane to be used to compute sign of angle.
        Otherwise, returned angle is between 0 and pi.
        """
        cos = self.dot(other) / (self.length * other.length)
        angle = np.arccos(np.clip(cos, -1, 1))
        if normal_vector is not None:
            angle = angle * np.sign(normal_vector.dot(self.cross(other)))
        return angle

    def as_so3(self) -> np.ndarray:
        """
        Returns the skew symetric (so3) representation of the vector
        https://en.wikipedia.org/wiki/Skew-symmetric_matrix
        """
        return np.array([
            [0, -self.z, self.y],
            [self.z, 0, -self.x],
            [-self.y, self.x, 0],
        ])

    @staticmethod
    def mean(*vectors: 'Vector', weights: Optional[Union[Sequence[float], np.ndarray]] = None) -> 'Vector':
        if weights is None:
            weights = np.ones(len(vectors))

        if len(vectors) != len(weights):
            raise ValueError("The number of weights needs to correspond to the number of vectors to average")
        if abs(sum(weights)) < float_eps:
            raise ValueError("Can not have all weights 0 or close to 0")

        return Vector(*np.average([vec.data for vec in vectors], axis=0, weights=weights))


# some units vectors
e0 = ex = Vector(1, 0, 0)
e1 = ey = Vector(0, 1, 0)
e2 = ez = Vector(0, 0, 1)
