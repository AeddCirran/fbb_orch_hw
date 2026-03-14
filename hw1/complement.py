#!/usr/bin/env python3

import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)


def rev_compl(seq: str) -> str:
    compl = seq.maketrans("ACGTUacgtu", "ACGTUacgtu")
    return seq.translate(compl)[::-1]


def main():
    logging.info("Starting task1")
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
    logging.info("Rev-compl seq: %s", rc_seq)
    gc_cont = (rc_seq.upper().count("G") + rc_seq.upper().count("C")) / len(rc_seq)
    logging.info("GC content: %.3f", gc_cont)
    print(f'{rc_seq}\n{gc_cont:.3f}')


if __name__ == "__main__":
    main()
