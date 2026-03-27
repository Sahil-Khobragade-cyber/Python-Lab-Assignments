s = input("Enter a string: ")

vowels = "aeiouAEIOU"
v = c = sp = low = 0

for ch in s:
    if ch in vowels:
        v += 1
    elif ch.isalpha():
        c += 1
    if ch == " ":
        sp += 1
    if ch.islower():
        low += 1

print("Number of Vowels:", v)
print("Number of Consonants:", c)
print("Number of Spaces:", sp)
print("Number of Lowercase Letters:", low)