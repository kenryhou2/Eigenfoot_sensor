# import serial
# import matplotlib.pyplot as plt
# import numpy as np
# import time

# data_window = 40  # Number of data points to keep in the buffer
# update_point = 14  # Number of data points to plot before updating the plot
# # Set up the serial lines
# ser1 = serial.Serial('/dev/ttyACM0', 9600)
# ser2 = serial.Serial('/dev/ttyACM1', 9600)

# # Set up the figures for plotting
# plt.ion() 
# fig1 = plt.figure()
# ax1 = fig1.add_subplot(111)
# fig2 = plt.figure()
# ax2 = fig2.add_subplot(111)

# def run():
#     indices = [2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15, 16]  # Indices to print
#     data_buffer1 = [[] for _ in indices]  # Initialize a list of lists to store the latest 100 data points for each index
#     data_buffer2 = [[] for _ in indices]  # Initialize a list of lists to store the latest 100 data points for each index
#     counter = 0  # Initialize a counter to keep track of the number of data points

#     while True:
#         # Read the line from the first serial port
#         line1 = ser1.readline().decode('utf-8').strip()
#         data1 = list(map(float, line1.split('\t')))
#         # Select only the values at the specified indices
#         selected_data1 = [data1[i] for i in indices]
#         print(selected_data1)

#         # Read the line from the second serial port
#         line2 = ser2.readline().decode('utf-8').strip()
#         data2 = list(map(float, line2.split('\t')))
#         # Select only the values at the specified indices
#         selected_data2 = [data2[i] for i in indices]
#         print(selected_data2)

#         # Add the selected data to the buffer and keep only the latest 100 data points
#         for i, value in enumerate(selected_data1):
#             data_buffer1[i].append(value)
#             if len(data_buffer1[i]) > data_window:
#                 data_buffer1[i].pop(0)

#         for i, value in enumerate(selected_data2):
#             data_buffer2[i].append(value)
#             if len(data_buffer2[i]) > data_window:
#                 data_buffer2[i].pop(0)

#         counter += 1  # Increment the counter

#         # Only update the plot every 10 data points
#         if counter % update_point == 0:
#             # Clear the current figures
#             plt.figure(fig1.number)
#             plt.clf()
#             plt.figure(fig2.number)
#             plt.clf()

#             # Plot each trace
#             for i, data_trace in enumerate(data_buffer1):
#                 plt.figure(fig1.number)
#                 plt.plot(data_trace, label=f'Index {indices[i]}')
#             for i, data_trace in enumerate(data_buffer2):
#                 plt.figure(fig2.number)
#                 plt.plot(data_trace, label=f'Index {indices[i]}')

#             # Adjust the Y axis to view all the data at once
#             plt.figure(fig1.number)
#             plt.ylim([min(value for data_trace in data_buffer1 for value in data_trace),
#                       max(value for data_trace in data_buffer1 for value in data_trace)])
#             plt.legend()
#             plt.figure(fig2.number)
#             plt.ylim([min(value for data_trace in data_buffer2 for value in data_trace),
#                       max(value for data_trace in data_buffer2 for value in data_trace)])
#             plt.legend()

#             # Redraw the figures
#             plt.figure(fig1.number)
#             plt.draw()
#             plt.pause(0.01)
#             plt.figure(fig2.number)
#             plt.draw()
#             plt.pause(0.01)

# if __name__ == "__main__":
#     try:
#         run()
#     except KeyboardInterrupt:
#         # Close the serial connections
#         ser1.close()
#         ser2.close()
#         print("Interrupted and serial connections closed.")



import serial
import matplotlib.pyplot as plt
import numpy as np
import time

# Set up the serial line
ser = serial.Serial('/dev/ttyACM4', 9600)

# Set up the figure for plotting
plt.ion() 
fig = plt.figure()
ax = fig.add_subplot(111)

def run():
    indices = [2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15, 16]  # Indices to print
    data_buffer = [[] for _ in indices]  # Initialize a list of lists to store the latest 100 data points for each index
    counter = 0  # Initialize a counter to keep track of the number of data points

    while True:
        # Read the line from the serial port
        line = ser.readline().decode('utf-8').strip()
        data = list(map(float, line.split('\t')))
        # Select only the values at the specified indices
        selected_data = [data[i] for i in indices]
        print(selected_data)

        # Add the selected data to the buffer and keep only the latest 100 data points
        for i, value in enumerate(selected_data):
            data_buffer[i].append(value)
            if len(data_buffer[i]) > 40:
                data_buffer[i].pop(0)

        counter += 1  # Increment the counter

        # Only update the plot every 10 data points
        if counter % 15 == 0:
            # Clear the current figure
            plt.clf()

            # Plot each trace
            for i, data_trace in enumerate(data_buffer):
                plt.plot(data_trace, label=f'Index {indices[i]}')

            # Adjust the Y axis to view all the data at once
            plt.ylim([min(value for data_trace in data_buffer for value in data_trace),
                      max(value for data_trace in data_buffer for value in data_trace)])

            # Add a legend
            # plt.legend()

            # Redraw the figure
            plt.draw()
            plt.pause(0.01)

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        # Close the serial connection
        ser.close()
        print("Interrupted and serial connection closed.")
