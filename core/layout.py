import math


A4_WIDTH = 794
A4_HEIGHT = 1123

CENTER_X = A4_WIDTH // 2
CENTER_Y = 420

BRANCH_RADIUS = 280


def calculate_positions(data):
    branches = data.get("branches", [])
    n = len(branches)
    if n == 0:
        return []

    angle_step = 2 * math.pi / n
    start_angle = -math.pi / 2

    positions = []
    for i, branch in enumerate(branches):
        angle = start_angle + i * angle_step
        bx = CENTER_X + BRANCH_RADIUS * math.cos(angle)
        by = CENTER_Y + BRANCH_RADIUS * math.sin(angle)
        side = "right" if math.cos(angle) >= 0 else "left"
        positions.append({
            "title": branch.get("title", ""),
            "points": branch.get("points", []),
            "x": bx,
            "y": by,
            "cx": CENTER_X,
            "cy": CENTER_Y,
            "angle": angle,
            "side": side,
            "index": i,
        })

    return positions


def layout_info():
    return {
        "width": A4_WIDTH,
        "height": A4_HEIGHT,
        "cx": CENTER_X,
        "cy": CENTER_Y,
        "radius": BRANCH_RADIUS,
    }
