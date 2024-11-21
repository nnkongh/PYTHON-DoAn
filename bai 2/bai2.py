import psycopg
import tkinter as tk
from tkinter import ttk, messagebox

class LibraryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý thư viện")
        self.root.geometry("900x500")
        
        self.create_widgets()
        
        try:
            self.connection = self.connect_db('books')
            if self.connection:
                self.create_table(self.connection)
        except Exception as e:
            messagebox.showerror("Lỗi Database", f"Không thể kết nối database: {str(e)}")
            self.root.quit()
        
        self.reload_books()
    
    def connect_db(self, dbname='postgres'):
        try:
            conn = psycopg.connect(
                dbname="LibraryManagement", 
                user="postgres", 
                password="1", 
                host="localhost", 
                port='5432'
            )
            return conn
        except Exception as e:
            print(f"Error while connecting to database {dbname}:", e)
            raise
    
    def create_table(self, connection):
        if connection is None:
            messagebox.showerror("Lỗi kết nối", "Không thể kết nối đến cơ sở dữ liệu")
            return
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(255) NOT NULL,
                    year INTEGER NOT NULL,
                    genre VARCHAR(100) NOT NULL
                );
            """)
            connection.commit()
        except Exception as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", str(e))
        finally:
            cursor.close()

    def add_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        year = self.entry_year.get()
        genre = self.entry_genre.get()
        
        if not all([title, author, year, genre]):
            messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ thông tin")
            return
        
        try:
            int(year)
        except ValueError:
            messagebox.showwarning("Lỗi", "Năm xuất bản phải là số")
            return
        
        try:
            conn = self.connect_db('books')
            cur = conn.cursor()
            cur.execute("INSERT INTO books (title, author, year, genre) VALUES (%s, %s, %s, %s)",
                        (title, author, int(year), genre))
            conn.commit()
            cur.close()
            conn.close()
            self.reload_books()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def update_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Lỗi", "Vui lòng chọn sách cần cập nhật")
            return
        
        book_id = self.tree.item(selected[0])['values'][0]
        title = self.entry_title.get()
        author = self.entry_author.get()
        year = self.entry_year.get()
        genre = self.entry_genre.get()
        
        if not all([title, author, year, genre]):
            messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ thông tin")
            return
        
        try:
            conn = self.connect_db('books')
            cur = conn.cursor()
            cur.execute("UPDATE books SET title=%s, author=%s, year=%s, genre=%s WHERE id=%s",
                        (title, author, int(year), genre, book_id))
            conn.commit()
            cur.close()
            conn.close()
            self.reload_books()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Lỗi", "Vui lòng chọn sách cần xóa")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa sách này?"):
            book_id = self.tree.item(selected[0])['values'][0]
            try:
                conn = self.connect_db('books')
                cur = conn.cursor()
                cur.execute("DELETE FROM books WHERE id=%s", (book_id,))
                conn.commit()
                cur.close()
                conn.close()
                self.reload_books()
                self.clear_entries()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def reload_books(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            conn = self.connect_db('books')
            cur = conn.cursor()
            cur.execute("SELECT * FROM books")
            for row in cur.fetchall():
                self.tree.insert("", "end", values=row)
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def clear_entries(self):
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)

    def search_books(self):
        search_term = self.entry_search.get()
        if not search_term:
            messagebox.showwarning("Lỗi", "Vui lòng nhập từ khóa tìm kiếm")
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            conn = self.connect_db('books')
            cur = conn.cursor()
            cur.execute("SELECT * FROM books WHERE title ILIKE %s OR author ILIKE %s", 
                        (f"%{search_term}%", f"%{search_term}%"))
            for row in cur.fetchall():
                self.tree.insert("", "end", values=row)
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])['values']
            self.clear_entries()
            self.entry_title.insert(0, item[1])
            self.entry_author.insert(0, item[2])
            self.entry_year.insert(0, item[3])
            self.entry_genre.insert(0, item[4])

    def create_widgets(self):
        # Tạo giao diện
        frame = tk.Frame(self.root)
        frame.pack(pady=10, padx=10)

        tk.Label(frame, text="Tên sách:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.entry_title = tk.Entry(frame, width=40)
        self.entry_title.grid(row=0, column=1, columnspan=2, pady=2)

        tk.Label(frame, text="Tác giả:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        self.entry_author = tk.Entry(frame, width=40)
        self.entry_author.grid(row=1, column=1, columnspan=2, pady=2)

        tk.Label(frame, text="Năm XB:").grid(row=2, column=0, sticky='e', padx=5, pady=2)
        self.entry_year = tk.Entry(frame, width=40)
        self.entry_year.grid(row=2, column=1, columnspan=2, pady=2)

        tk.Label(frame, text="Thể loại:").grid(row=3, column=0, sticky='e', padx=5, pady=2)
        self.entry_genre = tk.Entry(frame, width=40)
        self.entry_genre.grid(row=3, column=1, columnspan=2, pady=2)

        tk.Label(frame, text="Tìm kiếm:").grid(row=4, column=0, sticky='e', padx=5, pady=2)
        self.entry_search = tk.Entry(frame, width=40)
        self.entry_search.grid(row=4, column=1, columnspan=2, pady=2)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Thêm", command=self.add_book, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Cập nhật", command=self.update_book, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Xóa", command=self.delete_book, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Làm mới", command=self.reload_books, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Tìm kiếm", command=self.search_books, width=10).pack(side=tk.LEFT, padx=2)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Tên sách", "Tác giả", "Năm XB", "Thể loại"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên sách", text="Tên sách")
        self.tree.heading("Tác giả", text="Tác giả")
        self.tree.heading("Năm XB", text="Năm XB")
        self.tree.heading("Thể loại", text="Thể loại")
        self.tree.pack(pady=20, padx=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManager(root)
    root.mainloop()
