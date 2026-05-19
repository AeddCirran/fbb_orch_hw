#!/usr/bin/env python3

import sys
import socket

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9999
MAX_RETRIES = 3
BUFFER_SIZE = 1024


def send_msg(sock, addr, msg: str):
    sock.sendto((msg + "\n").encode("ascii"), addr)


def recv_response(sock, expected_prefixes, timeout: float):
    sock.settimeout(timeout)
    while True:
        try:
            data, _ = sock.recvfrom(BUFFER_SIZE)
            try:
                msg = data.decode("ascii").rstrip("\n\r")
            except UnicodeDecodeError:
                continue
            if any(msg.startswith(p) for p in expected_prefixes):
                return msg
        except socket.timeout:
            return None
        except OSError:
            return None


def request(sock, addr, msg, expected_prefixes, timeout):
    for _ in range(MAX_RETRIES):
        send_msg(sock, addr, msg)
        resp = recv_response(sock, expected_prefixes, timeout)
        if resp is not None:
            return resp
    return None


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    server_addr = (host, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sys.stdout.write("HELO ")
    sys.stdout.flush()
    time_input = sys.stdin.readline().strip()
    try:
        timeout = float(time_input) if time_input else 5.0
    except ValueError:
        timeout = 5.0

    helo_msg = f"HELO {timeout}"
    resp = request(sock, server_addr, helo_msg, ["WLCM"], timeout)
    if resp is None:
        print("Server is not responding.")
        sys.exit(1)
    print(resp)

    while True:
        sys.stdout.write("GUES ")
        sys.stdout.flush()
        guess_str = sys.stdin.readline().strip()
        if not guess_str:
            continue
        try:
            int(guess_str)
        except ValueError:
            continue

        gues_msg = f"GUES {guess_str}"
        resp = request(
            sock, server_addr, gues_msg, ["MORE", "LESS", "BING", "FAIL"], timeout
        )
        if resp is None:
            print("Lost connection to server.")
            break

        print(resp)
        if resp.startswith("BING") or resp.startswith("FAIL"):
            break

    sock.close()


if __name__ == "__main__":
    main()
