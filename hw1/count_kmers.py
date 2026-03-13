#!/usr/bin/env python3

import argparse
import json
from collections import Counter
from collections.abc import Iterator


def parse_fa(path: str) -> Iterator[tuple[str, str]]:
    with open(path, "r") as f:
        seq_id, seq = None, ""

        for line in f:
            line = line[:-1]
            if line.startswith(">"):
                if seq_id is not None:
                    yield seq_id, seq
                seq_id, seq = line[1:], ""
            else:
                seq += line

        if seq_id is not None:
            yield seq_id, seq


def get_kmers(seq: str, k: int) -> Iterator[str]:
    n = len(seq)
    if n < k:
        return

    for i in range(n - k + 1):
        yield seq[i:i + k]


def main():
    parser = argparse.ArgumentParser(
        description="Count k-mers (4-mers) in fasta file"
    )
    parser.add_argument(
        "--fa",
        required=True,
        help="Input fasta file"
    )
    parser.add_argument(
        "-k",
        default=2,
        help="Len of k-mers"
    )
    parser.add_argument(
        "--out",
        "-o",
        default="cnts.json",
        help="Output json file"
    )
    # И еще коммент добавлю, т.к. почему бы и нет 😊

    output = "cnts.json"
    args = parser.parse_args()

    result = {}
    for seq_id, seq in parse_fa(args.fa):
        counts = Counter(get_kmers(seq, args.k))
        result[seq_id] = dict(counts)

    with open(args.out, "w") as out_f:
        json.dump(result, out_f, ensure_ascii=False)

    raise RuntimeError("Fail task2")


if __name__ == "__main__":
    main()
