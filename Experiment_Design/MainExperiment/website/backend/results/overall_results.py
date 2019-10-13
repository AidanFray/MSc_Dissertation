import os
import sys
import pickle

sys.path.append("..")

trick_attacks = {}
all_attacks = {}

def usage():
    print(f"Usage: python {__name__} <TARGET_DIR>")
    exit()


if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        usage()

    target_dir = sys.argv[1]

    for file in os.listdir(f"{target_dir}"):
        if file.endswith(".pkl"):
            
            filepath = target_dir + file

            exp = pickle.load(open(filepath, "rb"))

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
        print("\t", attackID, round(trick_attacks[attackID] / all_attacks[attackID] * 100, 2))