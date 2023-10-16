from typing import Union
import numpy as np


def get_number_formatting(number: Union[float, int]) -> str:
    if number == -np.inf:
        return "-inf"
    elif isinstance(number, int):
        return str(number)
    elif number * 100 > 1:
        return "{:.3f}".format(number)
    else:
        return "{:.2E}".format(number)