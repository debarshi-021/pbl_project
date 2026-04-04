import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from usb_detector import USBDetector
from verifier import Verifier

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SDN Controller Security Dashboard v1.0")
        self.root.geometry("700x450")
        
        # Classic Windows Look
        style = ttk.Style()
        style.theme_use('vista') 

        self.detector = USBDetector()
        # Use resource_path so it works inside the EXE
        self.verifier = Verifier(resource_path("shared/trusted_pub.pem"))
        self.devices = {}

        self.setup_ui()
        self.poll()

    def setup_ui(self):
        # Header Area
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)
        
        ttk.Label(header_frame, text="SDN Controller Security Dashboard", font=("Arial", 16, "bold")).pack(anchor=tk.W)
        ttk.Label(header_frame, text="TPM-Inspired USB Authentication System").pack(anchor=tk.W)

        # Status Bar
        self.status_var = tk.StringVar(value="System Status: Monitoring Active...")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, padding=(5, 2))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Table (Treeview)
        table_frame = ttk.Frame(self.root, padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "path", "status", "reason", "time")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="Device ID")
        self.tree.heading("path", text="Drive Path")
        self.tree.heading("status", text="Status")
        self.tree.heading("reason", text="Reason")
        self.tree.heading("time", text="Verify Time")

        self.tree.column("id", width=100)
        self.tree.column("path", width=80)
        self.tree.column("status", width=100)
        self.tree.column("reason", width=200)
        self.tree.column("time", width=80)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Legend
        legend_frame = ttk.Frame(self.root, padding="10")
        legend_frame.pack(fill=tk.X)
        ttk.Label(legend_frame, text="Legend: AUTHENTICATED (Trusted) | REJECTED (Unauthorized)", font=("Arial", 8, "italic")).pack(side=tk.LEFT)

    def poll(self):
        added, removed = self.detector.detect_changes()

        for drive in removed:
            if drive in self.devices:
                del self.devices[drive]
                print(f"[INFO] Removed: {drive}")

        for drive in added:
            print(f"[INFO] Detected: {drive}")
            is_valid, dev_id, reason, v_time = self.verifier.verify_device(drive)
            self.devices[drive] = (dev_id, "AUTHENTICATED" if is_valid else "REJECTED", reason, f"{v_time}ms")
            
            if not is_valid:
                messagebox.showwarning("Security Alert", f"Unauthorized device detected at {drive}!\nReason: {reason}")

        self.update_table()
        self.root.after(1500, self.poll)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for drive, data in self.devices.items():
            self.tree.insert("", tk.END, values=(data[0], drive, data[1], data[2], data[3]))
        
        if not self.devices:
            self.status_var.set("System Status: No devices connected.")
        else:
            self.status_var.set(f"System Status: {len(self.devices)} device(s) monitored.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
