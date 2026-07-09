import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox

def run_test():
    # 1. Ask the user to pick a directory
    target_dir = filedialog.askdirectory(title="Select Drive or Folder for Test")
    
    if not target_dir:
        return

    try:
        file_path = os.path.join(target_dir, "speed_test.bin")
        file_size_mb = 500  # Smaller size for a quicker test
        data = os.urandom(1024 * 1024) # 1MB chunk

        label_status.config(text="Testing Write Speed...", fg="blue")
        root.update()

        # --- Write Test ---
        start_time = time.time()
        with open(file_path, 'wb') as f:
            for _ in range(file_size_mb):
                f.write(data)
            os.fsync(f.fileno())
        write_time = time.time() - start_time
        write_speed = file_size_mb / write_time

        label_status.config(text="Testing Read Speed...", fg="blue")
        root.update()

        # --- Read Test ---
        start_time = time.time()
        with open(file_path, 'rb') as f:
            while f.read(1024 * 1024):
                pass
        read_time = time.time() - start_time
        read_speed = file_size_mb / read_time

        # Cleanup
        os.remove(file_path)

        # Show Results
        messagebox.showinfo("Results", f"Write Speed: {write_speed:.2f} MB/s\nRead Speed: {read_speed:.2f} MB/s")
        label_status.config(text="Test Complete", fg="green")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        label_status.config(text="Test Failed", fg="red")

# --- GUI Setup ---
root = tk.Tk()
root.title("DiskSpeedor v1.0")
root.geometry("300x200")

tk.Label(root, text="Drive Speed Tester", font=("Arial", 14, "bold")).pack(pady=10)

btn_select = tk.Button(root, text="Select Drive & Start Test", command=run_test, height=2, bg="lightgrey")
btn_select.pack(pady=10)

label_status = tk.Label(root, text="Waiting for input...", font=("Arial", 10))
label_status.pack(pady=10)

root.mainloop()
