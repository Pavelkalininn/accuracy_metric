from main import OPERATOR, CORRECT, RISK


def get_decision(score: float):
    if score <= 29:
        return OPERATOR
    elif score >= 77:
        return CORRECT
    return RISK


if __name__ == '__main__':
    print(get_decision(56.5))
