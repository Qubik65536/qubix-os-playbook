"""Check composed PNG pixels without third-party image libraries or image modification."""
from pathlib import Path
import json
import struct
import sys
import zlib


def pixel(path, x, y):
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    compressed = bytearray()
    offset = 8
    while offset < len(data):
        size = struct.unpack('>I', data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + size]
        if kind == b'IHDR':
            width, height, depth, colour, _, _, interlace = struct.unpack('>IIBBBBB', payload)
            assert depth == 8 and colour in (2, 6) and interlace == 0
        if kind == b'IDAT':
            compressed.extend(payload)
        offset += size + 12
    assert x < width and y < height
    channels = 4 if colour == 6 else 3
    stride = width * channels
    raw = zlib.decompress(compressed)
    previous = bytearray(stride)
    for row in range(y + 1):
        start = row * (stride + 1)
        method = raw[start]
        scan = bytearray(raw[start + 1:start + 1 + stride])
        for index in range(stride):
            left = scan[index - channels] if index >= channels else 0
            up = previous[index]
            diagonal = previous[index - channels] if index >= channels else 0
            if method == 0:
                predictor = 0
            elif method == 1:
                predictor = left
            elif method == 2:
                predictor = up
            elif method == 3:
                predictor = (left + up) // 2
            else:
                assert method == 4
                estimate = left + up - diagonal
                differences = [abs(estimate - value) for value in (left, up, diagonal)]
                predictor = (left, up, diagonal)[differences.index(min(differences))]
            scan[index] = (scan[index] + predictor) & 255
        previous = scan
    return tuple(previous[x * channels:x * channels + 3])


def main():
    root = Path(sys.argv[1])
    values = {name: pixel(root / (name + '.png'), 100, 400)
              for name in ('before-red', 'before-blue', 'after-red', 'after-blue')}
    assert values['before-red'] == values['before-blue'], values
    assert values['after-red'][0] > values['after-blue'][0] + 30, values
    assert values['after-blue'][2] > values['after-red'][2] + 30, values
    print(json.dumps({'terminal_interior_rgb': values, 'scene_transparency_verified': True}))


if __name__ == '__main__':
    main()
