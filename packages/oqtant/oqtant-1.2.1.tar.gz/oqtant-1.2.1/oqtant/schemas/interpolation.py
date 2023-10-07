from bert_schemas import job as job_schema
from scipy.interpolate import interp1d


def interpolation_to_kind(interpolation: job_schema.InterpolationType) -> str:
    """Convert our InterpolationType to something scipy can understand

    Args:
        interpolation (InterpolationType): Job primitive interpolation type

    Returns:
        str: 'kind' string to be used by scipy's interp1d
    """
    interpolation_map = {"OFF": "zero", "STEP": "previous", "SMOOTH": "cubic"}

    return interpolation_map.get(interpolation, interpolation.lower())


def interpolate_1d(
    xs: list,
    ys: list,
    x: float,
    interpolation: job_schema.InterpolationType = "LINEAR",
) -> float:
    """
    Interpolates a 1D list of pairs [xs, ys] at the evaluation point x.
    Extrapolation requests return 0.0.
    Args:
        xs (list): List of x values
        ys (list): List of y values (of the same length as xs)
        x (float): Desired x-coord to evaluate the resulting interpolation function.
        interpolation (InterpolationType, optional):
            Interpolation style. Defaults to InterpolationType.LINEAR.

    Returns:
        float: Interpolation function value at the specified x.
    """
    f = interp1d(
        xs,
        ys,
        kind=interpolation_to_kind(interpolation),
        bounds_error=False,
        fill_value=(0.0, 0.0),
    )
    return f(x)[()]  # extract value


def interpolate_1d_list(
    xs: list,
    ys: list,
    x_values: list,
    interpolation: job_schema.InterpolationType = "LINEAR",
) -> list:
    """Interpolates a 1D list of pairs [xs, ys] at the evaluation points given by xs.
    Extrapolation requests return 0.0.
    Args:
        xs (list): List of x values
        ys (list): List of y values (of the same length as xs)
        xs (list): Desired x-coords to evaluate the resulting interpolation function.
        interpolation (InterpolationType, optional): Interpolation style.
            Defaults to InterpolationType.LINEAR.

    Returns:
        list: Floating point values corresponding to evaluation of the interpolation
        function value at the specified xs.
    """
    f = interp1d(
        xs,
        ys,
        kind=interpolation_to_kind(interpolation),
        bounds_error=False,
        fill_value=(0.0, 0.0),
    )
    return list(f(x_values))
