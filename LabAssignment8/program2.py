src = input("Enter source file name: ")
dst = input("Enter destination file name: ")

with open(src, "r") as f:
    lines = f.readlines()

cleaned = []
for line in lines:
    stripped = line.strip()
    if not stripped.startswith("#"):
        if "#" in line:
            line = line.split("#")[0] + "\n"
        cleaned.append(line)

with open(dst, "w") as f:
    f.writelines(cleaned)

print("\nSource File Content:")
with open(src, "r") as f:
    print(f.read())

print("\nDestination File Content:")
with open(dst, "r") as f:
    print(f.read())