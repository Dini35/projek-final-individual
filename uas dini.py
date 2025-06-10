import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3

status_pembayaran = False

conn = sqlite3.connect("pembayaran ukt mahasiswa.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS histori_pembayaran (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    invoice TEXT,
    nominal TEXT,
    metode TEXT,
    waktu TEXT
)
""")
conn.commit()

root = tk.Tk()
root.title("Pembayaran UKT")
root.geometry("450x600")
root.configure(bg='white')

form_frame = None
menu_frame = None

def tampilkan_struk(nama, invoice, nominal, metode):
    struk_popup = tk.Toplevel()
    struk_popup.title("Struk Pembayaran")
    struk_popup.geometry("300x280")
    struk_popup.resizable(False, False)
    struk_popup.configure(bg="white")

    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    tk.Label(struk_popup, text="STRUK PEMBAYARAN", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
    tk.Label(struk_popup, text=f"Nama     : {nama}", font=("Arial", 12), bg="white").pack(anchor="w", padx=20)
    tk.Label(struk_popup, text=f"Prodi    : PTI", font=("Arial", 12), bg="white").pack(anchor="w", padx=20)
    tk.Label(struk_popup, text=f"Invoice  : {invoice}", font=("Arial", 12), bg="white").pack(anchor="w", padx=20)
    tk.Label(struk_popup, text=f"Nominal  : {nominal}", font=("Arial", 12), bg="white").pack(anchor="w", padx=20)
    tk.Label(struk_popup, text=f"Metode   : {metode}", font=("Arial", 12), bg="white").pack(anchor="w", padx=20)
    tk.Label(struk_popup, text=f"Waktu    : {waktu}", font=("Arial", 12), bg="white").pack(anchor="w", padx=20)

    tk.Button(struk_popup, text="Tutup", font=("Arial", 12), command=struk_popup.destroy).pack(pady=15)

def proses_pembayaran():
    global status_pembayaran

    nama = entry_nama.get().strip()
    invoice = entry_invoice.get().strip()
    nominal = entry_nominal.get().strip()
    metode = metode_var.get()
    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    if not nama or not invoice or not nominal:
        label_keterangan.config(text="Semua field harus diisi!", fg="red")
        messagebox.showwarning("Peringatan", "Semua field harus diisi!")
        return

    konfirmasi = messagebox.askyesno(
        "Konfirmasi",
        f"Apakah Anda yakin ingin membayar sebesar {nominal} untuk invoice {invoice} menggunakan {metode}?"
    )

    if konfirmasi:
        status_pembayaran = True
        label_keterangan.config(text="Pembayaran berhasil diproses.", fg="green")

        # Simpan ke database SQLite
        cursor.execute("""
        INSERT INTO histori_pembayaran (nama, invoice, nominal, metode, waktu)
        VALUES (?, ?, ?, ?, ?)
        """, (nama, invoice, nominal, metode, waktu))
        conn.commit()

        # Tambahan: Cetak ke terminal
        print("Data berhasil disimpan:")
        print(nama, invoice, nominal, metode, waktu)

        popup = tk.Toplevel()
        popup.title("Info")
        popup.geometry("250x150")
        popup.resizable(False, False)
        popup.configure(bg="white")

        tk.Label(popup, text="Pembayaran Berhasil", font=("Arial", 12), bg="white").pack(pady=(10, 0))
        tk.Label(popup, text=nama, font=("Arial", 12), bg="white").pack()
        tk.Label(popup, text=f"Invoice: {invoice}", font=("Arial", 10), bg="white").pack(pady=(0, 10))

        def tutup_popup():
            popup.destroy()
            tampilkan_struk(nama, invoice, nominal, metode)

        selesai_button = tk.Button(popup, text="Selesai", font=("Arial", 12), command=tutup_popup)
        selesai_button.pack()
    else:
        label_keterangan.config(text="Pembayaran dibatalkan.", fg="orange")


def tampilkan_histori():
    histori_popup = tk.Toplevel()
    histori_popup.title("Histori Pembayaran")
    histori_popup.geometry("400x300")
    histori_popup.configure(bg="white")

    tk.Label(histori_popup, text="Histori Pembayaran", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    text_area = tk.Text(histori_popup, wrap=tk.WORD, bg="white", font=("Arial", 10))
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    cursor.execute("SELECT nama, invoice, nominal, metode, waktu FROM histori_pembayaran")
    data = cursor.fetchall()
    for row in data:
        isi = f"Nama: {row[0]}\nInvoice: {row[1]}\nNominal: {row[2]}\nMetode: {row[3]}\nWaktu: {row[4]}\n{'-'*40}\n"
        text_area.insert(tk.END, isi)

    text_area.config(state='disabled')

def tampilkan_form_pembayaran():
    menu_frame.pack_forget()
    form_frame.pack(pady=15)

def tampilkan_menu_keuangan():
    form_frame.pack_forget()
    menu_frame.pack(pady=15)

def tampilkan_isi_krs():
    if status_pembayaran:
        krs = tk.Toplevel()
        krs.title("Isi KRS")
        krs.geometry("300x250")
        krs.configure(bg="white")

        tk.Label(krs, text="Pilih Mata Kuliah", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        daftar_mk = ["Pemrograman Visual", "UI & UX", "Data Science", "TOEFL"]
        for mk in daftar_mk:
            tk.Checkbutton(krs, text=mk, bg="white").pack(anchor="w", padx=20)

        tk.Button(krs, text="Simpan", bg="green", fg="white", command=krs.destroy).pack(pady=10)
    else:
        messagebox.showwarning("Belum Bayar", "Silakan bayar UKT terlebih dahulu.")

def popup_masuk_edlink():
    login_popup = tk.Toplevel()
    login_popup.title("Masuk Edlink")
    login_popup.geometry("350x200")
    login_popup.resizable(False, False)
    login_popup.configure(bg="white")

    tk.Label(login_popup, text="Silakan login ke aplikasi Edlink", font=("Arial", 12, "bold"), bg="white", fg="blue").pack(pady=20)
    tk.Label(login_popup, text="login untuk melakukan pembayaran UKT", font=("Arial", 10), bg="white", fg="gray").pack()

    def masuk():
        login_popup.destroy()
        tampilkan_menu_keuangan()

    tk.Button(login_popup, text="Masuk Edlink", font=("Arial", 12), bg="green", fg="white", command=masuk).pack(pady=20)

menu_frame = tk.Frame(root, bg="white")
tk.Label(menu_frame, text="Menu Keuangan", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

def salin_invoice():
    invoice_default = "12345"
    entry_invoice.delete(0, tk.END)
    entry_invoice.insert(0, invoice_default)

    entry_nama.delete(0, tk.END)
    entry_nama.insert(0, "Dini Rahmawati")

    root.clipboard_clear()
    root.clipboard_append(invoice_default)
    messagebox.showinfo("Disalin", f"Nomor invoice '{invoice_default}' berhasil disalin.\nSilakan lanjut ke pembayaran.")

tk.Button(menu_frame, text="Salin Nomor Invoice", width=25, command=salin_invoice).pack(pady=5)
tk.Button(menu_frame, text="Bayar UKT", width=25, command=tampilkan_form_pembayaran).pack(pady=5)
tk.Button(menu_frame, text="Isi KRS", width=25, command=tampilkan_isi_krs).pack(pady=5)
tk.Button(menu_frame, text="Lihat Histori Pembayaran", width=25, command=tampilkan_histori).pack(pady=5)

form_frame = tk.Frame(root, bg="white")

tk.Label(form_frame, text="Pembayaran UKT", font=("Arial", 16, "bold"), bg='white').pack(pady=10)

tk.Label(form_frame, text="Nama", bg='white').pack()
entry_nama = tk.Entry(form_frame, width=40)
entry_nama.pack(pady=5)

tk.Label(form_frame, text="Nomor Invoice", bg='white').pack()
entry_invoice = tk.Entry(form_frame, width=40)
entry_invoice.pack(pady=5)

tk.Label(form_frame, text="Nominal Pembayaran", bg='white').pack()
entry_nominal = tk.Entry(form_frame, width=40)
entry_nominal.pack(pady=5)

metode_var = tk.StringVar()
metode_var.set("Transfer Bank")

frame_tombol = tk.Frame(form_frame, bg='white')
btn_bayar = tk.Button(frame_tombol, text="Bayar Sekarang", fg='black', width=15, command=proses_pembayaran)
btn_bayar.grid(row=0, column=0, padx=10)
frame_tombol.pack(pady=10)

label_keterangan = tk.Label(form_frame, text="Klik Bayar Sekarang untuk konfirmasi pembayaran.", bg='white', font=("Arial", 10), fg='blue')
label_keterangan.pack(pady=5)

tk.Button(form_frame, text="Kembali ke Menu Keuangan", command=tampilkan_menu_keuangan).pack(pady=10)

root.after(100, popup_masuk_edlink)
root.mainloop()
