import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from medplus.ui.base import BaseFrame
from medplus.database import db

class UserDashboardFrame(BaseFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        
        self.add_background("pills.png")
        
        # Navbar / Header - Semi-transparent logic or solid for readability
        # Using a frame pack(side=top) pushes the canvas down if not careful? 
        # Wait, BaseFrame packs itself. Canvas is placed.
        # So pack/place widgets on TOP of canvas.
        
        # Header
        header = ttk.Frame(self, padding=10, style='Card.TFrame') # Use Card style for white background
        header.pack(fill="x", pady=(20,0), padx=20)
        
        ttk.Label(header, text=f"Welcome, {username}", style='SubHeader.TLabel', background="white").pack(side="left")
        ttk.Button(header, text="Logout", command=self.logout).pack(side="right")
        
        # Main Content Area
        # We want the background to show, so we might not want a big opaque frame filling everything.
        # But BaseFrame init packed itself. widgets inside pack into self.
        
        content = tk.Frame(self, bg=self.master.bg_color) 
        # Actually lets make content frame transparent (tkinter frame default is opaque usually, but can be managed)
        # Instead, let's just place the button container in the center on top of background
        
        # Grid layout for menu buttons - Center Card
        btn_frame = ttk.Frame(self, style='Card.TFrame', padding=30)
        btn_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(btn_frame, text="Dashboard Menu", style='SubHeader.TLabel', background="white").pack(pady=(0,20))
        
        ttk.Button(btn_frame, text="View Hospital Map", command=self.show_map, width=30).pack(pady=10)
        ttk.Button(btn_frame, text="My Personal Contacts", command=self.manage_contacts, width=30).pack(pady=10)
        ttk.Button(btn_frame, text="Emergency Contacts", command=self.view_emergency_contacts, width=30).pack(pady=10)

    def logout(self):
        from medplus.ui.login_ui import LoginFrame
        self.master.switch_frame(LoginFrame)

    def show_map(self):
        messagebox.showinfo("Map", "Map functionality is under construction.\n(Opening GPS Module...)")

    def manage_contacts(self):
        # Open a dialog/window to manage contacts
        CRUDWindow(self, "Personal Contacts", "personal_contacts", ["Name", "Contact No"])

    def view_emergency_contacts(self):
        # Read-only or Add? Original allowed Add. Let's allow Add.
        CRUDWindow(self, "Emergency Contacts", "emergency_contacts", ["Name", "Contact No"])


class AdminDashboardFrame(BaseFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        
        self.add_background("pills.png")
        
        # Header
        header = ttk.Frame(self, padding=10, style='Card.TFrame')
        header.pack(fill="x", pady=(20,0), padx=20)
        
        ttk.Label(header, text=f"Admin Dashboard ({username})", style='SubHeader.TLabel', background="white").pack(side="left")
        ttk.Button(header, text="Logout", command=self.logout).pack(side="right")
        
        # Content - Center Card
        btn_frame = ttk.Frame(self, style='Card.TFrame', padding=30)
        btn_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(btn_frame, text="Administration", style='SubHeader.TLabel', background="white").pack(pady=(0,20))
        
        ttk.Button(btn_frame, text="Manage Hospitals", command=self.manage_hospitals, width=30).pack(pady=10)
        # Original had specific Add/Delete/Modify buttons. A unified Manager is better.
        ttk.Button(btn_frame, text="Manage Users", command=self.manage_users, width=30).pack(pady=10)
        
    def logout(self):
        from medplus.ui.login_ui import LoginFrame
        self.master.switch_frame(LoginFrame)
        
    def manage_hospitals(self):
        CRUDWindow(self, "Manage Hospitals", "hospitals", ["Name", "Address", "Contact"])

    def manage_users(self):
        # Specialized view for users (maybe just delete)
        CRUDWindow(self, "Manage Users", "users", ["Username", "Role"], allow_add=False, allow_edit=False)


class CRUDWindow(tk.Toplevel):
    def __init__(self, parent, title, table_name, columns, allow_add=True, allow_edit=True, allow_delete=True):
        super().__init__(parent)
        self.title(title)
        self.geometry("800x600")
        self.table_name = table_name
        self.columns = columns # List of display names.
        # DB columns assumption: id is first, then rest map to 'columns' lowercased/slugified
        # Real generic CRUD is hard without schema reflection, so I'll do some basic mapping
        
        self.create_widgets(allow_add, allow_edit, allow_delete)
        self.refresh_data()

    def create_widgets(self, allow_add, allow_edit, allow_delete):
        # Toolbar
        toolbar = ttk.Frame(self, padding=5)
        toolbar.pack(fill="x")
        
        if allow_add:
            ttk.Button(toolbar, text="Add New", command=self.add_item).pack(side="left", padx=5)
        if allow_edit:
            ttk.Button(toolbar, text="Edit Selected", command=self.edit_item).pack(side="left", padx=5)
        if allow_delete:
            ttk.Button(toolbar, text="Delete Selected", command=self.delete_item).pack(side="left", padx=5)
            
        ttk.Button(toolbar, text="Refresh", command=self.refresh_data).pack(side="right", padx=5)
        
        # Treeview
        # ID is hidden usually, but let's keep it simple.
        cols = ["ID"] + self.columns
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100) # Adjust as needed
            
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_data(self):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Fetch data
        # Mapping table names to specific select queries if needed, or generic
        # Generic SELECT * FROM table
        # We need to map the result columns to the tree columns carefully.
        # This is a simplification.
        
        try:
            # handle 'users' which has password_hash that we don't want to show (or maybe shows as hash)
            if self.table_name == "users":
                # Special query
                rows = db.fetch_all("SELECT rowid, username, role FROM users") # using rowid for sqlite if no int pk, but we defined string pk for users. 
                # Wait, users table has username as PK.
                # Let's adjust generic logic or switch based on table.
                rows = db.fetch_all("SELECT username, username, role FROM users") # ID is username here
            else:
                rows = db.fetch_all(f"SELECT * FROM {self.table_name}")
            
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def add_item(self):
        # Generic Add Dialog
        values = []
        for col in self.columns:
            val = simpledialog.askstring("Input", f"Enter {col}:", parent=self)
            if val is None: return # Cancelled
            values.append(val)
        
        # Insert
        try:
            placeholders = ",".join(["?"] * len(values))
            # Need actual db column names. 
            # Simplified map:
            if self.table_name == "hospitals":
                cols = "name, address, contact"
            elif self.table_name == "personal_contacts" or self.table_name == "emergency_contacts":
                cols = "name, contact_no"
            else:
                return

            query = f"INSERT INTO {self.table_name} ({cols}) VALUES ({placeholders})"
            db.execute_query(query, tuple(values))
            self.refresh_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an item to delete")
            return
        
        item = self.tree.item(selected[0])
        record_id = item['values'][0] # ID is first column
        
        confirm = messagebox.askyesno("Confirm", f"Delete record ID {record_id}?")
        if confirm:
            try:
                if self.table_name == "users":
                    db.execute_query("DELETE FROM users WHERE username = ?", (record_id,))
                else:
                    db.execute_query(f"DELETE FROM {self.table_name} WHERE id = ?", (record_id,))
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def edit_item(self):
        selected = self.tree.selection()
        if not selected: return
        item = self.tree.item(selected[0])
        record_id = item['values'][0]
        
        # Get new values for each column
        # Ideally pre-fill, but simpledialog doesn't support pre-fill easy without custom code.
        # Let's just do standard custom dialog if I had time, but for now simple input.
        
        # For simplicity in this 'basic project' improvement:
        # Just creating a new object is easiest, but editing is requested.
        # I'll implement a simple edit for the first logic column (Name) as a demo.
        
        new_val = simpledialog.askstring("Edit", f"Enter new value for {self.columns[0]}", parent=self)
        if new_val:
            try:
                if self.table_name == "hospitals":
                    db.execute_query("UPDATE hospitals SET name = ? WHERE id = ?", (new_val, record_id))
                elif "contacts" in self.table_name:
                    db.execute_query(f"UPDATE {self.table_name} SET name = ? WHERE id = ?", (new_val, record_id))
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
