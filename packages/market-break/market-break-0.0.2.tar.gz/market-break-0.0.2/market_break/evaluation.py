# evaluation.py

import json
from typing import Iterable, Optional, Union, Any, Dict, List

import numpy as np

from represent import represent, Modifiers

from market_break.process import (
    average_growth_rate,
    average_win_rate, average_shrink_rate, array,
    average_gain_rate, weighted_average_win_rate,
    average_change_rate, cumulative_shrink, cumulative_gain
)

__all__ = [
    "EvaluationResults",
    "results_report",
    "EvaluationResultsRecorder"
]

@represent
class EvaluationResults:
    """
    A class to represent a simulation results.
    This project is returned from the simulation function, as a
    data container to contain the simulation results, as well as
    the important initial parameters and values.

    This object can also be used to run analysis on the results' data,
    using the methods of the class.

    attributes:

    - balances:
        The balance values that were calculated during the simulation process.

    - predictions:
        The predicted balance values that were calculated during the simulation process.

    - trader:
        The trader object for the origin of the data.

    - best:
        The value to execute only the best arbitrage chain when several are found.

    - index:
        The index values of thew simulation process.
    """

    __modifiers__ = Modifiers(hidden=["predictions", "balances", "index"])

    def __init__(
            self,
            balances: Optional[Iterable[float]] = None,
            predictions: Optional[Iterable[float]] = None,
            index: Optional[Iterable] = None
    ) -> None:
        """
        Defines the class attributes.

        :param balances: The balances of the trades.
        :param predictions: The predictions of the trades.
        :param index: The index for the process.
        """

        self._balance_growth_rate = 0
        self._average_win_rate = 0
        self._weighted_average_win_rate = 0
        self._activity_rate = 0
        self._deviation_rate = 0
        self._prediction_accuracy = 0
        self._loss_growth_rate = 0
        self._profit_growth_rate = 0
        self._cumulative_shrink = 0
        self._cumulative_gain = 0

        self.balances = array(balances or [])
        self.predictions = array(predictions or [])
        self.index = index or []
    # end __init__

    @property
    def balance(self) -> float:
        """
        Returns thew value of the results.

        :return: The value.
        """

        if len(self.balances) > 0:
            return self.balances[-1] / self.balances[0]

        else:
            return 0
        # end if
    # end balance

    @property
    def profit(self) -> float:
        """
        Returns thew value of the results.

        :return: The value.
        """

        if len(self.balances) > 0:
            return self.balance - 1 if self.balance > 1 else 0

        else:
            return 0
        # end if
    # end profit

    @property
    def loss(self) -> float:
        """
        Returns thew value of the results.

        :return: The value.
        """

        if len(self.balances) > 0:
            return self.balance - 1 if self.balance < 1 else 0

        else:
            return 0
        # end if
    # end profit

    def cumulative_shrink(self) -> float:
        """
        Calculates the average balance rate.

        :return: The calculated number.
        """

        if (len(self.balances) > 1) and (self._cumulative_shrink == 0):
            gross_loss = cumulative_shrink(self.balances)

            if np.isnan(gross_loss):
                self._cumulative_shrink = 0

            else:
                self._cumulative_shrink = gross_loss
            # end if
        # end if

        return self._cumulative_shrink
    # end cumulative_shrink

    def cumulative_gain(self) -> float:
        """
        Calculates the average balance rate.

        :return: The calculated number.
        """

        if (len(self.balances) > 1) and (self._cumulative_gain == 0):
            gross_profit = cumulative_gain(self.balances)

            if np.isnan(gross_profit):
                self._cumulative_gain = 0

            else:
                self._cumulative_gain = gross_profit
            # end if
        # end if

        return self._cumulative_gain
    # end cumulative_gain

    def loss_growth_rate(self) -> float:
        """
        Calculates the average balance rate.

        :return: The calculated number.
        """

        if (len(self.balances) > 1) and (self._loss_growth_rate == 0):
            loss_growth_rate = average_shrink_rate(self.balances)

            if np.isnan(loss_growth_rate):
                self._loss_growth_rate = 0

            else:
                self._loss_growth_rate = loss_growth_rate
            # end if
        # end if

        return self._loss_growth_rate
    # end loss_growth_rate

    def profit_growth_rate(self) -> float:
        """
        Calculates the average balance rate.

        :return: The calculated number.
        """

        if (len(self.balances) > 1) and (self._profit_growth_rate == 0):
            profit_growth_rate = average_gain_rate(self.balances)

            if np.isnan(profit_growth_rate):
                self._profit_growth_rate = 0

            else:
                self._profit_growth_rate = profit_growth_rate
            # end if
        # end if

        return self._profit_growth_rate
    # end profit_growth_rate

    def balance_growth_rate(self) -> float:
        """
        Calculates the average balance rate.

        :return: The calculated number.
        """

        if (len(self.balances) > 1) and (self._balance_growth_rate == 0):
            balance_growth_rate = average_growth_rate(self.balances)

            if np.isnan(balance_growth_rate):
                self._balance_growth_rate = 0

            else:
                self._balance_growth_rate = balance_growth_rate
            # end if
        # end if

        return self._balance_growth_rate
    # end balance_growth_rate

    def win_rate(self) -> float:
        """
        Calculates the average win rate.

        :return: The calculated number.
        """

        if (len(self.balances) > 1) and (self._average_win_rate == 0):
            win_rate = average_win_rate(self.balances)

            if np.isnan(win_rate):
                self._average_win_rate = 0

            else:
                self._average_win_rate = win_rate
            # end if
        # end if

        return self._average_win_rate
    # end win_rate

    def weighted_win_rate(self) -> float:
        """
        Calculates the average win rate.

        :return: The calculated number.
        """

        if (len(self.balances) > 1) and (self._weighted_average_win_rate == 0):
            weighted_win_rate = weighted_average_win_rate(self.balances)

            if np.isnan(weighted_win_rate):
                self._weighted_average_win_rate = 0

            else:
                self._weighted_average_win_rate = weighted_win_rate
            # end if
        # end if

        return self._weighted_average_win_rate
    # end win_rate

    def activity_rate(self) -> float:
        """
        Calculates the average win rate.

        :return: The calculated number.
        """

        if (len(self.balances) > 1) and (self._activity_rate == 0):
            activity_rate = len(np.unique(self.balances)) / len(self.balances)

            if np.isnan(activity_rate):
                self._activity_rate = 0

            else:
                self._activity_rate = activity_rate
            # end if
        # end if

        return self._activity_rate
    # end activity_rate

    def deviation_rate(self) -> float:
        """
        Calculates the average win rate.

        :return: The calculated number.
        """

        if (len(self.balances) > 1) and (self._deviation_rate == 0):
            deviation_rate = average_change_rate(self.balances)

            if np.isnan(deviation_rate):
                self._deviation_rate = 0

            else:
                self._deviation_rate = deviation_rate
            # end if
        # end if

        return self._deviation_rate
    # end deviation_rate

    def prediction_accuracy(self) -> float:
        """
        Calculates the average win rate.

        :return: The calculated number.
        """

        if (self.predictions is None) or (len(self.predictions) != len(self.balances)):
            return np.nan
        # end if

        if (len(self.balances) > 1) and (self._prediction_accuracy == 0):
            predictions_change = (
                np.abs(self.predictions - self.balances) /
                self.balances
            )

            prediction_accuracy = (
                1 - (
                    np.sum(predictions_change) /
                    len(predictions_change)
                )
            )

            if np.isnan(prediction_accuracy):
                self._average_win_rate = 0

            else:
                self._prediction_accuracy = prediction_accuracy
            # end if
        # end if

        return self._prediction_accuracy
    # end prediction_accuracy
