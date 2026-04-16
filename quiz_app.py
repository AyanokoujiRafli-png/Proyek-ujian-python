import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

# ==================== DATA SOAL ====================
soal_data = [
    {
        "soal": "Apa ibu kota Indonesia?",
        "pilihan": ["Jakarta", "Bandung", "Surabaya", "Medan"],
        "jawaban": 0  # index 0 = Jakarta
    },
    {
        "soal": "Siapakah presiden pertama Indonesia?",
        "pilihan": ["Soeharto", "Soekarno", "Habibie", "Gus Dur"],
        "jawaban": 1
    },
    {
        "soal": "Berapa hasil 5 + 3 x 2?",
        "pilihan": ["16", "11", "10", "13"],
        "jawaban": 1  # 5+6=11
    },
    {
        "soal": "Planet terdekat dengan Matahari adalah?",
        "pilihan": ["Venus", "Mars", "Merkurius", "Bumi"],
        "jawaban": 2
    },
    {
        "soal": "Hewan apa yang bisa hidup di air dan darat?",
        "pilihan": ["Kucing", "Amfibi", "Ikan", "Burung"],
        "jawaban": 1
    }
]

# ==================== KELAS KARTUN SOSIS ====================
class SausageChar:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.eye_direction = "depan"  # depan, kiri, kanan
        self.mouth_shape = "normal"   # normal, senang, sedih, kaget
        
        # Gambar tubuh lonjong (sosis)
        self.body = canvas.create_oval(x-40, y-30, x+40, y+30, fill="#F4A460", outline="#D2691E", width=2)
        # Mata kiri dan kanan
        self.eye_left = canvas.create_oval(x-20, y-10, x-10, y, fill="white", outline="black")
        self.eye_right = canvas.create_oval(x+10, y-10, x+20, y, fill="white", outline="black")
        self.pupil_left = canvas.create_oval(x-17, y-7, x-13, y-3, fill="black")
        self.pupil_right = canvas.create_oval(x+13, y-7, x+17, y-3, fill="black")
        # Mulut
        self.mouth = canvas.create_arc(x-15, y+5, x+15, y+20, start=0, extent=-180, fill="#8B4513", outline="black")
        # Alis (opsional untuk ekspresi)
        self.brow_left = canvas.create_line(x-22, y-15, x-12, y-18, fill="black", width=2)
        self.brow_right = canvas.create_line(x+12, y-18, x+22, y-15, fill="black", width=2)
        
        self.default_mouth_extent = -180
        
    def update_expression(self, mood):
        # mood: "excited", "shy", "happy", "sad", "shock", "celebrate"
        if mood == "excited":   # bersemangat (mata besar, mulut terbuka lebar)
            self.canvas.itemconfig(self.eye_left, fill="yellow")
            self.canvas.itemconfig(self.eye_right, fill="yellow")
            self.canvas.coords(self.mouth, self.x-18, self.y+5, self.x+18, self.y+25)
            self.canvas.itemconfig(self.mouth, start=0, extent=-200)
            self.canvas.coords(self.brow_left, self.x-24, self.y-20, self.x-10, self.y-22)
            self.canvas.coords(self.brow_right, self.x+10, self.y-22, self.x+24, self.y-20)
        elif mood == "shy":     # malu/pura2 tidak lihat (mata ke samping)
            self.canvas.itemconfig(self.eye_left, fill="white")
            self.canvas.itemconfig(self.eye_right, fill="white")
            self.canvas.coords(self.pupil_left, self.x-7, self.y-7, self.x-3, self.y-3)  # mata ke kiri
            self.canvas.coords(self.pupil_right, self.x+3, self.y-7, self.x+7, self.y-3)
            self.canvas.coords(self.mouth, self.x-12, self.y+5, self.x+12, self.y+18)
            self.canvas.itemconfig(self.mouth, start=0, extent=-120)
        elif mood == "happy":
            self.canvas.itemconfig(self.eye_left, fill="white")
            self.canvas.itemconfig(self.eye_right, fill="white")
            self.canvas.coords(self.pupil_left, self.x-17, self.y-7, self.x-13, self.y-3)
            self.canvas.coords(self.pupil_right, self.x+13, self.y-7, self.x+17, self.y-3)
            self.canvas.coords(self.mouth, self.x-15, self.y+2, self.x+15, self.y+22)
            self.canvas.itemconfig(self.mouth, start=0, extent=-200)
        elif mood == "sad":
            self.canvas.itemconfig(self.eye_left, fill="lightblue")
            self.canvas.itemconfig(self.eye_right, fill="lightblue")
            self.canvas.coords(self.mouth, self.x-12, self.y+8, self.x+12, self.y+18)
            self.canvas.itemconfig(self.mouth, start=180, extent=-180)  # mulut terbalik
        elif mood == "celebrate":
            self.canvas.itemconfig(self.eye_left, fill="gold")
            self.canvas.itemconfig(self.eye_right, fill="gold")
            self.canvas.coords(self.mouth, self.x-18, self.y+2, self.x+18, self.y+25)
            self.canvas.itemconfig(self.mouth, start=0, extent=-220)
            
    def jelly_fall_animation(self, target_y):
        # Animasi jatuh kayak jelly
        steps = 20
        dy = (target_y - self.y) / steps
        for i in range(steps):
            self.y += dy
            self.canvas.move(self.body, 0, dy)
            self.canvas.move(self.eye_left, 0, dy)
            self.canvas.move(self.eye_right, 0, dy)
            self.canvas.move(self.pupil_left, 0, dy)
            self.canvas.move(self.pupil_right, 0, dy)
            self.canvas.move(self.mouth, 0, dy)
            self.canvas.move(self.brow_left, 0, dy)
            self.canvas.move(self.brow_right, 0, dy)
            self.canvas.update()
            time.sleep(0.02)
        # Efek jelly sedikit bouncing
        for bounce in range(3):
            self.canvas.move(self.body, 0, -3)
            self.canvas.move(self.eye_left, 0, -3)
            self.canvas.move(self.eye_right, 0, -3)
            self.canvas.move(self.pupil_left, 0, -3)
            self.canvas.move(self.pupil_right, 0, -3)
            self.canvas.move(self.mouth, 0, -3)
            self.canvas.move(self.brow_left, 0, -3)
            self.canvas.move(self.brow_right, 0, -3)
            self.canvas.update()
            time.sleep(0.02)
            self.canvas.move(self.body, 0, 3)
            self.canvas.move(self.eye_left, 0, 3)
            self.canvas.move(self.eye_right, 0, 3)
            self.canvas.move(self.pupil_left, 0, 3)
            self.canvas.move(self.pupil_right, 0, 3)
            self.canvas.move(self.mouth, 0, 3)
            self.canvas.move(self.brow_left, 0, 3)
            self.canvas.move(self.brow_right, 0, 3)
            self.canvas.update()
            time.sleep(0.02)

