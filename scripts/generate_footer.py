"""
Generates an ANIMATED pixel-art platformer-style footer (footer.svg) for the
GitHub profile README: sky, drifting clouds, hills, bushes, spinning coins,
a walking pixel hero and a flag at the end. Pure stdlib, no dependencies.
"""
import math

W, H = 800, 180
CELL = 6

SKY_TOP = "#5c94fc"
SKY_BOTTOM = "#a7d8fc"
HILL_BACK = "#3aa832"
HILL_FRONT = "#1c8a3c"
BUSH = "#2fae5f"
DIRT = "#a0522d"
DIRT_DARK = "#7a3b1e"
GRASS_TOP = "#3aa832"
COIN = "#ffd23f"
COIN_DARK = "#e0a800"
HERO_SHIRT = "#2aa9a0"
HERO_SKIN = "#f2c48b"
HERO_PANTS = "#3a3a5c"
FLAG_POLE = "#e5e5e5"
FLAG_CLOTH = "#ff5a5f"


def px_rect(x, y, w, h, color, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" {extra}/>'


def cloud(x, y, scale=1.0):
    c = CELL * scale
    parts = []
    blocks = [
        (0, 1, 4, 1), (1, 0, 3, 1),
        (4, 1, 3, 1), (5, 0, 2, 1),
        (0, 2, 7, 1),
    ]
    for bx, by, bw, bh in blocks:
        parts.append(px_rect(x + bx * c, y + by * c, bw * c, bh * c, "#ffffff"))
    return "".join(parts)


def hill(x, base_y, width_cells, height_cells, color):
    parts = []
    c = CELL
    for i in range(height_cells):
        row_w = width_cells - i * 2
        if row_w <= 0:
            break
        row_x = x + i * c
        parts.append(px_rect(row_x, base_y - (i + 1) * c, row_w * c, c, color))
    return "".join(parts)


def bush(x, base_y):
    c = CELL
    parts = [
        px_rect(x, base_y - c, 3 * c, c, BUSH),
        px_rect(x + c, base_y - 2 * c, c, c, BUSH),
    ]
    return "".join(parts)


def coin(cx, cy, begin):
    """A small square coin that does a squash 'spin' loop + gentle bob."""
    c = CELL
    return f'''
    <g transform="translate({cx},{cy})">
      <animateTransform attributeName="transform" type="translate"
        additive="sum" values="0,0; 0,-4; 0,0" keyTimes="0;0.5;1"
        dur="1.1s" begin="{begin}s" repeatCount="indefinite"/>
      <rect x="{-c}" y="{-c}" width="{2*c}" height="{2*c}" fill="{COIN}">
        <animateTransform attributeName="transform" type="scale"
          values="1,1; 0.15,1; 1,1" keyTimes="0;0.5;1"
          dur="1.1s" begin="{begin}s" repeatCount="indefinite"
          additive="sum"/>
      </rect>
      <rect x="{-c/2}" y="{-c/2}" width="{c}" height="{c}" fill="{COIN_DARK}"/>
    </g>'''


def ground(y_top):
    parts = []
    c = CELL
    cols = W // c
    for col in range(cols):
        x = col * c
        parts.append(px_rect(x, y_top, c, c, GRASS_TOP))
        for row in range(1, (H - y_top) // c):
            shade = DIRT if (col + row) % 2 == 0 else DIRT_DARK
            parts.append(px_rect(x, y_top + row * c, c, c, shade))
    return "".join(parts)


def hero(begin, duration):
    """A small pixel hero that bobs while walking across the whole width."""
    c = CELL
    body = f'''
    <rect x="{-2*c}" y="{-6*c}" width="{4*c}" height="{2*c}" fill="{HERO_SKIN}"/>
    <rect x="{-2*c}" y="{-4*c}" width="{4*c}" height="{2*c}" fill="{HERO_SHIRT}"/>
    <rect x="{-2*c}" y="{-2*c}" width="{4*c}" height="{2*c}" fill="{HERO_PANTS}"/>
    '''
    return f'''
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="{-40},0; {W+40},0" keyTimes="0;1"
        dur="{duration}s" begin="{begin}s" repeatCount="indefinite" calcMode="linear"/>
      <g>
        <animateTransform attributeName="transform" type="translate"
          additive="sum" values="0,0; 0,-3; 0,0; 0,-3; 0,0" keyTimes="0;0.25;0.5;0.75;1"
          dur="0.5s" begin="0s" repeatCount="indefinite"/>
        {body}
      </g>
    </g>'''


def scrolling_layer(content_fn, y, speed, *args):
    """Draws content twice side by side and loops translateX by -W for a seamless scroll."""
    g1 = content_fn(0, y, *args)
    g2 = content_fn(W, y, *args)
    return f'''
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="0,0; {-W},0" keyTimes="0;1" dur="{speed}s"
        repeatCount="indefinite" calcMode="linear"/>
      {g1}{g2}
    </g>'''


def clouds_layer():
    def draw(xoff, y):
        return cloud(xoff + 40, y, 1.1) + cloud(xoff + 260, y + 20, 0.8) + cloud(xoff + 520, y + 5, 1.3)
    return scrolling_layer(draw, 18, 26)


def build_svg():
    ground_y = H - 5 * CELL

    sky = f'''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{SKY_TOP}"/>
      <stop offset="100%" stop-color="{SKY_BOTTOM}"/>
    </linearGradient>'''

    hills_back = hill(20, ground_y, 26, 8, HILL_BACK) + hill(420, ground_y, 30, 9, HILL_BACK) + hill(660, ground_y, 22, 7, HILL_BACK)
    hills_front = hill(-20, ground_y, 22, 6, HILL_FRONT) + hill(200, ground_y, 26, 7, HILL_FRONT) + hill(560, ground_y, 24, 6, HILL_FRONT) + hill(740, ground_y, 20, 5, HILL_FRONT)

    bushes = bush(90, ground_y) + bush(340, ground_y) + bush(600, ground_y) + bush(720, ground_y)

    coins = "".join(coin(cx, ground_y - 40, i * 0.25) for i, cx in enumerate([160, 320, 480, 640]))

    flag_x, flag_base = 750, ground_y
    flag = f'''
    <rect x="{flag_x}" y="{flag_base - 60}" width="4" height="60" fill="{FLAG_POLE}"/>
    <g transform="translate({flag_x+4},{flag_base-58})">
      <polygon points="0,0 22,6 0,12" fill="{FLAG_CLOTH}">
        <animateTransform attributeName="transform" type="skewX"
          values="0;10;0;-6;0" keyTimes="0;0.3;0.5;0.8;1"
          dur="1.6s" repeatCount="indefinite"/>
      </polygon>
    </g>'''

    sun = f'''
    <circle cx="740" cy="34" r="18" fill="#ffe066">
      <animate attributeName="r" values="18;20;18" dur="2.4s" repeatCount="indefinite"/>
    </circle>'''

    return f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges">
  <defs>{sky}</defs>
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  {sun}
  {clouds_layer()}
  {hills_back}
  {hills_front}
  {bushes}
  {ground(ground_y)}
  {coins}
  {flag}
  {hero(0, 9)}
</svg>'''


if __name__ == "__main__":
    with open("footer.svg", "w") as f:
        f.write(build_svg())
    print("footer.svg generated")
