import os
import sys
import pickle

sys.path.append("..")

trick_attacks = {}
all_attacks = {}

for file in os.listdir("."):
    if file.endswith(".pkl"):
        
        exp = pickle.load(open(file, "rb"))

        for i, attack in enumerate(exp.AttackSchema):
            if attack:

                attack_id = f"{attack[0]}-{attack[1]}"

                if not attack_id in all_attacks:
                    all_attacks[attack_id] = 1
                else:
                    all_attacks[attack_id] += 1

                # Checks if verified
                if exp.Responses[i] == "True":
                    
                    if not attack_id in trick_attacks:
                        trick_attacks[attack_id] = 1
                    else:
                        trick_attacks[attack_id] += 1
                
print("[*] Successful attacks (%): ")
for attackID in trick_attacks:
    print("\t", attackID, round(trick_attacks[attackID] / all_attacks[attackID], 2))