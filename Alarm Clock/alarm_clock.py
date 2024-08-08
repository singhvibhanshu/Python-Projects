import tkinter as tk
import time
import threading
import pygame

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load an alarm sound
def load_sound():
    try:
        pygame.mixer.music.load("alarm_sound.mp3")
    except pygame.error as e:
        print(f"Error loading sound file: {e}")

def play_sound():
    pygame.mixer.music.play()

def stop_sound():
    pygame.mixer.music.stop()

class AlarmClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")

        self.alarm_time = None
        self.is_running = False

        self.time_label = tk.Label(root, text="Enter alarm time (HH:MM:SS):")
        self.time_label.pack(pady=10)

        self.time_entry = tk.Entry(root)
        self.time_entry.pack(pady=10)

        self.set_button = tk.Button(root, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Alarm", command=self.stop_alarm)
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=10)

        load_sound()

    def set_alarm(self):
        self.status_label.config(text="Alarm set. Timer running...")
        alarm_str = self.time_entry.get()
        try:
            alarm_hours, alarm_minutes, alarm_seconds = map(int, alarm_str.split(':'))
            now = time.localtime()
            self.alarm_time = time.mktime(now) + alarm_hours * 3600 + alarm_minutes * 60 + alarm_seconds
            self.is_running = True
            threading.Thread(target=self.run_timer).start()
        except ValueError:
            self.status_label.config(text="Invalid time format. Use HH:MM:SS.")

    def run_timer(self):
        while self.is_running:
            current_time = time.time()
            remaining_time = self.alarm_time - current_time

            if remaining_time <= 0:
                self.status_label.config(text="Alarm ringing!")
                play_sound()
                self.is_running = False
                break

            time_str = time.strftime("%H:%M:%S", time.gmtime(remaining_time))
            self.status_label.config(text=f"Time left: {time_str}")
            time.sleep(1)

    def stop_alarm(self):
        self.is_running = False
        stop_sound()
        self.status_label.config(text="Alarm stopped")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClockApp(root)
    root.mainloop()
