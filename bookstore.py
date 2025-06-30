from streamlit import title
import json
class Book:
    def __init__(self,title,price,sales_count=0):
        self.title=title
        self.price=price
        self.sales_count=sales_count

    def sell(self):
        self.sales_count+=1

    def __repr__(self):
        return f"{self.title}-{self.price} | Sold: {self.sales_count}"

    def to_dict(self):
        return{
            'title':self.title,
            'price':self.price,
            'sales_count':self.sales_count
        }

    @classmethod
    def from_dict(cls,d):
        return cls(d['title'],d['price'],d.get('sales_count',0))

    @classmethod
    def from_string(cls,string):
        try:
            title,price=string.split('-')
            price=int(price)
            return cls(title,price)
        except ValueError:
            print('Invalid format')
            return None
    @classmethod
    def tax_rate(cls,title,price):
        tax_rate=0.01
        total_price=int(price*(1+tax_rate))
        return cls(title,total_price)

    @staticmethod
    def is_valid_price(price):
        if not isinstance(price,int):
            raise TypeError('price must be an integer')
        return price>=400

    @staticmethod
    def apply_discount(price,discount):
        if not isinstance(price,int) or not isinstance(discount,(int,float)):
            raise TypeError('price must be an integer')
        discount=price*(discount/100)
        return int(price-discount)


class BookStore:
    def __init__(self):
        self.books=[]

    def add_book(self,book):
        if isinstance(book,Book):
            self.books.append(book)
        else:
            raise TypeError('book must be an instance of Book')

    def list_books(self):
        if not self.books:
            print('No books added')
        else:
            for book in self.books:
                print(book)

    def remove_book(self,title):
        for book in self.books:
            if book.title.lower()==title.lower():
                self.books.remove(book)
                print('Book removed')
                return
        print(f"Book{title} not found")

    def total_value(self):
        return sum(book.price for book in self.books)

    def total_books(self):
        return len(self.books)

    def search_by_title(self,keyword):
        return [book for book in self.books if keyword.lower() in book.title.lower()]

    def sell_book(self,title):
        for book in self.books:
            if book.title.lower() == title.lower():
                book.sell()
                print(f"Sold one copy of {book.title}")
                return
        print(f"No book found for {title}")

    def top_selling_books(self):
        if not self.books:
            print('No books to show')
            return
        sorted_books = sorted(self.books, key=lambda book: book.sales_count, reverse=True)
        print("Top selling books:")
        for book in sorted_books:
            print(book)

    def save_to_file(self,filename="books.json"):
        with open(filename,"w") as file:
            json.dump([books.to_dict() for books in self.books],file,indent=4)
        print("Books saved to file")

    def load_from_file(self,filename="books.json"):
        try:
            with open(filename,"r") as file:
                data = json.load(file)
                self.books=[Book.from_dict(book) for book in data]
            print("Books loaded from file")
        except FileNotFoundError:
            print("File not found")

def menu():
    store=BookStore()
    while True:
        print("\n Bookstore Menu")
        print("1. Add Book")
        print("2. List Books")
        print("3. Sell Book")
        print("4. Show Total Books Value")
        print("5. Search Book by Title")
        print("6. Save Books to JSON")
        print("7. Load Books from JSON")
        print("8.exit")

        choice=int(input("Enter your choice (1-8): "))
        if choice==1:
            title=input("Enter book title: ").strip()
            try:
                price=int(input("Enter book price: "))
                book=Book(title,price)
                store.add_book(book)
                print(f"Book {book.title} added to store")
            except ValueError:
                print("Invalid format")
        elif choice==2:
            print("Books in store")
            store.list_books()
        elif choice==3:
            title=input("Enter book title: ")
            store.sell_book(title)
        elif choice==4:
            print(f"Total books value: {store.total_value()}")
        elif choice==5:
            keyword=input("Enter book title: ")
            result=store.search_by_title(keyword)
            print("Search results:")
            for book in result:
                print(book)
            if not result:
                print("No books found")
        elif choice==6:
            store.save_to_file()
        elif choice==7:
            store.load_from_file()
        elif choice==8:
            print("Exsisting book")
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    menu()

