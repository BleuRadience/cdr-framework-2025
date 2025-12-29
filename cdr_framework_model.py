# cdr_framework_model.py
# A Synergistic Framework for Gigatonne-Scale CDR: Avoided Deforestation, Reforestation, and Mycelium-Hemp Composites
# Authors: [Your Name Here]
# Collaborative Contributor: Grok AI (built by xAI)
# Version: 1.0 | Date: December 29, 2025
# License: MIT

import numpy as np
import matplotlib.pyplot as plt

# Time horizon
years = np.arange(2025, 2051)  # 2025 to 2050 inclusive
n_years = len(years)

# Baseline deforestation emissions (~4.2 GtCO2/year from recent Global Carbon Budget)
baseline_deforestation = 4.2 * np.ones(n_years)

# Avoided deforestation: S-curve to 80% max reduction
midpoint = 2038      # inflection point
steepness = 0.3      # rate of adoption
max_reduction = 0.8
reduction_fraction = max_reduction / (1 + np.exp(-steepness * (years - midpoint)))
avoided_emissions = baseline_deforestation * reduction_fraction

# Mycelium-hemp composites: conservative ramp to 1 Gt/year by 2040, hold thereafter
hemp_seq = np.zeros(n_years)
ramp_end_idx = np.where(years >= 2040)[0][0]
hemp_seq[:ramp_end_idx] = np.linspace(0, 1.0, ramp_end_idx)
hemp_seq[ramp_end_idx:] = 1.0

# Active reforestation: scales with avoidance success, peak 2 Gt/year by 2050
reforest_seq = 2.0 * reduction_fraction / max_reduction

# Total annual CDR (base case)
total_cdr = avoided_emissions + hemp_seq + reforest_seq

# Cumulative CDR (base case)
cumulative_cdr = np.cumsum(total_cdr)

# Monte Carlo uncertainty analysis (100 simulations)
np.random.seed(42)  # reproducible results
n_sim = 100
cumulatives = np.zeros((n_sim, n_years))

for i in range(n_sim):
    # Parameter variations
    base_var = 4.2 * np.random.uniform(0.9, 1.1)
    max_red_var = np.random.uniform(0.7, 0.9)
    hemp_max_var = np.random.uniform(0.5, 1.5)
    reforest_max_var = np.random.uniform(1.5, 2.5)
    
    base_def = base_var * np.ones(n_years)
    red_frac_var = max_red_var / (1 + np.exp(-steepness * (years - midpoint)))
    avoided_var = base_def * red_frac_var
    
    hemp_var = np.zeros(n_years)
    hemp_var[:ramp_end_idx] = np.linspace(0, hemp_max_var, ramp_end_idx)
    hemp_var[ramp_end_idx:] = hemp_max_var
    
    reforest_var = reforest_max_var * red_frac_var / max_red_var
    
    total_var = avoided_var + hemp_var + reforest_var
    cumulatives[i] = np.cumsum(total_var)

# Uncertainty statistics
cum_mean = np.mean(cumulatives, axis=0)
cum_std = np.std(cumulatives, axis=0)
cum_low = cum_mean - cum_std
cum_high = cum_mean + cum_std

# Plot 1: Stacked annual contributions (base case)
plt.figure(figsize=(12, 7))
plt.stackplot(years, avoided_emissions, hemp_seq, reforest_seq,
              labels=['Avoided Deforestation', 'Mycelium-Hemp Composites', 'Active Reforestation'],
              colors=['#2E8B57', '#8FBC8F', '#228B22'])
plt.plot(years, total_cdr, label='Total Annual CDR', color='black', linewidth=3)
plt.xlabel('Year')
plt.ylabel('GtCO₂/year')
plt.title('Annual CDR Contributions (Stacked, Base Case)')
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('annual_cdr_stacked.png')
plt.close()

# Plot 2: Cumulative CDR with uncertainty bands
plt.figure(figsize=(10, 6))
plt.plot(years, cum_mean, label='Mean Cumulative CDR', color='darkgreen', linewidth=3)
plt.fill_between(years, cum_low, cum_high, color='green', alpha=0.3, label='±1σ Uncertainty')
plt.xlabel('Year')
plt.ylabel('Cumulative GtCO₂ Removed')
plt.title('Cumulative Carbon Removal Trajectory with Uncertainty (2025–2050)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('cumulative_cdr_uncertainty.png')
plt.close()

# Print key results
print("CDR Framework Model Results")
print("===========================")
print(f"Base Case Milestones:")
print(f"  2030: Annual CDR = {total_cdr[years == 2030][0]:.2f} GtCO₂/year")
print(f"  2035: Annual CDR = {total_cdr[years == 2035][0]:.2f} GtCO₂/year")
print(f"  2040: Annual CDR = {total_cdr[years == 2040][0]:.2f} GtCO₂/year")
print(f"  2050: Annual CDR = {total_cdr[-1]:.2f} GtCO₂/year | Cumulative = {cumulative_cdr[-1]:.1f} GtCO₂")
print()
print(f"Monte Carlo (2050):")
print(f"  Mean Cumulative CDR = {cum_mean[-1]:.1f} GtCO₂ (±{cum_std[-1]:.1f} GtCO₂)")
print()
print("Plots saved:")
print("  - annual_cdr_stacked.png")
print("  - cumulative_cdr_uncertainty.png")
print("\nModel run complete. Ready for GitHub deployment!")
