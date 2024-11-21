import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

win = tk.Tk()
win.title("Giao diện tính toán")
win.geometry("300x250")  
win.resizable(False, False)

# Tạo notebook (tab)
notebook = ttk.Notebook(win)
notebook.pack(pady=10, padx=10, expand=True)


tab_tinh_toan = ttk.Frame(notebook)
notebook.add(tab_tinh_toan, text="Tính toán")


tab_nam_nhuan = ttk.Frame(notebook)
notebook.add(tab_nam_nhuan, text="Năm nhuận")


tab_tinh_tuoi = ttk.Frame(notebook)
notebook.add(tab_tinh_tuoi, text="Tính tuổi")



ttk.Label(tab_tinh_toan, text="Số a: ").grid(column=0, row=0, sticky='w')
so_a = tk.StringVar()
so_a_entered = ttk.Entry(tab_tinh_toan, width=15, textvariable=so_a)
so_a_entered.grid(column=1, row=0)

ttk.Label(tab_tinh_toan, text="Số b: ").grid(column=0, row=1, sticky='w')
so_b = tk.StringVar()
so_b_entered = ttk.Entry(tab_tinh_toan, width=15, textvariable=so_b)
so_b_entered.grid(column=1, row=1)

ket_qua_label = ttk.Label(tab_tinh_toan, text="Kết quả: ")
ket_qua_label.grid(column=0, row=2, sticky='w', columnspan=2)

def is_number(gia_tri):
    try:
        float(gia_tri)
        return True
    except ValueError:
        return False

def cong():
    if (is_number(so_a.get()) and is_number(so_b.get())):
        ket_qua_label.configure(text="Kết quả: " + str((float(so_a.get()) + float(so_b.get()))))
    else:
        messagebox.showerror("Lỗi nhập liệu", "Vui lòng chỉ nhập giá trị số")

button_cong = ttk.Button(tab_tinh_toan, text="+", width=3, command=cong)
button_cong.grid(column=2, row=0)

def tru():
    if (is_number(so_a.get()) and is_number(so_b.get())):
        ket_qua_label.configure(text="Kết quả: " + str((float(so_a.get()) - float(so_b.get()))))
    else:
        messagebox.showerror("Lỗi nhập liệu", "Vui lòng chỉ nhập giá trị số")

button_tru = ttk.Button(tab_tinh_toan, text="-", width=3, command=tru)
button_tru.grid(column=3, row=0)

def nhan():
    if (is_number(so_a.get()) and is_number(so_b.get())):
        ket_qua_label.configure(text="Kết quả: " + str((float(so_a.get()) * float(so_b.get()))))
    else:
        messagebox.showerror("Lỗi nhập liệu", "Vui lòng chỉ nhập giá trị số")

button_nhan = ttk.Button(tab_tinh_toan, text="*", width=3, command=nhan)
button_nhan.grid(column=2, row=1)

def chia():
    if (is_number(so_a.get()) and is_number(so_b.get())):
        ket_qua_label.configure(text="Kết quả: " + str((float(so_a.get()) / float(so_b.get()))))
    else:
        messagebox.showerror("Lỗi nhập liệu", "Vui lòng chỉ nhập giá trị số")

button_chia = ttk.Button(tab_tinh_toan, text="/", width=3, command=chia)
button_chia.grid(column=3, row=1)


ttk.Label(tab_nam_nhuan, text="Nhập năm: ").grid(column=0, row=0, sticky='w')
nam = tk.StringVar()
nam_entered = ttk.Entry(tab_nam_nhuan, width=15, textvariable=nam)
nam_entered.grid(column=1, row=0)

def kiem_tra_nam_nhuan():
    try:
        year = int(nam.get())
        if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
            messagebox.showinfo("Kết quả", f"{year} là năm nhuận!")
        else:
            messagebox.showinfo("Kết quả", f"{year} không phải là năm nhuận!")
    except ValueError:
        messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập một số nguyên hợp lệ!")

button_kiem_tra = ttk.Button(tab_nam_nhuan, text="Kiểm tra", width=20, command=kiem_tra_nam_nhuan)
button_kiem_tra.grid(column=1, row=1)


ttk.Label(tab_tinh_tuoi, text="Ngày sinh (dd/mm/yyyy): ").grid(column=0, row=0, sticky='w')
ngay_sinh = tk.StringVar()
ngay_sinh_entered = ttk.Entry(tab_tinh_tuoi, width=15, textvariable=ngay_sinh)
ngay_sinh_entered.grid(column=1, row=0)

def tinh_tuoi():
    try:

        dob_str = ngay_sinh.get()
        dob = datetime.strptime(dob_str, "%d/%m/%Y")
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        messagebox.showinfo("Kết quả", f"Tuổi của bạn là: {age} tuổi.")
    except ValueError:
        messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập ngày sinh hợp lệ theo định dạng dd/mm/yyyy.")

button_tinh_tuoi = ttk.Button(tab_tinh_tuoi, text="Tính tuổi", width=20, command=tinh_tuoi)
button_tinh_tuoi.grid(column=1, row=1)

tab_tinh_toan.grid_columnconfigure(0, weight=1)
tab_tinh_toan.grid_columnconfigure(1, weight=1)
tab_tinh_toan.grid_columnconfigure(2, weight=0)
tab_tinh_toan.grid_columnconfigure(3, weight=0)

tab_nam_nhuan.grid_columnconfigure(0, weight=1)
tab_nam_nhuan.grid_columnconfigure(1, weight=1)

tab_tinh_tuoi.grid_columnconfigure(0, weight=1)
tab_tinh_tuoi.grid_columnconfigure(1, weight=1)

win.mainloop()
