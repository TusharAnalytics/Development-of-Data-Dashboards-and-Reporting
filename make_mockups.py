import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

NAVY = "#1F3A5F"; TEAL = "#2A9D8F"; AMBER = "#E9A23B"; RED = "#D1495B"
GREY = "#6B7280"; LIGHT = "#F3F5F8"; MID = "#D5DAE1"; GREEN = "#3A9D5D"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = "DejaVu Sans"

# ---------------------------------------------------------------- 1. Hi-fi mock-up
W, H = 16, 9
fig = plt.figure(figsize=(W, H), dpi=150, facecolor="white")
bg = fig.add_axes([0, 0, 1, 1]); bg.set_xlim(0, W); bg.set_ylim(0, H); bg.axis("off")
bg.add_patch(Rectangle((0, 0), W, H, color=LIGHT))

# header
bg.add_patch(Rectangle((0, H - 0.9), W, 0.9, color=NAVY))
bg.text(0.35, H - 0.45, "SUPPLY CHAIN PERFORMANCE DASHBOARD  |  Executive Overview",
        color="white", fontsize=15, fontweight="bold", va="center")
chips = ["Period: Last 12 months", "Region: All", "Category: All", "Supplier: All"]
x = 8.3
for c in chips:
    w = 0.088 * len(c) + 0.3
    bg.add_patch(FancyBboxPatch((x, H - 0.68), w, 0.45, boxstyle="round,pad=0.02,rounding_size=0.1",
                                fc="#2E4E7A", ec="none"))
    bg.text(x + w / 2, H - 0.455, c, color="white", fontsize=8.5, ha="center", va="center")
    x += w + 0.12

# KPI cards
kpis = [
    ("OTIF", "91.4%", "+1.2 pts vs LY", "Target 95%", AMBER),
    ("ORDER FILL RATE", "96.8%", "+0.4 pts vs LY", "Target 97%", GREEN),
    ("AVG LEAD TIME", "6.2 days", "-0.3 d vs LY", "Target 5.5 d", AMBER),
    ("INVENTORY TURNS", "8.1x", "+0.6 vs LY", "Target 8.0x", GREEN),
    ("STOCK-OUT RATE", "2.9%", "+0.5 pts vs LY", "Target 2.0%", RED),
    ("FREIGHT COST / UNIT", "$4.37", "+3.1% vs LY", "Target $4.20", AMBER),
]
cw = (W - 0.7 - 5 * 0.2) / 6
for i, (t, v, d, tg, col) in enumerate(kpis):
    x0 = 0.35 + i * (cw + 0.2); y0 = H - 2.25
    bg.add_patch(FancyBboxPatch((x0, y0), cw, 1.15, boxstyle="round,pad=0.02,rounding_size=0.08", fc="white", ec=MID))
    bg.add_patch(Rectangle((x0, y0 + 0.02), 0.09, 1.11, color=col))
    bg.text(x0 + 0.22, y0 + 0.93, t, fontsize=8, color=GREY, fontweight="bold")
    bg.text(x0 + 0.22, y0 + 0.50, v, fontsize=20, color=NAVY, fontweight="bold", va="center")
    bg.text(x0 + 0.22, y0 + 0.14, d, fontsize=8, color=col if col != AMBER else "#B97A0A", va="center")
    bg.text(x0 + cw - 0.12, y0 + 0.14, tg, fontsize=7.5, color=GREY, va="center", ha="right")

def panel(rect, title):
    x0, y0, w, h = rect
    bg.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc="white", ec=MID))
    bg.text(x0 + 0.18, y0 + h - 0.25, title, fontsize=9.5, color=NAVY, fontweight="bold", va="center")
    return fig.add_axes([ (x0 + 0.55) / W, (y0 + 0.35) / H, (w - 0.8) / W, (h - 0.95) / H ])

def style(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(MID)
    ax.tick_params(colors=GREY, labelsize=7.5, length=2)
    ax.grid(axis="y", color="#E8EBF0", lw=0.7); ax.set_axisbelow(True)

months = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
rng = np.random.default_rng(7)

# Panel A: OTIF trend vs target
ax = panel((0.35, 3.15, 5.2, 3.45), "A  OTIF % - 12-month trend vs target")
otif = np.array([88.1, 87.4, 86.9, 88.5, 89.2, 89.9, 90.6, 90.1, 91.0, 90.8, 91.2, 91.4])
ax.plot(months, otif, color=NAVY, lw=2, marker="o", ms=3.5)
ax.axhline(95, color=RED, ls="--", lw=1); ax.text(0.1, 95.25, "Target 95%", color=RED, fontsize=7.5)
ax.fill_between(months, otif, 85, color=NAVY, alpha=0.07)
ax.set_ylim(85, 97); style(ax)
ax.annotate("Holiday peak dip", xy=(2, 86.9), xytext=(3.2, 85.7), fontsize=7.5, color=GREY,
            arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))