# ==================== HALAMAN LOGIN ====================
class LoginPage:
    def __init__(self, parent, on_login_success):
        self.parent = parent
        self.on_login_success = on_login_success
        self.frame = tk.Frame(parent, bg="#FFF8DC")
        self.frame.pack(fill="both", expand=True)
        
        # Canvas untuk animasi
        self.canvas = tk.Canvas(self.frame, bg="#FFF8DC", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # Kartun sosis
        self.sausage = SausageChar(self.canvas, 200, 100)
        # Animasi jatuh dari atas
        self.sausage.y = -50
        self.sausage.canvas.coords(self.sausage.body, 200-40, -50-30, 200+40, -50+30)
        # Panggil animasi jelly jatuh
        self.sausage.jelly_fall_animation(200)
        self.sausage.update_expression("happy")
        
        # Frame kanan untuk login
        right_frame = tk.Frame(self.frame, bg="#FFF8DC")
        right_frame.pack(side="right", fill="both", expand=True, padx=50)
        
        tk.Label(right_frame, text="🎓 SELAMAT DATANG DI KUIS INTERAKTIF 🎓", font=("Arial", 16, "bold"), bg="#FFF8DC", fg="#8B4513").pack(pady=20)
        tk.Label(right_frame, text="Username:", font=("Arial", 12), bg="#FFF8DC").pack(anchor="w", pady=(20,5))
        self.entry_nama = tk.Entry(right_frame, font=("Arial", 12), width=25)
        self.entry_nama.pack(pady=5)
        self.entry_nama.bind("<FocusIn>", self.on_nama_focus)
        
        tk.Label(right_frame, text="Password:", font=("Arial", 12), bg="#FFF8DC").pack(anchor="w", pady=(10,5))
        self.entry_pass = tk.Entry(right_frame, show="*", font=("Arial", 12), width=25)
        self.entry_pass.pack(pady=5)
        self.entry_pass.bind("<FocusIn>", self.on_pass_focus)
        
        self.btn_login = tk.Button(right_frame, text="🚀 Login", font=("Arial", 12, "bold"), bg="#FFD700", fg="#8B4513", command=self.login)
        self.btn_login.pack(pady=30)
        
    def on_nama_focus(self, event):
        self.sausage.update_expression("excited")
        # Reset ekspresi setelah 1.5 detik
        self.parent.after(1500, lambda: self.sausage.update_expression("happy"))
        
    def on_pass_focus(self, event):
        self.sausage.update_expression("shy")
        self.parent.after(2000, lambda: self.sausage.update_expression("happy"))
        
    def login(self):
        nama = self.entry_nama.get().strip()
        pwd = self.entry_pass.get()
        if nama == "":
            messagebox.showwarning("Oops", "Nama tidak boleh kosong!")
            return
        if pwd != "123":  # password sederhana untuk demo
            messagebox.showerror("Gagal", "Password salah! Coba '123'")
            return
        self.frame.destroy()
        self.on_login_success(nama)

# ==================== HALAMAN KUIS ====================
class QuizPage:
    def __init__(self, parent, nama, soal_list):
        self.parent = parent
        self.nama = nama
        self.soal_list = soal_list
        self.current_index = 0
        self.score = 0
        
        self.frame = tk.Frame(parent, bg="#F0F8FF")
        self.frame.pack(fill="both", expand=True)
        
        # Header
        tk.Label(self.frame, text=f"Halo, {nama}!", font=("Arial", 14), bg="#F0F8FF").pack(anchor="w", padx=20, pady=5)
        self.progress_label = tk.Label(self.frame, text="", font=("Arial", 10), bg="#F0F8FF")
        self.progress_label.pack(anchor="e", padx=20)
        
        # Canvas untuk animasi dan kartun sosis
        self.canvas = tk.Canvas(self.frame, bg="#F0F8FF", height=250, highlightthickness=0)
        self.canvas.pack(fill="x", padx=20, pady=10)
        
        self.sausage = SausageChar(self.canvas, 300, 150)
        self.sausage.update_expression("happy")
        
        # Frame soal
        self.soal_frame = tk.Frame(self.frame, bg="#FFFFFF", relief="ridge", bd=2)
        self.soal_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.soal_label = tk.Label(self.soal_frame, text="", font=("Arial", 14, "bold"), bg="white", wraplength=600)
        self.soal_label.pack(pady=20)
        
        self.var_jawaban = tk.IntVar()
        self.pilihan_frame = tk.Frame(self.soal_frame, bg="white")
        self.pilihan_frame.pack(pady=10)
        
        self.tombol_pilihan = []
        for i in range(4):
            rb = tk.Radiobutton(self.pilihan_frame, text="", variable=self.var_jawaban, value=i, font=("Arial", 12), bg="white", anchor="w")
            rb.pack(fill="x", padx=20, pady=5)
            self.tombol_pilihan.append(rb)
        
        self.btn_next = tk.Button(self.soal_frame, text="➡️ Jawab & Lanjut", font=("Arial", 12, "bold"), bg="#32CD32", command=self.jawab)
        self.btn_next.pack(pady=20)
        
        self.load_soal()
        
    def load_soal(self):
        soal = self.soal_list[self.current_index]
        self.soal_label.config(text=f"Soal {self.current_index+1}: {soal['soal']}")
        for i, pilih in enumerate(soal['pilihan']):
            self.tombol_pilihan[i].config(text=pilih)
        self.var_jawaban.set(-1)
        self.progress_label.config(text=f"Progress: {self.current_index+1}/{len(self.soal_list)}")
        
    def tampilkan_animasi(self, benar):
        if benar:
            # Animasi jempol dan meriah
            self.sausage.update_expression("celebrate")
            # Tambahan efek confetti sederhana
            for _ in range(30):
                x = random.randint(50, 550)
                y = random.randint(50, 200)
                warna = random.choice(["red","green","blue","gold","orange"])
                self.canvas.create_oval(x, y, x+5, y+5, fill=warna, outline="")
            self.canvas.create_text(400, 50, text="👍👍👍 BENAR! 👍👍👍", font=("Arial", 20, "bold"), fill="green")
            self.parent.after(2000, self.clear_animasi)
        else:
            self.sausage.update_expression("sad")
            self.canvas.create_text(400, 50, text="😞 S A L A H 😞", font=("Arial", 20, "bold"), fill="red")
            self.parent.after(2000, self.clear_animasi)
            
    def clear_animasi(self):
        self.canvas.delete("all")
        # Redraw kartun sosis
        self.sausage = SausageChar(self.canvas, 300, 150)
        self.sausage.update_expression("happy")
        
    def jawab(self):
        if self.var_jawaban.get() == -1:
            messagebox.showwarning("Peringatan", "Pilih jawaban dulu ya!")
            return
        benar = (self.var_jawaban.get() == self.soal_list[self.current_index]['jawaban'])
        if benar:
            self.score += 1
        self.tampilkan_animasi(benar)
        
        # Tunggu animasi selesai (2 detik) lalu lanjut
        self.parent.after(2500, self.next_soal)
        
    def next_soal(self):
        self.current_index += 1
        if self.current_index < len(self.soal_list):
            self.load_soal()
        else:
            self.selesai()
            
    def selesai(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        tk.Label(self.frame, text=f"🎉 SELESAI! 🎉\nNilai kamu: {self.score}/{len(self.soal_list)}", 
                 font=("Arial", 20, "bold"), bg="#F0F8FF", fg="#8B4513").pack(expand=True)
        tk.Button(self.frame, text="Tutup Aplikasi", command=self.parent.quit, font=("Arial", 12), bg="orange").pack(pady=20)

# ==================== MAIN APP ====================
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Belajar Interaktif")
        self.root.geometry("800x600")
        self.root.configure(bg="#FFF8DC")
        self.show_login()
        
    def show_login(self):
        LoginPage(self.root, self.start_quiz)
        
    def start_quiz(self, nama):
        QuizPage(self.root, nama, soal_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()            self.canvas.coords(self.brow_right, self.x+10, self.y-22, self.x+24, self.y-20)
        elif mood == "shy":     # malu/pura2 tidak lihat (mata ke samping)
            self.canvas.itemconfig(self.eye_left, fill="white")
            self.canvas.itemconfig(self.eye_right, fill="white")
            self.canvas.coords(self.pupil_left, self.x-7, self.y-7, self.x-3, self.y-3)  # mata ke kiri
            self.canvas.coords(self.pupil_right, self.x+3, self.y-7, self.x+7, self.y-3)
            self.canvas.coords(self.mouth, self.x-12, self.y+5, self.x+12, self.y+18)
            self.canvas.itemconfig(self.mouth, start=0, extent=-120)
        elif mood == "happy":
            self.canvas.itemconfig(self.eye_left, fill="white")
            self.canvas.itemconfig(self.eye_right, fill="white")
            self.canvas.coords(self.pupil_left, self.x-17, self.y-7, self.x-13, self.y-3)
            self.canvas.coords(self.pupil_right, self.x+13, self.y-7, self.x+17, self.y-3)
            self.canvas.coords(self.mouth, self.x-15, self.y+2, self.x+15, self.y+22)
            self.canvas.itemconfig(self.mouth, start=0, extent=-200)
        elif mood == "sad":
            self.canvas.itemconfig(self.eye_left, fill="lightblue")
            self.canvas.itemconfig(self.eye_right, fill="lightblue")
            self.canvas.coords(self.mouth, self.x-12, self.y+8, self.x+12, self.y+18)
            self.canvas.itemconfig(self.mouth, start=180, extent=-180)  # mulut terbalik
        elif mood == "celebrate":
            self.canvas.itemconfig(self.eye_left, fill="gold")
            self.canvas.itemconfig(self.eye_right, fill="gold")
            self.canvas.coords(self.mouth, self.x-18, self.y+2, self.x+18, self.y+25)
            self.canvas.itemconfig(self.mouth, start=0, extent=-220)
            
    def jelly_fall_animation(self, target_y):
        # Animasi jatuh kayak jelly
        steps = 20
        dy = (target_y - self.y) / steps
        for i in range(steps):
            self.y += dy
            self.canvas.move(self.body, 0, dy)
            self.canvas.move(self.eye_left, 0, dy)
            self.canvas.move(self.eye_right, 0, dy)
            self.canvas.move(self.pupil_left, 0, dy)
            self.canvas.move(self.pupil_right, 0, dy)
            self.canvas.move(self.mouth, 0, dy)
            self.canvas.move(self.brow_left, 0, dy)
            self.canvas.move(self.brow_right, 0, dy)
            self.canvas.update()
            time.sleep(0.02)
        # Efek jelly sedikit bouncing
        for bounce in range(3):
            self.canvas.move(self.body, 0, -3)
            self.canvas.move(self.eye_left, 0, -3)
            self.canvas.move(self.eye_right, 0, -3)
            self.canvas.move(self.pupil_left, 0, -3)
            self.canvas.move(self.pupil_right, 0, -3)
            self.canvas.move(self.mouth, 0, -3)
            self.canvas.move(self.brow_left, 0, -3)
            self.canvas.move(self.brow_right, 0, -3)
            self.canvas.update()
            time.sleep(0.02)
            self.canvas.move(self.body, 0, 3)
            self.canvas.move(self.eye_left, 0, 3)
            self.canvas.move(self.eye_right, 0, 3)
            self.canvas.move(self.pupil_left, 0, 3)
            self.canvas.move(self.pupil_right, 0, 3)
            self.canvas.move(self.mouth, 0, 3)
            self.canvas.move(self.brow_left, 0, 3)
            self.canvas.move(self.brow_right, 0, 3)
            self.canvas.update()
            time.sleep(0.02)

# ==================== HALAMAN LOGIN ====================
class LoginPage:
    def __init__(self, parent, on_login_success):
        self.parent = parent
        self.on_login_success = on_login_success
        self.frame = tk.Frame(parent, bg="#FFF8DC")
        self.frame.pack(fill="both", expand=True)
        
        # Canvas untuk animasi
        self.canvas = tk.Canvas(self.frame, bg="#FFF8DC", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # Kartun sosis
        self.sausage = SausageChar(self.canvas, 200, 100)
        # Animasi jatuh dari atas
        self.sausage.y = -50
        self.sausage.canvas.coords(self.sausage.body, 200-40, -50-30, 200+40, -50+30)
        # Panggil animasi jelly jatuh
        self.sausage.jelly_fall_animation(200)
        self.sausage.update_expression("happy")
        
        # Frame kanan untuk login
        right_frame = tk.Frame(self.frame, bg="#FFF8DC")
        right_frame.pack(side="right", fill="both", expand=True, padx=50)
        
        tk.Label(right_frame, text="🎓 SELAMAT DATANG DI KUIS INTERAKTIF 🎓", font=("Arial", 16, "bold"), bg="#FFF8DC", fg="#8B4513").pack(pady=20)
        tk.Label(right_frame, text="Username:", font=("Arial", 12), bg="#FFF8DC").pack(anchor="w", pady=(20,5))
        self.entry_nama = tk.Entry(right_frame, font=("Arial", 12), width=25)
        self.entry_nama.pack(pady=5)
        self.entry_nama.bind("<FocusIn>", self.on_nama_focus)
        
        tk.Label(right_frame, text="Password:", font=("Arial", 12), bg="#FFF8DC").pack(anchor="w", pady=(10,5))
        self.entry_pass = tk.Entry(right_frame, show="*", font=("Arial", 12), width=25)
        self.entry_pass.pack(pady=5)
        self.entry_pass.bind("<FocusIn>", self.on_pass_focus)
        
        self.btn_login = tk.Button(right_frame, text="🚀 Login", font=("Arial", 12, "bold"), bg="#FFD700", fg="#8B4513", command=self.login)
        self.btn_login.pack(pady=30)
        
    def on_nama_focus(self, event):
        self.sausage.update_expression("excited")
        # Reset ekspresi setelah 1.5 detik
        self.parent.after(1500, lambda: self.sausage.update_expression("happy"))
        
    def on_pass_focus(self, event):
        self.sausage.update_expression("shy")
        self.parent.after(2000, lambda: self.sausage.update_expression("happy"))
        
    def login(self):
        nama = self.entry_nama.get().strip()
        pwd = self.entry_pass.get()
        if nama == "":
            messagebox.showwarning("Oops", "Nama tidak boleh kosong!")
            return
        if pwd != "123":  # password sederhana untuk demo
            messagebox.showerror("Gagal", "Password salah! Coba '123'")
            return
        self.frame.destroy()
        self.on_login_success(nama)

# ==================== HALAMAN KUIS ====================
class QuizPage:
    def __init__(self, parent, nama, soal_list):
        self.parent = parent
        self.nama = nama
        self.soal_list = soal_list
        self.current_index = 0
        self.score = 0
        
        self.frame = tk.Frame(parent, bg="#F0F8FF")
        self.frame.pack(fill="both", expand=True)
        
        # Header
        tk.Label(self.frame, text=f"Halo, {nama}!", font=("Arial", 14), bg="#F0F8FF").pack(anchor="w", padx=20, pady=5)
        self.progress_label = tk.Label(self.frame, text="", font=("Arial", 10), bg="#F0F8FF")
        self.progress_label.pack(anchor="e", padx=20)
        
        # Canvas untuk animasi dan kartun sosis
        self.canvas = tk.Canvas(self.frame, bg="#F0F8FF", height=250, highlightthickness=0)
        self.canvas.pack(fill="x", padx=20, pady=10)
        
        self.sausage = SausageChar(self.canvas, 300, 150)
        self.sausage.update_expression("happy")
        
        # Frame soal
        self.soal_frame = tk.Frame(self.frame, bg="#FFFFFF", relief="ridge", bd=2)
        self.soal_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.soal_label = tk.Label(self.soal_frame, text="", font=("Arial", 14, "bold"), bg="white", wraplength=600)
        self.soal_label.pack(pady=20)
        
        self.var_jawaban = tk.IntVar()
        self.pilihan_frame = tk.Frame(self.soal_frame, bg="white")
        self.pilihan_frame.pack(pady=10)
        
        self.tombol_pilihan = []
        for i in range(4):
            rb = tk.Radiobutton(self.pilihan_frame, text="", variable=self.var_jawaban, value=i, font=("Arial", 12), bg="white", anchor="w")
            rb.pack(fill="x", padx=20, pady=5)
            self.tombol_pilihan.append(rb)
        
        self.btn_next = tk.Button(self.soal_frame, text="➡️ Jawab & Lanjut", font=("Arial", 12, "bold"), bg="#32CD32", command=self.jawab)
        self.btn_next.pack(pady=20)
        
        self.load_soal()
        
    def load_soal(self):
        soal = self.soal_list[self.current_index]
        self.soal_label.config(text=f"Soal {self.current_index+1}: {soal['soal']}")
        for i, pilih in enumerate(soal['pilihan']):
            self.tombol_pilihan[i].config(text=pilih)
        self.var_jawaban.set(-1)
        self.progress_label.config(text=f"Progress: {self.current_index+1}/{len(self.soal_list)}")
        
    def tampilkan_animasi(self, benar):
        if benar:
            # Animasi jempol dan meriah
            self.sausage.update_expression("celebrate")
            # Tambahan efek confetti sederhana
            for _ in range(30):
                x = random.randint(50, 550)
                y = random.randint(50, 200)
                warna = random.choice(["red","green","blue","gold","orange"])
                self.canvas.create_oval(x, y, x+5, y+5, fill=warna, outline="")
            self.canvas.create_text(400, 50, text="👍👍👍 BENAR! 👍👍👍", font=("Arial", 20, "bold"), fill="green")
            self.parent.after(2000, self.clear_animasi)
        else:
            self.sausage.update_expression("sad")
            self.canvas.create_text(400, 50, text="😞 S A L A H 😞", font=("Arial", 20, "bold"), fill="red")
            self.parent.after(2000, self.clear_animasi)
            
    def clear_animasi(self):
        self.canvas.delete("all")
        # Redraw kartun sosis
        self.sausage = SausageChar(self.canvas, 300, 150)
        self.sausage.update_expression("happy")
        
    def jawab(self):
        if self.var_jawaban.get() == -1:
            messagebox.showwarning("Peringatan", "Pilih jawaban dulu ya!")
            return
        benar = (self.var_jawaban.get() == self.soal_list[self.current_index]['jawaban'])
        if benar:
            self.score += 1
        self.tampilkan_animasi(benar)
        
        # Tunggu animasi selesai (2 detik) lalu lanjut
        self.parent.after(2500, self.next_soal)
        
    def next_soal(self):
        self.current_index += 1
        if self.current_index < len(self.soal_list):
            self.load_soal()
        else:
            self.selesai()
            
    def selesai(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        tk.Label(self.frame, text=f"🎉 SELESAI! 🎉\nNilai kamu: {self.score}/{len(self.soal_list)}", 
                 font=("Arial", 20, "bold"), bg="#F0F8FF", fg="#8B4513").pack(expand=True)
        tk.Button(self.frame, text="Tutup Aplikasi", command=self.parent.quit, font=("Arial", 12), bg="orange").pack(pady=20)

# ==================== MAIN APP ====================
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Belajar Interaktif")
        self.root.geometry("800x600")
        self.root.configure(bg="#FFF8DC")
        self.show_login()
        
    def show_login(self):
        LoginPage(self.root, self.start_quiz)
        
    def start_quiz(self, nama):
        QuizPage(self.root, nama, soal_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

# ==================== DATA SOAL ====================
soal_data = [
    {
        "soal": "Apa ibu kota Indonesia?",
        "pilihan": ["Jakarta", "Bandung", "Surabaya", "Medan"],
        "jawaban": 0  # index 0 = Jakarta
    },
    {
        "soal": "Siapakah presiden pertama Indonesia?",
        "pilihan": ["Soeharto", "Soekarno", "Habibie", "Gus Dur"],
        "jawaban": 1
    },
    {
        "soal": "Berapa hasil 5 + 3 x 2?",
        "pilihan": ["16", "11", "10", "13"],
        "jawaban": 1  # 5+6=11
    },
    {
        "soal": "Planet terdekat dengan Matahari adalah?",
        "pilihan": ["Venus", "Mars", "Merkurius", "Bumi"],
        "jawaban": 2
    },
    {
        "soal": "Hewan apa yang bisa hidup di air dan darat?",
        "pilihan": ["Kucing", "Amfibi", "Ikan", "Burung"],
        "jawaban": 1
    }
]

# ==================== KELAS KARTUN SOSIS ====================
class SausageChar:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.eye_direction = "depan"  # depan, kiri, kanan
        self.mouth_shape = "normal"   # normal, senang, sedih, kaget
        
        # Gambar tubuh lonjong (sosis)
        self.body = canvas.create_oval(x-40, y-30, x+40, y+30, fill="#F4A460", outline="#D2691E", width=2)
        # Mata kiri dan kanan
        self.eye_left = canvas.create_oval(x-20, y-10, x-10, y, fill="white", outline="black")
        self.eye_right = canvas.create_oval(x+10, y-10, x+20, y, fill="white", outline="black")
        self.pupil_left = canvas.create_oval(x-17, y-7, x-13, y-3, fill="black")
        self.pupil_right = canvas.create_oval(x+13, y-7, x+17, y-3, fill="black")
        # Mulut
        self.mouth = canvas.create_arc(x-15, y+5, x+15, y+20, start=0, extent=-180, fill="#8B4513", outline="black")
        # Alis (opsional untuk ekspresi)
        self.brow_left = canvas.create_line(x-22, y-15, x-12, y-18, fill="black", width=2)
        self.brow_right = canvas.create_line(x+12, y-18, x+22, y-15, fill="black", width=2)
        
        self.default_mouth_extent = -180
        
    def update_expression(self, mood):
        # mood: "excited", "shy", "happy", "sad", "shock", "celebrate"
        if mood == "excited":   # bersemangat (mata besar, mulut terbuka lebar)
            self.canvas.itemconfig(self.eye_left, fill="yellow")
            self.canvas.itemconfig(self.eye_right, fill="yellow")
            self.canvas.coords(self.mouth, self.x-18, self.y+5, self.x+18, self.y+25)
            self.canvas.itemconfig(self.mouth, start=0, extent=-200)
            self.canvas.coords(self.brow_left, self.x-24, self.y-20, self.x-10, self.y-22)
            self.canvas.coords(self.brow_right, self.x+10, self.y-22, self.x+24, self.y-20)
        elif mood == "shy":     # malu/pura2 tidak lihat (mata ke samping)
            self.canvas.itemconfig(self.eye_left, fill="white")
            self.canvas.itemconfig(self.eye_right, fill="white")
            self.canvas.coords(self.pupil_left, self.x-7, self.y-7, self.x-3, self.y-3)  # mata ke kiri
            self.canvas.coords(self.pupil_right, self.x+3, self.y-7, self.x+7, self.y-3)
            self.canvas.coords(self.mouth, self.x-12, self.y+5, self.x+12, self.y+18)
            self.canvas.itemconfig(self.mouth, start=0, extent=-120)
        elif mood == "happy":
            self.canvas.itemconfig(self.eye_left, fill="white")
            self.canvas.itemconfig(self.eye_right, fill="white")
            self.canvas.coords(self.pupil_left, self.x-17, self.y-7, self.x-13, self.y-3)
            self.canvas.coords(self.pupil_right, self.x+13, self.y-7, self.x+17, self.y-3)
            self.canvas.coords(self.mouth, self.x-15, self.y+2, self.x+15, self.y+22)
            self.canvas.itemconfig(self.mouth, start=0, extent=-200)
        elif mood == "sad":
            self.canvas.itemconfig(self.eye_left, fill="lightblue")
            self.canvas.itemconfig(self.eye_right, fill="lightblue")
            self.canvas.coords(self.mouth, self.x-12, self.y+8, self.x+12, self.y+18)
            self.canvas.itemconfig(self.mouth, start=180, extent=-180)  # mulut terbalik
        elif mood == "celebrate":
            self.canvas.itemconfig(self.eye_left, fill="gold")
            self.canvas.itemconfig(self.eye_right, fill="gold")
            self.canvas.coords(self.mouth, self.x-18, self.y+2, self.x+18, self.y+25)
            self.canvas.itemconfig(self.mouth, start=0, extent=-220)
            
    def jelly_fall_animation(self, target_y):
        # Animasi jatuh kayak jelly
        steps = 20
        dy = (target_y - self.y) / steps
        for i in range(steps):
            self.y += dy
            self.canvas.move(self.body, 0, dy)
            self.canvas.move(self.eye_left, 0, dy)
            self.canvas.move(self.eye_right, 0, dy)
            self.canvas.move(self.pupil_left, 0, dy)
            self.canvas.move(self.pupil_right, 0, dy)
            self.canvas.move(self.mouth, 0, dy)
            self.canvas.move(self.brow_left, 0, dy)
            self.canvas.move(self.brow_right, 0, dy)
            self.canvas.update()
            time.sleep(0.02)
        # Efek jelly sedikit bouncing
        for bounce in range(3):
            self.canvas.move(self.body, 0, -3)
            self.canvas.move(self.eye_left, 0, -3)
            self.canvas.move(self.eye_right, 0, -3)
            self.canvas.move(self.pupil_left, 0, -3)
            self.canvas.move(self.pupil_right, 0, -3)
            self.canvas.move(self.mouth, 0, -3)
            self.canvas.move(self.brow_left, 0, -3)
            self.canvas.move(self.brow_right, 0, -3)
            self.canvas.update()
            time.sleep(0.02)
            self.canvas.move(self.body, 0, 3)
            self.canvas.move(self.eye_left, 0, 3)
            self.canvas.move(self.eye_right, 0, 3)
            self.canvas.move(self.pupil_left, 0, 3)
            self.canvas.move(self.pupil_right, 0, 3)
            self.canvas.move(self.mouth, 0, 3)
            self.canvas.move(self.brow_left, 0, 3)
            self.canvas.move(self.brow_right, 0, 3)
            self.canvas.update()
            time.sleep(0.02)

# ==================== HALAMAN LOGIN ====================
class LoginPage:
    def __init__(self, parent, on_login_success):
        self.parent = parent
        self.on_login_success = on_login_success
        self.frame = tk.Frame(parent, bg="#FFF8DC")
        self.frame.pack(fill="both", expand=True)
        
        # Canvas untuk animasi
        self.canvas = tk.Canvas(self.frame, bg="#FFF8DC", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # Kartun sosis
        self.sausage = SausageChar(self.canvas, 200, 100)
        # Animasi jatuh dari atas
        self.sausage.y = -50
        self.sausage.canvas.coords(self.sausage.body, 200-40, -50-30, 200+40, -50+30)
        # Panggil animasi jelly jatuh
        self.sausage.jelly_fall_animation(200)
        self.sausage.update_expression("happy")
        
        # Frame kanan untuk login
        right_frame = tk.Frame(self.frame, bg="#FFF8DC")
        right_frame.pack(side="right", fill="both", expand=True, padx=50)
        
        tk.Label(right_frame, text="🎓 SELAMAT DATANG DI KUIS INTERAKTIF 🎓", font=("Arial", 16, "bold"), bg="#FFF8DC", fg="#8B4513").pack(pady=20)
        tk.Label(right_frame, text="Username:", font=("Arial", 12), bg="#FFF8DC").pack(anchor="w", pady=(20,5))
        self.entry_nama = tk.Entry(right_frame, font=("Arial", 12), width=25)
        self.entry_nama.pack(pady=5)
        self.entry_nama.bind("<FocusIn>", self.on_nama_focus)
        
        tk.Label(right_frame, text="Password:", font=("Arial", 12), bg="#FFF8DC").pack(anchor="w", pady=(10,5))
        self.entry_pass = tk.Entry(right_frame, show="*", font=("Arial", 12), width=25)
        self.entry_pass.pack(pady=5)
        self.entry_pass.bind("<FocusIn>", self.on_pass_focus)
        
        self.btn_login = tk.Button(right_frame, text="🚀 Login", font=("Arial", 12, "bold"), bg="#FFD700", fg="#8B4513", command=self.login)
        self.btn_login.pack(pady=30)
        
    def on_nama_focus(self, event):
        self.sausage.update_expression("excited")
        # Reset ekspresi setelah 1.5 detik
        self.parent.after(1500, lambda: self.sausage.update_expression("happy"))
        
    def on_pass_focus(self, event):
        self.sausage.update_expression("shy")
        self.parent.after(2000, lambda: self.sausage.update_expression("happy"))
        
    def login(self):
        nama = self.entry_nama.get().strip()
        pwd = self.entry_pass.get()
        if nama == "":
            messagebox.showwarning("Oops", "Nama tidak boleh kosong!")
            return
        if pwd != "123":  # password sederhana untuk demo
            messagebox.showerror("Gagal", "Password salah! Coba '123'")
            return
        self.frame.destroy()
        self.on_login_success(nama)

# ==================== HALAMAN KUIS ====================
class QuizPage:
    def __init__(self, parent, nama, soal_list):
        self.parent = parent
        self.nama = nama
        self.soal_list = soal_list
        self.current_index = 0
        self.score = 0
        
        self.frame = tk.Frame(parent, bg="#F0F8FF")
        self.frame.pack(fill="both", expand=True)
        
        # Header
        tk.Label(self.frame, text=f"Halo, {nama}!", font=("Arial", 14), bg="#F0F8FF").pack(anchor="w", padx=20, pady=5)
        self.progress_label = tk.Label(self.frame, text="", font=("Arial", 10), bg="#F0F8FF")
        self.progress_label.pack(anchor="e", padx=20)
        
        # Canvas untuk animasi dan kartun sosis
        self.canvas = tk.Canvas(self.frame, bg="#F0F8FF", height=250, highlightthickness=0)
        self.canvas.pack(fill="x", padx=20, pady=10)
        
        self.sausage = SausageChar(self.canvas, 300, 150)
        self.sausage.update_expression("happy")
        
        # Frame soal
        self.soal_frame = tk.Frame(self.frame, bg="#FFFFFF", relief="ridge", bd=2)
        self.soal_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.soal_label = tk.Label(self.soal_frame, text="", font=("Arial", 14, "bold"), bg="white", wraplength=600)
        self.soal_label.pack(pady=20)
        
        self.var_jawaban = tk.IntVar()
        self.pilihan_frame = tk.Frame(self.soal_frame, bg="white")
        self.pilihan_frame.pack(pady=10)
        
        self.tombol_pilihan = []
        for i in range(4):
            rb = tk.Radiobutton(self.pilihan_frame, text="", variable=self.var_jawaban, value=i, font=("Arial", 12), bg="white", anchor="w")
            rb.pack(fill="x", padx=20, pady=5)
            self.tombol_pilihan.append(rb)
        
        self.btn_next = tk.Button(self.soal_frame, text="➡️ Jawab & Lanjut", font=("Arial", 12, "bold"), bg="#32CD32", command=self.jawab)
        self.btn_next.pack(pady=20)
        
        self.load_soal()
        
    def load_soal(self):
        soal = self.soal_list[self.current_index]
        self.soal_label.config(text=f"Soal {self.current_index+1}: {soal['soal']}")
        for i, pilih in enumerate(soal['pilihan']):
            self.tombol_pilihan[i].config(text=pilih)
        self.var_jawaban.set(-1)
        self.progress_label.config(text=f"Progress: {self.current_index+1}/{len(self.soal_list)}")
        
    def tampilkan_animasi(self, benar):
        if benar:
            # Animasi jempol dan meriah
            self.sausage.update_expression("celebrate")
            # Tambahan efek confetti sederhana
            for _ in range(30):
                x = random.randint(50, 550)
                y = random.randint(50, 200)
                warna = random.choice(["red","green","blue","gold","orange"])
                self.canvas.create_oval(x, y, x+5, y+5, fill=warna, outline="")
            self.canvas.create_text(400, 50, text="👍👍👍 BENAR! 👍👍👍", font=("Arial", 20, "bold"), fill="green")
            self.parent.after(2000, self.clear_animasi)
        else:
            self.sausage.update_expression("sad")
            self.canvas.create_text(400, 50, text="😞 S A L A H 😞", font=("Arial", 20, "bold"), fill="red")
            self.parent.after(2000, self.clear_animasi)
            
    def clear_animasi(self):
        self.canvas.delete("all")
        # Redraw kartun sosis
        self.sausage = SausageChar(self.canvas, 300, 150)
        self.sausage.update_expression("happy")
        
    def jawab(self):
        if self.var_jawaban.get() == -1:
            messagebox.showwarning("Peringatan", "Pilih jawaban dulu ya!")
            return
        benar = (self.var_jawaban.get() == self.soal_list[self.current_index]['jawaban'])
        if benar:
            self.score += 1
        self.tampilkan_animasi(benar)
        
        # Tunggu animasi selesai (2 detik) lalu lanjut
        self.parent.after(2500, self.next_soal)
        
    def next_soal(self):
        self.current_index += 1
        if self.current_index < len(self.soal_list):
            self.load_soal()
        else:
            self.selesai()
            
    def selesai(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        tk.Label(self.frame, text=f"🎉 SELESAI! 🎉\nNilai kamu: {self.score}/{len(self.soal_list)}", 
                 font=("Arial", 20, "bold"), bg="#F0F8FF", fg="#8B4513").pack(expand=True)
        tk.Button(self.frame, text="Tutup Aplikasi", command=self.parent.quit, font=("Arial", 12), bg="orange").pack(pady=20)

# ==================== MAIN APP ====================
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Belajar Interaktif")
        self.root.geometry("800x600")
        self.root.configure(bg="#FFF8DC")
        self.show_login()
        
    def show_login(self):
        LoginPage(self.root, self.start_quiz)
        
    def start_quiz(self, nama):
        QuizPage(self.root, nama, soal_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
