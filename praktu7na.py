from Crypto.PublicKey import RSA
import random
import os

def generate_RSA_sequence(bits):
    key = RSA.generate(bits, e=65537) 
    random_number = random.SystemRandom().randrange(2 ** (bits - 1), 2 ** bits)  
    encrypted = pow(random_number, key.e, key.n)  
    return encrypted.to_bytes((encrypted.bit_length() + 7) // 8, 'big') 

def save_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def read_parameters_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        bits = int(lines[0].strip()) 
        return bits

parameters_filename = 'parameters.txt'  
bits = read_parameters_from_file(parameters_filename)

generated_sequence = generate_RSA_sequence(bits)
save_to_file(generated_sequence, 'generated.txt')
def frequency_test(sequence):
    ones_count = sequence.count('1')
    zeros_count = sequence.count('0')
    total_bits = len(sequence)
    expected_frequency = total_bits / 2
    
    deviation = abs(ones_count - expected_frequency)
    return deviation < 0.05 * total_bits, deviation

def series_test(sequence):
    for i in range(len(sequence) - 2):
        if sequence[i] == sequence[i + 1] == sequence[i + 2]:
            return False, i  
    return True, None  

random_sequence = ''.join(str(random.randint(0, 1)) for _ in range(10000))

frequency_test_result, frequency_deviation = frequency_test(random_sequence)
series_test_result, series_index = series_test(random_sequence)

print(f"Тест частоти: {'Пройдено' if frequency_test_result else 'Не пройдено'}. Відхилення: {frequency_deviation}")
print(f"Тест серій: {'Пройдено' if series_test_result else 'Не пройдено'}. Індекс першої серії: {series_index if series_index is not None else 'Не знайдено'}")
