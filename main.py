import tkinter as tk
from nim_game import NimGame


if __name__ == "__main__":
    root = tk.Tk()
    root.title("NIMJA: Outsmart Your Opponents")
    game = NimGame(root)
    root.mainloop()
