from hashlib import sha3_256

MAX_NONCE = 18446744073709551615


def solve(
    block_hash: str,
    tx_id: str,
    difficulty: int,
):
    byte_hash = bytes(block_hash, "utf-8")
    # Function to calculate proof of work
    for nonce in range(0, 10000000):
        nonce = nonce.to_bytes(8, byteorder="big")
        new_key = b"Vega_SPAM_PoW" + byte_hash + tx_id + nonce
        hash_data = sha3_256(new_key).digest()

        if count_zeros(hash_data) >= difficulty:
            break

    nonce = int.from_bytes(nonce, byteorder="big")
    return nonce


def count_zeros(b):
    ret = 0
    for x in b:
        if x == 0:
            ret += 8
        else:
            if x & 128 != 0:
                break
            elif x & 64 != 0:
                ret += 1
                break
            elif x & 32 != 0:
                ret += 2
                break
            elif x & 16 != 0:
                ret += 3
                break
            elif x & 8 != 0:
                ret += 4
                break
            elif x & 4 != 0:
                ret += 5
                break
            elif x & 2 != 0:
                ret += 6
                break
            elif x & 1 != 0:
                ret += 7
                break
            break
    return ret
