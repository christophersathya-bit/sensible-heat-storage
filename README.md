# Sensible Heat Storage (SHS) Dataset

Datasets and visualizations of sensible heat storage media, covering operating temperatures from **0 °C to ~2000 °C**.

## Contents

| Path | Description |
|---|---|
| `data/shs_materials.csv` | 15 SHS media with temperature range, density, specific heat, conductivity, approx. cost, limiting mechanism and reference IDs |
| `data/shs_synthetic_dataset.csv` | 3,000 synthetic storage cases (200 per medium): stored energy, standby heat loss, efficiency |
| `scripts/generate_dataset.py` | Regenerates the synthetic dataset |
| `scripts/make_plots.py` | Regenerates all plots |
| `plots/` | PNG figures (shown below) |

## Temperature classes

- **Low (< 100 °C):** water
- **Medium (100–400 °C):** pressurized water, thermal oils, concrete
- **High (> 400 °C):** molten salts, metals, rocks, sand, ceramics, graphite

## Plots

### Operating temperature ranges
![Temperature ranges](plots/01_temperature_ranges.png)

### Theoretical volumetric energy density (ρ·cp·ΔT)
![Energy density](plots/02_energy_density.png)

### Material property map
![Property map](plots/03_property_map.png)

### Synthetic dataset: energy density vs ΔT
![Energy vs dT](plots/04_synthetic_energy_vs_dT.png)

### Synthetic dataset: efficiency after standby
![Efficiency](plots/05_synthetic_efficiency.png)

## Synthetic model

For each case the storage volume, temperature window, insulation U-value, ambient temperature and standby time are sampled at random within the medium's limits.

- Stored energy: `Q = m · cp · (T_high − T_low)`
- Standby loss: lumped first-order cooling of a cubic tank, `T(t) = T_amb + (T_high − T_amb) · exp(−t/τ)`, with `τ = m·cp / (U·A)`
- Efficiency: usable energy remaining above `T_low` divided by `Q`

The model ignores stratification, thermocline and internal conduction effects, so it is intended for screening and ML prototyping, not detailed design.

## Usage

```bash
pip install pandas numpy matplotlib
python scripts/generate_dataset.py
python scripts/make_plots.py
```

## Data notes

Property values are typical literature figures at mid-range temperature. Real limits and properties vary by supplier, purity and container design, and costs are rough order-of-magnitude estimates. Verify against primary sources before using the data in design work.

## References

Reference IDs are listed per material in the `references` column of `data/shs_materials.csv`.

| ID | Reference |
|---|---|
| R1 | Gil, A., Medrano, M., Martorell, I., Lázaro, A., Dolado, P., Zalba, B., Cabeza, L.F. (2010). State of the art on high temperature thermal energy storage for power generation. Part 1—Concepts, materials and modellization. *Renewable and Sustainable Energy Reviews*, 14(1), 31–55. https://doi.org/10.1016/j.rser.2009.07.035 |
| R2 | Kuravi, S., Trahan, J., Goswami, D.Y., Rahman, M.M., Stefanakos, E.K. (2013). Thermal energy storage technologies and systems for concentrating solar power plants. *Progress in Energy and Combustion Science*, 39(4), 285–319. https://doi.org/10.1016/j.pecs.2013.02.001 |
| R3 | Khare, S., Dell'Amico, M., Knight, C., McGarry, S. (2013). Selection of materials for high temperature sensible energy storage. *Solar Energy Materials and Solar Cells*, 115, 114–122. https://doi.org/10.1016/j.solmat.2013.03.009 |
| R4 | Dincer, I., Rosen, M.A. (2011). *Thermal Energy Storage: Systems and Applications* (2nd ed.). Wiley. |
| R5 | NIST Chemistry WebBook, SRD 69 — Thermophysical properties of fluid systems (water). https://webbook.nist.gov/chemistry/fluid/ |
| R6 | Eastman Chemical Company. Therminol VP-1 heat transfer fluid — technical data sheet. https://www.therminol.com/product/71093438 |
| R7 | Laing, D., Steinmann, W.-D., Tamme, R., Richter, C. (2006). Solid media thermal storage for parabolic trough power plants. *Solar Energy*, 80(10), 1283–1289. |
| R8 | Bauer, T., Pfleger, N., Laing, D., Steinmann, W.-D., Eck, M., Kaesche, S. (2013). High-temperature molten salts for solar power application. In F. Lantelme & H. Groult (Eds.), *Molten Salts Chemistry* (pp. 415–438). Elsevier. |
| R9 | Kearney, D., Herrmann, U., Nava, P., Kelly, B., Mahoney, R., Pacheco, J., Cable, R., Potrovitza, N., Blake, D., Price, H. (2003). Assessment of a molten salt heat transfer fluid in a parabolic trough solar field. *Journal of Solar Energy Engineering*, 125(2), 170–176. https://doi.org/10.1115/1.1565087 |
| R10 | Ding, W., Bauer, T. (2021). Progress in research and development of molten chloride salt technology for next generation concentrated solar power plants. *Engineering*, 7(3), 334–347. https://doi.org/10.1016/j.eng.2020.06.027 |
| R11 | Pacio, J., Wetzel, T. (2013). Assessment of liquid metal technology status and research paths for their use as efficient heat transfer fluids in solar central receiver systems. *Solar Energy*, 93, 11–22. |
| R12 | Ma, Z., Glatzmaier, G., Mehos, M. (2014). Development of solid particle thermal energy storage for concentrating solar power plants that use fluidized bed technology. *Energy Procedia*, 49, 898–907. |
| R13 | Mehos, M., Turchi, C., Vidal, J., Wagner, M., Ma, Z., Ho, C., Kolb, W., Andraka, C., Kruizenga, A. (2017). *Concentrating Solar Power Gen3 Demonstration Roadmap*. NREL/TP-5500-67464. National Renewable Energy Laboratory. |
| R14 | Steinmann, W.-D., Eck, M. (2006). Buffer storage for direct steam generation. *Solar Energy*, 80(10), 1277–1282. |

Values in the dataset are representative figures compiled from these sources. Exact numbers vary between sources and products, so cite the primary reference for any value used in published work.
