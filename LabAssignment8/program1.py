with open("input.txt", "r") as f:
    data = f.read()

with open("output.txt", "w") as f:
    f.write(data.upper())