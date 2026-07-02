import csv
import random


def get_positive_integer(message):
    while True:
        try:
            value = int(input(message))
            if value > 0:
                return value
            print("Please enter a positive integer.\n")
        except ValueError:
            print("Invalid input. Please enter an integer.\n")


def get_non_negative_integer(message):
    while True:
        try:
            value = int(input(message))
            if value >= 0:
                return value
            print("Please enter a non-negative integer.\n")
        except ValueError:
            print("Invalid input. Please enter an integer.\n")


print("=" * 55)
print("        CPU Scheduler Dataset Generator")
print("=" * 55)

n = get_positive_integer("Enter total number of processes: ")

filename = input("Enter output CSV filename: ").strip()

if not filename.endswith(".csv"):
    filename += ".csv"

print("\nArrival Time Configuration")

arrival_min = get_non_negative_integer("Minimum Arrival Time : ")
arrival_max = get_non_negative_integer("Maximum Arrival Time : ")

while arrival_min > arrival_max:
    print("\nMinimum Arrival Time cannot exceed Maximum Arrival Time.\n")
    arrival_min = get_non_negative_integer("Minimum Arrival Time : ")
    arrival_max = get_non_negative_integer("Maximum Arrival Time : ")

print("\nBurst Time Configuration")

burst_min = get_positive_integer("Minimum Burst Time : ")
burst_max = get_positive_integer("Maximum Burst Time : ")

while burst_min > burst_max:
    print("\nMinimum Burst Time cannot exceed Maximum Burst Time.\n")
    burst_min = get_positive_integer("Minimum Burst Time : ")
    burst_max = get_positive_integer("Maximum Burst Time : ")

processes = []

for _ in range(n):

    arrival = random.randint(arrival_min, arrival_max)
    burst = random.randint(burst_min, burst_max)
    priority = random.randint(1, 5)

    processes.append([arrival, burst, priority])

# Optional: sort by arrival time
processes.sort(key=lambda x: x[0])

with open(filename, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow(["Arrival", "Burst", "Priority"])

    writer.writerows(processes)

print("\n" + "=" * 55)
print("Dataset Generated Successfully")
print("=" * 55)

print(f"Processes Generated : {n}")
print(f"Arrival Time Range  : {arrival_min} - {arrival_max}")
print(f"Burst Time Range    : {burst_min} - {burst_max}")
print("Priority Range      : 1 - 5")
print(f"Output File         : {filename}")

print("=" * 55)