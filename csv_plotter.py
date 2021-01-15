import csv
import matplotlib.pyplot as plt


# Generate a plot for a metric in csv (0-based indexing)
def plot(csv_file_path, col_for_y_axis: int, plot_title: str,
         plot_y_label: str):
    x = []
    y = []
    with open(csv_file_path, 'r') as csvfile:
        plots = csv.reader(csvfile, skipinitialspace=True)
        for row in plots:
            x.append(row[0])  # post id, which is col 0 of csv
            y.append(float(row[col_for_y_axis]))
    plt.plot(x, y, marker='o')
    plt.title(plot_title)
    plt.xlabel('Post Id')
    plt.ylabel(plot_y_label)
    plt.show()
