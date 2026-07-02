# Current Limitations

The proposed Adaptive Round Robin (ARR) scheduler has been designed to demonstrate dynamic quantum computation using a priority-weighted scheduling strategy. While the implementation successfully performs CPU scheduling and computes the standard scheduling metrics, several limitations remain that will be addressed in future versions.

1 Scalability of Arrival Handling

The current implementation repeatedly scans the complete process list to identify newly arrived processes during each scheduling cycle.

Limitation:
This approach introduces unnecessary computational overhead for large datasets, since the entire process list is traversed multiple times throughout execution.

Impact:
Execution time increases considerably as the number of processes grows (for example, workloads containing tens of thousands of processes).

Future Improvement:
Implement an event-driven arrival mechanism using a moving arrival pointer so that each process is examined only once.

2 Dynamic Quantum Computation Overhead

The adaptive time quantum is recalculated before every scheduling decision by iterating through the entire ready queue.

Limitation:
Although this ensures that the quantum accurately reflects the current workload, the repeated traversal of the ready queue increases scheduling overhead.

Impact:
The computational cost grows with the size of the ready queue, especially for large workloads.

Future Improvement:
Introduce quantum caching so that recalculation occurs only when the ready queue changes due to process arrival or completion.

3 Console Debug Output

During development, the scheduler prints every dynamically computed quantum value.

Limitation:
Console input/output operations are significantly slower than in-memory computations.

Impact:
Extensive debug printing considerably increases execution time for large scheduling simulations.

Future Improvement:
Replace direct console printing with configurable logging levels, allowing detailed debugging information to be enabled or disabled as required.

4 Visualization of Large Workloads

The scheduler generates detailed Gantt charts and performance graphs for every execution.

Limitation:
Graphical rendering libraries such as Matplotlib are not optimized for visualizing extremely large scheduling traces containing thousands or millions of execution segments.

Impact:
Visualization becomes the dominant contributor to execution time for very large datasets.

Future Improvement:
Automatically disable detailed visualization beyond a configurable process threshold and instead generate summarized performance graphs.

5 Execution Trace Storage

Every CPU allocation is stored for later Gantt chart generation.

Limitation:
Long-running simulations generate very large execution traces.

Impact:
Although memory usage remains manageable, storing every execution interval increases processing and visualization time.

Future Improvement:
Provide optional trace compression or selective trace recording modes.

6 Current Optimization Strategy

The scheduler currently emphasizes scheduling quality over computational efficiency.

Limitation:
The implementation prioritizes accurate adaptive quantum computation instead of minimizing scheduling overhead.

Impact:
Large-scale workloads may require significantly longer execution times compared to optimized production schedulers.

Future Improvement:
Introduce additional algorithmic optimizations while preserving the adaptive scheduling policy.
