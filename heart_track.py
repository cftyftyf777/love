# -*- coding: utf-8 -*-
"""
爱心轨迹 · 文字框版
运行后会显示一条由许多文字框铺成的爱心轨迹：
一只光点沿着爱心轨迹移动，沿途铺下一枚枚文字框，
每个文字框里轮流显示一句话。仅依赖 Python 标准库（turtle），无需安装第三方库。
"""

import math
import time
import turtle

# 文字框里的祝福语（会依次循环出现）
PHRASES = [
    "多喝水",
    "好好爱自己",
    "好好吃饭",
    "保持好心态",
    "拒绝内耗",
    "顺顺利利",
    "别熬夜",
]

# 文字框配色（粉红 / 珊瑚 / 玫瑰色系，循环使用）
BOX_COLORS = [
    "#ff5d8f", "#ff7aa2", "#ff4d6d", "#ff8fab",
    "#f25f5c", "#ff6b8a", "#e63946",
]

BG_COLOR = "#1a1a2e"        # 深色背景
OUTLINE_COLOR = "#3d2c3d"   # 淡淡的爱心轮廓
CURSOR_COLOR = "#ffb3c6"    # 移动的光点

HEART_SCALE = 14            # 爱心整体大小
BOX_COUNT = 34              # 文字框数量
FONT_SIZE = 13              # 文字字号
TRACE_STEPS = 480           # 光点轨迹的平滑步数


def heart_points(n=720):
    """用经典心形参数方程生成心形轮廓上的点。"""
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x = 16 * math.sin(t) ** 3
        y = (13 * math.cos(t) - 5 * math.cos(2 * t)
             - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((x * HEART_SCALE, y * HEART_SCALE))
    return pts


def resample(points, count):
    """按弧长均匀重采样，让文字框 / 轨迹点分布更均匀。"""
    cum = [0.0]
    for i in range(len(points) - 1):
        cum.append(cum[-1] + math.dist(points[i], points[i + 1]))
    total = cum[-1]
    out = []
    j = 0
    for k in range(count):
        target = total * k / (count - 1)
        while j < len(cum) - 1 and cum[j + 1] < target:
            j += 1
        if j >= len(cum) - 1:
            out.append(points[-1])
            continue
        seg = cum[j + 1] - cum[j]
        ratio = (target - cum[j]) / seg if seg else 0.0
        x = points[j][0] + (points[j + 1][0] - points[j][0]) * ratio
        y = points[j][1] + (points[j + 1][1] - points[j][1]) * ratio
        out.append((x, y))
    return out


def rounded_rect(t, w, h, r):
    """以当前位置为左下角，顺时针绘制圆角矩形。"""
    t.penup()
    x, y = t.position()
    t.goto(x + r, y)
    t.pendown()
    t.forward(w - 2 * r)
    t.circle(r, 90)
    t.forward(h - 2 * r)
    t.circle(r, 90)
    t.forward(w - 2 * r)
    t.circle(r, 90)
    t.forward(h - 2 * r)
    t.circle(r, 90)
    t.penup()


def draw_text_box(t, cx, cy, text, color):
    """在 (cx, cy) 处画一个胶囊形文字框，并居中写入文字。"""
    size = FONT_SIZE
    pad = size * 0.8
    w = size * len(text) * 1.15 + pad * 2
    h = size * 1.9
    r = h / 2

    t.penup()
    t.goto(cx - w / 2, cy - h / 2)
    t.color(color)
    t.fillcolor(color)
    t.begin_fill()
    rounded_rect(t, w, h, r)
    t.end_fill()

    t.goto(cx, cy - size * 0.36)
    t.color("white")
    t.write(text, align="center", font=("Microsoft YaHei", size, "bold"))


def main():
    screen = turtle.Screen()
    screen.setup(820, 820)
    screen.bgcolor(BG_COLOR)
    screen.title("爱心轨迹 · 好好爱自己")
    screen.tracer(0)

    dense = heart_points()
    trace = resample(dense, TRACE_STEPS)
    box_pts = resample(dense, BOX_COUNT)

    # 1) 先画一条淡淡的爱心轮廓，作为“轨迹”背景
    outline = turtle.Turtle()
    outline.hideturtle()
    outline.speed(0)
    outline.pensize(1)
    outline.color(OUTLINE_COLOR)
    outline.penup()
    outline.goto(trace[0])
    outline.pendown()
    for x, y in trace[1:]:
        outline.goto(x, y)
    outline.penup()
    outline.hideturtle()

    # 2) 光点沿着轨迹移动，边移动边铺下文字框
    cursor = turtle.Turtle()
    cursor.shape("circle")
    cursor.shapesize(0.5, 0.5)
    cursor.color(CURSOR_COLOR)
    cursor.penup()
    cursor.goto(trace[0])

    drawer = turtle.Turtle()
    drawer.hideturtle()
    drawer.speed(0)

    drawn = 0
    total = len(trace)
    for i, (x, y) in enumerate(trace):
        cursor.goto(x, y)
        target = int((i + 1) * BOX_COUNT / total)
        while drawn < target and drawn < BOX_COUNT:
            bx, by = box_pts[drawn]
            text = PHRASES[drawn % len(PHRASES)]
            color = BOX_COLORS[drawn % len(BOX_COLORS)]
            draw_text_box(drawer, bx, by, text, color)
            drawn += 1
        screen.update()
        time.sleep(0.008)

    cursor.hideturtle()
    # 全部铺完后，窗口保持打开
    screen.mainloop()


if __name__ == "__main__":
    main()
