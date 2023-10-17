import math

import numpy as np
from sklearn import metrics as skmetrics


class CalcMetrics:
    def __init__(self):
        pass

    def MASE(self, training_series, testing_series, prediction_series):
        """
        Computes the MEAN-ABSOLUTE SCALED ERROR forcast error for univariate time series prediction.

        See "Another look at measures of forecast accuracy", Rob J Hyndman

        parameters:
                training_series: the series used to train the model, 1d numpy array
                testing_series: the test series to predict, 1d numpy array or float
                prediction_series: the prediction of testing_series, 1d numpy array (same size as testing_series) or float
                absolute: "squares" to use sum of squares and root the result, "absolute" to use absolute values.

        """
        # print "Needs to be tested."
        n = training_series.shape[0]
        d = np.abs(np.diff(training_series)).sum() / (n - 1)

        errors = np.abs(testing_series - prediction_series)
        return errors.mean() / d

    def main_ts_metrics(self, real, pred, train):
        R2 = skmetrics.r2_score(real, pred)
        MAPE = skmetrics.mean_absolute_percentage_error(real, pred)
        MAE = skmetrics.mean_absolute_error(real, pred)
        MSE = skmetrics.mean_squared_error(real, pred)

        return {
            "R2": R2,
            "MAPE": MAPE,
            "MAE": MAE,
            "MSE": MSE,
            "RMSE": math.sqrt(MSE),
            "MASE": self.MASE(train, real, pred) if len(train) else None,
        }
