import pandas as pd
import pywt
import numpy as np
import matplotlib.pyplot as plt

DATA_PATH = r'/Users/simon/Desktop/envs/troubleshooting/Emergence/project_folder/csv/outlier_corrected_movement_location/Example_1.csv'

df = pd.read_csv(DATA_PATH, index_col=0).dropna().reset_index(drop=True)
trajectory = df['Nose_x'].astype(int).values + 1j * df['Nose_y'].astype(int).values

# Increase the number of decomposition levels for finer time scales
levels = 5  # Adjust the number of decomposition levels as needed
coeffs = pywt.wavedec(trajectory, 'haar', level=levels)

# Create time values for the original data
time = np.linspace(0, len(trajectory), len(trajectory))

# Create time values for the Haar coefficients with finer scales
time_coeffs = [np.linspace(0, len(coeff), len(coeff)) for coeff in coeffs]

# Plot the original trajectory
plt.figure(figsize=(12, 6))
plt.subplot(levels + 2, 1, 1)
plt.title("Original Trajectory")
plt.plot(time, trajectory.real, label='x-coordinate')
plt.plot(time, trajectory.imag, label='y-coordinate')
plt.legend()

# Plot the Haar coefficients with finer scales
for i in range(levels + 1):
    plt.subplot(levels + 2, 1, i + 2)
    plt.title(f"Haar Scale {i + 1} Coefficients")
    plt.plot(time_coeffs[i], coeffs[i].real, label='x-coordinate')
    plt.plot(time_coeffs[i], coeffs[i].imag, label='y-coordinate')
    plt.legend()

plt.tight_layout()
plt.show()
