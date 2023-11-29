import hashlib
import matplotlib.pyplot as plt

def md5_hash(message):
    return hashlib.md5(message.encode()).hexdigest()

def change_bit(message, bit_position):
    byte_index = bit_position // 8
    if byte_index >= len(message):
        # Розширення тексту, якщо не вистачає символів для зміни біту
        message += ' ' * (byte_index - len(message) + 1)
    bit_index = bit_position % 8
    byte = ord(message[byte_index])
    mask = 1 << (7 - bit_index)
    changed_byte = byte ^ mask
    changed_char = chr(changed_byte)
    return message[:byte_index] + changed_char + message[byte_index + 1:]


def count_changed_bits(hash1, hash2):
    count = 0
    for ch1, ch2 in zip(hash1, hash2):
        diff = int(ch1, 16) ^ int(ch2, 16)
        count += bin(diff).count('1')
    return count

def visualize_rounds(bits_changed):
    plt.plot(range(1, len(bits_changed) + 1), bits_changed, marker='o')
    plt.xlabel('Round')
    plt.ylabel('Bits Changed')
    plt.title('Bits Changed in Hash per Round')
    plt.grid()
    plt.show()

def main():
    filename = 'message.txt'

    with open(filename, 'r') as file:
        message = file.read()

    initial_hash = md5_hash(message)

    rounds = 10
    bits_changed = []

    for round_num in range(rounds):
        bit_position_to_change = 8 * round_num
        modified_message = change_bit(message, bit_position_to_change)

        new_hash = md5_hash(modified_message)

        changed_bits_count = count_changed_bits(initial_hash, new_hash)
        bits_changed.append(changed_bits_count)

        initial_hash = new_hash

    visualize_rounds(bits_changed)

    with open('bits_changed_per_round.txt', 'w') as outfile:
        for count in bits_changed:
            outfile.write(f"{count}\n")

if __name__ == "__main__":
    main()
