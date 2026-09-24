import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", sys.argv[1] if len(sys.argv) > 1 else 8080))


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        ".html": "text/html",
        ".htm": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".mjs": "application/javascript",
        ".json": "application/json",
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".ico": "image/x-icon",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".txt": "text/plain",
        ".wasm": "application/wasm",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    # Clean URLs: /partners -> partners.html (mirrors production).
    PAGES = {
        "questionnaire", "results", "scheme-details", "saved-schemes",
        "reset-password", "profile-view", "profile", "calculator",
        "partners", "register", "login",
    }

    def do_GET(self):
        raw = self.path.split("?", 1)[0].rstrip("/")
        if raw in ("", "/index.html"):
            self.path = "/index.html"
        elif raw == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        elif raw == "/oauth/callback":
            self.path = "/oauth/callback.html" + self.path[len(raw):]
        elif raw.startswith("/oauth/") and raw.endswith(".html"):
            pass
        elif raw.lstrip("/") in self.PAGES:
            self.path = "/" + raw.lstrip("/") + ".html" + self.path[len(raw):]
        elif raw.endswith(".html"):
            # Canonicalize legacy .html links to clean URLs.
            qs = self.path[len(raw):]
            self.send_response(301)
            self.send_header("Location", (raw[:-5] or "/") + qs)
            self.end_headers()
            return
        return super().do_GET()

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print("VittVaani frontend running at http://127.0.0.1:%d" % PORT)
    print("Backend expected at http://127.0.0.1:8001  (see js/api.js)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()