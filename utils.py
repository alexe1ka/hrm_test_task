import argparse
import sys


def parse_arguments() -> (list, list):
    parser = argparse.ArgumentParser(description='Parse alphabet path and ')
    parser.add_argument('--alphabet', type=str, help='path for alphabet txt file', required=True)
    parser.add_argument('--probabilities', type=str, help='path for probabilities csv file', required=True)
    args = parser.parse_args()
    # print(args.alphabet)
    # print(args.probabilities)

    prob_list = read_probabilities_from_file(args.probabilities, delim=",")
    alphabet_list = read_alphabet_from_file(args.alphabet)
    return prob_list, alphabet_list


def read_alphabet_from_file(filepath: str) -> str:
    # алфавит - это всегда одна строка?
    alphabet = ''
    try:
        with open(filepath, encoding="utf-8") as f:
            alphabet = f.read()
            # print(alp)
    except FileNotFoundError:
        sys.exit(f'file {filepath} not found!')
    return alphabet


def read_probabilities_from_file(filepath: str, delim: str = ",") -> list:
    import csv
    probabilities = []
    try:
        with open(filepath, newline='') as file:
            probs_reader = csv.reader(file, delimiter=delim)
            for row in probs_reader:
                # print(f"row: {row}")
                row_with_int = [float(el) for el in
                                row]  # проверки - можем конвертнуть число,сумма вероятностей <1
                probabilities.append(row_with_int)
                # print(', '.join(row))
    except FileNotFoundError as fe:
        sys.exit(f'file {filepath} not found!')
    except csv.Error as e:
        sys.exit(f'file {filepath}, line {probs_reader.line_num}: {e}')
    return probabilities
