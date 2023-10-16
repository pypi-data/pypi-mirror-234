import pandas as pd


def generate_percentage_steps(close: pd.Series, step: float) -> list:
    """
    Generate a list of percentage steps from a pandas Series of closing prices.

    :param close: A pandas Series containing close prices.
    :param step: Step value for percentage change.
    :return: List of percentage steps.
    """
    decimals = len(str(step)[2:])

    # Factor to convert float to integer to maintain precision
    int_factor = 10 ** decimals

    # Calculate percentage change and fill NaNs
    returns = close.ffill().pct_change()

    # Convert float values to integers for iteration
    max_value = int(returns.max() * int_factor)
    min_value = int(returns.min() * int_factor)
    step_value = int(step * int_factor)

    # Generate levels using the step value
    levels = [i / int_factor for i in range(min_value, max_value, step_value)]

    # Add the negative levels and sort
    levels = sorted(levels + [-i for i in levels if i != 0])

    return levels
