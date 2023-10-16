"""Modules for statistic operations."""


import statistics
import numpy as np


def mean(input_list: list):
    """Return the mean of the of the given list.

    Args:
        input_list (list): _description_

    Returns:
        _type_: mean
    """
    return statistics.mean(input_list)


def mode(input_list: list):
    """Return the mode of the given list.

    Args:
        input_list (list): user given input list

    Returns:
        _type_: mode
    """
    try:
        return statistics.mode(input_list)
    except statistics.StatisticsError:
        print("values freaquency found equal")
    return None


def median(input_list: list):
    """Return the median of the given list.

    Args:
        input_list (list): user given input list

    Returns:
        _type_: median
    """
    return statistics.median(input_list)


def variance(input_list: list):
    """Return the variance of the given list.

    Args:
        input_list (list): user given input list

    Returns:
        _type_: variance
    """
    return statistics.pvariance(input_list)


def standard_devaition(input_list: list):
    """Return the standard_devaition of the given list.

    Args:
        input_list (list): user given input list

    Returns:
        _type_: standard_devaition
    """
    return statistics.stdev(input_list)


def transpose(input_matrix: list) -> list:
    """Return the transpose of given matrix.

    Args:
        input_matrix (list): user given input matrix

    Returns:
        list: transpose list
    """
    return list(np.transpose(input_matrix))


def determinant(input_matrix: list) -> float:
    """Return the transpose of given matrix.

    Args:
        input_matrix (list): user given input matrix

    Returns:
        float: determinant of given matrix
    """
    return np.linalg.det(input_matrix)
