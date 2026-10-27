from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


class Receiver(BaseHTTPRequestHandler):
    output: Path

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(length).decode("utf-8")
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.output.write_text(payload, encoding="utf-8")
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self.end_headers()
        self.wfile.flush()
        print(f"received {length} bytes -> {self.output}")

    def log_message(self, fmt: str, *args: object) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser(description="Receive one ReproLens webhook for demonstration.")
    parser.add_argument("--port", type=int, default=8770)
    parser.add_argument("--output", default="webhook-received.json")
    args = parser.parse_args()
    Receiver.output = Path(args.output).resolve()
    server = HTTPServer(("127.0.0.1", args.port), Receiver)
    print(f"Waiting for one POST on http://127.0.0.1:{args.port}/hook")
    server.handle_request()
    server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
