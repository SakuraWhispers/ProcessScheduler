import csv
from operator import add
import time #addition
import matplotlib.pyplot as plt
from collections import deque

class Process:
    def __init__(self, pid, at, bt, priority):
        self.pid = pid
        self.at = at
        self.bt = bt
        self.rt = bt #remaining time
        self.priority = priority
        self.ct = 0  #completion time
        self.tat = 0 #turnaround time
        self.wt = 0  #waiting time
        self.rt_time = -1  # first response time


def compute_quantum(queue, processes):
    if not queue:
        return 0

    weighted_sum = 0
    total_weight = 0

    for i in queue:
        if processes[i].rt > 0:
            # inverse priority 
            weight = 1 / (processes[i].priority + 1e-6)

            weighted_sum += processes[i].rt * weight
            total_weight += weight

    if total_weight == 0:
        return 1

    return max(1, int(weighted_sum / total_weight))

def read_processes_from_csv(filename):
    processes = []

    with open(filename, newline="") as file:
        reader = csv.DictReader(file)

        for i, row in enumerate(reader, start=1):
            processes.append(
                Process(
                    i,                              # Auto-generated PID
                    int(row["Arrival"]),
                    int(row["Burst"]),
                    int(row["Priority"])
                )
            )

    return processes

def adaptive_rr(processes):
    print("Scheduler Started")
    
    
    processes.sort(key=lambda x: x.at)
    
    n = len(processes)
    time = 0
    completed = 0

    ready_queue = deque()
    in_queue = [False] * n
    gantt = []

    benchmark = {
        #cpu data
        "busy_time": 0,
        "idle_time": 0,

        #.......Scheduler statistics.......
        "context_switches": 0,
        "scheduler_cycles": 0,

        #.......quantum statistics....
        "q_history": [],
        "quantum_updates": 0,

        # ---------- Timing ----------
        "execution_time": 0.0,
        "time": 0,

        # ---------- Reserved for Future(hopefully) ----------
        "memory_usage": 0,
        "throughput": 0,
        "cpu_utilization": 0
    } #variables used for benchmarking being placed as dictionart type 
      #later migrate to a class based or function based system, prelim test now
   
    print(f"Time={time}, Queue={list(ready_queue)}, Completed={completed}")

    # Adding first process
    ready_queue.append(0)
    in_queue[0] = True

    while completed < n:

        # If queue empty -> CPU idle
        if not ready_queue:
            time += 1
            for i in range(n):
                if processes[i].at <= time and processes[i].rt > 0 and not in_queue[i]:
                    ready_queue.append(i)
                    in_queue[i] = True
            continue

        idx = ready_queue.popleft()

        # Dynamic quantum calc
        q = compute_quantum(list(ready_queue), processes)
        print("quanta value\n", q)
        if q == 0:
            q = processes[idx].rt
            benchmark["q_history"].append(q)
            benchmark["quantum_updates"] += 1

        exec_time = min(q, processes[idx].rt)


        # Response time
        if processes[idx].rt_time == -1:
            processes[idx].rt_time = time - processes[idx].at

        # Gantt entry
        gantt.append((f"P{processes[idx].pid}", time, time + exec_time))

        benchmark["busy_time"] += exec_time #add

        
        processes[idx].rt -= exec_time

        # Adding newly arrived processes
        for i in range(n):
            if processes[i].at <= time and processes[i].rt > 0 and not in_queue[i]:
                ready_queue.append(i)
                in_queue[i] = True

        # Reinsert if not finished
        if processes[idx].rt > 0:
            ready_queue.append(idx)
        else:
            processes[idx].ct = time
            completed += 1
    

    return gantt, benchmark #modified 2

def calculate_metrics(processes):
    total_wt, total_tat = 0, 0

    print("\n"
      f"{'PID':<6}{'AT':<6}{'BT':<15}{'CT':<15}{'TAT':<15}{'WT':<15}{'RT':<15}{'PR':<6}")

    for p in processes:
        p.tat = p.ct - p.at
        p.wt = p.tat - p.bt

        total_wt += p.wt
        total_tat += p.tat

        print(f"{p.pid:<6}"
              f"{p.at:<6}"
              f"{p.bt:<15}"
              f"{p.ct:<15}"
              f"{p.tat:<15}"
              f"{p.wt:<15}"
              f"{p.rt_time:<15}"
              f"{p.priority:<6}")

    print("\nAverage WT:", total_wt / len(processes))
    print("Average TAT:", total_tat / len(processes))

def plot_gantt(gantt):
    plt.figure()

    for i, (pid, start, end) in enumerate(gantt):
        plt.barh(0, end - start, left=start)
        plt.text((start + end)/2, 0, pid, ha='center', va='center')

    plt.yticks([])
    plt.xlabel("Time")
    plt.title("Gantt Chart (Adaptive RR)")
    plt.show()

def plot_metrics(processes):
    pids = [f"P{p.pid}" for p in processes]
    wt = [p.wt for p in processes]
    tat = [p.tat for p in processes]

    plt.figure()
    plt.bar(pids, wt)
    plt.title("Waiting Time vs Process")
    plt.show()

    plt.figure()
    plt.bar(pids, tat)
    plt.title("Turnaround Time vs Process")
    plt.show()

if __name__ == "__main__":
    print("Choose Input Method")
    print("1. Manual")
    print("2. CSV File")

choice = input("Enter choice: ")

if choice == "1":

    n = int(input("Enter total number of processes: "))
    processes = []

    for i in range(n):

        at = int(input(f"Arrival Time of P{i+1}: "))
        bt = int(input(f"Burst Time of P{i+1}: "))

        while True:
            priority = int(input(f"Priority of P{i+1} (1-5): "))
            if 1 <= priority <= 5:
                break
            print("Priority must be between 1 and 5.")

        processes.append(Process(i+1, at, bt, priority))

elif choice == "2":

    filename = input("Enter CSV filename: ")
    processes = read_processes_from_csv(filename)

else:
    print("Invalid Choice")
    exit()

scheduler_start = time.perf_counter() #addition
    
gantt, benchmark = adaptive_rr(processes)#add

scheduler_end = time.perf_counter() #add start

scheduler_time = scheduler_end - scheduler_start #add end

calculate_metrics(processes)

total_time = max(p.ct for p in processes)

cpu_utilization = (benchmark["busy_time"] / total_time) * 100

print(
    f"Average Quantum : "
    f"{sum(benchmark['q_history']) / len(benchmark['q_history']):.2f}"
)#modification

print(f"Minimum Quantum : {min(benchmark['q_history'])}")#modifiation

print(f"Maximum Quantum : {max(benchmark['q_history'])}")#modification

print(
    f"Quantum Recalculations : "
    f"{benchmark['quantum_updates']}"
)#modification


print(f"CPU Utilization : {cpu_utilization:.2f}%")

print(gantt)

plot_gantt(gantt)

plot_metrics(processes)