import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer using Tkinter")
        self.root.geometry("900x700")
        self.root.configure(bg="#E6F3FF")  # Powder blue background
        
        # Initialize variables
        self.image_list = []
        self.image_index = 0
        self.current_photo = None
        
        # Create main UI components
        self.create_widgets()
        
        # Bind keyboard shortcuts
        self.root.bind('<Left>', lambda e: self.prev_image())
        self.root.bind('<Right>', lambda e: self.next_image())
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
    def create_widgets(self):
        # Title Label (fixed at top)
        title_label = tk.Label(
            self.root,
            text="🖼️ Image Viewer",
            font=("Arial", 20, "bold"),
            bg="#E6F3FF",
            fg="#2C3E50"
        )
        title_label.pack(side=tk.TOP, pady=10)
        
        # Create a canvas with scrollbar for image display
        canvas_frame = tk.Frame(self.root, bg="#34495E", bd=3, relief=tk.RAISED)
        canvas_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=(0, 10))
        
        # Create canvas
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        
        # Create scrollbars
        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Label to display image (inside canvas)
        self.image_label = tk.Label(self.canvas, bg="white", text="No Image Loaded\n\nClick 'Open Folder' to start", 
                                     font=("Arial", 14), fg="gray")
        self.canvas.create_window(0, 0, window=self.image_label, anchor=tk.NW)
        
        # Bottom section frame (fixed at bottom)
        bottom_section = tk.Frame(self.root, bg="#E6F3FF")
        bottom_section.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Keyboard shortcuts info
        shortcuts_label = tk.Label(
            bottom_section,
            text="Shortcuts: ← Previous | → Next | Esc Exit",
            font=("Arial", 9, "italic"),
            bg="#E6F3FF",
            fg="#7F8C8D"
        )
        shortcuts_label.pack(side=tk.BOTTOM, pady=5)
        
        # Status bar
        self.status_label = tk.Label(
            bottom_section,
            text="Ready | No images loaded",
            font=("Arial", 10),
            bg="#34495E",
            fg="white",
            anchor=tk.W,
            padx=10
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Buttons Frame
        button_frame = tk.Frame(bottom_section, bg="#E6F3FF")
        button_frame.pack(side=tk.BOTTOM, pady=15)
        
        # Button styling
        btn_style = {
            "bg": "#2C3E50",
            "fg": "white",
            "activebackground": "#E74C3C",
            "activeforeground": "white",
            "font": ("Arial", 11, "bold"),
            "width": 12,
            "height": 2,
            "relief": tk.RAISED,
            "bd": 3,
            "cursor": "hand2"
        }
        
        # Create buttons
        tk.Button(button_frame, text="📁 Open Folder", command=self.open_folder, **btn_style)\
            .grid(row=0, column=0, padx=8)
        tk.Button(button_frame, text="⬅️ Previous", command=self.prev_image, **btn_style)\
            .grid(row=0, column=1, padx=8)
        tk.Button(button_frame, text="Next ➡️", command=self.next_image, **btn_style)\
            .grid(row=0, column=2, padx=8)
        tk.Button(button_frame, text="❌ Exit", command=self.exit_app, **btn_style)\
            .grid(row=0, column=3, padx=8)
        
        # Mouse wheel binding for scrolling
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)  # Linux scroll up
        self.canvas.bind("<Button-5>", self._on_mousewheel)  # Linux scroll down
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
    
    def open_folder(self):
        """Open a folder and load all supported images"""
        folder_path = filedialog.askdirectory(title="Select Image Folder")
        
        if not folder_path:
            return
        
        # Supported image formats
        supported_formats = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".ico")
        
        # Load all image files from the folder
        try:
            self.image_list = [
                os.path.join(folder_path, file)
                for file in os.listdir(folder_path)
                if file.lower().endswith(supported_formats)
            ]
            
            # Sort images by name for consistent ordering
            self.image_list.sort()
            
            if not self.image_list:
                messagebox.showerror(
                    "No Images Found",
                    f"No supported image files found in the selected folder!\n\n"
                    f"Supported formats: {', '.join(supported_formats)}"
                )
                return
            
            self.image_index = 0
            self.show_image()
            
            messagebox.showinfo(
                "Folder Loaded",
                f"Successfully loaded {len(self.image_list)} image(s)"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load images:\n{str(e)}")
    
    def show_image(self):
        """Display the current image"""
        if not self.image_list:
            return
        
        try:
            image_path = self.image_list[self.image_index]
            
            # Open and process image
            image = Image.open(image_path)
            
            # Get original dimensions
            original_width, original_height = image.size
            
            # Get available canvas size (accounting for scrollbars)
            self.canvas.update_idletasks()
            canvas_width = self.canvas.winfo_width() - 20  # padding
            canvas_height = self.canvas.winfo_height() - 20
            
            # Calculate aspect ratio preserving resize
            # Only resize if image is larger than canvas
            if original_width > canvas_width or original_height > canvas_height:
                ratio = min(canvas_width/original_width, canvas_height/original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                image = image.resize((new_width, new_height), Image.LANCZOS)
            else:
                new_width = original_width
                new_height = original_height
            
            # Convert to PhotoImage
            self.current_photo = ImageTk.PhotoImage(image)
            
            # Update image label
            self.image_label.config(image=self.current_photo, text="")
            
            # Update canvas scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Center the image if smaller than canvas
            if new_width < canvas_width:
                x_offset = (canvas_width - new_width) // 2
            else:
                x_offset = 0
                
            if new_height < canvas_height:
                y_offset = (canvas_height - new_height) // 2
            else:
                y_offset = 0
            
            self.canvas.coords(self.canvas.find_withtag("all")[0], x_offset, y_offset)
            
            # Update window title
            filename = os.path.basename(image_path)
            self.root.title(f"Image Viewer - {filename}")
            
            # Update status bar
            self.status_label.config(
                text=f"Image {self.image_index + 1} of {len(self.image_list)} | "
                     f"{filename} | Original Size: {original_width}x{original_height}px | "
                     f"Display Size: {new_width}x{new_height}px"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error Loading Image",
                f"Could not load image:\n{str(e)}"
            )
    
    def next_image(self):
        """Navigate to the next image"""
        if not self.image_list:
            messagebox.showwarning("No Images", "Please load a folder with images first!")
            return
        
        self.image_index = (self.image_index + 1) % len(self.image_list)
        self.show_image()
    
    def prev_image(self):
        """Navigate to the previous image"""
        if not self.image_list:
            messagebox.showwarning("No Images", "Please load a folder with images first!")
            return
        
        self.image_index = (self.image_index - 1) % len(self.image_list)
        self.show_image()
    
    def exit_app(self):
        """Exit the application with confirmation"""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()