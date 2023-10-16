from __future__ import annotations
from typing import TypeVar
import numpy as np

from m3d.vector import Vector
from m3d.orientation import Orientation
from m3d.common import NumberType, float_eps


T = TypeVar('T')


class Transform:
    """
    Create a new Transform object
    Accepts an orientation and a vector or a matrix 4*4 as argument
    Rmq:
    When creating a transform from a 4*4 Matrix, the matrix is directly used
    as the Transform data
    When accessing/modifying the Orientation or Vector object you are
    modifying a vew of the matrix data
    When creating a new Transform object from an Orientation and
    Vector or 2 numpy arrays, you are copying them
    """
    def __init__(self, orientation=None, vector=None, matrix=None, dtype=np.float32, frozen=False) -> None:
        if matrix is not None:
            self._data = matrix
        else:
            self._data = np.identity(4, dtype=dtype)
        if orientation is None:
            pass
        elif isinstance(orientation, np.ndarray):
            if orientation.shape == (3, 3):
                self._data[:3, :3] = orientation
            else:
                raise ValueError()
        elif isinstance(orientation, Orientation):
            self._data[:3, :3] = orientation.data
        else:
            raise ValueError("orientation argument should be a numpy array, Orientation or None")
        self._orient = Orientation(self._data[:3, :3], dtype=dtype, frozen=frozen)

        if vector is None:
            pass
        elif isinstance(vector, np.ndarray):
            self._data[:3, 3] = vector
        elif isinstance(vector, Vector):
            self._data[:3, 3] = vector.data
        elif isinstance(vector, (list, tuple)):
            self._data[:3, 3] = vector
        else:
            raise ValueError("orientation argument should be a numpy array, Orientation or None")
        self._pos = Vector(self._data[:3, 3], dtype=dtype, frozen=frozen)
        self._frozen = frozen
        self._data.flags.writeable = not frozen

    def is_valid(self) -> bool:
        """
        Check if a transform is valid
        """
        if abs(self._data[3, 3] - 1) > float_eps:
            return False
        if not (abs(self._data[3, 0:3]) < float_eps).all():
            return False
        if np.isnan(self._data.sum()):
            return False
        return self.orient.is_valid()

    def _validate(self) -> Transform:
        if not self.is_valid():
            raise ValueError("Given args gives an invalid Transform")
        return self

    @property
    def frozen(self) -> bool:
        return self._frozen

    @frozen.setter
    def frozen(self, val: bool) -> None:
        self._frozen = val
        self._data.flags.writeable = not val
        self._pos._data.flags.writeable = not val
        self._orient._data.flags.writeable = not val

    def __str__(self) -> str:
        return "Transform(\n{},\n{}\n)".format(self.orient, self.pos)

    __repr__ = __str__

    @property
    def pos(self) -> Vector:
        """
        Access the position part of the matrix through a Vector object
        """
        return self._pos

    @pos.setter
    def pos(self, vector: Vector) -> None:
        if not isinstance(vector, Vector):
            raise ValueError()
        self._data[:3, 3] = vector.data
        self._pos = Vector(self._data[:3, 3])  # make sure vector data is a view on our data

    @property
    def orient(self) -> Orientation:
        """
        Access the orientation part of the matrix through an Orientation object
        """
        return self._orient

    @orient.setter
    def orient(self, orient: Orientation) -> None:
        if not isinstance(orient, Orientation):
            raise ValueError()
        self._data[:3, :3] = orient.data
        self._orient = Orientation(self._data[:3, :3])  # make sure orientation data is view on our data

    @property
    def data(self) -> np.ndarray:
        """
        Access the numpy array used by Transform
        """
        return self._data

    array = data
    matrix = data

    def inverse(self) -> Transform:
        """
        Return inverse of Transform
        """
        return Transform(matrix=np.linalg.inv(self._data))

    def invert(self) -> None:
        """
        In-place inverse the matrix
        """
        if self.frozen:
            raise ValueError("This Transform is frozen")
        self._data[:, :] = np.linalg.inv(self._data)

    def __eq__(self, other: object) -> bool:
        return self.similar(other)

    def __mul__(self, other: T) -> T:
        if isinstance(other, Vector):
            data = self.orient.data @ other.data + self.pos.data
            return Vector(data)  # type: ignore
        if isinstance(other, Transform):
            return Transform(matrix=self._data @ other.data)  # type: ignore
        if isinstance(other, np.ndarray):
            # This make it easy to support several format of point clouds but might be mathematically wrong
            if other.shape[0] == 3:
                return (self.orient.data @ other) + self.pos.data.reshape(3, 1)
            if other.shape[1] == 3:
                return (self.orient.data @ other.T).T + self.pos.data
            raise ValueError("Array shape must be 3, x or x, 3")
        return NotImplemented

    __matmul__ = __mul__

    @property
    def pose_vector(self) -> np.ndarray:
        return self.to_pose_vector()

    def to_pose_vector(self) -> np.ndarray:
        """
        Return a representation of transformation as 6 numbers array
        3 for position, and 3 for rotation vector
        """
        v = self.orient.to_rotation_vector()
        return np.array([self.pos.x, self.pos.y, self.pos.z, v.x, v.y, v.z])

    @classmethod
    def from_pose_vector(cls, x: NumberType, y: NumberType, z: NumberType, r1: NumberType, r2: NumberType, r3: NumberType) -> Transform:
        o = Orientation.from_rotation_vector(Vector(r1, r2, r3))
        return cls(o, [x, y, z])._validate()

    def to_ros(self):
        return self.orient.to_quaternion(), self.pos.data

    @classmethod
    def from_ros(cls, q, v):
        orient = Orientation.from_quaternion(*q)
        return cls(orient, Vector(v))._validate()

    def as_adjoint(self) -> np.ndarray:
        """
        Returns the 6x6 adjoint representation of the transform,
        that can be used to transform any 6-vector twist
        https://en.wikipedia.org/wiki/Adjoint_representation
        """
        return np.vstack([
            np.hstack([self.orient.data, np.zeros((3, 3))]),
            np.hstack([np.dot(self.pos.as_so3(), self.orient.data), self.orient.data]),
        ])

    @classmethod
    def from_corresponding_points(cls, fixed: np.ndarray, moving: np.ndarray) -> Transform:
        """
        Given a set of points and another set of points
        representing matching points of those in another coordinate
        system, compute a least squares transform between them using
        SVD

        """
        if fixed.shape != moving.shape:
            raise ValueError("input point clouds must be same length")

        if np.allclose(fixed, moving):
            return cls()

        centroid_f = np.mean(fixed, axis=0)
        centroid_m = np.mean(moving, axis=0)

        f_centered = fixed - centroid_f
        m_centered = moving - centroid_m

        B = f_centered.T @ m_centered

        # find rotation
        U, D, V = np.linalg.svd(B)
        R = V.T @ U.T

        # special reflection case
        if np.linalg.det(R) < 0:
            V[2, :] *= -1
            R = V.T @ U.T

        t = -R @ centroid_f + centroid_m

        return cls(Orientation(R), Vector(t))._validate()

    def copy(self) -> Transform:
        return Transform(matrix=self._data.copy())

    def dist(self, other: Transform) -> float:
        """
        Return distance equivalent between this matrix and a second one
        """
        return self.pos.dist(other.pos) + self.orient.ang_dist(other.orient)

    def similar(self, other: object, tol: NumberType = float_eps) -> bool:
        """
        Return True if distance to other transform is less than tol
        return False otherwise
        """
        if not isinstance(other, Transform):
            raise ValueError("Expecting a Transform object, received {} of type {}".format(other, type(other)))
        return bool(self.dist(other) <= tol)

    @staticmethod
    def mean(*transforms: Transform) -> Transform:
        return Transform(
            Orientation.mean(*(trf.orient for trf in transforms)),
            Vector.mean(*(trf.pos for trf in transforms))
        )
