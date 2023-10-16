from typing import Union

import numpy as np

float_eps = float(10 * np.finfo(np.float32).eps)
number_types = (float, int, np.number)
NumberType = Union[float, int, np.number]
