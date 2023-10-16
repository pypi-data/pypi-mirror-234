
import binascii

from .file import readBinaryFromPath, writeJsonToPath


def diffSources(src1, src2):
    src1_data = readBinaryFromPath(src1)
    src2_data = readBinaryFromPath(src2)

    info = {}

    for i, (data1, data2) in enumerate(zip(src1_data, src2_data)):
        if data1 != data2:
            i_hex = hex(i)

            data1 = data1.to_bytes(1, 'little')
            data2 = data2.to_bytes(1, 'little')

            info[i_hex] = {
                'original': binascii.hexlify(data1).decode(),
                'patched': binascii.hexlify(data2).decode()
            }

    return info


def createDiffAtPath(path1, path2, file):
    diff = diffSources(path1, path2)
    writeJsonToPath(file, diff)
