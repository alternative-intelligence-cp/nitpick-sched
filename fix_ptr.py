with open("src/fairness/rbtree.npk", "r") as f:
    content = f.read()

content = content.replace("idx * 40", "int64(idx) * 40")
content = content.replace("i * 40", "int64(i) * 40")

with open("src/fairness/rbtree.npk", "w") as f:
    f.write(content)
