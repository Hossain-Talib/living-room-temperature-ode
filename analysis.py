from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from website import create_website

BASE = Path(__file__).parent
DATA_FILE = BASE / 'data' / 'energydata_complete.csv'
FIGURES = BASE / 'figures'
FIGURES.mkdir(exist_ok=True)

if not DATA_FILE.exists():
    raise SystemExit('Missing real dataset. First run: python download_data.py')

# STEP 1: Open the real data. T2 is the living room; T6 is outside.
df = pd.read_csv(DATA_FILE, usecols=['date', 'T2', 'T6'])
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').dropna().reset_index(drop=True)

# Ensure that consecutive observations are exactly 10 minutes apart.
df['minutes_to_next'] = (df['date'].shift(-1) - df['date']).dt.total_seconds() / 60
next_10min = df['minutes_to_next'].eq(10)

# ANALYSIS 1: study how measured indoor changes relate to temperature differences.
df['difference'] = df['T6'] - df['T2']       # outside minus inside, in Celsius
df['change'] = df['T2'].shift(-1) - df['T2']  # next indoor temp minus current
pairs = df.loc[next_10min, ['date', 'T2', 'T6', 'difference', 'change']].copy()

# Time is in HOURS, so 10 minutes = 1/6 hour.
dt = 1 / 6
# We fit: measured_change ~= k * dt * (outside - inside).
# Least squares with no intercept: k = sum(x*y) / [dt*sum(x*x)]
# Fit only the FIRST 80% to test the model on later unseen data.
cutoff = int(len(pairs) * 0.8)
train = pairs.iloc[:cutoff].copy()
test = pairs.iloc[cutoff:].copy()

x = train['difference'].to_numpy()
y = train['change'].to_numpy()
raw_k = float(np.sum(x * y) / (dt * np.sum(x * x)))
# Newton's law requires k >= 0; zero is the best admissible value if raw_k < 0.
k = max(0.0, raw_k)

# ANALYSIS 2: evaluate 10-minute predictions on the unseen final 20%.
test['model_prediction'] = test['T2'] + k * dt * test['difference']
test['persistence_prediction'] = test['T2']
test['actual_next'] = test['T2'] + test['change']
model_mae = float(np.mean(abs(test['actual_next'] - test['model_prediction'])))
baseline_mae = float(np.mean(abs(test['actual_next'] - test['persistence_prediction'])))

# Extra descriptive indicators (not claimed as a third independent analysis).
correlation = float(pairs['difference'].corr(pairs['change']))

# Plot 1: genuine living-room and outdoor measurements over the first 3 days.
short = df.iloc[:3 * 24 * 6]
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(short['date'], short['T2'], label='Living room (T2)', linewidth=2)
ax.plot(short['date'], short['T6'], label='Outside north side (T6)', linewidth=1.6)
ax.set(title='Measured temperatures: first 3 days', xlabel='Date', ylabel='Temperature (°C)')
ax.legend()
ax.grid(alpha=0.2)
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(FIGURES / '01_measured_temperatures.pdf')
fig.savefig(FIGURES / '01_measured_temperatures.png', dpi=170)
plt.close(fig)

# Plot 2: actual next reading vs model next reading (first 100 test cases).
short_test = test.iloc[:100]
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(short_test['date'], short_test['actual_next'], label='Actual next temperature', linewidth=2)
ax.plot(short_test['date'], short_test['model_prediction'], label='ODE prediction', linewidth=1.5)
ax.plot(short_test['date'], short_test['persistence_prediction'], label='No-change prediction', linestyle='--', alpha=0.75)
ax.set(title='10-minute temperature predictions: unseen test period', xlabel='Date', ylabel='Temperature (°C)')
ax.legend()
ax.grid(alpha=0.2)
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(FIGURES / '02_actual_vs_predicted.pdf')
fig.savefig(FIGURES / '02_actual_vs_predicted.png', dpi=170)
plt.close(fig)

# Plot 3: analysis of the first-order differential-equation relationship.
fig, ax = plt.subplots(figsize=(8, 4.7))
# Sample evenly for a readable PDF (all training rows are used to calculate k).
sample = train.iloc[::max(1, len(train)//1600)]
ax.scatter(sample['difference'], sample['change'], s=8, alpha=0.25, label='Measured pairs')
line_x = np.linspace(float(pairs['difference'].min()), float(pairs['difference'].max()), 100)
ax.plot(line_x, k * dt * line_x, linewidth=2, color='#bc7135', label='Fitted ODE relation')
ax.set(title='Temperature difference vs. 10-minute indoor change', xlabel='Outside minus inside (°C)', ylabel='Indoor temperature change (°C)')
ax.legend()
ax.grid(alpha=0.2)
fig.tight_layout()
fig.savefig(FIGURES / '03_temperature_change_relation.pdf')
fig.savefig(FIGURES / '03_temperature_change_relation.png', dpi=170)
plt.close(fig)

results = {
    'original_rows': int(len(df)),
    'ten_minute_pairs': int(len(pairs)),
    'training_rows': int(len(train)),
    'test_rows': int(len(test)),
    'start_date': str(df['date'].iloc[0]),
    'end_date': str(df['date'].iloc[-1]),
    'raw_k_per_hour': raw_k,
    'k_per_hour': k,
    'correlation': correlation,
    'model_mae_c': model_mae,
    'persistence_mae_c': baseline_mae,
    'model_better_than_baseline': model_mae < baseline_mae,
}
(BASE / 'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
create_website(results, BASE)

print('\n--- REAL DATA RESULTS ---')
for key, value in results.items():
    print(f'{key}: {value}')
print('\nGenerated 3 PDF figures and matching PNGs in figures/.')
print('Generated index.html website. Open it in your browser.')
print('Read RESULTS_EXPLANATION.md to interpret what they mean.')
