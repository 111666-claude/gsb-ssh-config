"""解析 SSH 配置并按主机取值。"""

import fnmatch


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


class Block:
    def __init__(self, patterns, options):
        self.patterns = patterns
        self.options = options


class Config:
    def __init__(self, blocks):
        self.blocks = blocks

    def get(self, host, key, counter):
        value = ""
        for block in self.blocks:
            counter.scanned += 1
            if not _host_matches(block.patterns, host):
                continue
            for name, item in block.options:
                counter.scanned += 1
                if name == key:
                    value = item
        return value


def _host_matches(patterns, host):
    for pattern in patterns:
        if fnmatch.fnmatchcase(host, pattern):
            return True
    return False


def parse(text, files, counter):
    blocks = []
    current = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        counter.scanned += 1
        parts = line.split()
        key = parts[0]
        if key == "Host":
            current = Block(list(parts[1:]), [])
            blocks.append(current)
            continue
        if current is None:
            continue
        current.options.append((key, " ".join(parts[1:])))
    return Config(blocks)
