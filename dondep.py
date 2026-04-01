import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk
import psutil
import time # Thêm thư viện để tạo hiệu ứng chạy thanh progress

def get_size(bytes_value):
    factor = 1024**3
    return f"{round(bytes_value / factor, 2)} GB"

class KilluaCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Killua Speed v3.5 - Pro Edition")
        self.root.geometry("500x550")
        self.root.configure(bg='#0a0a0a')
        
        self.vars = {}
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="HỆ THỐNG TỐI ƯU ĐA Ổ ĐĨA", fg="#00f2ff", bg="#0a0a0a", 
                 font=("Arial", 16, "bold")).pack(pady=20)

        # Khung chứa danh sách ổ đĩa
        frame = tk.Frame(self.root, bg="#0a0a0a")
        frame.pack(fill="both", expand=True, padx=20)

        partitions = psutil.disk_partitions()
        for p in partitions:
            if 'fixed' in p.opts:
                drive = p.mountpoint
                try: usage = psutil.disk_usage(drive)
                except: continue
                
                var = tk.BooleanVar()
                self.vars[drive] = var
                
                d_frame = tk.Frame(frame, bg="#1a1a1a", pady=5)
                d_frame.pack(fill="x", pady=5)
                
                cb = tk.Checkbutton(d_frame, text=f"Ổ {drive}", variable=var, 
                                    bg="#1a1a1a", fg="#00f2ff", selectcolor="#000",
                                    activebackground="#1a1a1a", activeforeground="#00f2ff")
                cb.pack(side="left", padx=10)
                
                lbl = tk.Label(d_frame, text=f"Trống: {get_size(usage.free)} / {get_size(usage.total)}", 
                               bg="#1a1a1a", fg="#ccc", font=("Arial", 9))
                lbl.pack(side="right", padx=10)

        # --- PHẦN THÊM MỚI: PROGRESS BAR ---
        self.progress_label = tk.Label(self.root, text="Sẵn sàng tối ưu...", fg="#888", bg="#0a0a0a")
        self.progress_label.pack(pady=(20, 5))

        # Tạo style cho Progress Bar màu Neon
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Neon.Horizontal.TProgressbar", background='#00f2ff', troughcolor='#1a1a1a', borderwidth=0)
        
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate", style="Neon.Horizontal.TProgressbar")
        self.progress.pack(pady=10)
        # ----------------------------------

        self.btn_clean = tk.Button(self.root, text="BẮT ĐẦU DỌN DẸP", command=self.start_cleaning,
                              bg="#d72b18", fg="black", font=("Arial", 12, "bold"), pady=15)
        self.btn_clean.pack(side="bottom", fill="x", padx=50, pady=20)
        # --- PHẦN THÊM CRE (Tên của bạn) ---
        tk.Label(self.root, text="Cre: Thiên Hoàng", fg="#444", bg="#f70509", 
                 font=("Arial", 12, "italic")).pack(side="bottom", pady=10)

    def start_cleaning(self):
        selected_drives = [drive for drive, var in self.vars.items() if var.get()]
        if not selected_drives:
            messagebox.showwarning("Chú ý", "Vui lòng chọn ổ đĩa để dọn dẹp!")
            return

        # Hiệu ứng chạy thanh tiến trình
        self.btn_clean.config(state="disabled") # Khóa nút lại khi đang chạy
        self.progress['value'] = 0
        total_files = 0
        
        # Giả lập quét hệ thống cho thanh chạy mượt
        for i in range(1, 101):
            self.progress['value'] = i
            self.progress_label.config(text=f"Đang quét hệ thống... {i}%")
            self.root.update_idletasks()
            time.sleep(0.01) # Chạy nhanh nhưng vẫn tạo cảm giác đang quét

        # Bắt đầu dọn dẹp thật
        for drive in selected_drives:
            targets = []
            if drive == "C:\\":
                targets.extend([os.environ.get('TEMP'), r'C:\Windows\Temp', r'C:\Windows\Prefetch'])
            
            recycle_bin = os.path.join(drive, "$RECYCLE.BIN")
            if os.path.exists(recycle_bin): targets.append(recycle_bin)

            for folder in targets:
                if folder and os.path.exists(folder):
                    self.progress_label.config(text=f"Đang dọn dẹp: {folder}")
                    self.root.update_idletasks()
                    for item in os.listdir(folder):
                        try:
                            path = os.path.join(folder, item)
                            if os.path.isfile(path) or os.path.islink(path): os.unlink(path)
                            elif os.path.isdir(path): shutil.rmtree(path)
                            total_files += 1
                        except: continue

        self.progress['value'] = 100
        self.progress_label.config(text="Hoàn tất tối ưu!")
        messagebox.showinfo("Thành công", f"Đã dọn xong {total_files} mục rác!")
        self.btn_clean.config(state="normal") # Mở lại nút bấm

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = KilluaCleaner(root)
    root.mainloop()