import tkinter as tk
from tkinter import ttk

def update_entries():
    for widget in frame.winfo_children():
        widget.destroy()
    row_count = row_scale.get()
    letters = letters_entry.get().strip().split(',')
    letters = [letter.strip() for letter in letters if letter]
    letter_count = len(letters)

    if letter_count == 0:
        return

    column_count = letter_count + 1

    if row_count > 0:
        header_label_1 = tk.Label(frame, text="İlk Durum", font=("Arial", 10, "bold"))
        header_label_1.grid(row=0, column=0, padx=5, pady=5)

        conversion_label = tk.Label(frame, text="Dönüşüm Tablosu", font=("Arial", 10, "bold"))
        conversion_label.grid(row=0, column=1, columnspan=column_count - 1, padx=5, pady=5)

        for j, letter in enumerate(letters):
            letter_entry_label = tk.Label(frame, text=f"{letter} girişi/çıktı", font=("Arial", 9))
            letter_entry_label.grid(row=1, column=j + 1, padx=5, pady=5)

    transition_entries = []

    for i in range(2, row_count + 2):
        for j in range(column_count):
            if j == 0:
                entry = tk.Label(frame, text=f"q{(i - 2) % 10}", font=("Arial", 9))
                entry.grid(row=i, column=j, padx=5, pady=5)
            else:
                # "Durum, Çıkış" şeklinde seçenekler oluştur
                combined_values = [f"q{k}, {output}" for k in range(row_count) for output in output_letters_entry.get().strip().split(',')]
                
                combined_combobox = ttk.Combobox(frame, values=combined_values, state="readonly", width=10)
                combined_combobox.grid(row=i, column=j, padx=5, pady=5)
                combined_combobox.set("Durum, Çıkış")
                
                transition_entries.append(combined_combobox)

def calculate_values():
    row_count = row_scale.get()
    letters = letters_entry.get().strip().split(',')
    letters = [letter.strip() for letter in letters if letter]
    output_letters = output_letters_entry.get().strip().split(',')
    output_letters = [letter.strip() for letter in output_letters if letter]
    
    transition_matrix = [[None] * len(letters) for _ in range(row_count)]
    output_matrix = [[None] * len(letters) for _ in range(row_count)]
    
    i = 0
    for entry in frame.winfo_children():
        if isinstance(entry, ttk.Combobox):
            selected_value = entry.get()
            if selected_value != "Durum, Çıkış":
                try:
                    state_str, output_value = selected_value.split(', ')
                    if state_str.startswith("q") and output_value in output_letters:
                        q_index = int(state_str[1:])
                        transition_matrix[i // len(letters)][i % len(letters)] = q_index
                        output_matrix[i // len(letters)][i % len(letters)] = output_value
                    i += 1
                except ValueError:
                    print("Geçiş/çıkış seçiminde hata")

    input_text = input_entry.get()
    current_state = 0
    output_sequence = []
    states_sequence = []

    for char in input_text:
        if char in letters:
            char_index = letters.index(char)
            next_state = transition_matrix[current_state][char_index]
            if next_state is not None:
                output_sequence.append(output_matrix[current_state][char_index])
                current_state = next_state
                states_sequence.append(f"q{current_state}")
            else:
                print("Transition not defined.")
                break
        else:
            print(f"Invalid input character: {char}")
            break

    Baslangiclabel2.config(text="    " + "    ".join(input_text))
    Sonuclabel2.config(text="    " + "    ".join(output_sequence))
    Statelabel2.config(text="  " + "  ".join(states_sequence))

root = tk.Tk()
root.title("Mealy Makinası")

Baslangiclabel = tk.Label(root, text="Input Metni : ")
Baslangiclabel.pack(side=tk.TOP, anchor='nw', padx=20, pady=30)

Baslangiclabel2 = tk.Label(root, text=" ", font=("Arial", 16))
Baslangiclabel2.pack(side=tk.TOP, anchor='nw', padx=60, pady=0)

Sonuclabel = tk.Label(root, text="Çıkış Metni : ")
Sonuclabel.pack(side=tk.TOP, anchor='nw', padx=20, pady=0)

Sonuclabel2 = tk.Label(root, text="", font=("Arial", 16))
Sonuclabel2.pack(side=tk.TOP, anchor='nw', padx=60, pady=0)

Statelabel = tk.Label(root, text="State Metni : ")
Statelabel.pack(side=tk.TOP, anchor='nw', padx=20, pady=30)

Statelabel2 = tk.Label(root, text="", font=("Arial", 16))
Statelabel2.pack(side=tk.TOP, anchor='nw', padx=60, pady=0)

letters_entry_label = tk.Label(root, text="Harfleri (a, b, c, d) girin:")
letters_entry_label.pack(side=tk.TOP, anchor='e', padx=10)

letters_entry = tk.Entry(root, width=20)
letters_entry.pack(side=tk.TOP, anchor='e', padx=10)

output_letters_label = tk.Label(root, text="Çıktı alfabesini girin (örn. x, y, z):")
output_letters_label.pack(side=tk.TOP, anchor='e', padx=10)

output_letters_entry = tk.Entry(root, width=20)
output_letters_entry.pack(side=tk.TOP, anchor='e', padx=10)

input_entry_label = tk.Label(root, text="Input Stringi Giriniz:")
input_entry_label.pack(side=tk.TOP, anchor='e', padx=10)

input_entry = tk.Entry(root, width=20)
input_entry.pack(side=tk.TOP, anchor='e', padx=10)

row_scale_label = tk.Label(root, text="State Sayısını Giriniz")
row_scale_label.pack(side=tk.TOP, anchor='e', padx=10)

row_scale = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL)
row_scale.pack(side=tk.TOP, anchor='e', padx=10)

update_button = tk.Button(root, text="Tabloyu Güncelle", command=update_entries)
update_button.pack(side=tk.TOP, anchor='e', padx=10, pady=(5, 10))

calculate_button = tk.Button(root, text="Hesapla", command=calculate_values)
calculate_button.pack(side=tk.TOP, anchor='e', padx=10, pady=(5, 10))

canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame = scrollable_frame

update_entries()

root.mainloop()
