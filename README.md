# Force Data Processing and Visualization

This script processes and visualizes force data from multiple `.npz` files. It applies a lowpass Butterworth filter to the data, calculates the norm of the forces, and identifies peaks and troughs in the average force signal. The results are plotted for each leg.

## File Structure

The script expects the `.npz` files to be located in the `test/20240808_165323_good_flat_walk/` directory. The file paths are generated dynamically for six files corresponding to different legs.

## .npz File Format

Each `.npz` file contains the following data:
- `time`: An array of time stamps.
- `index_{j}`: Force measurements for different indices. The indices used in this script are `[2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15, 16]`.
There are 12 elements in the `index_{j}` array, corresponding to the x, y, z components of the force from 4 hall effect sensors.
The indices 2, 3, and 4, represent the forces in the x, y, and z directions for the first sensor, respectively.
The indices 6, 7, and 8, represent the forces in the x, y, and z directions for the second sensor, respectively.
The indices 10, 11, and 12, represent the forces in the x, y, and z directions for the third sensor, respectively.
The indices 14, 15, and 16, represent the forces in the x, y, and z directions for the fourth sensor, respectively.

The names of the indices are kind of confusing, but they are consistent with the data collected from the sensors which was streamed using UART and then captured in the `.npz` files.

## Script Overview

### Global Variables

- `file_paths`: List of file paths to the `.npz` files.
- `leg_names`: List of leg names corresponding to each file.
- `indices`: List of indices to extract force data.
- `fig, axs`: Matplotlib figure and axes for plotting.
- `forces`: List to store force measurements.
- `plot_start_time`: Start time for plotting in seconds.

### Functions

#### `butter_lowpass(cutoff, fs, order=5)`

Designs a lowpass Butterworth filter.

#### `lowpass_filter(data, cutoff, fs, order=5)`

Applies a lowpass Butterworth filter to the data.

#### `find_norm(forces, offset)`

Calculates the norm (magnitude) of the forces for each leg.

#### `find_peaks_troughs(force_avg)`

Finds the peaks and troughs in the average force signal.

#### `find_swing_stance(force_avg)`

Determines the swing and stance phases based on the average force signal.

#### `process_file(file_path, indices, leg_name, ax)`

Processes a single file to extract and plot force data.

### Main Function

The `main()` function processes all files and plots the results.

## Usage

To run the script, execute the following command:

```bash
./script_name.py