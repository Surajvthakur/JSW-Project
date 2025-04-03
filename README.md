# JSW Steel Renewable Energy Optimization – Code Overview
This project focuses on optimizing renewable energy (solar, wind, and hydro) usage in steel production while ensuring efficiency and regulatory compliance. The system uses machine learning to balance power distribution within the 300 MWh production limit, minimizing fines and enhancing sustainability.

1️⃣ app.py – Frontend & Dashboard
This file handles the web-based interface for visualizing model outputs and energy allocation insights.

Key Features:
✅ Built using Streamlit for interactive data visualization.
✅ Displays optimized energy allocation results.
✅ Provides graphs for energy usage trends, production efficiency, and model insights.
✅ Accepts user input for real-time predictions based on energy constraints.

2️⃣ appapi.py – API for Model Inference
This file sets up an API for making predictions based on the trained ML model.

Key Features:
✅ Built using FastAPI for efficient handling of requests.
✅ Accepts energy source data (solar, wind, hydro) and returns optimized values.
✅ Serves the trained ML model for real-time energy recommendations.
✅ Provides API documentation via Swagger UI for easy testing.

3️⃣ main.py – Model Training & Optimization Logic
This file contains the core ML model and energy optimization logic.

Key Features:
✅ Reads and preprocesses steel production and energy consumption data.
✅ Implements feature engineering for better model accuracy.
✅ Trains an ML model (e.g., Random Forest, XGBoost, or Linear Regression) to optimize energy allocation.
✅ Uses an optimization algorithm to prevent exceeding the 300 MWh limit.
✅ Saves the trained model for API deployment.
