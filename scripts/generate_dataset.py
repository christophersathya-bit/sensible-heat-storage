"""Generate a synthetic sensible heat storage dataset using Q = m * cp * dT
with simple first-order standby heat loss. Output: data/shs_synthetic_dataset.csv"""
import numpy as np, pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
mat = pd.read_csv(ROOT / "data" / "shs_materials.csv")
rng = np.random.default_rng(42)
rows = []
for _, m in mat.iterrows():
    for _ in range(200):
        vol = rng.uniform(0.5, 50)                       # m3
        t_low = rng.uniform(m.T_min_C, m.T_min_C + 0.3 * (m.T_max_C - m.T_min_C))
        t_high = rng.uniform(t_low + 20, m.T_max_C) if m.T_max_C - t_low > 20 else m.T_max_C
        dT = t_high - t_low
        mass = vol * m.density_kg_m3
        q_kwh = mass * m.cp_kJ_kgK * dT / 3600
        u = rng.uniform(0.2, 1.0)                        # insulation U-value W/m2K
        area = 6 * vol ** (2 / 3)                        # cube surface
        t_amb = min(rng.uniform(5, 35), t_low)           # ambient never above discharge temp
        hours = rng.uniform(1, 72)                       # standby time
        tau = mass * m.cp_kJ_kgK * 1000 / (u * area) / 3600   # time constant, h
        t_end = t_amb + (t_high - t_amb) * np.exp(-hours / tau)
        loss = mass * m.cp_kJ_kgK * (t_high - max(t_end, t_low)) / 3600   # usable energy lost
        rows.append(dict(medium=m.medium, category=m.category, volume_m3=vol, mass_kg=mass,
                         density_kg_m3=m.density_kg_m3, cp_kJ_kgK=m.cp_kJ_kgK, k_W_mK=m.k_W_mK,
                         T_low_C=t_low, T_high_C=t_high, delta_T_K=dT, U_W_m2K=u, T_ambient_C=t_amb,
                         standby_h=hours, stored_energy_kWh=q_kwh, T_after_standby_C=t_end, heat_loss_kWh=loss,
                         storage_efficiency=1 - loss / q_kwh,
                         energy_density_kWh_m3=q_kwh / vol))
df = pd.DataFrame(rows).round(4)
df.to_csv(ROOT / "data" / "shs_synthetic_dataset.csv", index=False)
print(f"Wrote {len(df)} rows")
