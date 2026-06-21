with open('src/structs/queue.npk', 'w') as f:
    f.write("""
use "arena.npk".{TCBArena, arena_init, tcb_arena_allocate, tcb_arena_get};

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

    if (q->count < 0) { pass invalid; }
    if (handle.index < 0) { pass invalid; }
    if (handle.index >= 1024) { pass invalid; }
    if (!arena->slots[handle.index].occupied) { pass invalid; }
    if (arena->slots[handle.index].generation != handle.generation) { pass invalid; }
    
    IdxHandle<TCB>: tail_cpy = q->tail;
    arena->slots[handle.index].item.prev = tail_cpy;
    arena->slots[handle.index].item.next = invalid;

    if (tail_cpy.index != -1) {
        if (tail_cpy.index >= 0) {
            if (tail_cpy.index < 1024) {
                arena->slots[tail_cpy.index].item.next = handle;
            }
        }
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

    if (head_cpy.index < 0) { pass invalid; }
    if (head_cpy.index >= 1024) { pass invalid; }

    IdxHandle<TCB>: tcb_next_cpy = arena->slots[head_cpy.index].item.next;
    q->head = tcb_next_cpy;

    if (tcb_next_cpy.index != -1) {
        if (tcb_next_cpy.index >= 0) {
            if (tcb_next_cpy.index < 1024) {
                arena->slots[tcb_next_cpy.index].item.prev = invalid;
            }
        }
    } else {
        q->tail = invalid;
    }

    arena->slots[head_cpy.index].item.prev = invalid;
    arena->slots[head_cpy.index].item.next = invalid;

    q->count = q->count - 1;

    pass head_cpy;
};

pub func:queue_remove = IdxHandle<TCB>(TCBQueue->:q, TCBArena->:arena, IdxHandle<TCB>:handle) {
    IdxHandle<TCB>: invalid;
    invalid.index = -1;
    invalid.generation = 0;

    if (handle.index < 0) { pass invalid; }
    if (handle.index >= 1024) { pass invalid; }

    IdxHandle<TCB>: prev_cpy = arena->slots[handle.index].item.prev;
    IdxHandle<TCB>: next_cpy = arena->slots[handle.index].item.next;

    if (prev_cpy.index != -1) {
        if (prev_cpy.index >= 0) {
            if (prev_cpy.index < 1024) {
                arena->slots[prev_cpy.index].item.next = next_cpy;
            }
        }
    } else {
        q->head = next_cpy;
    }

    if (next_cpy.index != -1) {
        if (next_cpy.index >= 0) {
            if (next_cpy.index < 1024) {
                arena->slots[next_cpy.index].item.prev = prev_cpy;
            }
        }
    } else {
        q->tail = prev_cpy;
    }

    arena->slots[handle.index].item.next = invalid;
    arena->slots[handle.index].item.prev = invalid;

    q->count = q->count - 1;
    pass handle;
};
""")
