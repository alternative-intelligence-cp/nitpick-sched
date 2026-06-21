with open("src/fairness/cfs_math.npk", "r") as f: content = f.read()
content = content.replace("i64.0fix256", ".0fix256")
with open("src/fairness/cfs_math.npk", "w") as f: f.write(content)

with open("src/smp/topology.npk", "r") as f: content = f.read()
content = content.replace("pass(0i64);", "pass(0i32);")
with open("src/smp/topology.npk", "w") as f: f.write(content)

with open("src/isolation/replenish.npk", "r") as f: content = f.read()
content = content.replace("pass(0i64);", "pass(0i32);")
content = content.replace("pass(1i64);", "pass(1i32);")
with open("src/isolation/replenish.npk", "w") as f: f.write(content)

with open("src/smp/rebalance.npk", "r") as f: content = f.read()
content = content.replace("npk_shim_atomic_thread_fence(1i64)", "npk_shim_atomic_thread_fence(1i32)")
content = content.replace("npk_shim_atomic_thread_fence(0i64)", "npk_shim_atomic_thread_fence(0i32)")
content = content.replace("chase_lev_push(dq, 0i64)", "chase_lev_push(dq, 0i32)")
content = content.replace("chase_lev_push(dq, 1i64)", "chase_lev_push(dq, 1i32)")
with open("src/smp/rebalance.npk", "w") as f: f.write(content)
