from scipy import stats
import pandas as pd
import numpy as np


# Summarization statistics by using a function
def summarize(df, field, title=None, description=None):
    """
    Generate and print a detailed summary of descriptive statistics for a DataFrame column.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data to summarize.
    field : str
        The column name in `df` to summarize.
    title : str, optional
        Title for the summary report. If None, uses `field`.
    description : str, optional
        Description of the measure. If None, 'Not provided.' is used.

    Returns
    -------
    None
        Prints the summary report to the console.

    Notes
    -----
    The summary includes measures of central tendency, spread, quantiles,
    skewness, kurtosis, and results of a normality test.
    """
    df = df.copy()
    measures = df[field].describe().round(2).drop(["count"])
    # Isolate the measures
    mean = measures.loc["mean"]
    std = measures.loc["std"]
    min = measures.loc["min"]
    q1 = measures.loc["25%"]
    median = measures.loc["50%"]
    q3 = measures.loc["75%"]
    max = measures.loc["max"]

    # Get kurtosis and skewness, handling possible NaN values
    # coming from percentual variations
    kurt = round(stats.kurtosis(df[field], nan_policy="omit"), 2)
    skew = round(stats.skew(df[field], nan_policy="omit"), 2)

    kurt_negative = kurt < 0
    skew_negative = skew < 0

    # Normality test
    # The test also has a nan_policy parameter
    statistic, p_value = stats.normaltest(df[field], nan_policy="omit")
    message = (
        "The data is unlikely to come from a normal distribution."
        if p_value < 0.05
        else "The data is likely to come from a normal distribution."
    )

    report = f"""
    {title or field}
    - Measure description: {description or 'Not provided.'}
    Central tendency
    - Mean: {mean}
    - Median: {median}

    Spread
    - Standard deviation: {std}

    Quantiles
    - Minimum value: {min}
    - 25th quantile: {q1}
    - 50th quantile: {median}
    - 75th quantile: {q3}
    - Maximum value: {max}

    Skewness and kurtosis
    - Skewness: {skew}
        {'Left-skewed: data concentrated on the right side; tail extends to the left. Expect: median higher than mean.'
        if skew_negative else
        'Right-skewed: data concentrated on the left side; tail extends to the right. Expect: mean higher than median.'}
    - Kurtosis: {kurt}
        {'Platikurtic: thinner tails and flatter peak. Expect: fewer extreme values than the normal.'
        if kurt_negative else
        'Leptokurtic: fatter tails and sharper peak. Expect: more extreme values than the normal.'}

    Normality test
    Null hypothesis: the data comes from a normal distribution.
    - Statistic: {round(statistic, 2)}
    - P-value: {p_value}
        {message}
  """
    print(report)


# Decade creation: functional aplication
def create_decades(dates: np.array):
    """
    Convert an array of datetime-like objects to their corresponding decades.

    Parameters
    ----------
    dates : numpy.array
        Array of datetime-like objects (must have a `.year` attribute).

    Returns
    -------
    list of int
        List of decades corresponding to each date in the input array.

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> create_decades(pd.to_datetime(['1995-01-01', '2003-05-12']))
    [1990, 2000]
    """
    years = [date.year for date in dates]
    decades = [int(np.floor(year / 10) * 10) for year in years]
    return decades
