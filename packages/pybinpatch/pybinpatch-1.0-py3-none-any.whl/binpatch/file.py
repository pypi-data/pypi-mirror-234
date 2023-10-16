
import json


def readBinaryFromPath(path):
    with open(path, 'rb') as f:
        return bytearray(f.read())


def writeBinaryToPath(path, data):
    with open(path, 'wb') as f:
        f.write(data)


def readJsonAtPath(path):
    with open(path) as f:
        return json.load(f)


def writeJsonToPath(path, data, indent=2):
    with open(path, 'w') as f:
        json.dump(data, f, indent=indent)
