import tkinter as tk
from tkinter import filedialog, simpledialog
import pandas as pd
import random
import unidecode


class FlashCardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Tarjetas de Aprendizaje")
        self.root.geometry('600x400')  # Cambiar el tamaño de la ventana
        self.root.configure(bg='lightblue')  # Cambiar el color de fondo
        self.root.withdraw()  # Ocultar la ventana principal
        self.card_index = None

        self.questions_seen = 0
        self.questions_correct = 0
        self.questions_limit = 0
        self.failed_questions = []

        self.question_counter_label = tk.Label(root, text="", font=("Arial", 12), bg='lightblue', fg='darkred')
        self.question_counter_label.pack(pady=10)

        self.question_label = tk.Label(root, text="", font=("Arial", 24), bg='lightblue', fg='darkblue')
        self.question_label.pack(pady=10)

        self.answer_entry = tk.Entry(root, font=("Arial", 20))
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', self.check_answer)

        self.stats_label = tk.Label(root, text="", font=("Arial", 20), bg='lightblue', fg='darkgreen')
        self.stats_label.pack(pady=10)

        self.buttons_frame = tk.Frame(root, bg='lightblue')
        self.buttons_frame.pack(pady=10)

        self.show_answer_button = tk.Button(self.buttons_frame, text="Comprobar Respuesta", command=self.check_answer,
                                            bg='darkgreen', fg='white', width=20)
        self.show_answer_button.pack(side='left', padx=5)

       # self.next_button = tk.Button(self.buttons_frame, text="Siguiente", command=self.show_next_card, bg='darkblue',
       #                             fg='white', width=20)
       #self.next_button.pack(side='right', padx=5)

        # Esperar hasta que la interfaz esté completamente inicializada antes de abrir la ventana de diálogo
        root.after(100, self.start_quiz)

    def start_quiz(self):
        self.questions_limit = simpledialog.askinteger("Preguntas", "¿Cuántas preguntas te gustaría hacer?", minvalue=1)
        self.load_csv()

    def load_csv(self):
        csv_file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.data = pd.read_csv(csv_file_path)
        self.root.deiconify()  # Mostrar la ventana principal
        self.show_next_card()

    def show_next_card(self):
        if self.questions_seen < self.questions_limit:
            self.card_index = random.randint(0, len(self.data) - 1)
            question = self.data.loc[self.card_index, 'Pregunta']
            self.question_label.config(text=question)
            self.answer_entry.delete(0, 'end')
            self.questions_seen += 1
            self.update_stats()
            self.question_counter_label.config(text=f"Pregunta {self.questions_seen}")
        else:
            self.question_label.config(text="Quiz finalizado")
            self.answer_entry.pack_forget()
            self.buttons_frame.pack_forget()
            self.show_failed_questions()

    def check_answer(self, event=None):
        user_answer = self.answer_entry.get().lower()
        correct_answer = unidecode.unidecode(self.data.loc[self.card_index, 'Respuesta'].lower())
        user_answer = unidecode.unidecode(user_answer)
        if user_answer == correct_answer:
            self.questions_correct += 1
        else:
            self.failed_questions.append(self.data.loc[self.card_index])
        self.show_next_card()
        self.update_stats()

    def update_stats(self):
        stats_text = f"Vistas: {self.questions_seen} / Correctas: {self.questions_correct}"
        self.stats_label.config(text=stats_text)

    def show_failed_questions(self):
        if self.failed_questions:
            failed_text = "Preguntas fallidas:\n"
            for question in self.failed_questions:
                failed_text += f"Pregunta: {question['Pregunta']} - Respuesta correcta: {question['Respuesta']}\n"
            self.failed_questions_label = tk.Label(self.root, text=failed_text, font=("Arial", 20), bg='lightblue', fg='darkred')
            self.failed_questions_label.pack(pady=10)


root = tk.Tk()
app = FlashCardApp(root)
root.mainloop()
