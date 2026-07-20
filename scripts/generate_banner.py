"""
Generates an animated PIXEL-STYLE fireworks banner (banner.svg) for the GitHub
profile README. Pure stdlib, no dependencies - runs as-is in GitHub Actions.
"""
import math

W, H = 800, 200
GRID = 8  # pixel "block" size -> everything snaps to this for a chunky 8-bit look
NAME = "RAJAN AHMADY"
SUBTITLE = "FULL-STACK DEVELOPER * CS STUDENT"

# retro game palette (PICO-8 inspired)
BG_TOP = "#1d1533"
BG_BOTTOM = "#2b1d4a"
PALETTE = ["#ff004d", "#29adff", "#ffec27", "#00e756", "#ff77a8", "#7ee8fa"]

# (center x, center y, color, start delay in seconds)
BURSTS = [
    (128, 56, PALETTE[0], 0.0),
    (248, 96, PALETTE[1], 0.9),
    (400, 40, PALETTE[2], 1.8),
    (552, 88, PALETTE[3], 0.5),
    (672, 56, PALETTE[4], 1.4),
    (616, 128, PALETTE[5], 2.3),
    (184, 128, PALETTE[1], 2.7),
]

STARS = [(40, 16), (88, 152), (296, 16), (480, 160), (712, 24), (760, 144), (16, 96), (744, 88)]


def snap(v):
    return round(v / GRID) * GRID


def burst(cx, cy, color, begin, dur=2.4, n=10, r=68):
    """A ring of small square 'pixels' that jump outward in discrete steps."""
    parts = []
    steps = 5  # number of discrete jumps -> chunky retro motion
    for i in range(n):
        angle = (2 * math.pi / n) * i
        positions = []
        for s in range(steps + 1):
            t = s / steps
            dx = snap(math.cos(angle) * r * t)
            dy = snap(math.sin(angle) * r * t)
            positions.append(f"{dx},{dy}")
        values = "; ".join(positions)
        key_times = ";".join(f"{s / steps:.3f}" for s in range(steps + 1))

        parts.append(f'''
    <rect x="{cx - 3}" y="{cy - 3}" width="6" height="6" fill="{color}" shape-rendering="crispEdges">
      <animateTransform attributeName="transform" type="translate"
        values="{values}" keyTimes="{key_times}"
        dur="{dur}s" begin="{begin}s" repeatCount="indefinite" calcMode="discrete"/>
      <animate attributeName="opacity" values="1;1;1;0;0" keyTimes="0;0.4;0.7;0.85;1"
        dur="{dur}s" begin="{begin}s" repeatCount="indefinite" calcMode="discrete"/>
    </rect>''')

    # bright flash pixel at the burst origin
    parts.append(f'''
    <rect x="{cx - 4}" y="{cy - 4}" width="8" height="8" fill="#ffffff" shape-rendering="crispEdges">
      <animate attributeName="opacity" values="0;0;1;0" keyTimes="0;0.02;0.08;0.25"
        dur="{dur}s" begin="{begin}s" repeatCount="indefinite" calcMode="discrete"/>
    </rect>''')
    return "\n".join(parts)


def pixel_text(x, y, text, size, fill, shadow=None, shadow_offset=4):
    """Blocky retro text: monospace font + a hard-offset duplicate as an 8-bit 'shadow'."""
    parts = []
    if shadow:
        parts.append(
            f'<text x="{x + shadow_offset}" y="{y + shadow_offset}" text-anchor="middle" '
            f'font-family="Courier New, monospace" font-weight="700" font-size="{size}" '
            f'letter-spacing="4" fill="{shadow}">{text}</text>'
        )
    parts.append(
        f'<text x="{x}" y="{y}" text-anchor="middle" '
        f'font-family="Courier New, monospace" font-weight="700" font-size="{size}" '
        f'letter-spacing="4" fill="{fill}">{text}</text>'
    )
    return "\n".join(parts)


def build_svg():
    body = "\n".join(burst(cx, cy, c, b) for cx, cy, c, b in BURSTS)
    stars = "\n".join(
        f'    <rect x="{x}" y="{y}" width="3" height="3" fill="#ffffff" shape-rendering="crispEdges"/>'
        for x, y in STARS
    )
    title = pixel_text(400, 104, NAME, 42, "#ffffff", shadow="#7ee8fa", shadow_offset=4)
    subtitle = pixel_text(400, 136, SUBTITLE, 13, "#ffec27")

    return f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges">
  <defs>
    <linearGradient id="sky" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{BG_TOP}"/>
      <stop offset="100%" stop-color="{BG_BOTTOM}"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#sky)"/>

  <g opacity="0.7">
{stars}
  </g>

{body}

  <!-- scanline / pixel-grid overlay for CRT feel -->
  <g opacity="0.05" fill="#000000">
    {"".join(f'<rect x="0" y="{y}" width="{W}" height="1"/>' for y in range(0, H, 4))}
  </g>

{title}
{subtitle}
</svg>'''


if __name__ == "__main__":
    with open("banner.svg", "w") as f:
        f.write(build_svg())
    print("banner.svg generated")
