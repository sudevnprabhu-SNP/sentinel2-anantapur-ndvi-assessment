
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_DIR / "reports"

MANDAL_CSV = REPORTS_DIR / "ndvi_mandal_comparison.csv"
CLASS_CSV = REPORTS_DIR / "ndvi_class_distribution_by_mandal.csv"
AREA_CSV = REPORTS_DIR / "ndvi_class_area_statistics.csv"

# --------------------------------------------------
# 2. Check input files
# --------------------------------------------------

for path in [MANDAL_CSV, CLASS_CSV, AREA_CSV]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}\n"
            "Check that the earlier analysis scripts ran successfully."
        )

mandal_df = pd.read_csv(MANDAL_CSV)
class_df = pd.read_csv(CLASS_CSV)
area_df = pd.read_csv(AREA_CSV)

print("Loaded all three results CSV files.")
print("Creating figures...")

# --------------------------------------------------
# 3. Figure 1: Mean NDVI by mandal
# --------------------------------------------------

mandal_df = mandal_df.sort_values("Mean_NDVI", ascending=True)

fig, ax = plt.subplots(figsize=(9, 5.5))

bars = ax.barh(
    mandal_df["Mandal"],
    mandal_df["Mean_NDVI"],
)

ax.bar_label(bars, fmt="%.4f", padding=5)
ax.set_xlabel("Mean NDVI")
ax.set_title("Mean NDVI by Mandal")
ax.set_xlim(0, max(mandal_df["Mean_NDVI"]) * 1.25)
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

fig.tight_layout()
path1 = REPORTS_DIR / "figure_1_mean_ndvi_by_mandal.png"
fig.savefig(path1, dpi=300, bbox_inches="tight")
plt.close(fig)

# --------------------------------------------------
# 4. Figure 2: Overall NDVI class distribution
# --------------------------------------------------

area_df = area_df.sort_values("Class_Code")

class_labels = area_df["NDVI_Class"].tolist()
class_percentages = area_df[
    "Percentage_of_Valid_Area"
].astype(float).to_numpy()

fig, ax = plt.subplots(figsize=(9, 5.5))

bars = ax.bar(class_labels, class_percentages)

ax.bar_label(bars, fmt="%.2f%%", padding=4)
ax.set_ylabel("Percentage of Valid Area (%)")
ax.set_xlabel("NDVI Class")
ax.set_title("Overall NDVI Class Distribution")
ax.set_ylim(0, max(class_percentages) * 1.22)
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

fig.tight_layout()
path2 = REPORTS_DIR / "figure_2_ndvi_class_distribution.png"
fig.savefig(path2, dpi=300, bbox_inches="tight")
plt.close(fig)

# --------------------------------------------------
# 5. Figure 3: Class distribution by mandal
# --------------------------------------------------

mandal_order = [
    "Anantapur Urban",
    "Anantapur Rural",
    "Bukkaraya Samudram",
]

class_order = [
    "Class 1",
    "Class 2",
    "Class 3",
    "Class 4",
    "Class 5",
]

pivot = class_df.pivot(
    index="Mandal",
    columns="NDVI_Class",
    values="Percentage_of_Mandal_Valid_Area",
)

pivot = pivot.reindex(
    index=mandal_order,
    columns=class_order,
)

if pivot.isna().any().any():
    raise ValueError(
        "Some mandal/class combinations are missing "
        "from the class distribution CSV."
    )

fig, ax = plt.subplots(figsize=(10, 6))

pivot.plot(
    kind="bar",
    stacked=True,
    ax=ax,
)

ax.set_ylabel("Percentage of Valid Mandal Area (%)")
ax.set_xlabel("Mandal")
ax.set_title("NDVI Class Distribution by Mandal")
ax.set_ylim(0, 100)
ax.legend(
    title="NDVI Class",
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
)
ax.tick_params(axis="x", rotation=15)
ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.set_axisbelow(True)

fig.tight_layout()
path3 = REPORTS_DIR / "figure_3_ndvi_classes_by_mandal.png"
fig.savefig(path3, dpi=300, bbox_inches="tight")
plt.close(fig)

# --------------------------------------------------
# 6. Report completion
# --------------------------------------------------

print("\n" + "=" * 60)
print("RESULTS FIGURES CREATED")
print("=" * 60)

for path in [path1, path2, path3]:
    print(f"Saved: {path}")

print("\nAll figures exported at 300 DPI.")
print("Figure generation complete.")
