with open('tests/unit/test_queue.npk', 'w') as f:
    f.write("""use "../../src/structs/queue.npk".{TCBQueue, queue_init, queue_enqueue2, queue_dequeue, queue_remove};
use "../../src/structs/arena.npk".{TCBArena, TCBPtr, arena_init, tcb_arena_allocate, tcb_arena_get};
use "../../src/structs/handle.npk".IdxHandle;
use "../../src/structs/tcb.npk".TCB;

pub func:main = int32() {
    TCBArena: arena;
    arena.capacity = 1024;
    drop arena_init(@arena);

    TCBQueue: q;
    q.count = 0;
    drop queue_init(@q);

    Result<IdxHandle<TCB> >: rh1 = tcb_arena_allocate(@arena);
    if (rh1.is_error) { exit 100; }
    IdxHandle<TCB>: h1 = rh1.value;

    Result<IdxHandle<TCB> >: rh2 = tcb_arena_allocate(@arena);
    if (rh2.is_error) { exit 100; }
    IdxHandle<TCB>: h2 = rh2.value;

    Result<IdxHandle<TCB> >: rh3 = tcb_arena_allocate(@arena);
    if (rh3.is_error) { exit 100; }
    IdxHandle<TCB>: h3 = rh3.value;

    if (h1.index == -1) { exit 1; }
    if (h2.index == -1) { exit 2; }
    if (h3.index == -1) { exit 3; }

    Result<IdxHandle<TCB> >: rok1 = queue_enqueue2(@q, @arena, h1);
    if (rok1.is_error) { exit 100; }
    IdxHandle<TCB>: ok1 = rok1.value;
    if (ok1.index == -1) { exit 101; }

    Result<IdxHandle<TCB> >: rok2 = queue_enqueue2(@q, @arena, h2);
    if (rok2.is_error) { exit 100; }
    IdxHandle<TCB>: ok2 = rok2.value;
    if (ok2.index == -1) { exit 102; }

    Result<IdxHandle<TCB> >: rok3 = queue_enqueue2(@q, @arena, h3);
    if (rok3.is_error) { exit 100; }
    IdxHandle<TCB>: ok3 = rok3.value;
    if (ok3.index == -1) { exit 103; }

    if (q.count != 3) { exit 7; }
    if (q.head.index != h1.index) { exit 8; }
    if (q.tail.index != h3.index) { exit 9; }

    Result<TCBPtr>: rt1 = tcb_arena_get(@arena, h1);
    if (rt1.is_error) { exit 100; }
    TCB->: t1 = rt1.value.ptr;

    Result<TCBPtr>: rt2 = tcb_arena_get(@arena, h2);
    if (rt2.is_error) { exit 100; }
    TCB->: t2 = rt2.value.ptr;

    Result<TCBPtr>: rt3 = tcb_arena_get(@arena, h3);
    if (rt3.is_error) { exit 100; }
    TCB->: t3 = rt3.value.ptr;

    if (t1->prev.index != -1) { exit 10; }
    if (t1->next.index != h2.index) { exit 11; }

    if (t2->prev.index != h1.index) { exit 12; }
    if (t2->next.index != h3.index) { exit 13; }

    if (t3->prev.index != h2.index) { exit 14; }
    if (t3->next.index != -1) { exit 15; }

    Result<IdxHandle<TCB> >: rrm1 = queue_remove(@q, @arena, h2);
    if (rrm1.is_error) { exit 100; }
    IdxHandle<TCB>: rm1 = rrm1.value;
    if (rm1.index == -1) { exit 112; }
    if (q.count != 2) { exit 17; }

    Result<TCBPtr>: rt1_new = tcb_arena_get(@arena, h1);
    if (rt1_new.is_error) { exit 100; }
    TCB->: t1_new = rt1_new.value.ptr;

    Result<TCBPtr>: rt2_new = tcb_arena_get(@arena, h2);
    if (rt2_new.is_error) { exit 100; }
    TCB->: t2_new = rt2_new.value.ptr;

    Result<TCBPtr>: rt3_new = tcb_arena_get(@arena, h3);
    if (rt3_new.is_error) { exit 100; }
    TCB->: t3_new = rt3_new.value.ptr;

    if (t1_new->next.index != h3.index) { exit 18; }
    if (t3_new->prev.index != h1.index) { exit 19; }
    if (t2_new->next.index != -1) { exit 20; }
    if (t2_new->prev.index != -1) { exit 21; }

    Result<IdxHandle<TCB> >: rdh1 = queue_dequeue(@q, @arena);
    if (rdh1.is_error) { exit 100; }
    IdxHandle<TCB>: dh1 = rdh1.value;
    if (dh1.index != h1.index) { exit 21; }
    if (q.count != 1) { exit 22; }

    Result<IdxHandle<TCB> >: rdh2 = queue_dequeue(@q, @arena);
    if (rdh2.is_error) { exit 100; }
    IdxHandle<TCB>: dh2 = rdh2.value;
    if (dh2.index != h3.index) { exit 23; }
    if (q.count != 0) { exit 24; }

    Result<IdxHandle<TCB> >: rdh3 = queue_dequeue(@q, @arena);
    if (rdh3.is_error) { exit 100; }
    IdxHandle<TCB>: dh3 = rdh3.value;
    if (dh3.index != -1) { exit 25; }

    exit 0;
};

func:failsafe = int32(tbb32:err) {
    exit 1;
};
""")
