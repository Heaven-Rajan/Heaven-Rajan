"""
Generates an animated fireworks banner (banner.svg) for the GitHub profile README.
Pure stdlib, no dependencies - runs as-is in GitHub Actions.
"""
import math

W, H = 800, 200
NAME = "Rajan Ahmady"
SUBTITLE = "Full-Stack Developer &#183; CS Student"
COLORS = ["#f7768e", "#7aa2f7", "#bb9af7", "#7dcfff", "#e0af68"]

# (center x, center y, color, start delay in seconds)
BURSTS = [
    (130, 60, COLORS[0], 0.0),
    (250, 100, COLORS[1], 0.9),
    (400, 45, COLORS[2], 1.8),
    (550, 90, COLORS[3], 0.5),
    (670, 55, COLORS[4], 1.4),
    (620, 130, COLORS[0], 2.3),
    (190, 130, COLORS[1], 2.7),
]

STARS = [(40, 20), (90, 150), (300, 20), (480, 160), (710, 25), (760, 140), (20, 100)]


def burst(cx, cy, color, begin, dur=2.0, n=14, r=70):
    parts = []
    for i in range(n):
        angle = (2 * math.pi / n) * i
        dx = round(math.cos(angle) * r, 1)
        dy = round(math.sin(angle) * r, 1)
        parts.append(f'''
    <circle cx="{cx}" cy="{cy}" r="2.4" fill="{color}">
      <animateTransform attributeName="transform" type="translate"
        values="0,0; {dx},{dy}" keyTimes="0;1"
        dur="{dur}s" begin="{begin}s" repeatCount="indefinite"
        calcMode="spline" keySplines="0.15 0.65 0.35 1"/>
      <animate attributeName="opacity" values="1;1;0" keyTimes="0;0.55;1"
        dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
      <animate attributeName="r" values="2.6;1.6;0.4" keyTimes="0;0.6;1"
        dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
    </circle>''')
    parts.append(f'''
    <circle cx="{cx}" cy="{cy}" r="1" fill="#ffffff">
      <animate attributeName="opacity" values="0;0;1;0" keyTimes="0;0.02;0.08;0.3"
        dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
      <animate attributeName="r" values="1;14;1" keyTimes="0;0.08;0.3"
        dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
    </circle>''')
    return "\n".join(parts)


def build_svg():
    body = "\n".join(burst(cx, cy, c, b) for cx, cy, c, b in BURSTS)
    stars = "\n".join(f'    <circle cx="{x}" cy="{y}" r="1"/>' for x, y in STARS)

    return f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sky" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0d0e17"/>
      <stop offset="100%" stop-color="#1a1b27"/>
    </linearGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#sky)"/>

  <g fill="#ffffff" opacity="0.5">
{stars}
  </g>

  <g filter="url(#glow)">
{body}
  </g>

  <text x="400" y="108" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
        font-size="46" font-weight="700" fill="#ffffff">{NAME}</text>
  <text x="400" y="140" text-anchor="middle" font-family="Fira Code, monospace"
        font-size="16" fill="#e6e6f0" opacity="0.85">{SUBTITLE}</text>
</svg>'''


if __name__ == "__main__":
    with open("banner.svg", "w") as f:
        f.write(build_svg())
    print("banner.svg generated")
