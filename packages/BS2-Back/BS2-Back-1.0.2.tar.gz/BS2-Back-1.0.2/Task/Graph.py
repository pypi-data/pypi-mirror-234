import pandas as pd
import matplotlib.pyplot as plt
import time

# Set the interval between updates in seconds
update_interval = 5

path = "12 - Combined Score Output.csv"

# Read in CSV file
df = pd.read_csv(path)

# Create initial plot
fig, ax = plt.subplots()
ax.set_title('Score by Date')
ax.set_xlabel('Date')
ax.set_ylabel('Score')
line, = ax.plot(df['Date'], df['Score'])

while True:
    # Read in the updated CSV file
    df = pd.read_csv(path)

    # Group data by date and calculate average score
    df = df.groupby('Date')['Score'].mean().reset_index()

    # Update the plot data
    line.set_xdata(df['Date'])
    line.set_ydata(df['Score'])
    ax.relim()
    ax.autoscale_view()

    # Draw the updated plot
    fig.canvas.draw()

    # Wait for the specified interval before updating again
    time.sleep(update_interval)
    
