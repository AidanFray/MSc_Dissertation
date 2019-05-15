with open("./target_keys.txt") as file:
    keys = file.readlines()

output = f"^{keys[0].strip()}"

for k in keys[1:]:
    output += f"|^{k.strip()}"

print(output)