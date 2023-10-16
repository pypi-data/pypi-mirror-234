from __future__ import annotations
import math
from typing import List, Optional, Tuple, TypeVar

import numpy as np

from m3d.vector import Vector
from m3d.common import NumberType, float_eps


T = TypeVar('T')


class Orientation:
    def __init__(self, data: Optional[np.ndarray] = None, dtype=np.float32, frozen: bool = False) -> None:
        if isinstance(data, np.ndarray):
            if data.shape == (3, 3):
                self._data = data
            else:
                raise ValueError(f"A numpy array of size (3, 3) is expected not {data.shape}")
        elif isinstance(data, list):
            self._data = np.array(data)
            if self._data.shape != (3, 3):
                raise ValueError(f"Creating an array from argument {data} did not lead to an array of shape (3, 3)")
        elif data is None:
            self._data = np.identity(3, dtype=dtype)
        else:
            raise ValueError(f"A numpy array of size (3, 3) is expected not {data}")
        self._frozen = frozen
        self._data.flags.writeable = not frozen

    @property
    def frozen(self) -> bool:
        return self._frozen

    @frozen.setter
    def frozen(self, val: bool) -> None:
        self._frozen = val
        self._data.flags.writeable = not val

    def is_valid(self) -> bool:
        """
        A real orthogonal matrix with det(R) = 1 provides a matrix representation of a proper
        rotation. Furthermore, a real orthogonal matrix with det (R) = −1 provides a matrix
        representation of an improper rotation.
        """
        if not np.allclose(self._data.T @ self._data, np.eye(3), float_eps, float_eps):
            return False
        if not (1 - np.linalg.det(self._data)) < float_eps:
            return False
        return True

    def _validate(self) -> Orientation:
        if not self.is_valid():
            raise ValueError("Given args gives an invalid Orientation")
        return self

    def rotate_xb(self, val: float) -> None:
        t = np.array([
            [1, 0, 0],
            [0, np.cos(val), -np.sin(val)],
            [0, np.sin(val), np.cos(val)],
        ])
        self._data[:] = t @ self._data

    def rotate_yb(self, val: float) -> None:
        t = np.array([
            [np.cos(val), 0, np.sin(val)],
            [0, 1, 0],
            [-np.sin(val), 0, np.cos(val)],
        ])
        self._data[:] = t @ self._data

    def rotate_zb(self, val: float) -> None:
        t = np.array([
            [np.cos(val), -np.sin(val), 0],
            [np.sin(val), np.cos(val), 0],
            [0, 0, 1],
        ])
        self._data[:] = t @ self._data

    def rotate_xt(self, val: float) -> None:
        t = np.array([
            [1, 0, 0],
            [0, np.cos(val), -np.sin(val)],
            [0, np.sin(val), np.cos(val)],
        ])
        self._data[:] = self._data @ t

    def rotate_yt(self, val: float) -> None:
        t = np.array([
            [np.cos(val), 0, np.sin(val)],
            [0, 1, 0],
            [-np.sin(val), 0, np.cos(val)],
        ])
        self._data[:] = self._data @ t

    def rotate_zt(self, val: float) -> None:
        t = np.array([
            [np.cos(val), -np.sin(val), 0],
            [np.sin(val), np.cos(val), 0],
            [0, 0, 1],
        ])
        self._data[:] = self._data @ t

    def __str__(self) -> str:
        data = np.array2string(self.data, separator=', ')
        return "Orientation(\n{}\n)".format(data)

    __repr__ = __str__

    def inverse(self) -> Orientation:
        return Orientation(np.linalg.inv(self.data))

    def ang_dist(self, other: Orientation) -> float:
        r = self * other.inverse()
        trace_r = r.data[0, 0] + r.data[1, 1] + r.data[2, 2]
        if trace_r > 3:
            # might happen with approximations/rouding
            trace_r = 3
        return np.arccos((trace_r - 1) / 2)

    @property
    def data(self) -> np.ndarray:
        return self._data

    @property
    def array(self) -> np.ndarray:
        return self._data

    matrix = data

    def __mul__(self, other: T) -> T:
        if isinstance(other, Vector):
            return Vector(self._data @ other.data)  # type: ignore
        if isinstance(other, Orientation):
            return Orientation(self._data @ other.data)  # type: ignore
        if isinstance(other, np.ndarray):
            if other.shape[0] == 3:
                return self.data @ other  # type: ignore
            if other.shape[1] == 3:
                return (self.data @ other.T).T  # type: ignore
            raise ValueError("Array shape must be 3,x or x,3")
        return NotImplemented

    __matmul__ = __mul__

    def __eq__(self, other: object) -> bool:
        return self.similar(other)

    def to_quaternion(self) -> Tuple[float, float, float, float]:
        '''
        Returns w, x, y, z
        adapted from
        https://github.com/matthew-brett/transforms3d/blob/master/transforms3d/quaternions.py
        '''

        Qxx, Qyx, Qzx, Qxy, Qyy, Qzy, Qxz, Qyz, Qzz = self._data.flat
        # Fill only lower half of symmetric matrix
        K = np.array([
            [Qxx - Qyy - Qzz, 0, 0, 0],
            [Qyx + Qxy, Qyy - Qxx - Qzz, 0, 0],
            [Qzx + Qxz, Qzy + Qyz, Qzz - Qxx - Qyy, 0],
            [Qyz - Qzy, Qzx - Qxz, Qxy - Qyx, Qxx + Qyy + Qzz],
        ]) / 3.0
        # Use Hermitian eigenvectors, values for speed
        vals, vecs = np.linalg.eigh(K)
        # Select largest eigenvector, reorder to w,x,y,z quaternion
        q = vecs[[3, 0, 1, 2], np.argmax(vals)]
        # Prefer quaternion with positive w
        # (q * -1 corresponds to same rotation as q)
        if q[0] < 0:
            q *= -1
        return q[0], q[1], q[2], q[3]

    @classmethod
    def from_quaternion(cls, w: NumberType, x: NumberType, y: NumberType, z: NumberType) -> Orientation:
        # adapted from
        # https://github.com/matthew-brett/transforms3d/blob/master/transforms3d/quaternions.py
        Nq = w * w + x * x + y * y + z * z
        if Nq < float_eps:
            return Orientation()
        s = 2.0 / Nq
        X = x * s
        Y = y * s
        Z = z * s
        wX = w * X
        wY = w * Y
        wZ = w * Z
        xX = x * X
        xY = x * Y
        xZ = x * Z
        yY = y * Y
        yZ = y * Z
        zZ = z * Z
        return cls(np.array([
            [1.0 - (yY + zZ), xY - wZ, xZ + wY],
            [xY + wZ, 1.0 - (xX + zZ), yZ - wX],
            [xZ - wY, yZ + wX, 1.0 - (xX + yY)],
        ]))._validate()

    @classmethod
    def from_axis_angle(cls, axis: Vector, angle: float, is_normalized: bool = False) -> Orientation:
        # adapted from
        # https://github.com/matthew-brett/transforms3d/blob/master/transforms3d/quaternions.py

        axis = Vector(axis) if not isinstance(axis, Vector) else axis

        if not is_normalized:
            axis.normalize()
        x, y, z = axis.x, axis.y, axis.z
        c = math.cos(angle)
        s = math.sin(angle)
        C = 1 - c
        xs = x * s
        ys = y * s
        zs = z * s
        xC = x * C
        yC = y * C
        zC = z * C
        xyC = x * yC
        yzC = y * zC
        zxC = z * xC
        return cls(np.array([
            [x * xC + c, xyC - zs, zxC + ys],
            [xyC + zs, y * yC + c, yzC - xs],
            [zxC - ys, yzC + xs, z * zC + c],
        ]))._validate()

    @classmethod
    def from_xy(cls, x_vec: Vector, y_vec: Vector) -> Orientation:
        """
        Generate a new Orientation from two vectors using x as reference
        """
        if not isinstance(x_vec, Vector):
            x_vec = Vector(x_vec)
        if not isinstance(y_vec, Vector):
            y_vec = Vector(y_vec)
        x_vec.normalize()
        y_vec.normalize()
        orient = cls()
        orient.data[:, 0] = x_vec.data
        orient.data[:, 2] = x_vec.cross(y_vec).normalized().data
        orient.data[:, 1] = Vector(np.cross(orient.data[:, 2], x_vec.data)).normalized().data
        return orient._validate()

    @classmethod
    def from_yz(cls, y_vec: Vector, z_vec: Vector) -> Orientation:
        """
        Generate a new Orientation from two vectors using y as reference
        """
        if not isinstance(y_vec, Vector):
            y_vec = Vector(y_vec)
        if not isinstance(z_vec, Vector):
            z_vec = Vector(z_vec)
        y_vec.normalize()
        z_vec.normalize()
        orient = cls()
        orient.data[:, 1] = y_vec.data
        orient.data[:, 0] = y_vec.cross(z_vec).normalized().data
        orient.data[:, 2] = Vector(np.cross(orient.data[:, 0], y_vec.data)).normalized().data
        return orient._validate()

    @classmethod
    def from_xz(cls, x_vec: Vector, z_vec: Vector, ref: str = 'x') -> Orientation:
        """
        Generate a new Orientation from two vectors using x as reference
        """
        if not isinstance(x_vec, Vector):
            x_vec = Vector(x_vec)
        if not isinstance(z_vec, Vector):
            z_vec = Vector(z_vec)
        x_vec.normalize()
        z_vec.normalize()
        orient = cls()
        orient.data[:, 1] = z_vec.cross(x_vec).normalized().data

        if ref == 'x':
            orient.data[:, 0] = x_vec.data
            orient.data[:, 2] = Vector(np.cross(x_vec.data, orient.data[:, 1])).normalized().data
        elif ref == 'z':
            orient.data[:, 2] = z_vec.data
            orient.data[:, 0] = Vector(np.cross(orient.data[:, 1], z_vec.data)).normalized().data
        else:
            raise ValueError('Value of ref can only be x or z')

        return orient._validate()

    def to_axis_angle(self, unit_thresh: float = 1e-4) -> Tuple[Vector, float]:
        # adapted from
        # https://github.com/matthew-brett/transforms3d/blob/master/transforms3d/quaternions.py
        M = np.asarray(self._data, dtype=np.float32)
        # direction: unit eigenvector of R33 corresponding to eigenvalue of 1
        L, W = np.linalg.eig(M.T)
        i = np.where(np.abs(L - 1.0) < unit_thresh)[0]
        if i.size == 0:
            raise ValueError("no unit eigenvector corresponding to eigenvalue 1")
        direction = np.real(W[:, i[-1]]).squeeze()
        # rotation angle depending on direction
        cosa = (np.trace(M) - 1.0) / 2.0
        if abs(direction[2]) > 1e-8:
            sina = (M[1, 0] + (cosa - 1.0) * direction[0] * direction[1]) / direction[2]
        elif abs(direction[1]) > 1e-8:
            sina = (M[0, 2] + (cosa - 1.0) * direction[0] * direction[2]) / direction[1]
        else:
            sina = (M[2, 1] + (cosa - 1.0) * direction[1] * direction[2]) / direction[0]
        angle = math.atan2(sina, cosa)
        return Vector(direction), angle

    def to_rotation_vector(self, unit_thresh: float = 1e-5) -> Vector:
        v, a = self.to_axis_angle(unit_thresh)
        return v * a

    @classmethod
    def from_rotation_vector(cls, v: Vector) -> Orientation:
        if isinstance(v, (np.ndarray, list, tuple)):
            v = Vector(*v)
        if not isinstance(v, Vector):
            raise ValueError("Method take a Vector as argument")
        if v.length == 0:
            return cls(np.identity(3, dtype=np.float32))
        u = v.normalized()
        idx = (u.data != 0).argmax()
        return cls.from_axis_angle(u, v[idx] / u[idx], True)._validate()

    def copy(self) -> Orientation:
        return Orientation(self.data.copy())

    def similar(self, other: object, tol: float = float_eps) -> bool:
        """
        Return True if angular distance to other Orientation is less than tol
        return False otherwise
        """
        if not isinstance(other, Orientation):
            raise ValueError("Expecting an Orientation object, received {} of type {}".format(other, type(other)))
        return bool(self.ang_dist(other) <= tol)

    @property
    def vec_x(self) -> Vector:
        return Vector(self._data[:, 0])

    @property
    def vec_y(self) -> Vector:
        return Vector(self._data[:, 1])

    @property
    def vec_z(self) -> Vector:
        return Vector(self._data[:, 2])

    @staticmethod
    def mean(*orientations: Orientation) -> Orientation:
        """
        Averaging quaternions
        https://ntrs.nasa.gov/api/citations/20070017872/downloads/20070017872.pdf
        """
        try:
            from scipy.optimize import minimize, NonlinearConstraint
        except ImportError:
            raise Exception("scipy must be installed to use this method")
        arit_mean = np.mean([ori.to_rotation_vector().data for ori in orientations], axis=0).tolist()
        arit_mean_ori = Orientation.from_rotation_vector(arit_mean)
        x0 = np.array(arit_mean_ori.to_quaternion())

        quats: List[Tuple[float, float, float, float]] = [ori.to_quaternion() for ori in orientations]
        ans = minimize(
            func_error_matrix,
            x0,
            args=(quats),
            method='SLSQP',
            constraints=NonlinearConstraint(np.linalg.norm, 1 - 1e-20, 1 + 1e-20),
        )

        return Orientation.from_quaternion(*ans.x)


def func_error_matrix(x0: np.ndarray, quats: List[Tuple[float, float, float, float]]) -> float:

    total_error: float = 0.0
    for q in quats:
        vec = np.array(q[:3])
        scal = q[3]
        I3 = np.eye(3)
        qX = np.array([
            [0, -q[2], q[1]],
            [q[2], 0, -q[0]],
            [-q[1], q[0], 0],
        ])

        err_mtx = np.vstack((
            scal * I3 + qX,
            -vec.T
        ))

        total_error += float(np.linalg.norm(np.matmul(err_mtx.T, x0)) ** 2)

    return total_error
