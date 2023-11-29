import hashlib
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import matplotlib.pyplot as plt

def calculate_md5(file_text):
    hashed_text = hashlib.md5(file_text.encode()).hexdigest()
    return hashed_text

def toggle_bit(text, bit_position):
    byte_position = bit_position // 8
    bit_shift = 7 - (bit_position % 8)
    byte = text[byte_position]
    byte = ord(byte)  # Convert character to ASCII code
    mask = 1 << bit_shift
    byte ^= mask
    toggled_byte = bytes([byte])
    modified_text = text[:byte_position] + toggled_byte + text[byte_position + 1:]
    return modified_text



def find_changed_bits(hash1, hash2):
    changed_bits = 0
    for i in range(len(hash1)):
        byte1, byte2 = int(hash1[i], 16), int(hash2[i], 16)
        diff = byte1 ^ byte2
        changed_bits += bin(diff).count('1')
    return changed_bits

def simulate_avalanche_effect(text, bit_position):
    rounds = []
    changed_bits = []
    original_hash = calculate_md5(text)

    with open('avalanche_data.txt', 'w') as file:
        file.write("Round,ChangedBits\n")
        file.write(f"0,0\n")  # Initial state

        for i in range(8 * len(text)):
            modified_text = toggle_bit(text, bit_position)
            new_hash = calculate_md5(modified_text)
            changed_bit_count = find_changed_bits(original_hash, new_hash)

            rounds.append(i)
            changed_bits.append(changed_bit_count)

            file.write(f"{i + 1},{changed_bit_count}\n")

            text = modified_text

    return rounds, changed_bits

def plot_avalanche_effect():
    try:
        with open('avalanche_data.txt', 'r') as file:
            next(file)  # Skip header
            data = [line.strip().split(',') for line in file]

        rounds = [int(row[0]) for row in data]
        changed_bits = [int(row[1]) for row in data]

        plt.figure(figsize=(8, 6))
        plt.plot(rounds, changed_bits, marker='o', linestyle='-', color='b')
        plt.title('Avalanche Effect in MD5')
        plt.xlabel('Rounds')
        plt.ylabel('Changed Bits in Hash')
        plt.grid(True)
        plt.show()
    except FileNotFoundError:
        messagebox.showerror("Error", "No data file found. Run simulation first.")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                text = file.read()
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

def save_hash():
    text = text_area.get(1.0, tk.END)
    hashed_text = calculate_md5(text)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(f"Original Text:\n{text}\n\nMD5 Hash:\n{hashed_text}")
                messagebox.showinfo("Success", "MD5 Hash saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

def update_hash():
    text = text_area.get(1.0, tk.END)
    hashed_text = calculate_md5(text)
    hash_area.delete(1.0, tk.END)
    hash_area.insert(tk.END, hashed_text)

root = tk.Tk()
root.title("MD5 Avalanche Effect")

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save MD5 Hash", command=save_hash)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

text_area = scrolledtext.ScrolledText(frame, width=50, height=10, wrap=tk.WORD)
text_area.grid(row=0, column=0, padx=5, pady=5)

hash_label = tk.Label(frame, text="MD5 Hash:")
hash_label.grid(row=1, column=0, padx=5, pady=5)

hash_area = scrolledtext.ScrolledText(frame, width=50, height=3, wrap=tk.WORD)
hash_area.grid(row=2, column=0, padx=5, pady=5)

update_button = tk.Button(frame, text="Update Hash", command=update_hash)
update_button.grid(row=3, column=0, padx=5, pady=5)

simulate_button = tk.Button(frame, text="Simulate Avalanche", command=lambda: simulate_avalanche_effect(text_area.get(1.0, tk.END), bit_position.get()))
simulate_button.grid(row=4, column=0, padx=5, pady=5)

plot_button = tk.Button(frame, text="Plot Avalanche Effect", command=plot_avalanche_effect)
plot_button.grid(row=5, column=0, padx=5, pady=5)

bit_position = tk.IntVar()
bit_position.set(0)
bit_position_entry = tk.Entry(frame, textvariable=bit_position)
bit_position_entry.grid(row=6, column=0, padx=5, pady=5)
bit_position_label = tk.Label(frame, text="Bit Position:")
bit_position_label.grid(row=7, column=0, padx=5, pady=5)

root.mainloop()
