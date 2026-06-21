# nitpick-sched

**Nitpick Native Scheduler**

A flagship, high-performance scheduler written natively in Nitpick for the Nikola AGI substrate and mixed-criticality systems. It synthesizes CFS proportional fairness, FreeBSD ULE interactivity heuristics, seL4 MCS sporadic servers, and lock-free Chase-Lev work-stealing deques.

See `ABOUT.md` for architectural details.

## Build Instructions

To build the scheduler matrix and formally verify the constraints via Z3, point the `npk` compiler at the primary scaffolding endpoint `init.npk`:

```bash
npk build src/core/init.npk
```

This will invoke the Nitpick compiler to verify all SMT solver invariants, resolve structural typings across the fair and isolation constraints, and natively compile the scheduler libraries.

## Usage

Include the `nitpick-sched` core package in your target Nitpick deployment:

```nitpick
use "nitpick-sched/src/core/scheduler.npk".*;
use "nitpick-sched/src/isolation/context.npk".*;
use "nitpick-sched/src/smp/chase_lev.npk".*;

// The main loop is exposed via:
// _? scheduler_tick(deque, tree, victim_deque, arena, rq);
```

Ensure all tasks correctly utilize `SchedulingContext` and are allocated using isolated `arena<TCB>@` instances.
