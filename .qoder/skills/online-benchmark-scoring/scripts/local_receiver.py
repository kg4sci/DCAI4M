"""Local HTTP receiver that saves browser-extracted sheet JSON straight to disk.

The kdocs grid dump is tens of KB per sheet; routing it through the agent
context twice (tool result + file write) is wasteful. Instead the browser
POSTs each sheet object to this local server, which writes it to
<outdir>/<safe_name>.json and returns a tiny acknowledgement.

Usage:
    python local_receiver.py --port 8765 --outdir summary/raw

The browser page is https, but http://127.0.0.1 is a trustworthy origin so the
fetch is not blocked as mixed content. CORS headers are sent so the kdocs
origin may POST (including the OPTIONS preflight for application/json).
"""

from __future__ import annotations

import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def safe_name(name: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z_\-\u4e00-\u9fff]+", "_", (name or "").strip())
    return cleaned.strip("_") or "sheet"


class Handler(BaseHTTPRequestHandler):
    outdir: Path = Path(".")

    def _cors(self, code: int) -> None:
        self.send_response(code)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._cors(204)
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            obj = json.loads(body.decode("utf-8"))
            name = safe_name(obj.get("name"))
            out = self.outdir / f"{name}.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
            msg = json.dumps({"saved": str(out), "rows": len(obj.get("rows") or [])}).encode()
        except Exception as e:  # pragma: no cover
            self._cors(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
            return
        self._cors(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(msg)

    def log_message(self, fmt, *args):  # silence default stderr logging
        pass


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--outdir", required=True)
    args = p.parse_args()

    Handler.outdir = Path(args.outdir)
    Handler.outdir.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"listening on 127.0.0.1:{args.port} -> {Handler.outdir}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
