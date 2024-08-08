import tkinter as tk
from tkinter import messagebox

# Define the questions and answers
questions = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is 2 + 2?", "answer": "4"},
    {"question": "What is the capital of Japan?", "answer": "Tokyo"},
    {"question": "What is the color of the sky?", "answer": "Blue"},
    {"question": "What is the capital of India?", "answer": "New Delhi"},
    {"question": "What is the largest ocean on Earth?", "answer": "Pacific"},
    {"question": "Who wrote 'Romeo and Juliet'?", "answer": "Shakespeare"},
    {"question": "What is the smallest prime number?", "answer": "2"},
    {"question": "Who is the founder of Microsoft", "answer": "Bill Gates"},
    {"question": "Who is known as the father of computers?", "answer": "Charles Babbage"}
]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        
        self.score = 0
        self.current_question_index = 0
        
        self.question_label = tk.Label(root, text="", wraplength=400)
        self.question_label.pack(pady=20)
        
        self.answer_entry = tk.Entry(root)
        self.answer_entry.pack(pady=20)
        self.answer_entry.bind("<Return>", self.check_answer)  # Bind Enter key to check_answer function
        
        self.submit_button = tk.Button(root, text="Submit", command=self.check_answer)
        self.submit_button.pack(pady=20)
        
        self.display_question()
        
    def display_question(self):
        if self.current_question_index < len(questions):
            question = questions[self.current_question_index]["question"]
            self.question_label.config(text=question)
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.focus()  # Focus on the entry widget for immediate typing
        else:
            self.show_result()
    
    def check_answer(self, event=None):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = questions[self.current_question_index]["answer"].strip().lower()
        
        if user_answer == correct_answer:
            self.score += 1
        
        self.current_question_index += 1
        self.display_question()
    
    def show_result(self):
        messagebox.showinfo("Quiz Result", f"You scored {self.score} out of {len(questions)}")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
