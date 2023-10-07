""" rsa-835-parser package """

# Importing standard libraries
import os
from tkinter import E
from typing import List
from warnings import warn

# Local imports
from rsa_835_parser.transaction_set.transaction_set import TransactionSet
from rsa_835_parser.transaction_set.transaction_sets import TransactionSets


def parse(path: str, debug: bool = False) -> TransactionSets:
    """Parses EDI 835 files into a TransactionSets object"""

    if path[0] == "~":
        path = os.path.expanduser(path)

    transaction_sets = []
    if os.path.isdir(path):
        files = _find_edi_835_files(path)
        for file in files:
            file_path = f"{path}/{file}"
            if debug:
                transaction_set = TransactionSet.build(file_path)
                transaction_sets.append(transaction_set)
            else:
                try:
                    transaction_set = TransactionSet.build(file_path)
                    transaction_sets.append(transaction_set)
                except FileNotFoundError as the_error:
                    warn(
                        f"Failed to build transaction_set from {file_path} with error: {the_error}"
                    )
    else:
        transaction_set = TransactionSet.build(path)
        transaction_sets.append(transaction_set)

    return TransactionSets(transaction_sets)


def _find_edi_835_files(path: str) -> List[str]:
    files = []
    for file in os.listdir(path):
        if file.endswith(".txt") or file.endswith(".835"):
            files.append(file)

    return files


def main():
    """Main function"""
    # The original code // Later, try to find the error
    # ---------------------------------------------------
    # data = parse("~/Desktop/eobs").to_dataframe()
    # data.to_csv("~/Desktop/transaction_sets.csv")


if __name__ == "__main__":
    main()
