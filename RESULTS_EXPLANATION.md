**Dataset.** UCI Appliances Energy Prediction: temperature every 10 minutes in a Belgian home. `T2` measures the living-room temperature. `T6` is a sensor outside the building on the north side.

**Analysis 1.** We calculate `difference = T6 - T2` and `change = next_T2 - T2`. If the simple ODE were a perfect description, these values would have a straight-line relationship: `change = k * (1/6) * difference`.

**What is k?** It describes the sensitivity of indoor temperature to the difference between inside and outside. With time in hours, its units are inverse hours. We calculate the least-squares slope from the first 80% of observations, without an intercept, then constrain k to be non-negative (as the simple model assumes).

**Analysis 2.** We predict the next 10-minute living-room temperature on the last 20% of observations. To check whether the ODE adds value, we compare with a no-change baseline: `prediction = current indoor temperature`.

**MAE.** Mean absolute error = average of `abs(actual - predicted)` measured in °C. Smaller MAE is better. In 10-minute intervals the room may hardly change, so the no-change baseline can be difficult to beat.

**Figure 1.** Measured living-room and outside temperatures for the first three days. The room is not expected to follow outside temperatures instantly.

**Figure 2.** Actual next-step indoor temperatures vs. ODE and no-change predictions (the first 100 test observations). Lines lying close together can still differ in MAE; use results.json to interpret.

**Figure 3.** Measured indoor temperature changes vs. indoor-outdoor difference, plus fitted ODE line. Scatter around the line indicates unmodeled processes (e.g., heating and sunlight).

**What the model cannot prove.** The fitted coefficient is not necessarily a physical building heat-transfer coefficient. The ODE ignores heating, occupancy, ventilation and thermal mass. This is a simplified, testable mathematical model, not a complete building simulator.
