#!/usr/bin/env python3

import argparse


def rev_compl(seq: str) -> str:
    compl = seq.maketrans("ACGTUacgtu", "ACGTUacgtu")
    return seq.translate(compl)[::-1]


def main():
    parser = argparse.ArgumentParser(
        description="Print rev-compl and GC-content of DNA/RNA seq"
    )
    parser.add_argument(
        "--seq",
        required=True,
        help="Input DNA/RNA seq",
    )
    args = parser.parse_args()

    rc_seq = rev_compl(args.seq)
    gc_cont = (rc_seq.upper().count("G") + rc_seq.upper().count("C")) / len(rc_seq)
    print(f'{rc_seq}\n{gc_cont:.3f}')


if __name__ == "__main__":
    main()