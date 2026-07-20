"""
Generates a pixel-art footer scene (footer.svg) for the GitHub profile README:
sunset sky, a castle silhouette, a rainbow arc, sunflowers and grass.
Pure stdlib, no dependencies - runs as-is in GitHub Actions.
"""
import math

W, H = 800, 170
CELL = 8
COLS, ROWS = W // CELL, H // CELL  # 100 x 21

# --- palette -----------------------------------------------------------
SKY_BANDS = ["#2b1055", "#4a1a6c", "#7b2d6e", "#b8416b", "#e8735a", "#f4a95a"]
RAINBOW = ["#ff004d", "#ff9d2f", "#ffec27", "#00e756", "#29adff", "#8b5cf6"]
CASTLE = "#1d1533"
CASTLE_LIGHT = "#2e2350"
GRASS_A = "#0a3d2e"
GRASS_B = "#0d4d3a"
STEM = "#1f8a4c"
LEAF = "#2fae5f"
PETAL = "#ffd23f"
PETAL_DARK = "#ffb703"
CENTER_SEED = "#7a3b12"

grid = {}  # (col, row) -> color


def set_cell(c, r, color):
    if 0 <= c < COLS and 0 <= r < ROWS:
        grid[(c, r)] = color


def sky():
    band_h = ROWS / len(SKY_BANDS)
    for r in range(ROWS):
        color = SKY_BANDS[min(int(r / band_h), len(SKY_BANDS) - 1)]
        for c in range(COLS):
            set_cell(c, r, color)


def castle(cx_col, base_row):
    """Simple blocky castle silhouette, centered at cx_col, sitting on base_row."""
    towers = [
        (cx_col - 11, base_row - 7, 4),
        (cx_col - 4, base_row - 10, 5),
        (cx_col + 3, base_row - 8, 4),
        (cx_col + 9, base_row - 6, 3),
    ]
    for tx, ttop, theight in towers:
        for r in range(ttop, base_row):
            for dx in range(4):
                set_cell(tx + dx, r, CASTLE)
        # crenellations
        for dx in (0, 2):
            set_cell(tx + dx, ttop - 1, CASTLE)
        # little window
        if theight > 4:
            set_cell(tx + 1, ttop + 2, CASTLE_LIGHT)
            set_cell(tx + 2, ttop + 2, CASTLE_LIGHT)
    # connecting wall
    for c in range(cx_col - 14, cx_col + 14):
        set_cell(c, base_row - 3, CASTLE)
        set_cell(c, base_row - 2, CASTLE)
    for c in range(cx_col - 14, cx_col + 14, 3):
        set_cell(c, base_row - 4, CASTLE)


def rainbow(cx_col, cy_row, r_outer_cells, band_w):
    cx_px = cx_col * CELL + CELL / 2
    cy_px = cy_row * CELL + CELL / 2
    r_outer_px = r_outer_cells * CELL
    band_px = band_w * CELL
    r_inner_total = r_outer_px - band_px * len(RAINBOW)

    for c in range(COLS):
        for r in range(ROWS):
            px = c * CELL + CELL / 2
            py = r * CELL + CELL / 2
            if py > cy_px:
                continue  # only upper half (the arch)
            dist = math.hypot(px - cx_px, py - cy_px)
            if dist > r_outer_px or dist < r_inner_total:
                continue
            band_idx = int((r_outer_px - dist) / band_px)
            band_idx = min(band_idx, len(RAINBOW) - 1)
            set_cell(c, r, RAINBOW[band_idx])


def ground(row_start):
    for r in range(row_start, ROWS):
        for c in range(COLS):
            color = GRASS_A if (c + r) % 2 == 0 else GRASS_B
            set_cell(c, r, color)


def sunflower(cx_col, base_row, h=6):
    # stem
    for r in range(base_row - h, base_row):
        set_cell(cx_col, r, STEM)
    # leaves
    set_cell(cx_col - 1, base_row - 2, LEAF)
    set_cell(cx_col - 2, base_row - 2, LEAF)
    set_cell(cx_col + 1, base_row - 3, LEAF)
    set_cell(cx_col + 2, base_row - 3, LEAF)
    # flower head (petals in a ring + dark center)
    hy = base_row - h - 1
    petal_offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    for dx, dy in petal_offsets:
        color = PETAL if (dx + dy) % 2 == 0 else PETAL_DARK
        set_cell(cx_col + dx, hy + dy, color)
    set_cell(cx_col, hy, CENTER_SEED)


def build_svg():
    sky()
    castle(cx_col=50, base_row=13)
    rainbow(cx_col=50, cy_row=19, r_outer_cells=34, band_w=2)
    ground(row_start=18)
    for cx in (18, 30, 68, 80):
        sunflower(cx, base_row=ROWS - 1, h=5 + (cx % 3))

    rects = []
    for (c, r), color in sorted(grid.items(), key=lambda kv: (kv[1], kv[0][1], kv[0][0])):
        rects.append(f'<rect x="{c*CELL}" y="{r*CELL}" width="{CELL}" height="{CELL}" fill="{color}"/>')

    return f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges">
{"".join(rects)}
</svg>'''


if __name__ == "__main__":
    with open("footer.svg", "w") as f:
        f.write(build_svg())
    print("footer.svg generated")
