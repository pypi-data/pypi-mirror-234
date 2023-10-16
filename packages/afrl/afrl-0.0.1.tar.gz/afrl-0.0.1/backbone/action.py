from typing import Dict

import numpy as np


class Action:
    def __init__(self):
        pass

    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__str__()


class DiscreteAction(Action):
    def __init__(self, action: int):
        super().__init__()
        self.action: int = action
        raise NotImplementedError

    @property
    def int_to_str(self) -> Dict[int, str]:
        raise NotImplementedError

    @property
    def str_to_int(self) -> Dict[str, int]:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.int_to_str[self.action]


class MultiDiscreteAction(Action):
    def __init__(self, action: np.ndarray):
        super().__init__()
        self.action: np.ndarray = action
        raise NotImplementedError

    @property
    def ints_to_str(self) -> Dict[np.ndarray, str]:
        raise NotImplementedError

    @property
    def str_to_ints(self) -> Dict[str, np.ndarray]:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.ints_to_str[self.action]


class ContinuousAction(Action):
    def __init__(self, action: float):
        super().__init__()
        self.action: float = action
        raise NotImplementedError

    def __str__(self):
        return str(self.action)


class MultiContinuousAction(Action):
    def __init__(self, action: np.ndarray):
        super().__init__()
        self.action: np.ndarray = action
        raise NotImplementedError

    def __str__(self):
        return str(self.action)
