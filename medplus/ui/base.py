import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class MedPlusApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MedPlus Hospital Management System")
        self.geometry("1000x800")
        
        # Style Configuration
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Colors - Modern Palette
        self.primary_color = "#2C3E50"  # Dark Blue-Grey
        self.secondary_color = "#18BC9C" # Teal/Green
        self.accent_color = "#E74C3C"    # Red
        self.bg_color = "#ecf0f1"        # Light Grey
        self.text_color = "#2c3e50"
        
        self.configure(bg=self.bg_color)
        
        # Configure Styles
        self.style.configure('TFrame', background=self.bg_color)
        
        # Modern Font Settings
        default_font = ('Segoe UI', 10)
        header_font = ('Segoe UI', 24, 'bold')
        subheader_font = ('Segoe UI', 14, 'bold')
        
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color, font=default_font)
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=8, background=self.secondary_color, foreground="white")
        self.style.map('TButton', background=[('active', "#16a085")]) 
        
        self.style.configure('Header.TLabel', font=header_font, foreground=self.primary_color, background=self.bg_color)
        self.style.configure('SubHeader.TLabel', font=subheader_font, foreground=self.primary_color, background=self.bg_color)
        
        # Transparent-ish label style for use on backgrounds (best effort in Tkinter)
        # Note: Tkinter labels aren't truly transparent, so we might need to handle backgrounds carefully.
        # For this implementation, we will try to match the parent background where possible, 
        # but heavily rely on container frames for "cards".
        
        self.style.configure('Card.TFrame', background="white", relief="raised")
        self.style.configure('Card.TLabel', background="white", foreground=self.text_color, font=default_font)
        
        self.current_frame = None

    def switch_frame(self, frame_class, *args, **kwargs):
        """Destroys current frame and replaces it with a new one."""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = frame_class(self, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

class BaseFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.bg_image_ref = None
        self.original_image = None
        self.canvas = None

    def add_background(self, image_path):
        """Adds a responsive background image to the frame."""
        # Find absolute path if not provided
        if not os.path.isabs(image_path):
            # Assuming images are in project root relative to execution or known location
            # Try project root
            base_dir = os.getcwd() # Or use a more robust path finding strategy
            full_path = os.path.join(base_dir, image_path)
        else:
            full_path = image_path

        if not os.path.exists(full_path):
             print(f"Warning: Background image not found at {full_path}")
             return

        try:
            self.original_image = Image.open(full_path)
            
            # Create a Canvas to hold the background
            # using place to ensure it covers everything at z=0 (bottom)
            self.canvas = tk.Canvas(self, highlightthickness=0)
            self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
            
            # Bind resize event
            self.bind('<Configure>', self._on_resize)
            
            # Lower canvas to bottom
            # Canvas.lower refers to items, so we need to validly lower the widget.
            # Using tk.Misc.lower(widget) works.
            tk.Misc.lower(self.canvas)
            
        except Exception as e:
            print(f"Error loading background: {e}")

    def _on_resize(self, event):
        if not self.original_image or not self.canvas:
            return
            
        # Get current frame size
        width = event.width
        height = event.height
        
        if width <= 1 or height <= 1: return # Ignore validation/init glitches
        
        # Resize image
        resized_image = self.original_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_image_ref = ImageTk.PhotoImage(resized_image)
        
        # Update canvas
        self.canvas.delete("bg")
        self.canvas.create_image(0, 0, image=self.bg_image_ref, anchor="nw", tags="bg")

