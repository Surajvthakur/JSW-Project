import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
df = pd.read_csv("energy_data_with_noise.csv")

# Convert 'timestamp' to datetime and extract features
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['minute'] = df['timestamp'].dt.minute
df['day'] = df['timestamp'].dt.day

# Streamlit App Title
st.title("Energy Consumption Prediction")

# Date range input for user to select the range of analysis
st.write("### Select Date Range for Analysis")
start_date = st.date_input("Start Date", df['timestamp'].min().date())
end_date = st.date_input("End Date", df['timestamp'].max().date())

# Filter data according to the selected date range
filtered_df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

# Features and target variable
X = filtered_df[['temperature_C', 'humidity_%', 'wind_speed_mps', 'is_sunny', 'cloud_cover_%', 'solar_irradiance_Wm2', 'air_density_kgm3', 'precipitation_mm', 'runoff_coefficient', 'hour', 'minute', 'day']]
y = filtered_df['energy_consumed_kWh']

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Model training (RandomForestRegressor)
model = RandomForestRegressor(n_estimators=2, random_state=42,max_depth=3)
model.fit(X_scaled, y)

# Predictions on the filtered dataset
y_pred = model.predict(X_scaled)

# Performance metrics
r2 = r2_score(y, y_pred)
mse = mean_squared_error(y, y_pred)

# Display Model Performance
st.write("### Model Performance")
st.write(f'R² Score: {r2:.4f}')
st.write(f'Mean Squared Error: {mse:.4f}')

# Plotting Actual vs Predicted Energy Consumption using Plotly
fig = go.Figure()

# Filter data to exclude future dates for actual values
filtered_df_valid = filtered_df[filtered_df['timestamp'] <= pd.Timestamp.now()]

# Actual Energy Consumption
fig.add_trace(go.Scatter(
    x=filtered_df_valid['timestamp'], 
    y=filtered_df_valid['energy_consumed_kWh'], 
    mode='lines+markers', 
    name='Actual Energy Consumption', 
    line=dict(color='blue')
))

# Predicted Energy Consumption (for all timestamps)
fig.add_trace(go.Scatter(
    x=filtered_df['timestamp'], 
    y=y_pred, 
    mode='lines+markers', 
    name='Predicted Energy Consumption', 
    line=dict(color='red')
))

# Update the layout for the x-axis to show 15-minute intervals and increase graph size
fig.update_layout(
    title="Actual vs Predicted Energy Consumption",
    xaxis_title="Time of Day",
    yaxis_title="Energy Consumption (kWh)",
    legend_title="Legend",
    template="plotly_dark",
    xaxis=dict(
        tickformat="%H:%M",
        tickmode="linear",
        tickangle=45,
        dtick=900000000,
        range=[filtered_df['timestamp'].iloc[0], filtered_df['timestamp'].iloc[-1]]
    ),
    autosize=True
)

# Make the graph occupy more space in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Streamlit App Title
st.title("Energy Consumption Analysis")

# First, display the correlation matrix using a heatmap
st.write("### Correlation Heatmap of Features")
correlation_matrix = filtered_df.corr()
heatmap = px.imshow(correlation_matrix, text_auto=True, color_continuous_scale='Blues', title="Correlation Heatmap")
st.plotly_chart(heatmap, use_container_width=True)

# Second, show the distribution of energy consumed
st.write("### Distribution of Energy Consumed (kWh)")
fig1 = px.histogram(filtered_df, x='energy_consumed_kWh', nbins=20, title="Energy Consumption Distribution")
st.plotly_chart(fig1, use_container_width=True)

# Third, scatter plot between Temperature and Energy Consumption with hue (Sunny or Not)
st.write("### Scatter Plot: Temperature vs Energy Consumption (Hue: Sunny or Not)")
fig2 = px.scatter(filtered_df, x='temperature_C', y='energy_consumed_kWh', color='is_sunny', title="Temperature vs Energy Consumption",
                  labels={"temperature_C": "Temperature (°C)", "energy_consumed_kWh": "Energy Consumed (kWh)", "is_sunny": "Sunny (0 = No, 1 = Yes)"})
st.plotly_chart(fig2, use_container_width=True)

# Fourth, scatter plot between solar_energy_kWh and Energy Consumption with hue (Sunny or Not)
st.write("### Scatter Plot: solar_energy_kWh vs wind_energy_kWh (Hue: Sunny or Not)")
fig3 = px.scatter(filtered_df, x='solar_energy_kWh', y='wind_energy_kWh', color='is_sunny', title="Solar_energy_kWh vs wind_energy_kWh",
                  labels={"solar_energy_kWh": "solar_energy_kWh", "wind_energy_kWh": "wind_energy_kWh", "is_sunny": "Sunny (0 = No, 1 = Yes)"})
st.plotly_chart(fig3, use_container_width=True)

# Fifth, time series plot of energy consumption with 15-minute intervals
st.write("### Time Series: Energy Consumption over Time")
fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=filtered_df['timestamp'], y=filtered_df['energy_consumed_kWh'], mode='lines+markers', name='Energy Consumption', line=dict(color='orange')))
fig4.update_layout(title="Energy Consumption over Time", xaxis_title="Time", yaxis_title="Energy Consumption (kWh)", template="plotly_dark")
st.plotly_chart(fig4, use_container_width=True)

# Sixth, box plot to show the spread of Energy Consumption based on the 'is_sunny' feature
st.write("### Box Plot: Energy Consumption Based on Weather (Sunny or Not)")
fig5 = px.box(filtered_df, x='is_sunny', y='energy_consumed_kWh', title="Energy Consumption Based on Weather (Sunny or Not)", 
              labels={"is_sunny": "Sunny (0 = No, 1 = Yes)", "energy_consumed_kWh": "Energy Consumed (kWh)"})
st.plotly_chart(fig5, use_container_width=True)

# Seventh, line plot to visualize the change in solar irradiance over time
st.write("### Line Plot: Solar Irradiance Over Time")
fig6 = go.Figure()
fig6.add_trace(go.Scatter(x=filtered_df['timestamp'], y=filtered_df['solar_irradiance_Wm2'], mode='lines', name='Solar Irradiance', line=dict(color='green')))
fig6.update_layout(title="Solar Irradiance over Time", xaxis_title="Time", yaxis_title="Solar Irradiance (W/m²)", template="plotly_dark")
st.plotly_chart(fig6, use_container_width=True)

# Eighth, bar plot showing the average energy consumption for each day
st.write("### Average Energy Consumption for Each Day")
filtered_df['day'] = filtered_df['timestamp'].dt.date
fig7 = px.bar(filtered_df.groupby('day')['energy_consumed_kWh'].mean().reset_index(), x='day', y='energy_consumed_kWh', 
              title="Average Energy Consumption per Day", labels={"day": "Day", "energy_consumed_kWh": "Average Energy Consumption (kWh)"})
st.plotly_chart(fig7, use_container_width=True)  