import csv
from typing import Tuple

CORRECT: str = 'correct'
OPERATOR: str = 'operator'
RISK: str = 'reask'
MIN_PERCENTAGE = 0
MAX_PERCENTAGE: int = 100
EXCEPTED_ACCURACY: float = 0.00001


def file_reader() -> list:
    with open("table_20(1).csv") as file_name:
        file_read = list(csv.reader(file_name))
        file_read.pop(0)
        return file_read


def get_true_and_all_count(
        row: list,
        left_limit: int,
        right_limit: int,
        value: str
) -> Tuple[int, int]:
    true_results = 0
    all_results = 0
    if left_limit < float(row[1]) <= right_limit:
        if row[2] == value:
            true_results += 1
        all_results += 1
    return true_results, all_results


def accuracy(
        array: list,
        left_limit: int,
        right_limit: int
) -> float:
    true_results = 0
    all_results = 0
    for row in array:
        for phrase, limit in {
            OPERATOR: [MIN_PERCENTAGE, left_limit],
            RISK: [left_limit, right_limit],
            CORRECT: [right_limit, MAX_PERCENTAGE]
        }.items():
            temp_true, temp_all = get_true_and_all_count(
                row,
                *limit,
                phrase
            )
            true_results += temp_true
            all_results += temp_all
    if not all_results:
        return 0
    result = true_results / all_results
    return result if result != 1 else EXCEPTED_ACCURACY


def get_decision(data: list) -> None:
    accuracies = []
    for operator_index in range(MIN_PERCENTAGE, MAX_PERCENTAGE):
        for correct_index in range(MIN_PERCENTAGE, MAX_PERCENTAGE):
            table_accuracy = accuracy(
                data, operator_index, correct_index)
            accuracies.append((table_accuracy, operator_index, correct_index))

    print(
        'Best table accuracy: {}.\n'
        'Operator limit: {}.\n'
        'Correct limit: {}.'.format(*max(accuracies))
    )


if __name__ == '__main__':
    get_decision(file_reader())
