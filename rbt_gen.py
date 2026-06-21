def generate():
    out = """// src/fairness/rbtree.npk
// Red-Black Tree for CFS Scheduling

use "../structs/memory_helpers.npk".*;

pub struct:RBTree = {
    int32: root;
    int32: leftmost;
    int32: capacity;
    int32: free_head;
};

pub func:rbt_init = RBTree->(int32: cap) {
    int64: bytes = 16 + (raw int32_to_int64(cap) * 40);
    RBTree->: tree = calloc(1, bytes) => RBTree->;
    int64: base = raw ptr_to_int(tree => any->);
    drop write_int32(base + 0, -1);
    drop write_int32(base + 4, -1);
    drop write_int32(base + 8, cap);
    drop write_int32(base + 12, 0);
    
    int32: i = 0;
    while (i < cap) {
        int64: ptr = base + 16 + (raw int32_to_int64(i) * 40);
        int32: next = i + 1;
        if (next == cap) { next = -1; }
        drop write_int32(ptr + 36, next);
        i = i + 1;
    }
    pass tree;
};

pub func:get_ptr = int64(RBTree->:tree, int32: idx) {
    int64: base = raw ptr_to_int(tree => any->);
    pass base + 16 + (raw int32_to_int64(idx) * 40);
};

pub func:get_left = int32(RBTree->:tree, int32: n) { if (n == -1) { pass -1; } pass raw read_int32(raw get_ptr(tree, n) + 0); };
pub func:set_left = NIL(RBTree->:tree, int32: n, int32: val) { if (n != -1) { drop write_int32(raw get_ptr(tree, n) + 0, val); } pass NIL; };

pub func:get_right = int32(RBTree->:tree, int32: n) { if (n == -1) { pass -1; } pass raw read_int32(raw get_ptr(tree, n) + 4); };
pub func:set_right = NIL(RBTree->:tree, int32: n, int32: val) { if (n != -1) { drop write_int32(raw get_ptr(tree, n) + 4, val); } pass NIL; };

pub func:get_parent = int32(RBTree->:tree, int32: n) { if (n == -1) { pass -1; } pass raw read_int32(raw get_ptr(tree, n) + 8); };
pub func:set_parent = NIL(RBTree->:tree, int32: n, int32: val) { if (n != -1) { drop write_int32(raw get_ptr(tree, n) + 8, val); } pass NIL; };

pub func:get_color = int32(RBTree->:tree, int32: n) { if (n == -1) { pass 0; } pass raw read_int32(raw get_ptr(tree, n) + 12); };
pub func:set_color = NIL(RBTree->:tree, int32: n, int32: val) { if (n != -1) { drop write_int32(raw get_ptr(tree, n) + 12, val); } pass NIL; };

pub func:get_vruntime = int64(RBTree->:tree, int32: n) { if (n == -1) { pass 0; } pass raw read_int64(raw get_ptr(tree, n) + 16); };
pub func:set_vruntime = NIL(RBTree->:tree, int32: n, int64: val) { if (n != -1) { drop write_int64(raw get_ptr(tree, n) + 16, val); } pass NIL; };

pub func:get_pid = int64(RBTree->:tree, int32: n) { if (n == -1) { pass 0; } pass raw read_int64(raw get_ptr(tree, n) + 24); };
pub func:set_pid = NIL(RBTree->:tree, int32: n, int64: val) { if (n != -1) { drop write_int64(raw get_ptr(tree, n) + 24, val); } pass NIL; };

pub func:get_tcb = int32(RBTree->:tree, int32: n) { if (n == -1) { pass -1; } pass raw read_int32(raw get_ptr(tree, n) + 32); };
pub func:set_tcb = NIL(RBTree->:tree, int32: n, int32: val) { if (n != -1) { drop write_int32(raw get_ptr(tree, n) + 32, val); } pass NIL; };

pub func:get_root = int32(RBTree->:tree) { pass raw read_int32(raw ptr_to_int(tree => any->) + 0); };
pub func:set_root = NIL(RBTree->:tree, int32: val) { drop write_int32(raw ptr_to_int(tree => any->) + 0, val); pass NIL; };

pub func:rbt_alloc = int32(RBTree->:tree) {
    int64: base = raw ptr_to_int(tree => any->);
    int32: free_head = raw read_int32(base + 12);
    if (free_head == -1) { pass -1; }
    
    int64: ptr = raw get_ptr(tree, free_head);
    drop write_int32(base + 12, raw read_int32(ptr + 36));
    
    drop set_left(tree, free_head, -1);
    drop set_right(tree, free_head, -1);
    drop set_parent(tree, free_head, -1);
    drop set_color(tree, free_head, 1); // Red
    pass free_head;
};

pub func:rbt_free = NIL(RBTree->:tree, int32: n) {
    if (n == -1) { pass NIL; }
    int64: base = raw ptr_to_int(tree => any->);
    int32: free_head = raw read_int32(base + 12);
    int64: ptr = raw get_ptr(tree, n);
    drop write_int32(ptr + 36, free_head);
    drop write_int32(base + 12, n);
    pass NIL;
};

pub func:rbt_compare = int32(RBTree->:tree, int32: a, int32: b) {
    int64: va = raw get_vruntime(tree, a);
    int64: vb = raw get_vruntime(tree, b);
    int32: cmp = va <=> vb;
    if (cmp != 0) { pass cmp; }
    pass raw get_pid(tree, a) <=> raw get_pid(tree, b);
};

pub func:rbt_rotate_left = NIL(RBTree->:tree, int32: x) {
    int32: y = raw get_right(tree, x);
    drop set_right(tree, x, raw get_left(tree, y));
    if (raw get_left(tree, y) != -1) {
        drop set_parent(tree, raw get_left(tree, y), x);
    }
    drop set_parent(tree, y, raw get_parent(tree, x));
    if (raw get_parent(tree, x) == -1) {
        drop set_root(tree, y);
    } else {
        if (x == raw get_left(tree, raw get_parent(tree, x))) {
            drop set_left(tree, raw get_parent(tree, x), y);
        } else {
            drop set_right(tree, raw get_parent(tree, x), y);
        }
    }
    drop set_left(tree, y, x);
    drop set_parent(tree, x, y);
    pass NIL;
};

pub func:rbt_rotate_right = NIL(RBTree->:tree, int32: x) {
    int32: y = raw get_left(tree, x);
    drop set_left(tree, x, raw get_right(tree, y));
    if (raw get_right(tree, y) != -1) {
        drop set_parent(tree, raw get_right(tree, y), x);
    }
    drop set_parent(tree, y, raw get_parent(tree, x));
    if (raw get_parent(tree, x) == -1) {
        drop set_root(tree, y);
    } else {
        if (x == raw get_right(tree, raw get_parent(tree, x))) {
            drop set_right(tree, raw get_parent(tree, x), y);
        } else {
            drop set_left(tree, raw get_parent(tree, x), y);
        }
    }
    drop set_right(tree, y, x);
    drop set_parent(tree, x, y);
    pass NIL;
};

pub func:rbt_insert_fixup_safe = NIL(RBTree->:tree, int32: z_in) {
    int32: z = z_in;
    bool: running = true;
    while (running) {
        int32: p = raw get_parent(tree, z);
        if (p == -1) { running = false; }
        if (running) {
            if (raw get_color(tree, p) == 0) { running = false; }
        }
        
        if (running) {
            int32: pp = raw get_parent(tree, p);
            if (pp == -1) { 
                running = false; 
            } else {
                bool: skip = false;
                if (p == raw get_left(tree, pp)) {
                    int32: y = raw get_right(tree, pp);
                    if (y != -1) {
                        if (raw get_color(tree, y) == 1) {
                            drop set_color(tree, p, 0);
                            drop set_color(tree, y, 0);
                            drop set_color(tree, pp, 1);
                            z = pp;
                            skip = true;
                        }
                    }
                    if (!skip) {
                        if (z == raw get_right(tree, p)) {
                            z = p;
                            drop rbt_rotate_left(tree, z);
                            p = raw get_parent(tree, z);
                            pp = raw get_parent(tree, p);
                        }
                        drop set_color(tree, p, 0);
                        drop set_color(tree, pp, 1);
                        drop rbt_rotate_right(tree, pp);
                    }
                } else {
                    int32: y = raw get_left(tree, pp);
                    if (y != -1) {
                        if (raw get_color(tree, y) == 1) {
                            drop set_color(tree, p, 0);
                            drop set_color(tree, y, 0);
                            drop set_color(tree, pp, 1);
                            z = pp;
                            skip = true;
                        }
                    }
                    if (!skip) {
                        if (z == raw get_left(tree, p)) {
                            z = p;
                            drop rbt_rotate_right(tree, z);
                            p = raw get_parent(tree, z);
                            pp = raw get_parent(tree, p);
                        }
                        drop set_color(tree, p, 0);
                        drop set_color(tree, pp, 1);
                        drop rbt_rotate_left(tree, pp);
                    }
                }
            }
        }
    }
    drop set_color(tree, raw get_root(tree), 0);
    pass NIL;
};

pub func:rbt_insert = int32(RBTree->:tree, int64: vruntime, int64: pid, int32: tcb_h) {
    int32: z = raw rbt_alloc(tree);
    if (z == -1) { pass -1; }
    
    drop set_vruntime(tree, z, vruntime);
    drop set_pid(tree, z, pid);
    drop set_tcb(tree, z, tcb_h);
    
    int32: y = -1;
    int32: x = raw get_root(tree);
    
    while (x != -1) {
        y = x;
        int32: cmp = raw rbt_compare(tree, z, x);
        if (cmp < 0) {
            x = raw get_left(tree, x);
        } else {
            x = raw get_right(tree, x);
        }
    }
    
    drop set_parent(tree, z, y);
    if (y == -1) {
        drop set_root(tree, z);
    } else {
        if (raw rbt_compare(tree, z, y) < 0) {
            drop set_left(tree, y, z);
        } else {
            drop set_right(tree, y, z);
        }
    }
    
    drop rbt_insert_fixup_safe(tree, z);
    
    // Update leftmost cache
    int64: base = raw ptr_to_int(tree => any->);
    int32: lm = raw read_int32(base + 4);
    if (lm == -1) {
        drop write_int32(base + 4, z);
    } else {
        if (raw rbt_compare(tree, z, lm) < 0) {
            drop write_int32(base + 4, z);
        }
    }
    pass z;
};

pub func:rbt_min = int32(RBTree->:tree, int32: node) {
    if (node == -1) { pass -1; }
    int32: current = node;
    bool: running = true;
    while (running) {
        int32: l = raw get_left(tree, current);
        if (l == -1) {
            running = false;
        } else {
            current = l;
        }
    }
    pass current;
};

pub func:rbt_peek_min = int32(RBTree->:tree) {
    int64: base = raw ptr_to_int(tree => any->);
    pass raw read_int32(base + 4);
};

pub func:rbt_transplant = NIL(RBTree->:tree, int32: u, int32: v) {
    int32: p = raw get_parent(tree, u);
    if (p == -1) {
        drop set_root(tree, v);
    } else {
        if (u == raw get_left(tree, p)) {
            drop set_left(tree, p, v);
        } else {
            drop set_right(tree, p, v);
        }
    }
    if (v != -1) {
        drop set_parent(tree, v, p);
    }
    pass NIL;
};

pub func:rbt_extract_min = int32(RBTree->:tree) {
    int64: base = raw ptr_to_int(tree => any->);
    int32: z = raw read_int32(base + 4); // leftmost
    if (z == -1) { pass -1; }
    
    int32: x = raw get_right(tree, z);
    drop rbt_transplant(tree, z, raw get_right(tree, z));
    
    int32: tcb_h = raw get_tcb(tree, z);
    drop rbt_free(tree, z);
    
    int32: root = raw get_root(tree);
    if (root == -1) {
        drop write_int32(base + 4, -1);
    } else {
        drop write_int32(base + 4, raw rbt_min(tree, root));
    }
    
    pass tcb_h;
};
"""
    with open("src/fairness/rbtree.npk", "w") as f:
        f.write(out)

generate()
