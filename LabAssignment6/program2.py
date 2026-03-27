def capitalize_lines():
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break
    for line in lines:
        print(line.upper())

capitalize_lines()