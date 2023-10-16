import collections
import datetime
import warnings
from typing import List, Tuple
import dateutil
import statistics
from matplotlib import pyplot as plt


def compare_metric_to_prev_period(
    datetime_index: List[datetime.datetime],
    metric_vector: List[int | float],
    define_period: Tuple[datetime.datetime],
    compare_to_previous: str,  # {"year","quarter", "month", "week", "day", "hour"}
    plot: bool = True,
) -> dict:
    """Compare the behaviour of a continuous metric in 2 different time periods

    Compares
    --------
    Relative change in:
        - Average (mean) Observation
        - Min
        - Max
        - Linear Trend
        - Variance

    TODO:   raise a warning if the 2 comparison periods overlap

    Example Usage
    -------------
    import pandas as pd
    temp_df = pd.read_csv("/Users/josephbolton/personal_projects/cognisant/cognisant/time_series/datetime/example_data/walmart_weekly_sales.csv").query("store_id==2")
    date_time_vec = [datetime.datetime.strptime(x,"%d-%m-%Y") for x in temp_df["date"]]

    result = compare_metric_to_prev_period(
        datetime_index = date_time_vec,
        metric_vector = temp_df.weekly_sales.tolist(),
        define_period = (
            datetime.datetime(year=2012, month=7, day=1),
            datetime.datetime(year=2012, month=9, day=1),
        ),
        compare_to_previous = "year",
        plot = True,
    )
    [print(result["comparisons"][k]["description"]) for k in result["comparisons"]]

    """
    DataPoint: collections.namedtuple = collections.namedtuple(
        "DataEntry", ["dt", "metric"]
    )
    ts_data: List[DataPoint] = [
        DataPoint(dt=datetime_index[i], metric=metric_vector[i])
        for i in range(len(datetime_index))
    ]
    ts_data.sort(key=lambda x: x.dt)  # sort datapoints by datetime

    period_len: datetime.timedelta = define_period[1] - define_period[0]

    if compare_to_previous == "year":
        periods_diff: dateutil.relativedelta.relativedelta = (
            dateutil.relativedelta.relativedelta(years=1)
        )
        compare_period_start_date: datetime.datetime = define_period[0] - periods_diff

    elif compare_to_previous == "quarter":
        periods_diff: dateutil.relativedelta.relativedelta = (
            dateutil.relativedelta.relativedelta(months=3)
        )
        compare_period_start_date: datetime.datetime = define_period[0] - periods_diff
    elif compare_to_previous == "month":
        periods_diff: dateutil.relativedelta.relativedelta = (
            dateutil.relativedelta.relativedelta(months=1)
        )
        compare_period_start_date: datetime.datetime = define_period[0] - periods_diff
    elif compare_to_previous == "week":
        periods_diff: dateutil.relativedelta.relativedelta = (
            dateutil.relativedelta.relativedelta(weeks=1)
        )
        compare_period_start_date: datetime.datetime = define_period[0] - periods_diff
    elif compare_to_previous == "day":
        periods_diff: dateutil.relativedelta.relativedelta = (
            dateutil.relativedelta.relativedelta(days=1)
        )
        compare_period_start_date: datetime.datetime = define_period[0] - periods_diff
    elif compare_to_previous == "hour":
        periods_diff: dateutil.relativedelta.relativedelta = (
            dateutil.relativedelta.relativedelta(hours=1)
        )
        compare_period_start_date: datetime.datetime = define_period[0] - periods_diff
    else:
        raise ValueError(
            f"invalid input argument compare_to_previous='{compare_to_previous}' - must be one of ['year','quarter','month','week','day','hour']"
        )

    warnings.warn("JOE CHECK TODO: The comparison periods are overlapping")

    define_compare_period: Tuple[datetime.datetime] = (
        compare_period_start_date,
        compare_period_start_date + period_len,
    )

    period_data: List[DataPoint] = [
        x for x in ts_data if x.dt >= define_period[0] and x.dt <= define_period[1]
    ]

    compare_period_data: List[DataPoint] = [
        x
        for x in ts_data
        if x.dt >= define_compare_period[0] and x.dt <= define_compare_period[1]
    ]

    results: dict = {
        "period": [
            define_period[0].strftime("%Y-%m-%d %H:%M:%S"),
            define_period[1].strftime("%Y-%m-%d %H:%M:%S"),
        ],
        "compare_period": [
            define_compare_period[0].strftime("%Y-%m-%d %H:%M:%S"),
            define_compare_period[1].strftime("%Y-%m-%d %H:%M:%S"),
        ],
        "comparisons": {
            "mean_metric_value": {
                "description": None,
                "period_value": statistics.mean([x[1] for x in period_data]),
                "compare_period_value": statistics.mean(
                    [x[1] for x in compare_period_data]
                ),
                "ratio": None,
            },
            "smallest_metric_value": {
                "description": None,
                "period_value": min([x[1] for x in period_data]),
                "compare_period_value": min([x[1] for x in compare_period_data]),
                "ratio": None,
            },
            "largest_metric_value": {
                "description": None,
                "period_value": max([x[1] for x in period_data]),
                "compare_period_value": max([x[1] for x in compare_period_data]),
                "ratio": None,
            },
            "linear_trend_in_metric_value": {
                "description": None,
                "period_value": None,
                "compare_period_value": None,
                "ratio": None,
                "model_params": {
                    "period": {},
                    "compare_period": {},
                },
            },
            # "variance_in_metric_value": {
            #     "description": "TODO",
            #     "period_value": 0,
            #     "compare_period_value": 0,
            #     "ratio": 0,
            # },
        },
    }

    period_slope, period_intercept = statistics.linear_regression(
        list(range(len(period_data))),
        [x.metric for x in period_data],
    )
    results["comparisons"]["linear_trend_in_metric_value"]["model_params"]["period"] = {
        "intercept": period_intercept,
        "slope": period_slope,
    }
    results["comparisons"]["linear_trend_in_metric_value"][
        "period_value"
    ] = period_slope
    compare_period_slope, compare_period_intercept = statistics.linear_regression(
        list(range(len(compare_period_data))),
        [x.metric for x in compare_period_data],
    )
    results["comparisons"]["linear_trend_in_metric_value"][
        "compare_period_value"
    ] = compare_period_slope
    results["comparisons"]["linear_trend_in_metric_value"]["model_params"][
        "compare_period"
    ] = {
        "intercept": compare_period_intercept,
        "slope": compare_period_slope,
    }

    for metric_name in [
        "mean_metric_value",
        "smallest_metric_value",
        "largest_metric_value",
        "linear_trend_in_metric_value",
    ]:
        results["comparisons"][metric_name]["ratio"] = (
            results["comparisons"][metric_name]["period_value"]
            / results["comparisons"][metric_name]["compare_period_value"]
        )
        if (
            results["comparisons"][metric_name]["period_value"]
            > results["comparisons"][metric_name]["compare_period_value"]
        ):
            results["comparisons"][metric_name][
                "description"
            ] = f"{metric_name.replace('_',' ')} is {results['comparisons'][metric_name]['ratio']:,.4f} times higher ({100*(results['comparisons'][metric_name]['ratio']-1):,.2f}%) in the later period (1 {compare_to_previous} later)"
        else:
            results["comparisons"][metric_name][
                "description"
            ] = f"{metric_name.replace('_',' ')} is {results['comparisons'][metric_name]['ratio']:,.4f} times lower ({100*(results['comparisons'][metric_name]['ratio']-1):,.2f}%) in the later period (1 {compare_to_previous} later)"

    if plot:
        plt.figure(figsize=(10, 5))
        plt.plot(
            [x.dt for x in period_data],
            [x.metric for x in period_data],
            label=f"later period [{define_period[0].strftime('%Y-%m-%d %H:%M:%S')}, {define_period[1].strftime('%Y-%m-%d %H:%M:%S')}]",
            color="red",
        )
        plt.plot(
            [x.dt for x in period_data],
            [x * period_slope + period_intercept for x in range(len(period_data))],
            color="red",
            linestyle="dashed",
            alpha=0.3,
        )
        plt.plot(
            [x.dt + periods_diff for x in compare_period_data],
            [x.metric for x in compare_period_data],
            label=f"earlier period [{define_compare_period[0].strftime('%Y-%m-%d %H:%M:%S')}, {define_compare_period[1].strftime('%Y-%m-%d %H:%M:%S')}]",
            color="blue",
        )
        plt.plot(
            [x.dt + periods_diff for x in compare_period_data],
            [
                x * compare_period_slope + compare_period_intercept
                for x in range(len(compare_period_data))
            ],
            color="blue",
            linestyle="dashed",
            alpha=0.3,
        )
        plt.xticks(rotation=270)
        plt.ylabel("metric value")
        plt.xlabel("Date-Time (later period)")
        plt.title(f"Comparison to same period in previous {compare_to_previous}")
        plt.legend()

    return results
