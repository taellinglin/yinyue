import tkinter as tk
from tkinter import ttk

class SequencerApp:
    def __init__(self, master):
        self.master = master
        master.title("Simple Sequencer App")

        # Create the main window
        self.main_window = ttk.Notebook(master)
        self.main_window.pack(fill=tk.BOTH, expand=True)

        # Create the performance (clips) view
        self.clip_view = tk.Frame(self.main_window, bg="gray")
        self.main_window.add(self.clip_view, text="Performance")

        # Create the arrangement view
        self.arrangement_view = tk.Frame(self.main_window, bg="white")
        self.main_window.add(self.arrangement_view, text="Arrangement")

def main():
    root = tk.Tk()
    app = SequencerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
