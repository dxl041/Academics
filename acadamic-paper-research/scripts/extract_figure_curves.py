#!/usr/bin/env python3
"""从位图曲线图（论文里的 PNG/JPG 图）里读出各序列的数值——纯像素分析，无 OCR。

用途：论文/审稿意见只给出「图上的曲线」，而你需要在正文里引用具体数值，
或者需要核对某个数字（例：审稿人说 "at 60% load it is much more than 5.8% worse"）。

方法：
  1) 用两个已知的 y 轴像素行标定纵轴（通常取两条水平网格线）；
  2) 用数据点的像素列标定横轴（数据点通常等距，列距 = 相邻 x 刻度间距）；
  3) 按序列的 RGB 配色收集像素，在每个 x 刻度附近的竖条里找「最密标记带」的中心；
  4) 换算成数值。务必用一个已知点反校验标定（见 references/figure-data-extraction.md）。

必须用 terminal 运行（execute_code 的沙箱没有 PIL）。

示例
----
python3 extract_figure_curves.py chart.png \
    --y-axis 64:1600 947:800 \
    --x-ticks 640,1040,1440,1840 --x-labels 20,40,60,80 \
    --series EDFLet=240,0,0 CONGA=60,120,180 Clove=240,180,0 \
    --exclude-rows 0:460 --y-label "FCT (ms)"
"""
import argparse
import collections

from PIL import Image


def parse_pair(s):
    a, b = s.split(":")
    return float(a), float(b)


def parse_color(s):
    return tuple(int(x) for x in s.split(","))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("--y-axis", nargs=2, required=True, metavar="ROW:VALUE",
                    help="两条已知的 y 轴像素行:数值，如 64:1600 947:800（行像素随像素坐标增大而数值一般减小）")
    ap.add_argument("--x-ticks", required=True, help="数据点的像素列，逗号分隔（等距）")
    ap.add_argument("--x-labels", required=True, help="与 --x-ticks 对应的 x 值，逗号分隔")
    ap.add_argument("--series", nargs="+", required=True, metavar="NAME=R,G,B",
                    help="每个序列的配色，如 EDFLet=240,0,0")
    ap.add_argument("--tol", type=int, default=55, help="颜色匹配容差（每通道）")
    ap.add_argument("--half-window", type=int, default=20, help="x 刻度左右的采样半宽（像素）")
    ap.add_argument("--exclude-rows", default="",
                    help="要屏蔽的行区间（如图例带），如 0:460；多个用逗号分隔")
    ap.add_argument("--y-label", default="value")
    a = ap.parse_args()

    (r1, v1), (r2, v2) = parse_pair(a.y_axis[0]), parse_pair(a.y_axis[1])

    def val(y):
        return v1 + (y - r1) * (v2 - v1) / (r2 - r1)

    ex = []
    if a.exclude_rows:
        for part in a.exclude_rows.split(","):
            lo, hi = part.split(":")
            ex.append((int(lo), int(hi)))

    def masked(y):
        return any(lo <= y <= hi for lo, hi in ex)

    im = Image.open(a.image).convert("RGB")
    W, H = im.size
    px = im.load()

    xt = [int(x) for x in a.x_ticks.split(",")]
    xl = a.x_labels.split(",")
    series = []
    for s in a.series:
        name, rgb = s.split("=")
        series.append((name, parse_color(rgb)))

    def close(c, t):
        return all(abs(c[i] - t[i]) < a.tol for i in range(3))

    print(f"# calibration: {a.y_label}={val(r1):.1f} @ row {r1:.0f}, "
          f"{val(r2):.1f} @ row {r2:.0f}")
    print(f"{'x':>8} " + "".join(f"{n:>12}" for n, _ in series))
    for x0, xv in zip(xt, xl):
        row = f"{xv:>8} "
        for name, col in series:
            ys = [y
                  for x in range(x0 - a.half_window, x0 + a.half_window + 1)
                  if 0 <= x < W
                  for y in range(H)
                  if not masked(y) and close(px[x, y], col)]
            if len(ys) < 30:
                row += f"{'--':>12}"
                continue
            hist = collections.Counter(ys)
            best = max(range(min(ys), max(ys) + 1),
                       key=lambda c: sum(hist[t] for t in range(c - 8, c + 9)))
            row += f"{val(best):>12.1f}"
        print(row)


if __name__ == "__main__":
    main()
