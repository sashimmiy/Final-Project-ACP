import tkinter as tk
from tkinter import messagebox, scrolledtext

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Category:
    def __init__(self, name, products):
        self.name = name
        self.products = products

class Order:
    def __init__(self):
        self.items = {}
        self.total = 0

    def add_item(self, product, quantity):
        if product in self.items:
            self.items[product] += quantity
        else:
            self.items[product] = quantity
        self.total += product.price * quantity    

    def apply_discount(self, percentage):
        self.total *= (1 - percentage / 100)

    def add_delivery(self, fee):
        self.total += fee

    def display(self):
        return "\n".join([f"- {product.name}: {quantity} {'bottles' if 'milk' in product.name else 'kilos'}" for product, quantity in self.items.items()]) + f"\nThe total cost is {self.total} pesos.\nThank you for shopping with us!"

products = {
    "fruits": [Product("banana", 70), Product("mango", 145), Product("apple", 150)],
    "vegetables": [Product("carrot", 80), Product("cabbage", 78), Product("potato", 80)],
    "meat": [Product("beef", 381), Product("pork", 250), Product("chicken", 170)],
    "goods": [Product("garlic", 168.5), Product("chillies", 550), Product("nuts", 500)]
}

categories = [Category(name, products[name]) for name in products]

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Local Goods Store")
        self.geometry("805x625")
        self.resizable(False, False)
        self.order = Order()
        self.create_widgets()

    def create_widgets(self):
        for i, category in enumerate(categories):
            frame = tk.LabelFrame(self, text=category.name.upper(), padx=5, pady=5)
            frame.grid(row=0, column=i, padx=10, pady=10)
            for product in category.products:
                button = tk.Button(frame, text=f"{product.name}: {product.price} pesos per kilo", command=lambda p=product: self.add_to_order(p), width=20, padx=10)
                button.pack(side="top")

        self.order_text = scrolledtext.ScrolledText(self)
        self.order_text.grid(row=1, column=0, columnspan=len(categories))

        self.discount_entry = tk.Entry(self)
        self.discount_entry.grid(row=2, column=0, columnspan=len(categories))
        self.discount_button = tk.Button(self, text="Apply Discount Percentage", command=self.apply_discount)
        self.discount_button.grid(row=3, column=0, columnspan=len(categories))

        self.checkout_button = tk.Button(self, text="Checkout", command=self.checkout)
        self.checkout_button.grid(row=4, column=0, columnspan=len(categories))

        self.reset_button = tk.Button(self, text="Reset", command=self.reset_order)
        self.reset_button.grid(row=5, column=0, columnspan=len(categories))

    def add_to_order(self, product):
        self.order.add_item(product, 1)
        self.order_text.insert(tk.END, self.order.display() + "\n")

    def apply_discount(self):
        try:
            percentage = int(self.discount_entry.get())
            if 0 <= percentage <= 100:
                self.order.apply_discount(percentage)
                self.order_text.delete(1.0, tk.END)
                self.order_text.insert(tk.END, self.order.display() + "\n")
            else:
                messagebox.showerror("Error", "Invalid input. Please enter a percentage between 0 and 100.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter an integer.")

    def checkout(self):
        messagebox.showinfo("Order", self.order.display())
    
    def reset_order(self):
        self.order = Order()
        self.order_text.delete(1.0, tk.END)

app = Application()
app.eval('tk::PlaceWindow . center')
app.mainloop()
