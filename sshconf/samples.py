"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def value(text, host, key, files=None):
    config = core.parse(text, files or {}, core.Counter())
    return config.get(host, key, core.Counter())


def run(name):
    if name == "first":
        text = "Host *.example.com\n  User alice\nHost web.example.com\n  User bob\n"
        _line({"user": value(text, "web.example.com", "User")})
        return 0
    if name == "negate":
        text = "Host *.example.com !bad.example.com\n  User alice\n"
        _line({"user": value(text, "bad.example.com", "User")})
        return 0
    if name == "case":
        text = "Host web\n  user alice\n"
        _line({"user": value(text, "web", "User")})
        return 0
    if name == "include":
        text = "Include extra.conf\nHost web\n  Port 2222\n"
        files = {"extra.conf": "Host web\n  User alice\n"}
        _line({"user": value(text, "web", "User", files)})
        return 0
    if name == "work":
        lines = []
        for i in range(800):
            lines.append("Host h%04d" % i)
            lines.append("  User u%04d" % i)
        config = core.parse("\n".join(lines) + "\n", {}, core.Counter())
        counter = core.Counter()
        for i in range(800):
            config.get("h%04d" % i, "User", counter)
        _line({"blocks": 800, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