# Panel B: Supplier lead time (horizontal bars, sorted)
ax = panel((5.75, 3.15, 4.9, 3.45), "B  Avg lead time by supplier (days)")
sup = ["Supplier E", "Supplier C", "Supplier A", "Supplier D", "Supplier B", "Supplier F"][::-1]
lt = np.array([9.4, 8.1, 6.3, 5.4, 4.8, 4.1])[::-1]
cols = [RED if v > 7 else (AMBER if v > 5.5 else TEAL) for v in lt]
ax.barh(sup, lt, color=cols, height=0.62)
ax.axvline(5.5, color=NAVY, ls="--", lw=1); ax.text(5.6, 5.45, "Target 5.5 d", fontsize=7.5, color=NAVY)
for i, v in enumerate(lt): ax.text(v + 0.1, i, f"{v}", va="center", fontsize=7.5, color=GREY)
style(ax); ax.grid(axis="y", visible=False); ax.grid(axis="x", color="#E8EBF0", lw=0.7)

# Panel C: Inventory days of supply by category
ax = panel((10.85, 3.15, 4.8, 3.45), "C  Days of supply by category")
cat = ["Electronics", "Apparel", "Grocery", "Home", "Health"]
dos = [48, 62, 14, 39, 27]
cols = [AMBER, RED, TEAL, TEAL, TEAL]
ax.bar(cat, dos, color=cols, width=0.6)
ax.axhline(45, color=NAVY, ls="--", lw=1); ax.text(2.55, 47, "Max policy 45 d", fontsize=7.5, color=NAVY)
for i, v in enumerate(dos): ax.text(i, v + 1.2, str(v), ha="center", fontsize=7.5, color=GREY)
ax.set_ylim(0, 75); style(ax)

# Panel D: Freight cost vs volume combo
ax = panel((0.35, 0.3, 5.2, 2.65), "D  Freight cost per unit vs shipment volume")
vol = np.array([42, 40, 38, 41, 45, 47, 49, 50, 52, 51, 53, 55])
cpu = np.array([4.52, 4.58, 4.61, 4.47, 4.40, 4.36, 4.31, 4.33, 4.29, 4.35, 4.34, 4.37])
ax.bar(months, vol, color=MID, width=0.6); ax.set_ylabel("Units (000)", fontsize=7.5, color=GREY)
style(ax)
ax2 = ax.twinx(); ax2.plot(months, cpu, color=TEAL, lw=2, marker="o", ms=3)
ax2.set_ylim(4.0, 4.8); ax2.tick_params(colors=GREY, labelsize=7.5, length=2)
for s in ("top",): ax2.spines[s].set_visible(False)
ax2.spines["right"].set_color(MID); ax2.spines["left"].set_visible(False); ax2.spines["bottom"].set_visible(False)

# Panel E: Delivery status mix (stacked 100% bar by region)
ax = panel((5.75, 0.3, 4.9, 2.65), "E  Order status mix by region")
reg = ["North", "South", "East", "West"]
ontime = np.array([93, 90, 88, 94]); late = np.array([5, 7, 9, 4]); fail = 100 - ontime - late
ax.barh(reg[::-1], ontime[::-1], color=TEAL, label="On time")
ax.barh(reg[::-1], late[::-1], left=ontime[::-1], color=AMBER, label="Late")
ax.barh(reg[::-1], fail[::-1], left=(ontime + late)[::-1], color=RED, label="Failed")
ax.set_xlim(0, 100); style(ax); ax.grid(axis="y", visible=False)
ax.legend(fontsize=7, frameon=False, ncol=3, loc="upper right", bbox_to_anchor=(1.0, 1.18))

# Panel F: Exception table
x0, y0, w, h = 10.85, 0.3, 4.8, 2.65
bg.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc="white", ec=MID))
bg.text(x0 + 0.18, y0 + h - 0.25, "F  Exceptions needing attention (top 5)", fontsize=9.5, color=NAVY, fontweight="bold", va="center")
hdr = ["Item / Lane", "Issue", "Impact", ""]
cx = [x0 + 0.2, x0 + 1.55, x0 + 3.15, x0 + 4.35]
for c, t in zip(cx, hdr): bg.text(c, y0 + h - 0.6, t, fontsize=7.5, color=GREY, fontweight="bold")
rows = [("SKU-1043 (Apparel)", "Stock-out risk", "High", RED), ("Supplier E - Lane 3", "Late 4 wks in a row", "High", RED),
        ("SKU-2210 (Electr.)", "Overstock 62 d", "Med", AMBER), ("East region", "OTIF < 90%", "Med", AMBER),
        ("Port transfer P-07", "Delay +2.1 d", "Low", TEAL)]
for i, (a, b, c, col) in enumerate(rows):
    yy = y0 + h - 0.92 - i * 0.37
    bg.add_patch(Rectangle((x0 + 0.1, yy - 0.16), w - 0.2, 0.33, color="#F8F9FB" if i % 2 == 0 else "white"))
    bg.text(cx[0], yy, a, fontsize=7.5, color=NAVY, va="center"); bg.text(cx[1], yy, b, fontsize=7.5, color=GREY, va="center")
    bg.text(cx[2], yy, c, fontsize=7.5, color=NAVY, va="center")
    bg.add_patch(plt.Circle((cx[3] + 0.1, yy), 0.08, color=col))

