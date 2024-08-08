#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

# List of file paths
file_paths = [f'data__dev_ttyACM{i}.npz' for i in range(6)]

print(file_paths)
# Initialize a figure with 6 subplots
fig, axs = plt.subplots(6, 1, sharex=True, figsize=(10, 15))

# Loop through each file and plot the data
for i, file_path in enumerate(file_paths):
    print(file_path)
    # Load the data from the .npz file
    data = np.load(file_path)
    
    # Extract time and force magnitude fields
    time = data['time'] - data['time'][0] # Normalize time to start at 0
    force1 = data['index_2']
    force2 = data['index_7']
    force3 = data['index_10']
    force4 = data['index_15']

    # Take the average force between force1, force2, force3, and force4 for each time step
    force_avg = (force1 + force2 + force3 + force4) / 4

    # Calculate the threshold value
    threshold = (np.min(force_avg) + np.max(force_avg)) / 2.5

    # Determine stance and swing phases
    stance = force_avg >= threshold
    swing = force_avg < threshold

    # Plot the data on the corresponding subplot
    axs[i].plot(time, force1, label='Force 1')
    axs[i].plot(time, force2, label='Force 2')
    axs[i].plot(time, force3, label='Force 3')
    axs[i].plot(time, force4, label='Force 4')

    # Plot the average force
    axs[i].plot(time, force_avg, label='Average Force', color='black', linestyle='--')

    # Plot stance and swing phases
    axs[i].fill_between(time, 0, np.max(force_avg), where=stance, color='black', alpha=0.5, label='Stance')
    axs[i].fill_between(time, 0, np.max(force_avg), where=swing, color='lightgrey', alpha=0.5, label='Swing')
    
    # Set the title and labels
    axs[i].set_title(f'Device ACM{i}')
    axs[i].set_ylabel('Force Magnitude')
    axs[i].legend()

# Set the x-axis label for the last subplot
axs[-1].set_xlabel('Time')

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()