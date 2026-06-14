import json
import tkinter as tk
from tkinter import messagebox

class Book:
    def __init__(self, title: str, author: str, year: int, is_read: bool = False):
        self.title = title
        self.author = author
        self.year = year
        self.is_read = is_read
    def __str__(self) -> str:
        return f'{self.author} --- {self.title} ({self.year}) [{self.is_read}]'

class Library:

    def __init__(self, file_path: str = 'library.json'):
        self.books = []
        self.file_path = file_path

    def add_book(self, title: str, author: str, year: int):
        for b in self.books:
            if b.title == title and b.author == author:
                return False
            
        new_book = Book(title, author, year)
        self.books.append(new_book)
        return True
    
    def list_books(self):
        if len(self.books) > 0:
            for book in self.books:
                print(book)
        else:
            print('Библиотека пуста')
            
    def mark_as_read(self, title: str):
        for book in self.books:
            if book.title == title:
                book.is_read = not is_read
                print('Данные о книги успешно изменены: прочитано')
                return            
        print('Не нашлось книги с таким названием')
    
    def save_to_file(self):
        data_to_save = []
        for book in self.books:
            data_to_save.append({'title': book.title, 'author': book.author,
                               'year': book.year, 'is_read': book.is_read})
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
    
    def load_from_file(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for book_dict in data:
                    new_book = Book(title=book_dict['title'], author=book_dict['author'], 
                                year=book_dict['year'], is_read=book_dict['is_read'])
                    self.books.append(new_book)
                
        except FileNotFoundError:
            print('Создана новая библиотека')
            data = []
            return data
class LibraryApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title('Моя Библиотека')
        self.root.geometry('500x400')
        
        #Бэкенд
        
        self.library = Library()
        self.library.load_from_file()
        
        #Фронтенд, создание самого интерфейса
        
        #Поле ввода названия книги
        self.title_label = tk.Label(root, text='Название книги:')
        self.title_label.pack(pady=2)
        self.title_entry = tk.Entry(root, font='Arial 20', width=40)
        self.title_entry.pack(pady=5)
        
        #Полу ввода автора
        
        self.author_label = tk.Label(root, text='Автор книги:')
        self.author_label.pack(pady=2)
        self.author_entry = tk.Entry(root, font='Arial 20', width=40)
        self.author_entry.pack()
        
        #Поле ввода года
        
        self.year_label = tk.Label(root, text='Год написания:')
        self.year_label.pack(pady=2)
        self.year_entry = tk.Entry(root, font='Arial 20', width=40)
        self.year_entry.pack()
        
        #Список для отображения книг
        
        self.books_listbox = tk.Listbox(root, width=60, height=15)
        self.books_listbox.pack(pady=5)
        
        #кнопка для добавления книги в конструкторе
        self.add_button = tk.Button(root, text='Добавить книгу', command=self.ui_add_book)
        self.add_button.pack(pady=10)
        
        #обновляем список книг на экране при старте
        self.update_listbox()
        
    #метод для добавления книги
    def ui_add_book(self):
        
        title = self.title_entry.get()
        author = self.author_entry.get()
        try:
            year = int(self.year_entry.get())
        except ValueError:
            messagebox.showerror('Ошибка', 'Год должен быть числом.')
            return
        if self.library.add_book(title, author, year):
            #Если метод вернул True (это флаг, указанный в методе класса Library.add_book)
            self.library.save_to_file()
            self.update_listbox()
        else:
            messagebox.showwarning('Ошибка', 'Книга уже добавлена в библиотеку')
        
        self.library.save_to_file()
        self.update_listbox()
        
    #метод для обновления. Он очищает список на экране и заново выводит актуальные книжки     
    def update_listbox(self):
        self.books_listbox.delete(0, tk.END)
        for book in self.library.books:
            self.books_listbox.insert(tk.END, str(book))

if __name__ == '__main__':
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
