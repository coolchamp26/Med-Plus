import tkinter as tk
from tkinter import ttk, messagebox
from medplus.ui.base import BaseFrame
from medplus.auth import auth

class LoginFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Add background image
        self.add_background("image0.png")
        
        # Center container - styled as a card
        container = ttk.Frame(self, style='Card.TFrame', padding=30)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(container, text="Login to MedPlus", style='Header.TLabel', background="white").pack(pady=(0, 20))
        
        # Username
        ttk.Label(container, text="Username", style='Card.TLabel').pack(anchor="w")
        self.username_var = tk.StringVar()
        ttk.Entry(container, textvariable=self.username_var, width=30, font=('Segoe UI', 10)).pack(pady=(0, 10))
        
        # Password
        ttk.Label(container, text="Password", style='Card.TLabel').pack(anchor="w")
        self.password_var = tk.StringVar()
        ttk.Entry(container, textvariable=self.password_var, show="*", width=30, font=('Segoe UI', 10)).pack(pady=(0, 10))
        
        # Role Selection
        ttk.Label(container, text="Role", style='Card.TLabel').pack(anchor="w")
        self.role_var = tk.StringVar(value="USER")
        role_frame = ttk.Frame(container, style='Card.TFrame')
        role_frame.pack(pady=(0, 20), fill="x")
        
        # Custom style for radio buttons to match card background
        style = ttk.Style()
        style.configure('Card.TRadiobutton', background="white", font=('Segoe UI', 10))
        
        ttk.Radiobutton(role_frame, text="User", variable=self.role_var, value="USER", style='Card.TRadiobutton').pack(side="left", padx=10)
        ttk.Radiobutton(role_frame, text="Admin", variable=self.role_var, value="ADMIN", style='Card.TRadiobutton').pack(side="left", padx=10)
        
        # Buttons
        ttk.Button(container, text="Login", command=self.login).pack(fill="x", pady=5)
        ttk.Button(container, text="Create Account", command=self.go_to_register).pack(fill="x", pady=5)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        role = self.role_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return

        success, message = auth.login(username, password, role)
        if success:
            if hasattr(self.master, 'on_login_success'):
                self.master.on_login_success(role, username)
            else:
                messagebox.showinfo("Success", f"Logged in as {role}")
        else:
            messagebox.showerror("Error", message)

    def go_to_register(self):
        self.master.switch_frame(RegisterFrame)


class RegisterFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.add_background("image0.png")
        
        container = ttk.Frame(self, style='Card.TFrame', padding=30)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(container, text="Create Account", style='Header.TLabel', background="white").pack(pady=(0, 20))
        
        # Username
        ttk.Label(container, text="Username", style='Card.TLabel').pack(anchor="w")
        self.username_var = tk.StringVar()
        ttk.Entry(container, textvariable=self.username_var, width=30, font=('Segoe UI', 10)).pack(pady=(0, 10))
        
        # Password
        ttk.Label(container, text="Password", style='Card.TLabel').pack(anchor="w")
        self.password_var = tk.StringVar()
        ttk.Entry(container, textvariable=self.password_var, show="*", width=30, font=('Segoe UI', 10)).pack(pady=(0, 10))
        
        # Role
        ttk.Label(container, text="Role", style='Card.TLabel').pack(anchor="w")
        self.role_var = tk.StringVar(value="USER")
        role_frame = ttk.Frame(container, style='Card.TFrame')
        role_frame.pack(pady=(0, 20), fill="x")
        
        style = ttk.Style()
        style.configure('Card.TRadiobutton', background="white", font=('Segoe UI', 10))
        
        ttk.Radiobutton(role_frame, text="User", variable=self.role_var, value="USER", style='Card.TRadiobutton').pack(side="left", padx=10)
        ttk.Radiobutton(role_frame, text="Admin", variable=self.role_var, value="ADMIN", style='Card.TRadiobutton').pack(side="left", padx=10)
        
        # Buttons
        ttk.Button(container, text="Register", command=self.register).pack(fill="x", pady=5)
        ttk.Button(container, text="Back to Login", command=self.go_to_login).pack(fill="x", pady=5)

    def register(self):
        username = self.username_var.get()
        password = self.password_var.get()
        role = self.role_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return

        success, message = auth.register(username, password, role)
        if success:
            messagebox.showinfo("Success", "Account created! Please login.")
            self.go_to_login()
        else:
            messagebox.showerror("Error", message)

    def go_to_login(self):
        self.master.switch_frame(LoginFrame)
