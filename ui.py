import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
from database import Database
from PIL import Image, ImageTk

class DersProgramiUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lise Ders Programı")
        self.root.geometry("950x750")
        self.root.config(bg="#f0f0f0")

        # Veritabanı bağlantısı
        self.db = Database()

        # Logo dosyasının bulunduğu klasörü belirt
        logo_path = "klasor_adı/logo.png"  # Logo dosyasının yolunu belirt

        # Logo'yu yükleme ve boyutlandırma
        try:
            logo_image = Image.open(logo_path)  # Logo dosyasını aç
            logo_image = logo_image.resize((50, 50))  # Logonun boyutunu ayarla (50x50 px)
            self.logo = ImageTk.PhotoImage(logo_image)  # tkinter ile kullanılabilir hale getir
        except Exception as e:
            print(f"Logo yüklenemedi: {e}")
            self.logo = None

        # Üst bilgi çerçevesi
        self.header_frame = tk.Frame(root, bg="#f0f0f0")
        self.header_frame.pack(pady=20)

        # Logo ve başlığı yan yana hizala
        if self.logo:
            self.logo_label = tk.Label(self.header_frame, image=self.logo, bg="#f0f0f0")
            self.logo_label.grid(row=0, column=0, padx=10)  # Logoyu ilk sütuna yerleştir

        # Başlık
        self.title_label = tk.Label(self.header_frame, text="Lise Ders Programı", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        self.title_label.grid(row=0, column=1, padx=10)  # Başlığı logo'nun sağına hizala

        # Öğrenci Bilgileri Bölümü
        self.student_frame = tk.Frame(root, bg="#f0f0f0")
        self.student_frame.pack(pady=10, padx=10, fill="x")

        self.ogrenci_bilgisi_label = tk.Label(self.student_frame, text="ÖĞRENCİ BİLGİSİ", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
        self.ogrenci_bilgisi_label.grid(row=0, column=0, columnspan=6, pady=10)

        self.ad_label = tk.Label(self.student_frame, text="Ad:", font=("Helvetica", 12), bg="#f0f0f0")
        self.ad_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ad_entry = tk.Entry(self.student_frame, font=("Helvetica", 12), bd=2, relief="groove", width=20)
        self.ad_entry.grid(row=1, column=1, padx=10, pady=5)

        self.soyad_label = tk.Label(self.student_frame, text="Soyad:", font=("Helvetica", 12), bg="#f0f0f0")
        self.soyad_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.soyad_entry = tk.Entry(self.student_frame, font=("Helvetica", 12), bd=2, relief="groove", width=20)
        self.soyad_entry.grid(row=1, column=3, padx=10, pady=5)

        self.note_label = tk.Label(self.student_frame, text="Not:", font=("Helvetica", 12), bg="#f0f0f0")
        self.note_label.grid(row=1, column=4, padx=10, pady=5, sticky="w")
        self.note_text = tk.Text(self.student_frame, font=("Helvetica", 12), height=2, width=30, bd=2, relief="groove")
        self.note_text.grid(row=1, column=5, padx=10, pady=5)

        # Ders Programı Bölümü
        self.program_frame = tk.Frame(root, bg="#f0f0f0")
        self.program_frame.pack(pady=20, padx=10, fill="x")

        self.create_gun_cizelge()

        # Kaydet, Öğrenci Listesi ve Öğrenci Sil Butonları
        self.button_frame = tk.Frame(root, bg="#f0f0f0")
        self.button_frame.pack(pady=30)

        self.kaydet_button = tk.Button(self.button_frame, text="Kaydet", command=self.kaydet, font=("Helvetica", 12), bg="#4CAF50", fg="white", width=15)
        self.kaydet_button.grid(row=0, column=0, padx=20, pady=10)

        self.show_students_button = tk.Button(self.button_frame, text="Öğrencileri Görüntüle", command=self.show_students, font=("Helvetica", 12), bg="#2196F3", fg="white", width=20)
        self.show_students_button.grid(row=0, column=1, padx=20, pady=10)

        self.delete_student_button = tk.Button(self.button_frame, text="Öğrenci Sil", command=self.delete_student_screen, font=("Helvetica", 12), bg="#f44336", fg="white", width=15)
        self.delete_student_button.grid(row=0, column=2, padx=20, pady=10)

    def create_gun_cizelge(self):
        # Haftanın günleri için her gün 3 ders, 3 konu ve 3 saat seçimi
        self.cizelge = {}
        self.dersler = ["Türkçe", "Matematik", "Fizik", "Biyoloji", "Türk Edebiyatı"]
        self.gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

        for i, gun in enumerate(self.gunler):
            gun_label = tk.Label(self.program_frame, text=f"{gun}:", font=("Helvetica", 12, "bold"), bg="#f0f0f0")
            gun_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            self.cizelge[gun] = []
            for j in range(3):
                ders_var = tk.StringVar()
                konu_var = tk.StringVar()
                saat_var = tk.StringVar()

                ders_dropdown = ttk.Combobox(self.program_frame, values=self.dersler, textvariable=ders_var, font=("Helvetica", 10), width=15)
                ders_dropdown.grid(row=i, column=j * 3 + 1, padx=5, pady=5)

                konu_dropdown = ttk.Combobox(self.program_frame, values=[], textvariable=konu_var, font=("Helvetica", 10), width=15)
                konu_dropdown.grid(row=i, column=j * 3 + 2, padx=5, pady=5)

                saat_dropdown = ttk.Combobox(self.program_frame, values=["1", "2", "3", "4"], textvariable=saat_var, font=("Helvetica", 10), width=5)
                saat_dropdown.grid(row=i, column=j * 3 + 3, padx=5, pady=5)

                ders_dropdown.bind("<<ComboboxSelected>>", lambda event, d=ders_var, k=konu_dropdown: self.update_konular(event, d, k))

                self.cizelge[gun].append({"ders": ders_var, "konu": konu_var, "saat": saat_var})

    def update_konular(self, event, ders_var, konu_dropdown):
        ders = ders_var.get()
        konular = {
            "Türkçe": ["Sözcükte Anlam", "Cümlede Anlam", "Paragraf", "Ses Bilgisi", "Yazım Kuralları"],
            "Matematik": ["Fonksiyonlar", "Trigonometri", "Permütasyon-Kombinasyon", "Limit ve Türev", "İstatistik"],
            "Fizik": ["Kuvvet ve Hareket", "Elektrik ve Manyetizma", "Optik", "Termodinamik", "Atom Fiziği"],
            "Biyoloji": ["Hücre", "Canlılar ve Çevre", "Ekoloji", "Genetik", "Bitkiler"],
            "Türk Edebiyatı": ["Divan Edebiyatı", "Tanzimat Dönemi", "Servet-i Fünun", "Milli Edebiyat", "Cumhuriyet Dönemi"]
        }
        konu_dropdown['values'] = konular.get(ders, [])

    def kaydet(self):
        ad = self.ad_entry.get()
        soyad = self.soyad_entry.get()
        notu = self.note_text.get("1.0", "end-1c")
        if not ad or not soyad:
            messagebox.showwarning("Uyarı", "Lütfen öğrencinin adını ve soyadını girin.")
            return
        ogrenci_id = self.db.insert_ogrenci(ad, soyad, notu)
        for gun, ders_bilgileri in self.cizelge.items():
            for ders_konu in ders_bilgileri:
                ders = ders_konu["ders"].get()
                konu = ders_konu["konu"].get()
                saat = ders_konu["saat"].get()
                if ders and konu and saat:
                    self.db.insert_program(ogrenci_id, gun, ders, konu, saat)
        messagebox.showinfo("Başarılı", f"{ad} {soyad}'nın ders programı kaydedildi.")
        self.clear_form()

    def clear_form(self):
        self.ad_entry.delete(0, 'end')
        self.soyad_entry.delete(0, 'end')
        self.note_text.delete("1.0", 'end')

    def show_students(self):
        ogrenciler = self.db.get_ogrenciler()
        if not ogrenciler:
            messagebox.showinfo("Bilgi", "Henüz kayıtlı öğrenci yok.")
            return
        show_window = tk.Toplevel(self.root)
        show_window.title("Öğrenci Listesi")
        show_window.geometry("600x400")

        columns = ("Ad", "Soyad", "Not")
        tree = ttk.Treeview(show_window, columns=columns, show='headings', height=10)
        tree.heading("Ad", text="Ad", anchor=tk.CENTER)
        tree.heading("Soyad", text="Soyad", anchor=tk.CENTER)
        tree.heading("Not", text="Not", anchor=tk.CENTER)
        tree.pack(expand=True, fill="both")

        for ogrenci in ogrenciler:
            tree.insert("", "end", values=(ogrenci[1], ogrenci[2], ogrenci[3]))

        tree.bind("<Double-1>", lambda event: self.show_student_detail(tree.item(tree.selection())['values']))

    def show_student_detail(self, ogrenci_info):
        ad, soyad, notu = ogrenci_info
        ogrenci_id = self.db.get_ogrenci_id(ad, soyad)
        program = self.db.get_program_by_ogrenci(ogrenci_id)

        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"{ad} {soyad} - Detaylar")
        detail_window.geometry("600x400")

        columns = ("Gün", "Ders", "Konu", "Saat")
        detail_table = ttk.Treeview(detail_window, columns=columns, show="headings", height=10)
        detail_table.heading("Gün", text="Gün", anchor=tk.CENTER)
        detail_table.heading("Ders", text="Ders", anchor=tk.CENTER)
        detail_table.heading("Konu", text="Konu", anchor=tk.CENTER)
        detail_table.heading("Saat", text="Saat", anchor=tk.CENTER)

        for gun, ders, konu, saat in program:
            detail_table.insert("", "end", values=(gun, ders, konu, saat))

        detail_table.pack(expand=True, fill="both")

    def delete_student_screen(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Öğrenci Sil")
        delete_window.geometry("400x200")

        tk.Label(delete_window, text="Silmek istediğiniz öğrencinin adını ve soyadını girin:", font=("Helvetica", 12)).pack(pady=10)
        ad_entry = tk.Entry(delete_window, font=("Helvetica", 12))
        ad_entry.pack(pady=5)

        soyad_entry = tk.Entry(delete_window, font=("Helvetica", 12))
        soyad_entry.pack(pady=5)

        delete_button = tk.Button(delete_window, text="Sil", font=("Helvetica", 12), bg="#f44336", fg="white",
                                  command=lambda: self.delete_student(ad_entry.get(), soyad_entry.get(), delete_window))
        delete_button.pack(pady=20)

    def delete_student(self, ad, soyad, window):
        if not ad or not soyad:
            messagebox.showwarning("Uyarı", "Lütfen öğrencinin adını ve soyadını girin.")
            return
        ogrenci_id = self.db.get_ogrenci_id(ad, soyad)
        if ogrenci_id:
            self.db.delete_ogrenci(ogrenci_id)
            messagebox.showinfo("Başarılı", f"{ad} {soyad} başarıyla silindi.")
            window.destroy()
        else:
            messagebox.showerror("Hata", "Bu isimde bir öğrenci bulunamadı.")


# Ana pencereyi oluşturma
if __name__ == "__main__":
    root = tk.Tk()
    app = DersProgramiUI(root)
    root.mainloop()
