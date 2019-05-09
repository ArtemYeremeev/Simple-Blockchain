import json
import os
import hashlib

blockchain_dir = os.curdir + '/block_list/'

def gen_hash(filename):
    file = open(blockchain_dir + filename, 'rb').read()
    return hashlib.md5(file).hexdigest()


def get_files():
    files = os.listdir(blockchain_dir)
    return sorted([int(e) for e in files])


def check_integrity():
    files = get_files()
    result = []
    for file in files[1:]:
        f = open(blockchain_dir + str(file))
        h = json.load(f)['hash']

        prev_object = str(file - 1)
        actual_hash = gen_hash(prev_object)

        if h == actual_hash:
            res = 'Ok'
        else:
            res = 'Corrupted'

        print('block {} is {}'.format(prev_object, res))

        result.append({'block': prev_object, 'result': res})

    return result

def create_object(name, amount, recipient, prev_hash=''):
    prev_file = files[-1]
    filename = str(prev_file + 1)

    prev_hash = gen_hash(str(prev_file))

    data = {"name": name,
            "amount": amount,
            "recipient": recipient,
            "hash": prev_hash}

    with open(blockchain_dir + filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    print(check_integrity())


if __name__ == "__main__":
    main()