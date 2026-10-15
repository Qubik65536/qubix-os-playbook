"""Export code-native boot artwork with outlined Krypton-derived lettering."""
from pathlib import Path
import subprocess
import tempfile

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
FONT = TTFont(ROOT / "assets/fonts/QubixBootMono-Regular.ttf")
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
EM = FONT["head"].unitsPerEm


def lettering(text, x, y, size, color, tracking=0):
    paths = []
    for char in text:
        name = CMAP[ord(char)]
        pen = SVGPathPen(GLYPHS)
        GLYPHS[name].draw(pen)
        paths.append(f'<path transform="translate({x:.4f} {y}) scale({size / EM:.8f} {-size / EM:.8f})" d="{pen.getCommands()}"/>')
        x += FONT["hmtx"][name][0] * size / EM + tracking
    return f'<g fill="{color}">' + "".join(paths) + "</g>"


def export(source, destination):
    subprocess.run(["inkscape", "--export-area-page", "--export-type=png",
                    "--export-filename=" + str(destination), str(source)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main():
    boot = ROOT / "assets/boot"
    boot.mkdir(exist_ok=True)
    # Reuse the canonical detailed cube; the native menu supplies its own heading.
    body = '''<image xmlns:xlink="http://www.w3.org/1999/xlink"
      xlink:href="../wallpaper/qubix.png" width="1920" height="1080"/>'''
    wallpaper = boot / "wallpaper.svg"
    wallpaper.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">' + body + '</svg>\n')
    export(wallpaper, boot / "wallpaper.png")

    watermark = ROOT / "assets/plymouth/watermark.svg"
    watermark.write_text('''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="240" height="72" viewBox="0 0 240 72">
    <defs><filter id="steel" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values=".16 .54 .06 0 .24 .2 .67 .07 0 .29 .24 .8 .08 0 .34 0 0 0 1 0"/></filter></defs>
    <image xlink:href="../branding/logo.svg" x="0" y="0" width="72" height="72" filter="url(#steel)"/>
    ''' + lettering("QUBIX OS", 78, 45, 25, "#f4f8fc", 1.5) + '</svg>\n')
    export(watermark, ROOT / "assets/plymouth/theme/watermark.png")

    # Original vector animation: a quiet track and rotating ice-blue arc.
    spinner = ROOT / "assets/plymouth/spinner.svg"
    template = '''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <circle cx="16" cy="16" r="12" fill="none" stroke="#7898b4" stroke-opacity=".45" stroke-width="2"/>
      <path transform="rotate(ANGLE 16 16)" d="M16 4A12 12 0 1 1 4 16" fill="none" stroke="#edf6ff" stroke-width="2" stroke-linecap="round"/>
    </svg>\n'''
    spinner.write_text(template.replace("ANGLE", "0"))
    with tempfile.TemporaryDirectory(prefix="qubix-boot-art.") as directory:
        frame = Path(directory) / "frame.svg"
        for index in range(30):
            frame.write_text(template.replace("ANGLE", str(index * 12)))
            export(frame, ROOT / f"assets/plymouth/theme/throbber-{index + 1:04}.png")
    print("Exported midnight wallpaper, outlined Qubix wordmark and 30 native spinner frames")


if __name__ == "__main__":
    main()