# end EvaluationResults

class EvaluationResultsRecorder:
    """A class to represent a record visualizer."""

    INDEX = "index"
    BALANCES = "balances"
    ADDING_BALANCES = "adding_balances"
    PREDICTIONS = "predictions"
    ADDING_PREDICTIONS = "predictions"

    ATTRIBUTES = (INDEX, BALANCES, ADDING_BALANCES, PREDICTIONS, ADDING_PREDICTIONS)

    def __init__(self, keys: Iterable[Any]) -> None:
        """
        Defines the class attributes.

        :param keys: The keys for the reports.
        """

        self.record: Dict[str, Dict[str, List[Union[float, Any]]]] = {
            key: {attribute: [] for attribute in self.ATTRIBUTES}
            for key in keys
        }

        self.sum_record: Dict[str, List[Union[float, Any]]] = {
            attribute: [] for attribute in self.ATTRIBUTES
        }
    # end __init__

    def update(
            self,
            data: Dict[Any, Union[Dict[str, Iterable[Union[float, Any]]], EvaluationResults]],
            start: Optional[float] = None,
            adjust: Optional[bool] = True,
            sort: Optional[bool] = True,
            padding: Optional[bool] = False
    ) -> None:
        """
        Updates the record of the evaluation results.

        :param data: The data to add.
        :param start: start value for the adding values.
        :param adjust: The value to adjust for unknown keys.
        :param sort: The value to sort the indexes.
        :param padding: The value to pad the short values.
        """

        if start is None:
            start = 0
        # end if

        add = True

        start_add_balance = (
            self.sum_record[self.ADDING_BALANCES][0]
            if self.sum_record[self.ADDING_BALANCES] else start
        )
        start_add_prediction = (
            self.sum_record[self.ADDING_PREDICTIONS][0]
            if self.sum_record[self.ADDING_PREDICTIONS] else start
        )

        for key, results in data.items():
            if key not in self.record:
                if not adjust:
                    raise KeyError(
                        f"Key: {repr(key)} is not present in the record. "
                        f"All keys must be defined during initialization."
                    )

                else:
                    continue
                # end if
            # end if

            for attribute in (self.INDEX, self.BALANCES, self.PREDICTIONS):
                if (
                    hasattr(results, attribute)
                    if isinstance(results, EvaluationResults) else
                    attribute in results
                ):
                    # noinspection PyUnresolvedReferences
                    for i, value in enumerate(
                        getattr(results, attribute)
                        if isinstance(results, EvaluationResults) else
                        results[attribute]
                    ):
                        self.record[key][attribute].append(value)

                        if attribute != self.INDEX:
                            self.record[key][f"adding_{attribute}"].append(
                                value + self.record[key][attribute][-1]
                            )

                            if add:
                                self.sum_record[attribute].append(value)
                                self.sum_record[f"adding_{attribute}"].append(
                                    value + (
                                        self.sum_record[f"adding_{attribute}"][-1]
                                        if self.sum_record[f"adding_{attribute}"] else
                                        self.sum_record[attribute][-1]
                                    )
                                )

                                add = False

                            else:
                                self.sum_record[attribute][i] += value
                                self.sum_record[f"adding_{attribute}"][i] += value
                            # end if
                        # end if

                        if (
                            (attribute == self.INDEX) and
                            (value not in self.sum_record[attribute])
                        ):
                            self.sum_record[attribute].append(value)

                            if sort:
                                try:
                                    self.sum_record[attribute].sort()

                                except Exception as e:
                                    if adjust:
                                        pass

                                    else:
                                        raise e
                                    # end if
                                # end try
                            # end if
                        # end if
                    # end for
                # end if
            # end for
        # end for

        try:
            self.sum_record[self.ADDING_BALANCES][0] = start_add_balance
            self.sum_record[self.ADDING_PREDICTIONS][0] = start_add_prediction

        except IndexError:
            pass
        # end try

        if padding:
            length = max(
                max(len(values) for values in result.values())
                for result in self.record.values()
            )

            for key, value in self.record.items():
                self.record[key] = {
                    attribute: [*values, *([0] * (length - len(values)))]
                    for attribute, values in value.items()
                }
            # end for
        # end if
    # end update

    def sum_evaluation_result(self) -> EvaluationResults:
        """
        Creates all results from the record.

        :return: The result objects.
        """

        return EvaluationResults(
            **{
                attribute: values
                for attribute, values in self.sum_record.items()
                if attribute in (self.INDEX, self.BALANCES, self.PREDICTIONS)
            }
        )
    # end sum_evaluation_result

    def adding_sum_evaluation_result(self) -> EvaluationResults:
        """
        Creates all results from the record.

        :return: The result objects.
        """

        return EvaluationResults(
            **{
                attribute.replace("adding_", ""): values
                for attribute, values in self.sum_record.items()
                if attribute in (
                    self.INDEX, self.ADDING_BALANCES, self.ADDING_PREDICTIONS
                )
            }
        )
    # end adding_sum_evaluation_result

    def evaluation_results(
        self, padding: Optional[bool] = False
    ) -> Dict[Any, EvaluationResults]:
        """
        Creates all results from the record.

        :param padding: The value to pad the short values.

        :return: The result objects.
        """

        length = max(
            max(len(v) for v in result.values())
            for result in self.record.values()
        )

        return {
            key: EvaluationResults(
                **{
                    attribute: (
                        [*([0] * (length - len(values))), *values]
                        if padding else values
                    )
                    for attribute, values in results.items()
                    if attribute in (self.INDEX, self.BALANCES, self.PREDICTIONS)
                }
            ) for key, results in self.record.items()
        }
    # end evaluation_results

    def adding_evaluation_results(
            self, padding: Optional[bool] = False
    ) -> Dict[Any, EvaluationResults]:
        """
        Creates all results from the record.

        :param padding: The value to pad the short values.

        :return: The result objects.
        """

        length = max(
            max(len(v) for v in result.values())
            for result in self.record.values()
        )

        return {
            key: EvaluationResults(
                **{
                    attribute.replace("adding_", ""): (
                        [*([0] * (length - len(values))), *values]
                        if padding else values
                    )
                    for attribute, values in results.items()
                    if attribute in (
                        self.INDEX, self.ADDING_BALANCES, self.ADDING_PREDICTIONS
                    )
                }
            ) for key, results in self.record.items()
        }
    # end adding_evaluation_results
