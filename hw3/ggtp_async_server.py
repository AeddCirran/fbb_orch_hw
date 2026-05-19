#!/usr/bin/env python3

import asyncio
import sys
import zlib
import hashlib
import numpy as np

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 9999
BUFFER_SIZE = 1024


def crc32_ip(ip: str) -> int:
    return zlib.crc32(ip.encode()) & 0xFFFFFFFF


class GGTPAsyncServer(asyncio.DatagramProtocol):
    def __init__(self):
        self.clients = {}
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        sockname = transport.get_extra_info("sockname")
        print(f"GGTP server listening on {sockname[0]}:{sockname[1]}")

    def datagram_received(self, data, addr):
        self._process_datagram(data, addr)

    def _send(self, addr, msg: str):
        self.transport.sendto((msg + "\n").encode("ascii"), addr)

    def _start_game(self, ip, rng):
        upper = int(rng.integers(100, 1001))
        target = int(rng.integers(1, upper + 1))
        max_att = int(np.ceil(np.log2(upper)))
        self.clients[ip] = {
            "state": "playing",
            "target": target,
            "upper_bound": upper,
            "max_attempts": max_att,
            "attempts_used": 0,
            "rng_state": rng.bit_generator.state,
        }
        return upper, max_att

    def _handle_helo(self, addr, parts):
        ip = addr[0]
        if ip not in self.clients:
            rng = np.random.default_rng(crc32_ip(ip))
            upper, _ = self._start_game(ip, rng)
            return f"WLCM 1 {upper}"
        else:
            entry = self.clients[ip]
            if entry["state"] == "playing":
                return f"WLCM 1 {entry['upper_bound']}"
            else:
                rng = np.random.default_rng(crc32_ip(ip))
                rng.bit_generator.state = entry["rng_state"]
                upper, _ = self._start_game(ip, rng)
                return f"WLCM 1 {upper}"

    def _handle_gues(self, addr, parts):
        ip = addr[0]
        if ip not in self.clients or self.clients[ip]["state"] != "playing":
            return None
        if len(parts) < 2:
            return None
        try:
            guess = int(parts[1])
        except ValueError:
            return None

        entry = self.clients[ip]
        entry["attempts_used"] += 1

        if guess < entry["target"]:
            resp = "MORE"
        elif guess > entry["target"]:
            resp = "LESS"
        else:
            key = hashlib.sha256(f"{ip}:{entry['target']}".encode()).hexdigest()
            resp = f"BING {key}"
            entry["state"] = "idle"
            entry.pop("target")
            entry.pop("upper_bound")
            entry.pop("max_attempts")
            entry.pop("attempts_used")
            return resp

        if entry["attempts_used"] >= entry["max_attempts"]:
            resp = "FAIL"
            del self.clients[ip]
            return resp

        return resp

    def _process_datagram(self, data, addr):
        try:
            msg = data.decode("ascii").rstrip("\n\r")
        except UnicodeDecodeError:
            return

        parts = msg.split()
        if not parts:
            return

        cmd = parts[0].upper()
        response = None

        if cmd == "HELO":
            response = self._handle_helo(addr, parts)
        elif cmd == "GUES":
            response = self._handle_gues(addr, parts)

        if response is not None:
            self._send(addr, response)

    def error_received(self, exc):
        pass


async def main():
    host = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT

    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        GGTPAsyncServer, local_addr=(host, port)
    )

    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")
