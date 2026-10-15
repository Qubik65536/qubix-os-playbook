"""Developer-only Krypton derivatives. Normal deployment uses committed assets."""
import argparse
import hashlib
import json
import unicodedata
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

SOURCE_SHA256 = "6a25353a9584464293d372077a8d2914e33df5e0adb90395c034fd12143f6dc5"
REVISION = "f31794b6e9e65698a062262e2f826f679dcb7070"
CONTROLS = "\x00☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼"
FALLBACKS = {3, 4, 5, 6, 13, 14, 23, 127, 244, 245}


def characters():
    return [CONTROLS[i] if i < 32 else "⌂" if i == 127 else bytes([i]).decode("cp437") for i in range(256)]


def fallback(code):
    """Original geometric forms for ten CP437 symbols absent from upstream Krypton."""
    image = Image.new("L", (8, 20))
    d = ImageDraw.Draw(image)
    if code == 3:
        d.polygon([(1, 7), (3, 7), (4, 9), (5, 7), (7, 7), (7, 10), (4, 14), (1, 10)], fill=255)
    elif code == 4:
        d.polygon([(4, 6), (7, 10), (4, 14), (1, 10)], fill=255)
    elif code in (5, 6):
        if code == 5:
            for box in [(2, 6, 5, 9), (0, 9, 3, 12), (4, 9, 7, 12)]: d.ellipse(box, fill=255)
        else:
            d.polygon([(4, 6), (7, 11), (6, 13), (4, 12), (2, 13), (1, 11)], fill=255)
        d.line([(4, 10), (4, 15)], fill=255)
        d.line([(2, 15), (6, 15)], fill=255)
    elif code in (13, 14):
        d.line([(3, 14), (3, 6), (6, 5), (6, 12)], fill=255)
        d.ellipse((0, 12, 3, 14), fill=255)
        if code == 14: d.ellipse((4, 11, 7, 13), fill=255)
    elif code == 23:
        d.line([(4, 5), (4, 14)], fill=255)
        d.line([(2, 7), (4, 5), (6, 7)], fill=255)
        d.line([(2, 12), (4, 14), (6, 12)], fill=255)
        d.line([(1, 16), (7, 16)], fill=255)
    elif code == 127:
        d.line([(0, 9), (4, 5), (7, 9)], fill=255)
        d.line([(1, 9), (1, 15), (6, 15), (6, 9)], fill=255)
    elif code == 244:
        d.line([(3, 19), (3, 7), (4, 5), (6, 5)], fill=255)
    elif code == 245:
        d.line([(4, 0), (4, 12), (3, 14), (1, 14)], fill=255)
    else:
        raise AssertionError(code)
    return image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Pinned upstream Frozen Regular TTF")
    parser.add_argument("--output", type=Path, default=Path("assets/fonts"))
    args = parser.parse_args()
    assert hashlib.sha256(args.source.read_bytes()).hexdigest() == SOURCE_SHA256, "Unexpected upstream font"
    args.output.mkdir(parents=True, exist_ok=True)
    font = TTFont(args.source, recalcTimestamp=False)
    cmap = font.getBestCmap()
    cp437 = characters()
    assert {i for i, c in enumerate(cp437) if ord(c) not in cmap and i != 0} == FALLBACKS
    requested = set(range(0x20, 0x250)) | set(range(0x300, 0x370)) | set(range(0x2000, 0x2070))
    requested |= {ord(c) for c in cp437} | {0xFFFD}
    options = subset.Options()
    options.recalc_timestamp = False
    options.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14, 16, 17]
    options.name_legacy = True
    options.name_languages = [0x409]
    tool = subset.Subsetter(options=options)
    tool.populate(unicodes=requested & set(cmap))
    tool.subset(font)
    names = {1: "Qubix Boot Mono", 2: "Regular", 3: "QubixBootMono-Regular-1.400-subset",
             4: "Qubix Boot Mono Regular", 6: "QubixBootMono-Regular", 16: "Qubix Boot Mono", 17: "Regular"}
    for record in font["name"].names:
        if record.nameID in names:
            record.string = names[record.nameID].encode(record.getEncoding())
    ttf = args.output / "QubixBootMono-Regular.ttf"
    font.save(ttf, reorderTables=True)
    raster = ImageFont.truetype(str(args.source), 13, layout_engine=ImageFont.Layout.BASIC)
    sheet = Image.new("RGB", (16 * 32, 16 * 56), "#0b121c")
    draw = ImageDraw.Draw(sheet)
    bitmap = bytearray()
    for index, char in enumerate(cp437):
        cell = Image.new("L", (8, 20))
        if index in FALLBACKS:
            cell = fallback(index)
        elif index not in (0, 32, 255):
            ImageDraw.Draw(cell).text((0, 14), char, font=raster, anchor="ls", fill=255)
        cell = cell.point(lambda value: 255 if value >= 100 else 0)
        # A firmware cell has no font leading: join CP437 borders at every cell edge.
        if 0x2500 <= ord(char) <= 0x257F:
            name = unicodedata.name(char)
            left, top, right, bottom = cell.getbbox()
            if "VERTICAL" in name or "UP" in name:
                for x in range(8):
                    if cell.getpixel((x, top)):
                        ImageDraw.Draw(cell).line((x, 0, x, top), fill=255)
            if "VERTICAL" in name or "DOWN" in name:
                for x in range(8):
                    if cell.getpixel((x, bottom - 1)):
                        ImageDraw.Draw(cell).line((x, bottom - 1, x, 19), fill=255)
            if "HORIZONTAL" in name or "LEFT" in name:
                for y in range(20):
                    if cell.getpixel((left, y)):
                        ImageDraw.Draw(cell).line((0, y, left, y), fill=255)
            if "HORIZONTAL" in name or "RIGHT" in name:
                for y in range(20):
                    if cell.getpixel((right - 1, y)):
                        ImageDraw.Draw(cell).line((right - 1, y, 7, y), fill=255)
        for y in range(20):
            bitmap.append(sum((1 << (7-x)) for x in range(8) if cell.getpixel((x, y))))
        x, y = (index % 16) * 32 + 4, (index // 16) * 56 + 4
        sheet.paste("#c9dfef", (x, y), cell.resize((24, 40), Image.Resampling.NEAREST))
        draw.text((x, y + 41), f"{index:02X}", fill="#7894ad")
    assert len(bitmap) == 256 * 20
    binary = args.output / "QubixBootMono-8x20.bin"
    binary.write_bytes(bitmap)
    sheet.save(args.output / "cp437-contact-sheet.png")
    metadata = {"upstream": "https://github.com/githubnext/monaspace", "version": "v1.400",
                "revision": REVISION, "source": "MonaspaceKryptonFrozen-Regular.ttf", "source_sha256": SOURCE_SHA256,
                "license": "OFL-1.1", "family": "Qubix Boot Mono", "bitmap_cell": [8, 20],
                "bitmap_glyphs": 256, "geometric_cp437_fallbacks": sorted(FALLBACKS),
                "subset_codepoints": sorted(font.getBestCmap()),
                "files": [{"filename": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                           "bytes": p.stat().st_size} for p in (ttf, binary, args.output / "OFL.txt")]}
    (args.output / "manifest.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Generated {ttf.stat().st_size} byte TTF subset and {len(bitmap)} byte CP437 bitmap")


if __name__ == "__main__":
    main()
