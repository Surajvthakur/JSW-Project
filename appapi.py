import streamlit as st
import requests
import math
import matplotlib.pyplot as plt

# Constants
SOLAR_MAX_IRRADIANCE = 5  # kWh/m²/day (approx. for sunny areas in India)
AIR_DENSITY = 1.225  # kg/m³ (at sea level)
WATER_DENSITY = 1000  # kg/m³ (density of water)
GRAVITY = 9.81  # m/s² (acceleration due to gravity)

# API setup
API_KEY = "5a5dc4c0a633d9df1f1fd24f47b52ea0"
LOCATION = "Pen,IN"  # Replace with your city
URL = f"http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}"

# Fetch data from API
response = requests.get(URL)
weather_data = response.json()

# Check if the request was successful
if response.status_code == 200:
    st.write("Weather data fetched successfully!")
else:
    st.write("Failed to fetch weather data. Please check the API key or city name.")
    st.stop()

# Extract required values
cloud_cover = weather_data["clouds"]["all"]  # Cloud cover (%)

# Parameters for Solar, Wind, and Hydro Energy
# Solar
solar_area = 5000  # m² (panel area)
solar_efficiency = 0.18  # 18%
performance_ratio = 0.85  # System efficiency

# Solar Energy Calculation
def calculate_solar_energy(area, efficiency, cloud_cover, performance_ratio):
    irradiance = SOLAR_MAX_IRRADIANCE * (1 - cloud_cover / 100)
    energy = area * efficiency * irradiance * performance_ratio
    return energy

# Calculate energies
solar_energy = calculate_solar_energy(solar_area, solar_efficiency, cloud_cover, performance_ratio)

# Wind Energy Calculation
def calculate_wind_energy(blade_radius, wind_speed, turbine_efficiency, hours):
    swept_area = math.pi * blade_radius**2
    power = 0.5 * AIR_DENSITY * swept_area * (wind_speed**3) * turbine_efficiency
    energy = power * hours / 1000  # Convert Watts to kWh
    return energy

# Extract wind speed
wind_speed = weather_data["wind"]["speed"]  # Wind speed (m/s)

# Wind Energy Parameters
blade_radius = 45  # meters (turbine blade length)
turbine_efficiency = 0.3  # 30%
hours = 24  # Time in hours

wind_energy = calculate_wind_energy(blade_radius, wind_speed, turbine_efficiency, hours)

# Hydropower Calculation
def estimate_hydropower(flow_rate, head_height, efficiency=0.85):
    density_water = 1000  # kg/m³ (density of water)
    g = 9.81  # m/s² (acceleration due to gravity)
    power = density_water * g * flow_rate * head_height * efficiency  # Power in Watts
    return power / 1000  # Convert to kW

def calculate_flow_rate(precipitation, catchment_area, runoff_coefficient=0.8):
    # Convert catchment area from km² to m²
    catchment_area_m2 = catchment_area * 1e6
    # Convert precipitation from mm to meters
    precipitation_m = precipitation / 1000
    # Calculate flow volume (m³/s) using runoff coefficient
    flow_volume_m3_per_hour = precipitation_m * catchment_area_m2 * runoff_coefficient
    flow_rate = flow_volume_m3_per_hour / 3600  # Convert to m³/s
    return flow_rate

# Hydropower parameters
precipitation = 50  # mm/hour (example rainfall data)
catchment_area = 2  # km²
head_height = 20  # meters
runoff_coefficient = 0.85  # Adjust based on terrain (e.g., urban vs rural)

flow_rate = calculate_flow_rate(precipitation, catchment_area, runoff_coefficient)

hydropower = estimate_hydropower(flow_rate, head_height)

# Display results on Streamlit
st.write(f"Cloud Cover: {cloud_cover}%")
st.write(f"Solar Energy Generated: {solar_energy:.2f} kWh/day")
st.write(f"Wind Speed: {wind_speed} m/s")
st.write(f"Wind Energy Generated: {wind_energy:.2f} kWh/day")
st.write(f"Precipitation: {precipitation} mm/hour")
st.write(f"Catchment Area: {catchment_area} km²")
st.write(f"Flow Rate: {flow_rate:.2f} m³/s")
st.write(f"Head Height: {head_height} m")
st.write(f"Estimated Hydropower: {hydropower:.2f} kW")

# User input for energy demand
energy_demand = st.number_input("Enter the energy demand (in kWh):", min_value=0.0, value=0.0)

# Calculate the remaining energy that needs to be generated
total_energy_generated = solar_energy + wind_energy + hydropower
need_to_generate = max(0, energy_demand - total_energy_generated)

# Display the results
st.write(f"Total Energy Generated: {total_energy_generated:.2f} kWh/day")
st.write(f"Energy Demand: {energy_demand:.2f} kWh/day")
st.write(f"Need to Generate: {need_to_generate:.2f} kWh/day")

# Create pie chart data
labels = ['Solar Energy', 'Wind Energy', 'Hydropower', 'Need to Generate']
values = [solar_energy, wind_energy, hydropower, need_to_generate]
colors = ['gold', 'skyblue', 'lightgreen', 'red']
explode = [0.1, 0.2, 0.1, 0.1]  # Adds spacing for all slices

# Plot the pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, explode=explode)
ax.set_title('Energy Generation vs. Demand')

# Display the chart in Streamlit
st.pyplot(fig)
