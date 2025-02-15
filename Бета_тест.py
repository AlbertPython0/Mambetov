import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import re
import gensim
import numpy as np
from sentence_transformers import SentenceTransformer
import pdfplumber

class DiagnosisAI:
    def __init__(self, db_path="diagnoses.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.init_database()  # Создаём таблицу и заполняем данными из PDF, если база пуста
        self.vectorizer = TfidfVectorizer()
        self.model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        self.synonyms = {
            "тошнота": "рвотное ощущение",
            "головная боль": "мигрень",
            "повышенная температура": "лихорадка",
        }
        self.load_tfidf_model()

    def init_database(self):
        # Создаём таблицу, если её нет
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS diagnoses (id INTEGER PRIMARY KEY AUTOINCREMENT, diagnosis TEXT, details TEXT)"
        )
        self.conn.commit()
        # Если база пуста, заполняем её данными из PDF-файла
        self.cursor.execute("SELECT COUNT(*) FROM diagnoses")
        count = self.cursor.fetchone()[0]
        if count == 0:
            self.populate_database_from_pdf("болезни.pdf")

    def populate_database_from_pdf(self, pdf_path):
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        except Exception as e:
            print("Ошибка загрузки PDF:", e)
            return

        # Разбиваем текст на строки и пытаемся распознать заголовки симптомов
        lines = text.splitlines()
        entries = {}
        current_symptom = None
        buffer = []
        # Предполагаем, что заголовки начинаются с цифры и заглавной буквы
        pattern = re.compile(r"^\d+\s+[А-ЯЁ].*")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if pattern.match(line):
                if current_symptom and buffer:
                    entries[current_symptom] = "\n".join(buffer).strip()
                parts = line.split(maxsplit=1)
                current_symptom = parts[1]
                buffer = []
            else:
                if current_symptom:
                    buffer.append(line)
        if current_symptom and buffer:
            entries[current_symptom] = "\n".join(buffer).strip()
        
        # Очищаем таблицу и заполняем её распознанными данными
        self.cursor.execute("DELETE FROM diagnoses")
        for symptom, description in entries.items():
            self.cursor.execute(
                "INSERT INTO diagnoses (diagnosis, details) VALUES (?, ?)",
                (symptom, description)
            )
        self.conn.commit()

    def load_tfidf_model(self):
        self.cursor.execute("SELECT diagnosis, details FROM diagnoses")
        rows = self.cursor.fetchall()
        self.diagnoses = [f"{diag} {det}" for diag, det in rows]
        self.diagnosis_names = [diag for diag, _ in rows]
        if self.diagnoses:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.diagnoses)
            self.embeddings = self.model.encode(self.diagnoses, convert_to_tensor=True)
        else:
            self.tfidf_matrix = None
            self.embeddings = None

    def normalize_text(self, text):
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        for word, synonym in self.synonyms.items():
            text = text.replace(word, synonym)
        return text

    def find_diagnosis(self, symptoms):
        symptoms = self.normalize_text(symptoms).strip()
        if not symptoms:
            return "Пожалуйста, введите симптомы."

        if self.tfidf_matrix is None:
            return "База данных диагнозов пуста."

        # TF-IDF сходство
        input_vec = self.vectorizer.transform([symptoms])
        similarities_tfidf = cosine_similarity(input_vec, self.tfidf_matrix)[0]
        # Семантические эмбеддинги с помощью Sentence-BERT
        input_embedding = self.model.encode([symptoms], convert_to_tensor=True)
        similarities_semantic = np.array(cosine_similarity(input_embedding.cpu(), self.embeddings.cpu())[0])
        
        # Гибридный расчёт итоговых оценок
        final_scores = (similarities_tfidf + similarities_semantic) / 2
        ranked_diagnoses = sorted(zip(self.diagnosis_names, final_scores), key=lambda x: x[1], reverse=True)

        if ranked_diagnoses[0][1] > 0:
            return "\n".join([f"{diag} (вероятность: {score:.2f})" for diag, score in ranked_diagnoses[:10]])
        else:
            return "Диагноз не найден."

    def populate_database(self, symptom_data):
        self.cursor.execute("DELETE FROM diagnoses")
        for symptom, description in symptom_data.items():
            self.cursor.execute(
                "INSERT INTO diagnoses (diagnosis, details) VALUES (?, ?)", (symptom, description)
            )
        self.conn.commit()
        self.load_tfidf_model()

    def close(self):
        self.conn.close()

class DiagnosisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Диагностическое приложение")
        self.root.geometry("900x600")
        self.ai = DiagnosisAI()

        ttk.Label(root, text="Введите симптомы через запятую:").pack(pady=10)
        self.symptoms_entry = ttk.Entry(root, width=70)
        self.symptoms_entry.pack(pady=5)

        self.search_button = ttk.Button(root, text="Определить диагноз", command=self.get_diagnosis)
        self.search_button.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(root, width=100, height=20, wrap=tk.WORD)
        self.result_text.pack(pady=10)

    def get_diagnosis(self):
        symptoms = self.symptoms_entry.get()
        result = self.ai.find_diagnosis(symptoms)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiagnosisApp(root)
    root.mainloop()
