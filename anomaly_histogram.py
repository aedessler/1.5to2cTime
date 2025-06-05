import csv
from collections import defaultdict
import matplotlib.pyplot as plt

# Load data
with open('annual_global_averages.csv', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    # first column is year
    years = []
    data = defaultdict(list)
    for row in reader:
        year = int(row[0])
        years.append(year)
        for col_name, value in zip(header[1:], row[1:]):
            if value:
                data[col_name].append(float(value))
            else:
                data[col_name].append(float('nan'))

# Determine baseline (1850-1900 inclusive)
baseline_indices = [i for i, y in enumerate(years) if 1850 <= y <= 1900]
baseline_avgs = {}
for model, temps in data.items():
    subset = [temps[i] for i in baseline_indices if i < len(temps)]
    baseline_avgs[model] = sum(subset) / len(subset)

# Compute anomalies and year differences
diffs = []
for model, temps in data.items():
    baseline = baseline_avgs[model]
    anomalies = [t - baseline for t in temps]
    year_15 = None
    year_20 = None
    for yr, val in zip(years, anomalies):
        if year_15 is None and val >= 1.5:
            year_15 = yr
        if year_20 is None and val >= 2.0:
            year_20 = yr
        if year_15 is not None and year_20 is not None:
            break
    if year_15 is not None and year_20 is not None:
        diffs.append(year_20 - year_15)

# Plot histogram if we have results
if diffs:
    plt.hist(diffs, bins=10, edgecolor='black')
    plt.xlabel('Years between 1.5°C and 2°C thresholds')
    plt.ylabel('Number of models')
    plt.title('Warming Rate in CMIP Models')
    plt.show()
else:
    print('No models reach both thresholds')
