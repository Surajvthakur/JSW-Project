import pandas as pd
import numpy as np

df = pd.read_csv("energy_data_generation.csv")
# Create DataFrame
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Scaling factor to bring energy consumption to the range of earlier data
scaling_factor = 19898.17 / 2.81  # First old energy value divided by first new energy value
df["energy_consumed_kWh"] *= scaling_factor

# Accumulate energy values for each day, resetting at the start of a new day
def accumulate_daily_energy(group):
    group = group.copy()
    group["cumulative_energy_consumed"] = group["energy_consumed_kWh"].cumsum()
    group["cumulative_solar_energy"] = group["solar_energy_kWh"].cumsum()
    group["cumulative_wind_energy"] = group["wind_energy_kWh"].cumsum()
    group["cumulative_hydro_energy"] = group["hydro_energy_kWh"].cumsum()
    return group

df["date"] = df["timestamp"].dt.date
df = df.groupby("date").apply(accumulate_daily_energy)

# Drop the temporary date column
df.drop(columns=["date"], inplace=True)

# Save the updated DataFrame
df.to_csv("updated_energy_data.csv", index=False)

print(df)