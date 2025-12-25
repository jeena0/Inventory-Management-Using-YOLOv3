from tkinter import *
from tkinter.ttk import Combobox
from addinventory import AddInventoryPanel
from mainmenuleft import leftPanel
from mainmenushowtime import timeloop
from mainmenutop import topPanel
from qrscanner import display_qr
from showinventorydetails import InventoryViewDetailsPanel
from showinventorydetailstable import Inventorydetailstable
from showoutofstockdetails import OutofStockInventoryViewDetailsPanel
from showoutofstockinventorydetailstable import OutofStockInventorydetailstable
from showpricedetails import PriceInventoryViewDetailsPanel
from showpricedetailstable import Pricedetailstable
from showpurchasedetails import PurchaseInventoryViewDetailsPanel
from tkinter import messagebox
import sqlite3

from showsalesdetails import SalesInventoryViewDetailsPanel




class MainPage:
    def __init__(self, Mainmenuroot, usr, name):
        Mainmenuroot.after(0, Mainmenuroot.deiconify)
        self.name = name
        self.usr = usr
        self.dateto = "Choose date"
        self.datefrom = "Choose date"
        self.updatedateto = "Choose date"
        self.updatedatefrom = "Choose date"
        self.updatedatefromabsnt= "Choose date"
        self.updatedatetoabsnt = "Choose date"
        self.Mainmenuroot = Mainmenuroot
        self.Mainmenuroot.title("Main")
        self.width = "1199"
        self.height = "650"
        self.mbmrid = ""
        self.lst=[]
       
        self.count=-1
        self.Mainmenuroot.geometry(self.width + "x" + self.height + "+100+30")
        self.Mainmenuroot.resizable(False, False)
        self.a = 0
        self.month = ""
        self.left()
        self.top()

    def left(self):
        leftPanel(self)

    def time(self):
        timeloop(self)

    def top(self):
        topPanel(self)


    def logout(self):
        self.close_window_mainmenu()
        from login import Login
        Login(Tk())

    def showsalesdetails(self):
        SalesInventoryViewDetailsPanel(self)
    def addinventory(self):
        AddInventoryPanel(self)
    def showinventorydetail(self):
        InventoryViewDetailsPanel(self)
    def showoutofstockdetails(self):
        OutofStockInventoryViewDetailsPanel(self)
    def showpricedetails(self):
        PriceInventoryViewDetailsPanel(self)
    def showpurchasedetails(self):
        PurchaseInventoryViewDetailsPanel(self)
    def showpricedetailstable(self):
         Pricedetailstable(self)

    def showinventorydetails(self):
        InventoryViewDetailsPanel(self)
    
    def showinventorydetailstable(self):
         Inventorydetailstable(self)

    def showoutofstockinventorydetailtable(self):
         OutofStockInventorydetailstable(self)
    

    
    def add(self):
        add_window = Toplevel()
        add_window.title("Add Price Details")
        add_window.geometry("300x200")
        add_window.configure(bg="#FFFFFF")
        
        # Create entry fields
        Label(add_window, text="Name:", bg="#FFFFFF", font=("Goudy old style", 12)).pack(pady=5)
        name_entry = Entry(add_window)
        name_entry.pack(pady=5)
        
        Label(add_window, text="Price:", bg="#FFFFFF", font=("Goudy old style", 12)).pack(pady=5)
        price_entry = Entry(add_window)
        price_entry.pack(pady=5)

        def save_new_record():
            new_name = name_entry.get()
            new_price = price_entry.get()
            if not new_price.isdigit():
                messagebox.showerror("Invalid Input", "Please enter a valid whole number for the quantity.")
                return
            conn = sqlite3.connect('db/inventory.db')
            c = conn.cursor()
            c.execute('SELECT name FROM inventory_price WHERE name = ?', (new_name,))
            existing_name = c.fetchone()
            if existing_name:
                messagebox.showerror("Duplicate Name", "A record with the same name already exists.")
                return
            c.execute("INSERT INTO inventory_price (name, price) VALUES (?, ?)", 
                    (new_name, new_price))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Record added successfully!")
            add_window.destroy()
            
            # Refresh the table
            for widget in self.myframe.winfo_children():
                widget.destroy()
            self.showpricedetailstable()

        # Save button
        Button(add_window, text="Save", command=save_new_record, 
                bg="#4CAF50", fg="white", font=("Goudy old style", 12)).pack(pady=20)
        
    def delete(self, nr):
        response = messagebox.askyesno("Delete", "Are you sure you want to delete this record?")
        if response:
            conn = sqlite3.connect('db/inventory.db')
            c = conn.cursor()
            c.execute("DELETE FROM inventory_price WHERE id=?", (nr,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record deleted successfully!")
            
            # Clear existing widgets in myframe
            for widget in self.myframe.winfo_children():
                widget.destroy()
                
            # Reload the table
            self.showpricedetailstable()
    def delete_inventory(self, nr):
        response = messagebox.askyesno("Delete", "Are you sure you want to delete this record?")
        if response:
            conn = sqlite3.connect('db/inventory.db')
            c = conn.cursor()
            c.execute("DELETE FROM inventory_stock WHERE id=?", (nr,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record deleted successfully!")
            
            # Clear existing widgets in myframe
            for widget in self.myframe.winfo_children():
                widget.destroy()
                
            # Reload the table
            self.showinventorydetailstable()
    def edit_price(self, nr):
    # Create edit dialog window
        edit_window = Toplevel()
        edit_window.title("Edit Price Details")
        edit_window.geometry("300x200")
        edit_window.configure(bg="#FFFFFF")
        
        # Get current values from database
        conn = sqlite3.connect('db/inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM inventory_price WHERE id=?", (nr,))
        current_data = c.fetchone()
        conn.close()
        
        # Create entry fields
        Label(edit_window, text="Name:", bg="#FFFFFF", font=("Goudy old style", 12)).pack(pady=5)
        name_entry = Entry(edit_window)
        name_entry.insert(0, current_data[1])
        name_entry.pack(pady=5)
        
        Label(edit_window, text="Price:", bg="#FFFFFF", font=("Goudy old style", 12)).pack(pady=5)
        price_entry = Entry(edit_window)
        price_entry.insert(0, current_data[2])
        price_entry.pack(pady=5)
    
        def save_changes():
            new_name = name_entry.get()
            new_price = price_entry.get()
            if not new_price.isdigit():
                messagebox.showerror("Invalid Input", "Please enter a valid whole number for the quantity.")
                return
            conn = sqlite3.connect('db/inventory.db')
            c = conn.cursor()
            c.execute("UPDATE inventory_price SET name=?, price=? WHERE id=?", 
                    (new_name, new_price, nr))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Record updated successfully!")
            edit_window.destroy()
            
            # Refresh the table
            for widget in self.myframe.winfo_children():
                widget.destroy()
            self.showpricedetailstable()
    
    # Save button
        Button(edit_window, text="Save", command=save_changes, 
                bg="#4CAF50", fg="white", font=("Goudy old style", 12)).pack(pady=20)
    def edit_inventory(self, nr):
    # Create edit dialog window
        edit_window = Toplevel()
        edit_window.title("Edit Quantity Details")
        edit_window.geometry("300x150")
        edit_window.configure(bg="#FFFFFF")
        
        # Get current values from database
        conn = sqlite3.connect('db/inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM inventory_stock WHERE id=?", (nr,))
        current_data = c.fetchone()
        
        conn.close()
        
        # Create entry fields
        Label(edit_window, text="Quantity:", bg="#FFFFFF", font=("Goudy old style", 12)).pack(pady=5)
        quantity_entry = Entry(edit_window)
        quantity_entry.insert(0, current_data[3])
        quantity_entry.pack(pady=5)
    
        def save_changes():
            new_quantity = quantity_entry.get()

            if not new_quantity.isdigit():
                messagebox.showerror("Invalid Input", "Please enter a valid whole number for the quantity.")
                return
            conn = sqlite3.connect('db/inventory.db')
            c = conn.cursor()
            c.execute("UPDATE inventory_stock SET quantity=? WHERE id=?", 
                    (new_quantity, nr))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Record updated successfully!")
            edit_window.destroy()
            
            # Refresh the table
            for widget in self.myframe.winfo_children():
                widget.destroy()
            self.showinventorydetailstable()
    
    # Save button
        Button(edit_window, text="Save", command=save_changes, 
                bg="#4CAF50", fg="white", font=("Goudy old style", 12)).pack(pady=20)

    

    def close_window_mainmenu(self):
        self.Mainmenuroot.destroy()
    
    # def sales_inventory(self,nr,quantity):
    #     print(nr, quantity)
    #     add_window = Toplevel()
    #     add_window.title("Purchase")
    #     add_window.geometry("300x150")
    #     add_window.configure(bg="#FFFFFF")
        
    #     # Create entry fields
    #     options = ["Select Quantity"] 
    #     for i in range(1, quantity+1): 
    #         options.append(i) 
    #     dropdown =Combobox(add_window, values=options, state="readonly")
    #     dropdown.pack(pady=20)
    #     dropdown.current(0)  

    #     def save_new_record():
    #         selected_value = dropdown.get()
    #         if(selected_value == "Select Quantity"):
    #             add_window.destroy()
    #             messagebox.showerror("Error", "Please select a quantity")
               
    #         else:
    #             add_window.destroy()
    #             self.qr_window = Toplevel()
    #             self.qr_window.title("QR Code Display")
    #             display_qr(self.qr_window, selected_value,nr)


    #     # Save button
    #     Button(add_window, text="Save", command=save_new_record, 
    #             bg="#4CAF50", fg="white", font=("Goudy old style", 12)).pack(pady=20)
        
    def sales_inventory(self, nr, quantity):
    # Initialize or access the cart dictionary to store items and quantities
        if not hasattr(self, 'cart'):
            self.cart = {}  # {'item_id': quantity}

        add_window = Toplevel()
        add_window.title("Add Item to Cart")
        add_window.geometry("300x150")
        add_window.configure(bg="#FFFFFF")

        # Create dropdown for quantity selection
        options = ["Select Quantity"]
        for i in range(1, quantity + 1):
            options.append(i)
        dropdown = Combobox(add_window, values=options, state="readonly")
        dropdown.pack(pady=20)
        dropdown.current(0)

        def add_to_cart():
            selected_value = dropdown.get()
            if selected_value == "Select Quantity":
                messagebox.showerror("Error", "Please select a valid quantity")
            else:
                # Add the item to the cart
                self.cart[nr] = int(selected_value)
                db_connection = sqlite3.connect('db/inventory.db')
                connection = db_connection.cursor()
                connection.execute("select name from inventory_stock where id=?", (nr,))
                result = connection.fetchone()
                item_name = result[0]
                messagebox.showinfo("Success", f" {selected_value} {item_name} added to cart ")
            add_window.destroy()

        # Add to Cart button
        Button(
            add_window,
            text="Add to Cart",
            command=add_to_cart,
            bg="#4CAF50",
            fg="white",
            font=("Goudy old style", 12)
        ).pack(pady=20)

    def generate_qr_for_cart(self):
        if not hasattr(self, 'cart') or not self.cart:
            messagebox.showerror("Error", "Cart is empty! Add items before generating QR.")
            return

        # Combine cart data into a structured payload
        cart_payload = [{"id": item_id, "quantity": quantity} for item_id, quantity in self.cart.items()]
        # cart_payload = {
        #     "items": [{"id": item_id, "quantity": quantity} for item_id, quantity in self.cart.items()]
        # }
        print(cart_payload)
        # Open QR display window
        self.qr_window = Toplevel()
        self.qr_window.title("QR Code for Cart")
        display_qr(self.qr_window, cart_payload)


        # Optionally, clear the cart after QR is generated
        self.cart.clear()

    def destroy_qr_window(self):
        self.qr_window.destroy()


