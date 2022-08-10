import csv
from typing import Tuple

from sklearn.metrics import f1_score

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


def f1(
        array: list,
        left_limit: int,
        right_limit: int
) -> float:
    TN, FN, TP, FP = 0, 0, 0, 0

    for row in array:
        value = round(float(row[1]), 2)
        if MIN_PERCENTAGE <= value <= left_limit and row[2] == OPERATOR:
            TP += 1
        elif row[2] == OPERATOR:
            FP += 1
        elif right_limit <= value < MAX_PERCENTAGE and row[2] == CORRECT:
            TP += 1
        elif row[2] == CORRECT:
            FP += 1
        elif left_limit < value < right_limit and row[2] == RISK:
            TP += 1  # TN += 1 ?
        elif row[2] == RISK:
            FP += 1  # FN += 1 ?

    precision = TP / (TP + FP)
    recall_score = TP / (TP + FN)
    return round(
        2 * ((precision * recall_score) / (precision + recall_score)), 4)


def get_decision(data: list) -> None:
    accuracies = []
    for operator_index in range(MIN_PERCENTAGE, MAX_PERCENTAGE):
        for correct_index in range(MIN_PERCENTAGE, MAX_PERCENTAGE):
            table_f1 = f1(
                data, operator_index, correct_index)
            this_f1 = (table_f1, operator_index, correct_index)
            print(this_f1)
            accuracies.append(this_f1)

    print(
        'Best table accuracy: {}.\n'
        'Operator limit: {}.\n'
        'Correct limit: {}.'.format(*max(accuracies))
    )


if __name__ == '__main__':
    get_decision(file_reader())
