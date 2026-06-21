with open('src/structs/queue.npk', 'w') as f:
    f.write("""
use "arena.npk".{TCBArena, TCBPtr, arena_init, tcb_arena_allocate, tcb_arena_get};

pub struct:TCBQueue = {
    IdxHandle<TCB>: head;
    IdxHandle<TCB>: tail;
    int64: count;
};

pub func:queue_init = NIL(TCBQueue->:q) {
    IdxHandle<TCB>: invalid;
    invalid.index = -1;
    invalid.generation = 0;

    q->head = invalid;
    q->tail = invalid;
    q->count = 0;
    pass NIL;
};

pub func:queue_enqueue2 = IdxHandle<TCB>(TCBQueue->:q, TCBArena->:arena, IdxHandle<TCB>:handle) {
    IdxHandle<TCB>: invalid;
    invalid.index = -1;
    invalid.generation = 0;

    if (q->count < 0) { 
        pass invalid; 
    }

    Result<TCBPtr>: rtcb = tcb_arena_get(arena, handle);
    if (rtcb.is_error) { pass invalid; }
    TCB->: tcb = rtcb.value.ptr;
    
    IdxHandle<TCB>: tail_cpy = q->tail;
    tcb->prev = tail_cpy;
    tcb->next = invalid;

    if (tail_cpy.index != -1) {
        Result<TCBPtr>: rtail = tcb_arena_get(arena, tail_cpy);
        if (rtail.is_error) { pass invalid; }
        TCB->: tail_tcb = rtail.value.ptr;
        tail_tcb->next = handle;
    } else {
        q->head = handle;
    }

    q->tail = handle;
    q->count = q->count + 1;

    pass handle;
};

pub func:queue_dequeue = IdxHandle<TCB>(TCBQueue->:q, TCBArena->:arena) {
    IdxHandle<TCB>: invalid;
    invalid.index = -1;
    invalid.generation = 0;

    IdxHandle<TCB>: head_cpy = q->head;
    if (head_cpy.index == -1) {
        pass invalid;
    }

    Result<TCBPtr>: rtcb = tcb_arena_get(arena, head_cpy);
    if (rtcb.is_error) { pass invalid; }
    TCB->: tcb = rtcb.value.ptr;

    IdxHandle<TCB>: tcb_next_cpy = tcb->next;
    q->head = tcb_next_cpy;

    if (tcb_next_cpy.index != -1) {
        Result<TCBPtr>: rnext = tcb_arena_get(arena, tcb_next_cpy);
        if (rnext.is_error) { pass invalid; }
        TCB->: next_tcb = rnext.value.ptr;
        next_tcb->prev = invalid;
    } else {
        q->tail = invalid;
    }

    tcb->prev = invalid;
    tcb->next = invalid;

    q->count = q->count - 1;

    pass head_cpy;
};

pub func:queue_remove = IdxHandle<TCB>(TCBQueue->:q, TCBArena->:arena, IdxHandle<TCB>:handle) {
    IdxHandle<TCB>: invalid;
    invalid.index = -1;
    invalid.generation = 0;

    Result<TCBPtr>: rtcb = tcb_arena_get(arena, handle);
    if (rtcb.is_error) { pass invalid; }
    TCB->: tcb = rtcb.value.ptr;
    if (tcb == NULL) {
        pass invalid;
    }

    IdxHandle<TCB>: prev_cpy = tcb->prev;
    IdxHandle<TCB>: next_cpy = tcb->next;

    if (prev_cpy.index != -1) {
        Result<TCBPtr>: rprev = tcb_arena_get(arena, prev_cpy);
        if (rprev.is_error) { pass invalid; }
        TCB->: prev_tcb = rprev.value.ptr;
        prev_tcb->next = next_cpy;
    } else {
        q->head = next_cpy;
    }

    if (next_cpy.index != -1) {
        Result<TCBPtr>: rnext = tcb_arena_get(arena, next_cpy);
        if (rnext.is_error) { pass invalid; }
        TCB->: next_tcb = rnext.value.ptr;
        next_tcb->prev = prev_cpy;
    } else {
        q->tail = prev_cpy;
    }

    tcb->next = invalid;
    tcb->prev = invalid;

    q->count = q->count - 1;
    pass handle;
};
""")