# end EvaluationResultsRecorder

class JSONEncoder(json.JSONEncoder):
    """A class to represent a json encoder."""

    def default(self, obj: Any) -> Any:
        """
        encodes the value of the object to valid json data.

        :param obj: The object to encode.

        :return: The encoded json value.
        """

        if isinstance(obj, np.integer):
            return int(obj)
        # end if

        if isinstance(obj, np.floating):
            return float(obj)
        # end if

        if isinstance(obj, np.ndarray):
            return obj.tolist()
        # end if

        try:
            if np.isnan(obj):
                obj = None
            # end if

        except TypeError:
            pass
        # end try

        return json.JSONEncoder.default(self, obj)
    # end default
# end JSONEncoder

def results_report(
        results: EvaluationResults,
        precision: Optional[int] = 3,
        prefix: Optional[str] = "",
        info: Optional[bool] = True,
        performance: Optional[bool] = True,
        total: Optional[bool] = True
) -> Dict[str, Union[str, float]]:
    """
    Calculates the results.

    :param results: The results object.
    :param precision: The precision of the floating point numbers.
    :param prefix: The prefix for each key.
    :param info: The value to include the basic info.
    :param performance: The value to include the performance analysis.
    :param total: The value to include the total results.

    :return: The data of the results.
    """

    data = {
        **(
            {
                f"{prefix}Info": "",
                f"{prefix}iterations": len(results.balances),
                f"{prefix}periods": len(results.index),
                **(
                    {
                        f"{prefix}start": str(results.index[0]),
                        f"{prefix}end": str(results.index[-1]),
                        f"{prefix}span": str(results.index[-1] - results.index[0]),
                    } if results.index else {}
                ),
                f"{prefix}starting balance": (
                    str(round(results.balances[0], precision))
                    if len(results.balances) > 0 else "none"
                ),
            } if info else {}
        ),
        **(
            {
                f"{prefix}Performance": "",
                f"{prefix}win rate (%)": results.win_rate() * 100,
                f"{prefix}weighted win rate (%)": results.weighted_win_rate() * 100,
                f"{prefix}activity rate (%)": results.activity_rate() * 100,
                f"{prefix}deviation rate (%)": results.deviation_rate() * 100,
                f"{prefix}accuracy rate (%)": results.prediction_accuracy() * 100,
                f"{prefix}profit growth rate (%)": results.profit_growth_rate() * 100,
                f"{prefix}loss growth rate (%)": results.loss_growth_rate() * 100,
                f"{prefix}balance growth rate (%)": results.balance_growth_rate() * 100,
            } if performance else {}
        ),
        **(
            {
                f"{prefix}Total Results": "",
                f"{prefix}ending balance": (
                    str(round(results.balances[-1], precision))
                    if len(results.balances) > 0 else "none"
                ),
                f"{prefix}gross profit (%)": results.cumulative_gain() * 100,
                f"{prefix}net profit (%)": results.profit * 100,
                f"{prefix}gross loss (%)": results.cumulative_shrink() * 100,
                f"{prefix}net loss (%)": results.loss * 100,
                f"{prefix}balance (%)": results.balance * 100
            } if total else {}
        )
    }

    return json.loads(json.dumps(data, cls=JSONEncoder))
# end results_report

def bidirectional_results_report(
        long_results: EvaluationResults,
        short_results: EvaluationResults,
        precision: Optional[int] = 3,
        prefix: Optional[str] = "",
        info: Optional[bool] = True,
        performance: Optional[bool] = True,
        total: Optional[bool] = True
) -> Dict[str, Union[str, float]]:
    """
    Calculates the results.

    :param long_results: The long results object.
    :param short_results: The long results object.
    :param precision: The precision of the floating point numbers.
    :param prefix: The prefix for each key.
    :param info: The value to include the basic info.
    :param performance: The value to include the performance analysis.
    :param total: The value to include the total results.

    :return: The data of the results.
    """

    results = EvaluationResults(
        index=long_results.index,
        balances=long_results.balances + short_results.balances
    )

    data = {
        **results_report(
            results=results, precision=precision, prefix=prefix,
            info=info, performance=performance, total=total
        ),
        **results_report(
            results=long_results, precision=precision,
            prefix=prefix, performance=performance, total=total
        ),
        **results_report(
            results=short_results, precision=precision,
            prefix=prefix, performance=performance, total=total
        )
    }

    return json.loads(json.dumps(data, cls=JSONEncoder))
# end bidirectional_results_report