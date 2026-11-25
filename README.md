# Living Room Temperature Prediction Using Newton's Law of Cooling

## Research Question

Can Newton's Law of Cooling predict living room temperature changes over a 10-minute interval using outdoor temperature measurements?

## Project Overview

The project aims to investigate whether a first-order differential equation ODE can be used to predict short-term indoor temperature changes using real building sensor measurements.

## Connection to my Advanced Mathematics lessons

The project is based on Chapter 3 and related WPO practice math that we learned.

The mathematical model is based on "Newton's Law of Cooling" which is:

**dT/dt = k(T_outside - T_inside)**

Where:

- T_inside is the indoor temperature.
- T_outside is the outdoor temperature.
- k is the temperature adjustment coefficient.
- t represents time.

## Planned Dataset

The project will use the **UCI Appliances Energy Prediction Dataset**, containing measurements from a residential building in Belgium.

Dataset source: https://archive.ics.uci.edu/dataset/374/appliances%2Benergy%2Bprediction

The analysis will focus on only:

- `date` — Measurement date and time
- `T2` — Living room temperature
- `T6` — Outdoor temperature on the north side of the building

## Project Plan

The following work is planned:

1. Obtain and examine the temperature dataset.
2. Analyze the relationship between indoor–outdoor temperature differences and indoor temperature changes.
3. Apply Newton's Law of Cooling to predict short-term indoor temperature.
4. Evaluate the predictions against actual measurements.
5. Create at least two Python visualizations.
6. Interpret the results and limitations.
7. Publish the findings on an HTML website.

## Dataset

For this project, I am using the **Appliances Energy Prediction Dataset** from the UCI Machine Learning Repository.

Dataset source: https://archive.ics.uci.edu/dataset/374/appliances%2Benergy%2Bprediction

The dataset contains 19,735 observations collected from a residential building in Belgium between January and May 2016. Measurements were recorded at 10-minute intervals.

Although the original dataset contains temperature, humidity, and energy consumption measurements, this project focuses on three variables:

| Variable | Description |
|---|---|
| `date` | Date and time of the measurement |
| `T2` | Living room temperature (°C) |
| `T6` | Outside temperature on the north side of the building (°C) |

### Data Preparation

I downloaded the original dataset using `download_data.py` and examined the selected variables in Python.

The steps included:

1. Loading the CSV file using pandas.
2. Selecting the `date`, `T2`, and `T6` columns.
3. Checking the number of observations.
4. Examining the first few measurements and basic temperature statistics.
5. Checking the selected columns for missing values.

The dataset is saved locally as `data/energydata_complete.csv`.

The repository contains the download script and data source instructions so that the original measurements can be obtained again.

