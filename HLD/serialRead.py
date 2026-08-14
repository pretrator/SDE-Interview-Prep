import json
import time

def append_entry(path, entry):
    record = {
        "timestamp": time.time(),
        "data": entry
    }

    with open(path, "ab") as f:
        data = (json.dumps(record) + "\n").encode()
        f.write(data)
        f.flush()


def update_at_offset(path, offset, data):
    with open(path, "r+b") as f:
        f.seek(offset)
        f.write(data)
        f.flush()


Append only log
Journal 