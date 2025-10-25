#!/usr/bin/env python3
"""
ESRI Scene Viewer HTML Generator
Creates HTML wrapper files for embedding ESRI Scene Viewer URLs
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
import sys

class SceneViewerGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("ESRI Scene Viewer HTML Generator")
        self.root.geometry("700x400")
        self.root.resizable(False, False)

        # Store the last generated file path
        self.last_generated_file = None

        # Configure style
        style = ttk.Style()
        style.theme_use('vista')  # Windows native look

        # Create main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="ESRI Scene Viewer HTML Generator",
                               font=('Segoe UI', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Scene Viewer URL
        ttk.Label(main_frame, text="Scene Viewer URL:",
                 font=('Segoe UI', 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=70, font=('Segoe UI', 9))
        self.url_entry.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        self.url_entry.insert(0, "https://www.arcgis.com/home/webscene/viewer.html?webscene=")

        # Output Folder
        ttk.Label(main_frame, text="Output Folder:",
                 font=('Segoe UI', 10)).grid(row=3, column=0, sticky=tk.W, pady=5)

        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))

        self.folder_entry = ttk.Entry(folder_frame, width=55, font=('Segoe UI', 9))
        self.folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.folder_entry.insert(0, os.path.expanduser("~/Desktop"))

        browse_btn = ttk.Button(folder_frame, text="Browse...", command=self.browse_folder)
        browse_btn.grid(row=0, column=1)

        # File Name
        ttk.Label(main_frame, text="File Name:",
                 font=('Segoe UI', 10)).grid(row=5, column=0, sticky=tk.W, pady=5)

        filename_frame = ttk.Frame(main_frame)
        filename_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))

        self.filename_entry = ttk.Entry(filename_frame, width=55, font=('Segoe UI', 9))
        self.filename_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.filename_entry.insert(0, "scene-viewer")

        ttk.Label(filename_frame, text=".html",
                 font=('Segoe UI', 10)).grid(row=0, column=1)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=20)

        generate_btn = ttk.Button(button_frame, text="Generate HTML File",
                                 command=self.generate_html, width=20)
        generate_btn.grid(row=0, column=0, padx=5)

        self.show_folder_btn = ttk.Button(button_frame, text="Show in Folder",
                                         command=self.show_in_folder, width=20,
                                         state='disabled')
        self.show_folder_btn.grid(row=0, column=1, padx=5)

        clear_btn = ttk.Button(button_frame, text="Clear",
                              command=self.clear_form, width=15)
        clear_btn.grid(row=0, column=2, padx=5)

        # Status label
        self.status_label = ttk.Label(main_frame, text="",
                                     font=('Segoe UI', 9), foreground='green')
        self.status_label.grid(row=8, column=0, columnspan=3)

        # Instructions
        instructions = ("Enter your Scene Viewer URL, choose output location, and click Generate.\n" +
                       "Tip: Use ui=min parameter for cleaner embeds")
        instructions_label = ttk.Label(main_frame, text=instructions,
                                      font=('Segoe UI', 8), foreground='gray')
        instructions_label.grid(row=9, column=0, columnspan=3, pady=(20, 0))

    def browse_folder(self):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory(
            title="Select Output Folder",
            initialdir=self.folder_entry.get()
        )
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

    def generate_html(self):
        """Generate the HTML file"""
        # Get values
        url = self.url_entry.get().strip()
        folder = self.folder_entry.get().strip()
        filename = self.filename_entry.get().strip()

        # Validate inputs
        if not url:
            messagebox.showerror("Error", "Please enter a Scene Viewer URL")
            return

        if not url.startswith("http"):
            messagebox.showerror("Error", "URL must start with http:// or https://")
            return

        if not folder:
            messagebox.showerror("Error", "Please select an output folder")
            return

        if not filename:
            messagebox.showerror("Error", "Please enter a file name")
            return

        # Ensure folder exists
        if not os.path.exists(folder):
            messagebox.showerror("Error", f"Folder does not exist: {folder}")
            return

        # Add .html extension if not present
        if not filename.endswith('.html'):
            filename += '.html'

        # Create full file path
        filepath = os.path.join(folder, filename)

        # Check if file exists
        if os.path.exists(filepath):
            result = messagebox.askyesno(
                "File Exists",
                f"{filename} already exists. Do you want to overwrite it?"
            )
            if not result:
                return

        # Generate HTML content
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESRI Scene Viewer</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
        }}
        iframe {{
            width: 100vw;
            height: 100vh;
            border: none;
        }}
    </style>
</head>
<body>
    <iframe frameborder="0" scrolling="no" allowfullscreen src="{url}"></iframe>
</body>
</html>
"""

        # Write file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)

            self.last_generated_file = filepath
            self.show_folder_btn.config(state='normal')
            self.status_label.config(
                text=f"✓ Successfully created: {filename}",
                foreground='green'
            )

            # Ask if user wants to open the file
            result = messagebox.askyesno(
                "Success",
                f"HTML file created successfully!\n\nDo you want to open it in your browser?"
            )
            if result:
                os.startfile(filepath)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create file: {str(e)}")
            self.status_label.config(
                text=f"✗ Error: {str(e)}",
                foreground='red'
            )

    def show_in_folder(self):
        """Open File Explorer to the output location"""
        if self.last_generated_file and os.path.exists(self.last_generated_file):
            # Open Explorer and select the file
            subprocess.run(['explorer', '/select,', os.path.normpath(self.last_generated_file)])
        else:
            folder = self.folder_entry.get().strip()
            if os.path.exists(folder):
                os.startfile(folder)

    def clear_form(self):
        """Clear all form fields"""
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, "https://www.arcgis.com/home/webscene/viewer.html?webscene=")

        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, "scene-viewer")

        self.status_label.config(text="")
        self.show_folder_btn.config(state='disabled')
        self.last_generated_file = None

def main():
    root = tk.Tk()
    app = SceneViewerGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
