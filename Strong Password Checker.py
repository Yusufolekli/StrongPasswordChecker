import tkinter as tk
from tkinter import messagebox
import re
import random
import string
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO)

class WordList:
    def __init__(self, word_file):
        self.word_set = set()
        self.load_words(word_file)

    def load_words(self, word_file):
        try:
            with open(word_file, 'r') as file:
                for line in file:
                    self.word_set.add(line.strip().lower())
            logging.info("Kelime listesi yüklendi.")
        except Exception as e:
            logging.error(f"Kelime listesi yüklenirken hata: {e}")

    def is_common_word(self, word):
        return word.lower() in self.word_set

class PasswordStrength:
    def __init__(self):
        self.strength = "Zayıf"

    def check_strength(self, password):
        if len(password) < 8:
            self.strength = "Zayıf"
        elif re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'\d', password) and re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            self.strength = "Güçlü"
        elif re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'\d', password):
            self.strength = "Orta"
        else:
            self.strength = "Zayıf"
        return self.strength

class PasswordStrengthChecker:
    def __init__(self, word_list):
        self.word_list = word_list

    def check_password(self, password):
        if self.word_list.is_common_word(password):
            return "Zayıf (yaygın kelime)"
        strength_checker = PasswordStrength()
        return strength_checker.check_strength(password)

class PasswordGenerator:
    @staticmethod
    def generate_password(length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

class PasswordStrengthGUI:
    def __init__(self, master):
        self.master = master
        master.title("Şifre Gücü Denetleyicisi")

        self.word_list = WordList("common_words.txt")  # Kelime listesi dosyası
        self.checker = PasswordStrengthChecker(self.word_list)

        self.label = tk.Label(master, text="Şifre Girin:", font=('calibre', 12, 'bold'))
        self.label.pack()

        # Password entry
        self.password_entry = tk.Entry(master, show='*', width=30, font=('calibre', 12, 'normal'))
        self.password_entry.pack()

        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        self.show_password_checkbox = tk.Checkbutton(master, text="Şifreyi Göster", variable=self.show_password_var, command=self.toggle_password_visibility, font=('calibre', 12))
        self.show_password_checkbox.pack()

        # Check and generate buttons
        self.check_button = tk.Button(master, text="Şifreyi Kontrol Et", command=self.check_password, font=('calibre', 12))
        self.check_button.pack()

        self.generate_button = tk.Button(master, text="Güçlü Şifre Oluştur", command=self.generate_password, font=('calibre', 12))
        self.generate_button.pack()

        self.result_label = tk.Label(master, text="", font=('calibre', 12))
        self.result_label.pack()

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show='')  # Show password
        else:
            self.password_entry.config(show='*')  # Hide password

    def check_password(self):
        password = self.password_entry.get()
        result = self.checker.check_password(password)
        self.result_label.config(text=f"Sonuç: {result}")

    def generate_password(self):
        password = PasswordGenerator.generate_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.result_label.config(text="Yeni şifre oluşturuldu.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = PasswordStrengthGUI(root)
    root.mainloop()