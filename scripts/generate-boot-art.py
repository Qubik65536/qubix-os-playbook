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
    body = '''<defs>
      <linearGradient id="night" x2="1" y2="1"><stop stop-color="#080f18"/><stop offset="1" stop-color="#1c3349"/></linearGradient>
      <radialGradient id="glow"><stop stop-color="#56728b" stop-opacity=".18"/><stop offset="1" stop-color="#56728b" stop-opacity="0"/></radialGradient>
    </defs>
    <rect width="1920" height="1080" fill="url(#night)"/>
    <ellipse cx="1535" cy="490" rx="650" ry="630" fill="url(#glow)"/>
    <g fill="none" stroke="#7195b2" stroke-width="1" opacity=".075">
      <path d="M880 0L1920 600M680 0L1920 716M480 0L1920 831M280 0L1920 946"/>
      <path d="M1920 0L880 600M1920 116L980 658M1920 232L1080 716M1920 348L1180 774"/>
    </g>
    <g fill="none" stroke="#789bb8" stroke-width="2" stroke-linejoin="round" opacity=".16">
      <path d="M1450 230L1680 363L1450 496L1220 363Z M1220 363V629L1450 762L1680 629V363 M1450 496V762"/>
      <path d="M1450 290L1628 393 M1272 393V599L1450 702" opacity=".55"/>
    </g>
    <path d="M80 999H155 M80 1007H120" stroke="#56728b" stroke-width="2"/>
    '''
    body += lettering("QUBIX OS", 1498, 983, 28, "#b6cee1", 2)
    body += lettering("BOOT / RECOVER / CONTINUE", 1498, 1008, 9, "#7894ad", .8)
    wallpaper = boot / "wallpaper.svg"
    wallpaper.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">' + body + '</svg>\n')
    export(wallpaper, boot / "wallpaper.png")

    watermark = ROOT / "assets/plymouth/watermark.svg"
    watermark.write_text('''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="240" height="72" viewBox="0 0 240 72">
    <defs><filter id="steel" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values=".16 .54 .06 0 .04 .2 .67 .07 0 .05 .24 .8 .08 0 .06 0 0 0 1 0"/></filter></defs>
    <image xlink:href="../branding/logo.svg" x="0" y="0" width="72" height="72" filter="url(#steel)"/>
    ''' + lettering("QUBIX OS", 78, 37, 25, "#d5e8f6", 1.5)
    + lettering("PLAYBOOK", 80, 54, 9, "#789bb8", 2)
    + '<path d="M80 64H122" stroke="#56728b" stroke-width="2"/></svg>\n')
    export(watermark, ROOT / "assets/plymouth/theme/watermark.png")

    # Original vector animation: a quiet track and rotating ice-blue arc.
    spinner = ROOT / "assets/plymouth/spinner.svg"
    template = '''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <circle cx="16" cy="16" r="12" fill="none" stroke="#56728b" stroke-opacity=".3" stroke-width="2"/>
      <path transform="rotate(ANGLE 16 16)" d="M16 4A12 12 0 1 1 4 16" fill="none" stroke="#b2d2ea" stroke-width="2" stroke-linecap="round"/>
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
