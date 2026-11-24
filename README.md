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

