import sys
import os
import tkinter as tk
from ui.dashboard import DashboardApp

def main():
    # Ensure the shared directory exists (for dev mode)
    if not os.path.exists("shared"):
        os.makedirs("shared")

    # Initialize Tkinter
    root = tk.Tk()
    
    # Initialize the Dashboard App
    app = DashboardApp(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
