"""Create visualizations of the SHS datasets into plots/."""
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "plots"; OUT.mkdir(exist_ok=True)
mat = pd.read_csv(ROOT / "data" / "shs_materials.csv")
syn = pd.read_csv(ROOT / "data" / "shs_synthetic_dataset.csv")
COL = {"Low": "#3b82f6", "Medium": "#f59e0b", "High": "#dc2626"}
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

# 1. Operating temperature ranges
m = mat.sort_values("T_max_C")
fig, ax = plt.subplots(figsize=(10, 6.5))
ax.barh(m.medium, m.T_max_C - m.T_min_C, left=m.T_min_C, color=[COL[c] for c in m.category])
for y, (lo, hi) in enumerate(zip(m.T_min_C, m.T_max_C)):
    ax.text(hi + 15, y, f"{lo:.0f}–{hi:.0f} °C", va="center", fontsize=8.5)
for lvl, col in COL.items():
    ax.bar(0, 0, color=col, label=f"{lvl} temperature")
ax.axvline(100, ls="--", c="grey", lw=0.8); ax.axvline(400, ls="--", c="grey", lw=0.8)
ax.set_xlabel("Temperature (°C)"); ax.set_xlim(0, 2300)
ax.set_title("Operating temperature range of sensible heat storage media")
ax.legend(loc="lower right", frameon=False); fig.tight_layout()
fig.savefig(OUT / "01_temperature_ranges.png", dpi=150); plt.close(fig)

# 2. Volumetric energy density over full range
mat["energy_density_kWh_m3"] = mat.density_kg_m3 * mat.cp_kJ_kgK * (mat.T_max_C - mat.T_min_C) / 3600
m = mat.sort_values("energy_density_kWh_m3")
fig, ax = plt.subplots(figsize=(10, 6.5))
ax.barh(m.medium, m.energy_density_kWh_m3, color=[COL[c] for c in m.category])
for y, v in enumerate(m.energy_density_kWh_m3):
    ax.text(v + 10, y, f"{v:.0f}", va="center", fontsize=8.5)
ax.set_xlabel("Energy density over full ΔT (kWh/m³)")
ax.set_title("Theoretical volumetric energy density (ρ·cp·ΔT)"); fig.tight_layout()
fig.savefig(OUT / "02_energy_density.png", dpi=150); plt.close(fig)

# 3. Property map: volumetric heat capacity vs conductivity
fig, ax = plt.subplots(figsize=(9, 6))
vhc = mat.density_kg_m3 * mat.cp_kJ_kgK / 1000
ax.scatter(mat.k_W_mK, vhc, s=mat.T_max_C / 4, c=[COL[c] for c in mat.category], alpha=0.75, edgecolor="k")
for x, y, n in zip(mat.k_W_mK, vhc, mat.medium):
    ax.annotate(n if n.startswith("Water") else n.split(" (")[0], (x, y), xytext=(5, 4), textcoords="offset points", fontsize=8)
ax.set_xscale("log"); ax.set_xlabel("Thermal conductivity (W/m·K, log)")
ax.set_ylabel("Volumetric heat capacity (MJ/m³·K)")
ax.set_title("Material property map (bubble size = max temperature)"); fig.tight_layout()
fig.savefig(OUT / "03_property_map.png", dpi=150); plt.close(fig)

# 4. Synthetic dataset: stored energy vs delta T
fig, ax = plt.subplots(figsize=(9, 6))
for cat, g in syn.groupby("category"):
    ax.scatter(g.delta_T_K, g.energy_density_kWh_m3, s=8, alpha=0.5, c=COL[cat], label=cat)
ax.set_xlabel("ΔT (K)"); ax.set_ylabel("Energy density (kWh/m³)")
ax.set_title("Synthetic dataset: energy density vs temperature swing")
ax.legend(title="Category", frameon=False); fig.tight_layout()
fig.savefig(OUT / "04_synthetic_energy_vs_dT.png", dpi=150); plt.close(fig)

# 5. Synthetic dataset: storage efficiency vs standby time
fig, ax = plt.subplots(figsize=(9, 6))
for cat, g in syn.groupby("category"):
    ax.scatter(g.standby_h, g.storage_efficiency * 100, s=8, alpha=0.5, c=COL[cat], label=cat)
ax.set_xlabel("Standby time (h)"); ax.set_ylabel("Storage efficiency (%)")
ax.set_title("Synthetic dataset: efficiency after standby heat loss")
ax.legend(title="Category", frameon=False); fig.tight_layout()
fig.savefig(OUT / "05_synthetic_efficiency.png", dpi=150); plt.close(fig)
print("Plots saved to", OUT)