bg.text(W - 0.3, 0.08, "Illustrative sample data - for design purposes only", fontsize=7, color=GREY, ha="right")
fig.savefig(os.path.join(OUT, "mockup_dashboard.png"), dpi=150)
plt.close(fig)

# ---------------------------------------------------------------- 2. Wireframe
fig = plt.figure(figsize=(W, H), dpi=150)
bg = fig.add_axes([0, 0, 1, 1]); bg.set_xlim(0, W); bg.set_ylim(0, H); bg.axis("off")
def box(x, y, w, h, label, fc="#EEF0F4", fs=11, sub=None):
    bg.add_patch(Rectangle((x, y), w, h, fc=fc, ec="#9AA3B2", lw=1.4, ls="-"))
    bg.text(x + w / 2, y + h / 2 + (0.15 if sub else 0), label, ha="center", va="center", fontsize=fs, color="#2B3445", fontweight="bold")
    if sub: bg.text(x + w / 2, y + h / 2 - 0.25, sub, ha="center", va="center", fontsize=9, color=GREY)
box(0.2, 8.0, 15.6, 0.8, "HEADER  -  Title  |  Global filters (Date, Region, Category, Supplier)  |  Export / Refresh", "#DDE3EC", 11)
for i, l in enumerate(["KPI 1\nOTIF", "KPI 2\nFill rate", "KPI 3\nLead time", "KPI 4\nInv. turns", "KPI 5\nStock-outs", "KPI 6\nFreight/unit"]):
    box(0.2 + i * 2.62, 6.55, 2.46, 1.25, l, "#E4EEF0", 10)
box(0.2, 3.55, 5.1, 2.8, "A  TREND (line)", sub="Reliability over time vs target")
box(5.45, 3.55, 5.0, 2.8, "B  RANKING (bar)", sub="Suppliers / lanes sorted by performance")
box(10.6, 3.55, 5.2, 2.8, "C  COMPARISON (column)", sub="Inventory days of supply by category")
box(0.2, 0.35, 5.1, 3.0, "D  RELATIONSHIP (combo)", sub="Cost vs volume")
box(5.45, 0.35, 5.0, 3.0, "E  COMPOSITION (100% bar)", sub="Order status by region")
box(10.6, 0.35, 5.2, 3.0, "F  EXCEPTION TABLE", "#F9E9EC", 11, sub="Top issues, RAG status, drill-through links")
bg.annotate("", xy=(0.15, 6.5), xytext=(0.15, 7.9), arrowprops=dict(arrowstyle="-", color="none"))
bg.text(15.8, 0.1, "Reading order: Z-pattern (top-left to bottom-right)  |  1 Header -> 2 KPIs -> 3 Trend/Ranking -> 4 Exceptions",
        ha="right", fontsize=8, color=GREY)
fig.savefig(os.path.join(OUT, "wireframe_dashboard.png"), dpi=150)
plt.close(fig)

# ---------------------------------------------------------------- 3. Data flow
fig = plt.figure(figsize=(16, 4.6), dpi=150)
bg = fig.add_axes([0, 0, 1, 1]); bg.set_xlim(0, 16); bg.set_ylim(0, 4.6); bg.axis("off")
stages = [
    ("1. DATA SOURCES", ["Public datasets (CSV/API)", "ERP / WMS / TMS exports", "Supplier & carrier files"], "#DDE3EC"),
    ("2. EXTRACT & CLEAN", ["Python / Power Query", "Fix types, dates, duplicates", "Handle missing values"], "#E4EEF0"),
    ("3. DATA MODEL", ["Fact: orders, shipments,", "inventory snapshots", "Dims: date, product, supplier, region"], "#EAF3E8"),
    ("4. KPI LAYER", ["Calculated measures", "(OTIF, fill rate, turns...)", "Targets & RAG thresholds"], "#FBF1DC"),
    ("5. DASHBOARD", ["Power BI / Tableau /", "Looker Studio", "Filters, drill-down, alerts"], "#F9E9EC"),
]
bw = 2.85; gap = 0.4
for i, (t, lines, fc) in enumerate(stages):
    x0 = 0.25 + i * (bw + gap)
    bg.add_patch(FancyBboxPatch((x0, 0.9), bw, 2.7, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec="#9AA3B2", lw=1.2))
    bg.text(x0 + bw / 2, 3.2, t, ha="center", fontsize=10.5, fontweight="bold", color=NAVY)
    for j, l in enumerate(lines):
        bg.text(x0 + bw / 2, 2.55 - j * 0.45, l, ha="center", fontsize=9, color="#2B3445")
    if i < 4:
        bg.add_patch(FancyArrowPatch((x0 + bw + 0.03, 2.25), (x0 + bw + gap - 0.03, 2.25), arrowstyle="-|>", mutation_scale=18, color=NAVY, lw=2))
bg.text(8, 0.4, "Users: Executives  |  Supply chain managers  |  Planners  |  Procurement  |  Logistics   --  feedback loop drives iterative improvement",
        ha="center", fontsize=9.5, color=GREY, style="italic")
fig.savefig(os.path.join(OUT, "data_flow.png"), dpi=150)
plt.close(fig)
print("done")
