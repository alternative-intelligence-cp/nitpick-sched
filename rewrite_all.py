import os

with open('src/structs/arena.npk', 'r') as f:
    arena = f.read()
arena = arena.replace('''pub struct:TCBPtr = {
    TCB->: ptr;
    int64: padding;
};

pub struct:TCBArena = {''', 'pub struct:TCBArena = {')
arena = arena.replace('pub func:tcb_arena_get = TCBPtr(TCBArena->:arena, IdxHandle<TCB>:h)', 'pub func:tcb_arena_get = TCB->(TCBArena->:arena, IdxHandle<TCB>:h)')
arena = arena.replace('TCBPtr: res;', '')
arena = arena.replace('res.ptr = NULL; pass res;', 'pass NULL;')
arena = arena.replace('res.ptr = @(arena->slots[h.index].item);\n    pass res;', 'pass @(arena->slots[h.index].item);')
with open('src/structs/arena.npk', 'w') as f:
    f.write(arena)

with open('src/structs/queue.npk', 'r') as f:
    queue = f.read()
queue = queue.replace('use "arena.npk".{TCBArena, TCBPtr, arena_init, tcb_arena_allocate, tcb_arena_get};', 'use "arena.npk".{TCBArena, arena_init, tcb_arena_allocate, tcb_arena_get};')
queue = queue.replace('Result<TCBPtr>: rtcb', 'Result<TCB->>: rtcb')
queue = queue.replace('rtcb.value.ptr', 'rtcb.value')
queue = queue.replace('Result<TCBPtr>: rtail', 'Result<TCB->>: rtail')
queue = queue.replace('rtail.value.ptr', 'rtail.value')
queue = queue.replace('Result<TCBPtr>: rnext', 'Result<TCB->>: rnext')
queue = queue.replace('rnext.value.ptr', 'rnext.value')
queue = queue.replace('Result<TCBPtr>: rprev', 'Result<TCB->>: rprev')
queue = queue.replace('rprev.value.ptr', 'rprev.value')
with open('src/structs/queue.npk', 'w') as f:
    f.write(queue)

with open('tests/unit/test_queue.npk', 'r') as f:
    test_queue = f.read()
test_queue = test_queue.replace('use "../../src/structs/arena.npk".{TCBArena, TCBPtr, arena_init, tcb_arena_allocate, tcb_arena_get};', 'use "../../src/structs/arena.npk".{TCBArena, arena_init, tcb_arena_allocate, tcb_arena_get};')
test_queue = test_queue.replace('Result<TCBPtr>:', 'Result<TCB->>:')
test_queue = test_queue.replace('.value.ptr', '.value')
with open('tests/unit/test_queue.npk', 'w') as f:
    f.write(test_queue)

