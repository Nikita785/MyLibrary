import json
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class Book:
    def __init__(self, title: str, author: str, year: int, is_read: bool = False):
        self.title = title
        self.author = author
        self.year = year
        self.is_read = is_read
        self.notes = []
    
    def __str__(self) -> str:
        return f'{self.author} --- {self.title} ({self.year}) [{self.is_read}]'
    
    def add_note(self, text: str):
        if text.strip():
            self.notes.append(text.strip())

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
                book.is_read = not book.is_read
                print('Данные о книги успешно изменены: прочитано')
                return            
        print('Не нашлось книги с таким названием')
    
    def save_to_file(self):
        data_to_save = []
        for book in self.books:
            data_to_save.append({'title': book.title, 
                                 'author': book.author,
                                 'year': book.year, 
                                 'is_read': book.is_read,
                                 'notes': book.notes})
            
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
    
    def load_from_file(self, custom_path: str = None):
        path_to_open = custom_path if custom_path else self.file_path
        try:
            with open(path_to_open, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for book_dict in data:
                    new_book = Book(title=book_dict['title'], 
                                    author=book_dict['author'], 
                                    year=book_dict['year'], 
                                    is_read=book_dict['is_read'])
                    new_book.notes = book_dict.get('notes', [])
                    self.books.append(new_book)
                    
                if custom_path:
                    self.file_path = custom_path
                
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
        
        #кнопка для открытия и добавления заметок (окошко)
        self.notes_button = tk.Button(root, text='Заметки к книге', command=self.ui_open_notes)
        self.notes_button.pack(pady=5)
        
        #кнопка ручной загрузки книг из файла
        self.load_button = tk.Button(root, text='Загрузить список книг из файла', command = self.ui_load_books)
        self.load_button.pack(pady=5)
        
        #кнопка для изменения статуса прочтения
        self.read_button = tk.Button(root, text='Отметить как прочитано/непрочитано', command=self.ui_mark_as_read)
        self.read_button.pack(pady=5)
        
        #кнопка для ручного сохранения в файл
        self.save_button = tk.Button(root, text='Сохранить библиотеку в файл', command=self.ui_save_books)
        self.save_button.pack(pady=5)
        
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
            #Для удобства очищаем поля ввода
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
        else:
            messagebox.showwarning('Ошибка', 'Книга уже добавлена в библиотеку')
            
    #метод для загрузки книг из фала json        
    def ui_load_books(self):
        
        #диалоговое окно для выбора JSON-файла
        selected_file = filedialog.askopenfilename(
            title='Выберите файл библиотеки',
            filetypes=[('JSON файлы', '*.json'), ('Все файлы', '*.*')]
        )
        
        if not selected_file:
            return
        
        self.library.books = []
        self.library.load_from_file(custom_path=selected_file)
        self.update_listbox()
        
        messagebox.showinfo('Готово', 'Список книг успешно загружен из файла')
        
    #метод для смены статуса прочтения выбранной книги
    def ui_mark_as_read(self):
        selected_index = self.books_listbox.curselection()
        
        if not selected_index:
            messagebox.showwarning('Ошибка', 'Выберите книгу из списка')
            return
        book = self.library.books[selected_index[0]]
        self.library.mark_as_read(book.title)
        
        #Автоматическое сохранение изменений в файл и обновление экрана
        self.library.save_to_file()
        self.update_listbox()
        messagebox.showinfo('Готово', f'Статус книги "{book.title}" успешно изменён')
        
    #Метод для ручного сохранения текущего состояния в файл
    def ui_save_books(self):
        
        
        
    #метод для добавления заметок
    def ui_open_notes(self):
        
        #получаем индекс выбранной книги в списке
        selected_index = self.books_listbox.curselection()
        
        if not selected_index:
            messagebox.showwarning('Ошибка', 'Вы не выбрали книгу')
            return
        
        book = self.library.books[selected_index[0]]
        
        #Логика всплывающего окна (Toplevel)
        notes_window = tk.Toplevel(self.root)
        notes_window.title(f'Заметки {book.title}')
        notes_window.geometry('400x450')
        
        #уже существующие заметки
        notes_listbox = tk.Listbox(notes_window, width=50, height=12)
        notes_listbox.pack(pady=10)
        
        #функция для обновления списка заметок внутри окна
        def update_notes_listbox():
            notes_listbox.delete(0, tk.END)
            for note in book.notes:
                notes_listbox.insert(tk.END, note)
        update_notes_listbox() #сразу обновляем список заметок внутри окна
        
        #поле ввода новой заметки
        
        tk.Label(notes_window, text='Добавить новую заметку по книге:').pack()
        note_entry = tk.Entry(notes_window, font='Arial 12', width=38)
        note_entry.pack(pady=5)
        
        #функция сохраненя заметки
        
        def save_new_note():
            text = note_entry.get()
            if text.strip():
                book.add_note(text)
                self.library.save_to_file()
                update_notes_listbox()
                note_entry.delete(0, tk.END)
            else:
                messagebox.showwarning('Ошибка', 'Нельзя добавить пустую заметку')
                
        #кнопка для сохранения заметки
        
        save_button = tk.Button(notes_window, text='Сохранить заметку', command=save_new_note)
        save_button.pack(pady=10)
        
    #метод для обновления. Он очищает список на экране и заново выводит актуальные книжки     
    def update_listbox(self):
        self.books_listbox.delete(0, tk.END)
        for book in self.library.books:
            self.books_listbox.insert(tk.END, str(book))

if __name__ == '__main__':
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
