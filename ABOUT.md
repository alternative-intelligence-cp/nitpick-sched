# About `nitpick-sched`

`nitpick-sched` is the flagship native scheduler for the Nitpick ecosystem and the Nikola AGI substrate. It is designed to handle mixed-criticality systems with absolute mathematical determinism and memory safety.

## Architecture Highlights
- **Hybrid Proportional Fairness:** Synthesizes the Linux Completely Fair Scheduler (CFS) for robust load balancing with the FreeBSD ULE interactivity heuristics for tactile responsiveness.
- **Temporal Isolation:** Implements seL4 MCS Sporadic Servers with precise budget and period tracking to prevent priority inversion and guarantee hard real-time execution bounds.
- **Lock-Free Work Stealing:** Utilizes Chase-Lev dynamic circular deques per processor to maximize Symmetric Multiprocessing (SMP) throughput while maintaining processor affinity.
- **Deterministic Foundation:** Employs `fix256` fixed-point arithmetic instead of floating-point numbers to ensure bit-exact, cross-platform deterministic physics propagation.
- **M:N Threading Model:** Fuses cooperative user-space coroutines with preemptive OS-level threads, providing zero-cost context switching with a hard preemptive backstop.
