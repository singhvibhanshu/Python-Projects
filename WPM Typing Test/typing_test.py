import tkinter as tk
import time

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")

        self.sample_text = (
            "The quick brown fox jumps over the lazy dog. "
            "This is a typing speed test. Try to type this text as quickly and accurately as you can."
        )

        self.start_time = None

        self.sample_label = tk.Label(root, text=self.sample_text, wraplength=400)
        self.sample_label.pack(pady=20)

        self.input_text = tk.Text(root, height=10, width=50)
        self.input_text.pack(pady=20)
        self.input_text.bind("<KeyPress>", self.start_timer)
        self.input_text.bind("<KeyRelease>", self.highlight_text)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=20)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_test)
        self.reset_button.pack(pady=20)

    def start_timer(self, event):
        if self.start_time is None:
            self.start_time = time.time()

    def highlight_text(self, event):
        typed_text = self.input_text.get("1.0", tk.END).strip()
        sample_words = self.sample_text.split()
        typed_words = typed_text.split()

        self.input_text.tag_remove("correct", "1.0", tk.END)
        self.input_text.tag_remove("incorrect", "1.0", tk.END)

        for i, word in enumerate(typed_words):
            if i < len(sample_words) and word == sample_words[i]:
                start_idx = "1.0 + {}c".format(len(" ".join(typed_words[:i])) + i)
                end_idx = "1.0 + {}c".format(len(" ".join(typed_words[:i + 1])) + i)
                self.input_text.tag_add("correct", start_idx, end_idx)
            else:
                start_idx = "1.0 + {}c".format(len(" ".join(typed_words[:i])) + i)
                end_idx = "1.0 + {}c".format(len(" ".join(typed_words[:i + 1])) + i)
                self.input_text.tag_add("incorrect", start_idx, end_idx)

        self.input_text.tag_configure("correct", foreground="green")
        self.input_text.tag_configure("incorrect", foreground="red")

        self.calculate_wpm()

    def calculate_wpm(self):
        if self.start_time is None:
            return

        elapsed_time = time.time() - self.start_time
        typed_text = self.input_text.get("1.0", tk.END).strip()
        typed_words = typed_text.split()
        correct_words = 0
        sample_words = self.sample_text.split()

        for i, word in enumerate(typed_words):
            if i < len(sample_words) and word == sample_words[i]:
                correct_words += 1

        wpm = (correct_words / elapsed_time) * 60
        self.result_label.config(text=f"Your typing speed is {wpm:.2f} words per minute")

    def reset_test(self):
        self.start_time = None
        self.input_text.delete("1.0", tk.END)
        self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()
