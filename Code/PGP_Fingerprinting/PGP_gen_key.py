import gnupg

target_short_id = "FB65"

gpg = gnupg.GPG(gnupghome="./", options=["--debug-quick-random"])

def find_pair():

    while True:

        input_data = gpg.gen_key_input(key_type='RSA', key_length=1024, passphrase="1234")
        key = gpg.gen_key(input_data)
        fp = key.fingerprint

        if check_near_collisions(fp):
            print("Collision found!")
            print(gpg.export_keys(fp))
            exit()


def check_near_collisions(signature):
    short_id = signature[39:]
    if short_id == target_short_id:
        return True
    else:
        return False

def check_existsing_keys():

    for x in gpg.list_keys().fingerprints:
        if check_near_collisions(x):
            print("Collision found!")
            print(gpg.export_keys(x))
            exit()

check_existsing_keys()
find_pair()