import streamlit as st
import pandas as pd

st.title("HVAC Duct Sizing Calculator")

# Unit system
unit = st.radio("Select Unit System", ["SI (mm, L/s)", "Imperial (in, CFM)"])

# Input fields
if unit == "SI (mm, L/s)":
    airflow = st.number_input("Airflow (L/s)", value=500.0)
    width = st.number_input("Duct Width (mm)", value=400.0)
    depth = st.number_input("Duct Depth (mm)", value=250.0)
    width_m = width / 1000
    depth_m = depth / 1000
    q = airflow
else:
    airflow = st.number_input("Airflow (CFM)", value=1059.0)
    width = st.number_input("Duct Width (in)", value=15.75)
    depth = st.number_input("Duct Depth (in)", value=9.84)
    width_m = width * 0.0254
    depth_m = depth * 0.0254
    q = airflow * 0.472  # Convert CFM to L/s

# Calculate
if st.button("Calculate"):
    try:
        area = width_m * depth_m
        aspect_ratio = width_m / depth_m
        velocity = q / area
        de = 2 * width_m * depth_m / (width_m + depth_m)
        pressure_loss = round(0.1091 * (velocity ** 1.9), 2)  # simplified

        # Feedback
        velocity_msg = "✅ Good (within typical range)"
        if velocity < 4:
            velocity_msg = "⚠️ Low velocity (might be inefficient)"
        elif velocity > 10:
            velocity_msg = "❌ High velocity (risk of noise/pressure)"

        # Pressure class suggestion (based on velocity only for now)
        pressure_class = "Low Pressure (< 750 Pa)" if pressure_loss < 0.75 else "Medium Pressure (> 750 Pa)"

        st.subheader("Results")
        st.write(f"Aspect Ratio: {aspect_ratio:.2f}")
        st.write(f"Area: {area:.4f} m²")
        st.write(f"Velocity: {velocity:.2f} m/s ({velocity_msg})")
        st.write(f"Hydraulic Diameter: {de * 1000:.0f} mm")
        st.write(f"Duct Pressure Loss: {pressure_loss} Pa/m")
        st.write(f"Suggested Pressure Class: {pressure_class}")

        # Save results
        df = pd.DataFrame([{
            "Airflow (L/s)": q,
            "Width (mm)": width_m * 1000,
            "Depth (mm)": depth_m * 1000,
            "Velocity (m/s)": round(velocity, 2),
            "Pressure Loss (Pa/m)": pressure_loss,
            "Hydraulic Diameter (mm)": round(de * 1000),
            "Aspect Ratio": round(aspect_ratio, 2)
        }])

        st.download_button("Download Results as CSV", df.to_csv(index=False), file_name="duct_calculation.csv")

    except Exception as e:
        st.error(f"Calculation error: {e}")