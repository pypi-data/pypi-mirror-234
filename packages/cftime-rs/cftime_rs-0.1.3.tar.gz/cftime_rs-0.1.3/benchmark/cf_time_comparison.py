import numpy as np
import cftime_rs
import cftime
import time
import matplotlib.pyplot as plt
from typing import Tuple

ITERATIONS = [1, 10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
UNITS = "hours since 2000-01-01 00:00:00"
CALENDAR = "gregorian"


def performance_comparison_chart():
    """
    Generate a bar chart to compare the performance of cftime_rs and cftime.
    """

    cftime_rs_times = []
    cftime_times = []

    for n in ITERATIONS:
        print(f"Number of Iterations: {n}")
        arr = np.array(range(n))

        cftime_rs_duration = cftime_rs_benchmark(arr)
        cftime_rs_times.append(cftime_rs_duration)
        cftime_duration = cftime_benchmark(arr)
        cftime_times.append(cftime_duration)

    # Calculate performance improvement percentage
    performance_improvement = [
        ((cftime_time - cftime_rs_time) / cftime_rs_time) * 100
        for cftime_time, cftime_rs_time in zip(cftime_times, cftime_rs_times)
    ]
    fig, ax1 = plt.subplots(figsize=(10, 6))
    x_ticks = np.linspace(min(ITERATIONS), max(ITERATIONS), len(ITERATIONS))
    width = ITERATIONS[-1] / len(ITERATIONS) / 2
    ax1.bar(
        x_ticks - width / 2,
        cftime_rs_times,
        width=width,
        label="cftime_rs",
        color="royalblue",
        alpha=0.7,
    )
    ax1.bar(
        x_ticks + width / 2,
        cftime_times,
        width=width,
        label="cftime",
        color="orange",
        alpha=0.7,
    )
    ax1.set_xlabel("Number of Iterations")
    ax1.set_ylabel("Execution time (seconds)")
    ax1.set_xticks(x_ticks, [str(int(x)) for x in ITERATIONS])
    ax1.set_title(
        "Performance Comparison: cftime_rs vs. cftime. Encoding, calling __str__ and encoding. \nLower is better"
    )
    ax1.set_xticks(x_ticks)
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    # Create the secondary y-axis for performance improvement
    ax2 = ax1.twinx()
    ax2.plot(
        x_ticks,
        performance_improvement,
        marker="o",
        color="green",
        label="Performance Improvement (%)",
        alpha=0.7,
    )
    ax2.set_ylabel("Performance Improvement (%)")

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    plt.savefig("performance_comparison_with_str.png")


def cftime_benchmark(arr: np.array) -> float:
    cftime_start = time.time()
    datetimes = cftime.num2date(arr, UNITS, CALENDAR)
    for datetime in datetimes:
        datetime.__str__()
    _ = cftime.date2num(datetimes, UNITS, CALENDAR)
    cftime_end = time.time()
    return cftime_end - cftime_start


def cftime_rs_benchmark(arr: np.array) -> float:
    cftime_rs_start = time.time()
    datetimes = cftime_rs.num2date(arr, UNITS, CALENDAR)
    for datetime in datetimes:
        datetime.__str__()
    _ = cftime_rs.date2num(datetimes, UNITS, CALENDAR, dtype="int")
    cftime_rs_end = time.time()
    return cftime_rs_end - cftime_rs_start


def performance_comparison_chart_without_str():
    """
    Generate a bar chart to compare the performance of cftime_rs and cftime.
    """

    cftime_rs_times = []
    cftime_times = []

    for n in ITERATIONS:
        arr = np.array(range(n))

        cftime_rs_duration = cftime_rs_benchmark_without_str(arr)
        cftime_rs_times.append(cftime_rs_duration)
        cftime_duration = cftime_benchmark_without_str(arr)
        cftime_times.append(cftime_duration)

    # Calculate performance improvement percentage
    performance_improvement = [
        ((cftime_time - cftime_rs_time) / cftime_rs_time) * 100
        for cftime_time, cftime_rs_time in zip(cftime_times, cftime_rs_times)
    ]
    fig, ax1 = plt.subplots(figsize=(10, 6))
    x_ticks = np.linspace(min(ITERATIONS), max(ITERATIONS), len(ITERATIONS))
    width = ITERATIONS[-1] / len(ITERATIONS) / 2
    ax1.bar(
        x_ticks - width / 2,
        cftime_rs_times,
        width=width,
        label="cftime_rs",
        color="royalblue",
        alpha=0.7,
    )
    ax1.bar(
        x_ticks + width / 2,
        cftime_times,
        width=width,
        label="cftime",
        color="orange",
        alpha=0.7,
    )
    ax1.set_xlabel("Number of Iterations")
    ax1.set_ylabel("Execution time (seconds)")
    ax1.set_xticks(x_ticks, [str(int(x)) for x in ITERATIONS])
    ax1.set_title(
        "Performance Comparison: cftime_rs vs. cftime. Encoding, calling __str__ and encoding. \nLower is better"
    )
    ax1.set_xticks(x_ticks)
    ax1.grid(axis="y", linestyle="--", alpha=0.7)
    ax1.legend()

    # Create the secondary y-axis for performance improvement
    ax2 = ax1.twinx()
    ax2.plot(
        x_ticks,
        performance_improvement,
        marker="o",
        color="green",
        label="Performance Improvement (%)",
        alpha=0.7,
    )
    ax2.set_ylabel("Performance Improvement (%)")
    ax2.legend(loc="upper right")

    plt.savefig("performance_comparison_without_str.png")


def cftime_benchmark_without_str(arr: np.array) -> float:
    cftime_start = time.time()
    datetimes = cftime.num2date(arr, UNITS, CALENDAR)
    _ = cftime.date2num(datetimes, UNITS, CALENDAR)
    cftime_end = time.time()
    return cftime_end - cftime_start


def cftime_rs_benchmark_without_str(arr: np.array) -> float:
    cftime_rs_start = time.time()
    datetimes = cftime_rs.num2date(arr, UNITS, CALENDAR)
    _ = cftime_rs.date2num(datetimes, UNITS, CALENDAR, dtype="int")
    cftime_rs_end = time.time()
    return cftime_rs_end - cftime_rs_start


if __name__ == "__main__":
    performance_comparison_chart()
    performance_comparison_chart_without_str()
