import argparse
import numpy as np

from typing import Tuple
from scipy.stats import rankdata
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression


def load_data(path: str):
    """
    Loads the data from the source by the specified path.
    Input format: lines with separated x and y observations respectively.
    """
    with open(path, 'r') as data_file:
        raw_data = [line.split(' ') for line in data_file.readlines()]
    return np.array(raw_data, dtype=np.int)


def save_results(ranks_diff: float, std_err: float, contingency_measure: float, path: str):
    """
    Saves the obtained metrics to the output file with a specified path.
    """
    with open(path, 'w') as results_file:
        results_file.write(f'{int(round(ranks_diff))} {int(round(std_err))} {round(contingency_measure, 2)}')


def repeated_median_regression(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
    """
    Bonus function. which calculates weights of the repeated median regression.
    We actually don't need it for the task.
    """
    x_diff = x[np.newaxis, :] - x[:, np.newaxis]
    y_diff = y[np.newaxis, :] - y[:, np.newaxis]
    coefficients = np.divide(y_diff, x_diff, where=x_diff != 0,
                             out=np.full_like(x_diff, dtype=np.float, fill_value=np.nan)).T
    bs = np.nanmedian(coefficients, axis=0)
    b = np.median(bs)
    a = np.median(y - b * x)
    return (b, a)


def monotonic_conjugacy_method(data: np.ndarray, print_coefficients: bool) -> Tuple[float, float, float]:
    """
    Applies the monotonic conjugacy method.
    """
    n = data.shape[0]
    data = data[np.argsort(data, 0)[:, 0]]
    ranks = n + 1 - rankdata(data[:, 1])
    p = round(n / 3)
    R1, R2 = ranks[:p].sum(), ranks[-p:].sum()
    contingency_measure = (R1 - R2) / (p * (n - p))
    std_err = (n + 1 / 2) * np.sqrt(p / 6)
    if print_coefficients:
        x, y = data[:, 0], data[:, 1]
        b, a = repeated_median_regression(x, y)
        y_pred = b * x + a
        print(f'Repeated median regression coefficients: Y = {b} * X + {a}, R2 score: {r2_score(y, y_pred)}')
        lr = LinearRegression().fit(x.reshape(-1, 1), y)
        print(f'Classical linear regression R2 score: {r2_score(y, lr.predict(x.reshape(-1, 1)))}')
    return R1 - R2, std_err, contingency_measure


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=False, type=str, default='in.txt',
                        help="Path to the input file")
    parser.add_argument('--output', required=False, type=str, default='out.txt',
                        help="Path to the output file")
    parser.add_argument('--print_coefficients', required=False, action='store_true',
                        help='Apply the repeated median regression, and print results to stdout.')
    args = parser.parse_args()
    try:
        input_data = load_data(args.input)
    except Exception as e:
        print(f'Error occurred during data loading: {e}')
        exit(1)
    if input_data.shape[0] < 9:
        print(f'Required a series of at least 9 observations, {input_data.shape[0]} provided')
        exit(1)
    results = monotonic_conjugacy_method(input_data, args.print_coefficients)
    try:
        save_results(*results, args.output)
    except Exception as e:
        print(f'Error occurred during output writing: {e}')
        exit(1)
