#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import butter, filtfilt

# Define a function to create a Butterworth low-pass filter
def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

# Define a function to apply the low-pass filter
def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# List of file paths
file_paths = [f'test/20240808_164938_terrain/data__dev_ttyACM{i}.npz' for i in range(6)]
# file_paths = [f'test/20240808_165323_good_flat_walk/data__dev_ttyACM{i}.npz' for i in range(6)]

print(file_paths)
# Initialize a figure with 6 subplots
fig, axs = plt.subplots(6, 1, sharex=True, figsize=(10, 15))

#create list of forces from each device (for 6 devices, 12 forces each. 72 forces total)
forces = []
leg_names = ['L1', 'L2', 'L3', 'R1', 'R2', 'R3']
indices = [2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15, 16]  # Indices to print


# Loop through each file and plot the data
for i, file_path in enumerate(file_paths):
    print(file_path)
    # Load the data from the .npz file
    data = np.load(file_path)
    
    # Extract time and force magnitude fields
    time = data['time'] - data['time'][0] # Normalize time to start at 0

    #find average sampling rate
    sampling_rate = 1/np.mean(np.diff(time))
    # print(f'Sampling rate: {sampling_rate} Hz')

    
    #loop through data and plot each force
    for j in indices:
        # print(j)
        force = data[f'index_{j}']
        forces.append(force)
        # axs[i].plot(time, force, label=f'Force {j}')

    hall_effect_sensor_offset = 12*i #offset for each group of 3 forces
    # #for each group of 3 forces, calculate the Euliclidean norm force
    norm_force1 = np.sqrt(forces[0+hall_effect_sensor_offset]**2 + forces[1+hall_effect_sensor_offset]**2 + forces[2+hall_effect_sensor_offset]**2)
    norm_force2 = np.sqrt(forces[3+hall_effect_sensor_offset]**2 + forces[4+hall_effect_sensor_offset]**2 + forces[5+hall_effect_sensor_offset]**2)
    norm_force3 = np.sqrt(forces[6+hall_effect_sensor_offset]**2 + forces[7+hall_effect_sensor_offset]**2 + forces[8+hall_effect_sensor_offset]**2)
    norm_force4 = np.sqrt(forces[9+hall_effect_sensor_offset]**2 + forces[10+hall_effect_sensor_offset]**2 + forces[11+hall_effect_sensor_offset]**2)

    #for each group of 3 forces, calculate the Manhatten norm force
    # norm_force1 = np.abs(forces[0+hall_effect_sensor_offset]) + np.abs(forces[1+hall_effect_sensor_offset]) + np.abs(forces[2+hall_effect_sensor_offset])
    # norm_force2 = np.abs(forces[3+hall_effect_sensor_offset]) + np.abs(forces[4+hall_effect_sensor_offset]) + np.abs(forces[5+hall_effect_sensor_offset])
    # norm_force3 = np.abs(forces[6+hall_effect_sensor_offset]) + np.abs(forces[7+hall_effect_sensor_offset]) + np.abs(forces[8+hall_effect_sensor_offset])
    # norm_force4 = np.abs(forces[9+hall_effect_sensor_offset]) + np.abs(forces[10+hall_effect_sensor_offset]) + np.abs(forces[11+hall_effect_sensor_offset])

    # Calculate the average force from the norm forces
    force_avg = (norm_force1 + norm_force2 + norm_force3 + norm_force4) / 4

    # Filtering
    # # apply a moving ave filter window size 200 to the average force 
    # window_size = 100
    # force_avg = np.convolve(force_avg, np.ones(window_size)/window_size, mode='same')

    # Apply a low-pass filter to the average force with a sampling frequency of sampling_rate
    force_avg = lowpass_filter(force_avg, int(sampling_rate/2)-1, int(sampling_rate))

    # Find peaks in the ave force data
    peaks, _ = find_peaks(force_avg)
    
    #Find troughs in the ave force data
    inverted_force_avg = -force_avg
    troughs, _ = find_peaks(inverted_force_avg)

    #plotting

    #find the index of time that starts at 76s
    plot_time_offset = np.where(time >= 0)[0][0]
    

    #truncate the plots to start at 76s
    plotting_time = time[plot_time_offset:]

    #plot each norm force
    # axs[i].plot(time, norm_force1, label='Norm Force 1')
    # axs[i].plot(time, norm_force2, label='Norm Force 2')
    # axs[i].plot(time, norm_force3, label='Norm Force 3')
    # axs[i].plot(time, norm_force4, label='Norm Force 4')

    # Plot the average force starting after the plot_time_offset
    axs[i].plot(plotting_time, force_avg[plot_time_offset:], label='Average Force')

     # Adjust peaks and troughs indices to match the truncated plotting time
    adjusted_peaks = peaks[peaks >= plot_time_offset] - plot_time_offset
    adjusted_troughs = troughs[troughs >= plot_time_offset] - plot_time_offset

    # Plot peaks and troughs on the average force plot starting after the plot_time_offset
    axs[i].scatter(plotting_time[adjusted_peaks], force_avg[plot_time_offset:][adjusted_peaks], color='red', label='Peak')
    axs[i].scatter(plotting_time[adjusted_troughs], force_avg[plot_time_offset:][adjusted_troughs], color='green', label='Trough')

    #From global min and global max, find a threshold value 1/2 of the peak to peak value
    peak_to_peak = np.max(force_avg) - np.min(force_avg)
    threshold = np.min(force_avg) + peak_to_peak/(4)

    # Determine stance and swing phases
    stance = force_avg >= threshold
    swing = force_avg < threshold

    axs[i].fill_between(plotting_time, 0, 1, where=stance[plot_time_offset:], color='darkgray', alpha=0.5, transform=axs[i].get_xaxis_transform())
    axs[i].fill_between(plotting_time, 0, 1, where=swing[plot_time_offset:], color='lightgray', alpha=0.5, transform=axs[i].get_xaxis_transform())

    # Set the title and labels
    axs[i].set_title(f'Leg {leg_names[i]}')
    axs[i].set_ylabel('Force Magnitude')
    axs[i].legend()

# Set the x-axis label for the last subplot
axs[-1].set_xlabel('Time')

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()