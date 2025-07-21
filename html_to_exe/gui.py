import os
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from threading import Thread
import json
import sys
import webbrowser
from PIL import Image, ImageTk
import tempfile
import http.server
import socketserver
import socket
import time



class HTMLtoEXEConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML To Exe")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        self.icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(self.icon_path):
            self.root.iconbitmap(self.icon_path)
        
        # Variables
        self.html_dir = tk.StringVar()
        self.app_name = tk.StringVar(value="MyApp")
        self.output_dir = tk.StringVar(value=os.path.join(os.getcwd(), "dist"))
        self.icon_path = tk.StringVar()
        self.platform_var = tk.StringVar(value="win")
        self.installation_status = tk.StringVar(value="Checking requirements...")
        self.electron_options = {
            "width": tk.StringVar(value="800"),
            "height": tk.StringVar(value="600"),
            "min_width": tk.StringVar(value="400"),
            "min_height": tk.StringVar(value="300"),
            "max_width": tk.StringVar(value=""),
            "max_height": tk.StringVar(value=""),
            "resizable": tk.BooleanVar(value=True),
            "fullscreen": tk.BooleanVar(value=False),
            "kiosk": tk.BooleanVar(value=False),
            "title": tk.StringVar(value=""),
            "transparent": tk.BooleanVar(value=False),
            "frame": tk.BooleanVar(value=True),
            "node_integration": tk.BooleanVar(value=True),
            "context_isolation": tk.BooleanVar(value=False),
            "background_color": tk.StringVar(value="#ffffff"),
            "show": tk.BooleanVar(value=True),
            "webgl": tk.BooleanVar(value=True),
            "sandbox": tk.BooleanVar(value=False)
        }
        
        # Preview server
        self.preview_server = None
        self.preview_port = self.find_free_port()
        self.preview_process = None
        self.httpd = None
        
        # UI Setup
        self.create_advanced_ui()
        
        # Initial checks
        self.root.after(100, self.check_requirements)
    
    def find_free_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]
    
    def create_advanced_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Settings Tab
        settings_tab = ttk.Frame(notebook, padding="10")
        notebook.add(settings_tab, text="Settings")
        
        # HTML Folder
        ttk.Label(settings_tab, text="HTML Folder:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(settings_tab, textvariable=self.html_dir, width=50).grid(row=0, column=1, padx=2)
        ttk.Button(settings_tab, text="Browse", command=self.browse_html, width=8).grid(row=0, column=2)
        
        # App Name
        ttk.Label(settings_tab, text="App Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(settings_tab, textvariable=self.app_name, width=50).grid(row=1, column=1, padx=2)
        
        # Output Directory
        ttk.Label(settings_tab, text="Output Folder:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(settings_tab, textvariable=self.output_dir, width=50).grid(row=2, column=1, padx=2)
        ttk.Button(settings_tab, text="Browse", command=self.browse_output, width=8).grid(row=2, column=2)
        
        # Icon File
        ttk.Label(settings_tab, text="App Icon:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(settings_tab, textvariable=self.icon_path, width=50).grid(row=3, column=1, padx=2)
        ttk.Button(settings_tab, text="Browse", command=self.browse_icon, width=8).grid(row=3, column=2)
        
        # Platform Selection
        ttk.Label(settings_tab, text="Platform:").grid(row=4, column=0, sticky=tk.W, pady=2)
        platform_frame = ttk.Frame(settings_tab)
        platform_frame.grid(row=4, column=1, columnspan=2, sticky=tk.W)
        ttk.Radiobutton(platform_frame, text="Windows", variable=self.platform_var, value="win").pack(side=tk.LEFT)
        ttk.Radiobutton(platform_frame, text="macOS", variable=self.platform_var, value="mac").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(platform_frame, text="Linux", variable=self.platform_var, value="linux").pack(side=tk.LEFT)
        
        # Options Tab
        options_tab = ttk.Frame(notebook, padding="10")
        notebook.add(options_tab, text="Electron Options")
        
        # Window Options
        ttk.Label(options_tab, text="Window Options", font=("", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(options_tab, text="Width:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(options_tab, textvariable=self.electron_options["width"], width=10).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(options_tab, text="Height:").grid(row=1, column=2, sticky=tk.W)
        ttk.Entry(options_tab, textvariable=self.electron_options["height"], width=10).grid(row=1, column=3, sticky=tk.W)
        
        ttk.Label(options_tab, text="Min Width:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(options_tab, textvariable=self.electron_options["min_width"], width=10).grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(options_tab, text="Min Height:").grid(row=2, column=2, sticky=tk.W)
        ttk.Entry(options_tab, textvariable=self.electron_options["min_height"], width=10).grid(row=2, column=3, sticky=tk.W)
        
        ttk.Label(options_tab, text="Max Width:").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(options_tab, textvariable=self.electron_options["max_width"], width=10).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Label(options_tab, text="Max Height:").grid(row=3, column=2, sticky=tk.W)
        ttk.Entry(options_tab, textvariable=self.electron_options["max_height"], width=10).grid(row=3, column=3, sticky=tk.W)
        
        ttk.Checkbutton(options_tab, text="Resizable", variable=self.electron_options["resizable"]).grid(row=4, column=0, sticky=tk.W)
        ttk.Checkbutton(options_tab, text="Fullscreen", variable=self.electron_options["fullscreen"]).grid(row=4, column=1, sticky=tk.W)
        ttk.Checkbutton(options_tab, text="Kiosk Mode", variable=self.electron_options["kiosk"]).grid(row=4, column=2, sticky=tk.W)
        
        ttk.Label(options_tab, text="Title:").grid(row=5, column=0, sticky=tk.W)
        ttk.Entry(options_tab, textvariable=self.electron_options["title"], width=30).grid(row=5, column=1, columnspan=3, sticky=tk.W)
        
        ttk.Label(options_tab, text="Background Color:").grid(row=6, column=0, sticky=tk.W)
        ttk.Entry(options_tab, textvariable=self.electron_options["background_color"], width=10).grid(row=6, column=1, sticky=tk.W)
        
        # Web Preferences
        ttk.Label(options_tab, text="Web Preferences", font=("", 10, "bold")).grid(row=7, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(options_tab, text="Node Integration", variable=self.electron_options["node_integration"]).grid(row=8, column=0, sticky=tk.W)
        ttk.Checkbutton(options_tab, text="Context Isolation", variable=self.electron_options["context_isolation"]).grid(row=8, column=1, sticky=tk.W)
        ttk.Checkbutton(options_tab, text="Show Window", variable=self.electron_options["show"]).grid(row=8, column=2, sticky=tk.W)
        ttk.Checkbutton(options_tab, text="WebGL", variable=self.electron_options["webgl"]).grid(row=9, column=0, sticky=tk.W)
        ttk.Checkbutton(options_tab, text="Sandbox", variable=self.electron_options["sandbox"]).grid(row=9, column=1, sticky=tk.W)
        ttk.Checkbutton(options_tab, text="Transparent Window", variable=self.electron_options["transparent"]).grid(row=10, column=0, sticky=tk.W)
        ttk.Checkbutton(options_tab, text="Show Frame", variable=self.electron_options["frame"]).grid(row=10, column=1, sticky=tk.W)
        
        # Preview Tab
        preview_tab = ttk.Frame(notebook)
        notebook.add(preview_tab, text="Preview")
        
        self.preview_frame = ttk.Frame(preview_tab)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.preview_label = ttk.Label(self.preview_frame, text="No preview available", anchor=tk.CENTER)
        self.preview_label.pack(fill=tk.BOTH, expand=True)
        
        preview_btn_frame = ttk.Frame(preview_tab)
        preview_btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(preview_btn_frame, text="Start Preview", command=self.start_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(preview_btn_frame, text="Stop Preview", command=self.stop_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(preview_btn_frame, text="Open in Browser", command=self.open_in_browser).pack(side=tk.RIGHT, padx=5)
        
        # Console Output
        console_frame = ttk.LabelFrame(main_frame, text="Output Log", padding="5")
        console_frame.pack(fill=tk.BOTH, expand=False, pady=5)
        
        # Create a container frame for the console with fixed height
        console_container = ttk.Frame(console_frame, height=150)
        console_container.pack(fill=tk.BOTH, expand=True)
        console_container.pack_propagate(False)  # Prevent the frame from resizing to contents
        
        self.console = scrolledtext.ScrolledText(
            console_container, 
            wrap=tk.WORD,
            font=("Consolas", 8),
            state='disabled'
        )
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # Status and Buttons
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(bottom_frame, textvariable=self.installation_status).pack(side=tk.LEFT, padx=5)
        
        self.install_btn = ttk.Button(
            bottom_frame, 
            text="Install Requirements", 
            command=self.install_requirements,
            width=20
        )
        self.install_btn.pack(side=tk.RIGHT, padx=2)
        
        self.convert_btn = ttk.Button(
            bottom_frame, 
            text="Convert to EXE", 
            command=self.start_conversion,
            state=tk.DISABLED,
            width=20
        )
        self.convert_btn.pack(side=tk.RIGHT, padx=2)
    
    def browse_html(self):
        dir_path = filedialog.askdirectory(title="Select HTML Folder")
        if dir_path:
            self.html_dir.set(dir_path)
            default_name = os.path.basename(dir_path)
            if default_name:
                self.app_name.set(default_name)
                self.electron_options["title"].set(default_name)
    
    def browse_output(self):
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir.set(dir_path)
    
    def browse_icon(self):
        file_path = filedialog.askopenfilename(
            title="Select Icon File",
            filetypes=[("Icon Files", "*.ico;*.icns;*.png"), ("All Files", "*.*")]
        )
        if file_path:
            self.icon_path.set(file_path)
    
    def log(self, message):
        self.console.configure(state='normal')
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.configure(state='disabled')
        self.root.update()
    
    def clear_log(self):
        self.console.configure(state='normal')
        self.console.delete(1.0, tk.END)
        self.console.configure(state='disabled')
    
    def check_requirements(self):
        self.clear_log()
        self.log("Checking system requirements...")
        
        try:
            # Check Node.js
            node_version = subprocess.check_output(
                ["node", "--version"],
                stderr=subprocess.STDOUT,
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            ).decode().strip()
            self.log(f"✔ Node.js {node_version} detected")
            
            # Check npm
            npm_version = subprocess.check_output(
                ["npm", "--version"],
                stderr=subprocess.STDOUT,
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            ).decode().strip()
            self.log(f"✔ npm {npm_version} detected")
            
            # Check Electron
            try:
                electron_version = subprocess.check_output(
                    ["electron", "--version"],
                    stderr=subprocess.STDOUT,
                    shell=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                ).decode().strip()
                self.log(f"✔ {electron_version} detected")
                self.installation_status.set("Requirements satisfied")
                self.convert_btn.config(state=tk.NORMAL)
                return True
            except subprocess.CalledProcessError:
                self.log("✖ Electron not found (but Node.js is installed)")
                self.installation_status.set("Electron not found - install required")
                return False
            
        except subprocess.CalledProcessError:
            self.log("✖ Node.js and npm are not installed or not in PATH")
            self.log("Please install Node.js from https://nodejs.org/")
            self.installation_status.set("Node.js not found - install required")
            return False
    
    def install_requirements(self):
        self.clear_log()
        self.log("Installing required packages...")
        
        try:
            # Install only essential packages
            packages = ["electron@latest", "electron-packager@latest"]
            
            process = subprocess.Popen(
                ["npm", "install", "-g"] + packages,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            for line in process.stdout:
                self.log(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.log("✔ Packages installed successfully")
                self.installation_status.set("Requirements satisfied")
                self.convert_btn.config(state=tk.NORMAL)
                messagebox.showinfo("Success", "Required packages installed successfully")
            else:
                raise Exception("Failed to install packages")
        
        except Exception as e:
            self.log(f"Error: {str(e)}")
            self.installation_status.set("Installation failed")
            messagebox.showerror("Error", f"Failed to install requirements: {str(e)}")
    
    def start_conversion(self):
        if not self.html_dir.get():
            messagebox.showerror("Error", "Please select an HTML folder to convert")
            return
            
        self.convert_btn.config(state=tk.DISABLED)
        self.install_btn.config(state=tk.DISABLED)
        Thread(target=self.convert_to_exe, daemon=True).start()
    
    def generate_main_js(self):
        options = []
        
        # Window size options
        options.append(f"width: {self.electron_options['width'].get()},")
        options.append(f"height: {self.electron_options['height'].get()},")
        
        if self.electron_options['min_width'].get():
            options.append(f"minWidth: {self.electron_options['min_width'].get()},")
        if self.electron_options['min_height'].get():
            options.append(f"minHeight: {self.electron_options['min_height'].get()},")
        if self.electron_options['max_width'].get():
            options.append(f"maxWidth: {self.electron_options['max_width'].get()},")
        if self.electron_options['max_height'].get():
            options.append(f"maxHeight: {self.electron_options['max_height'].get()},")
        
        # Boolean options
        options.append(f"resizable: {str(self.electron_options['resizable'].get()).lower()},")
        options.append(f"fullscreen: {str(self.electron_options['fullscreen'].get()).lower()},")
        options.append(f"kiosk: {str(self.electron_options['kiosk'].get()).lower()},")
        options.append(f"transparent: {str(self.electron_options['transparent'].get()).lower()},")
        options.append(f"frame: {str(self.electron_options['frame'].get()).lower()},")
        options.append(f"show: {str(self.electron_options['show'].get()).lower()},")
        
        # Other options
        title = self.electron_options['title'].get()
        if title:
            options.append(f'title: "{title}",')
        
        bg_color = self.electron_options['background_color'].get()
        if bg_color:
            options.append(f'backgroundColor: "{bg_color}",')
        
        # Web preferences
        web_prefs = []
        web_prefs.append(f"nodeIntegration: {str(self.electron_options['node_integration'].get()).lower()},")
        web_prefs.append(f"contextIsolation: {str(self.electron_options['context_isolation'].get()).lower()},")
        web_prefs.append(f"webgl: {str(self.electron_options['webgl'].get()).lower()},")
        web_prefs.append(f"sandbox: {str(self.electron_options['sandbox'].get()).lower()}")
        
        options.append(f"webPreferences: {{{''.join(web_prefs)}}}")
        
        main_js = f"""const {{ app, BrowserWindow }} = require('electron')
const path = require('path')

function createWindow() {{
    const win = new BrowserWindow({{
        {''.join(options)}
    }})

    win.loadFile('index.html')
    
    // Open DevTools if in development
    if (process.env.NODE_ENV === 'development') {{
        win.webContents.openDevTools()
    }}
}}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {{
    if (process.platform !== 'darwin') app.quit()
}})

app.on('activate', () => {{
    if (BrowserWindow.getAllWindows().length === 0) {{
        createWindow()
    }}
}})
"""
        return main_js
    
    def convert_to_exe(self):
        try:
            self.clear_log()
            self.log("Starting conversion process...")
            
            html_dir = self.html_dir.get()
            app_name = self.app_name.get()
            output_dir = self.output_dir.get()
            icon_path = self.icon_path.get()
            platform = self.platform_var.get()
            
            if not os.path.exists(html_dir):
                raise Exception(f"HTML folder not found: {html_dir}")
            
            # Check for index.html
            if not os.path.exists(os.path.join(html_dir, "index.html")):
                raise Exception("No index.html found in the selected folder")
            
            os.makedirs(output_dir, exist_ok=True)
            
            project_dir = os.path.join(output_dir, f"{app_name}-electron")
            if os.path.exists(project_dir):
                shutil.rmtree(project_dir)
            os.makedirs(project_dir)
            
            self.log("Creating project files...")
            
            # Create package.json with minimal dependencies
            package_json = {
                "name": app_name.lower().replace(" ", "-"),
                "version": "1.0.0",
                "main": "main.js",
                "scripts": {
                    "start": "electron .",
                    "package": "electron-packager . --out=../dist --overwrite"
                },
                "devDependencies": {
                    "electron": "latest"
                }
            }
            
            with open(os.path.join(project_dir, "package.json"), "w") as f:
                json.dump(package_json, f, indent=2)
            
            # Create main.js with all options
            with open(os.path.join(project_dir, "main.js"), "w") as f:
                f.write(self.generate_main_js())
            
            # Copy all files from HTML folder
            for item in os.listdir(html_dir):
                s = os.path.join(html_dir, item)
                d = os.path.join(project_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            
            # Prepare platform-specific packaging command
            platform_map = {
                "win": "--platform=win32 --arch=x64",
                "mac": "--platform=darwin --arch=x64",
                "linux": "--platform=linux --arch=x64"
            }
            
            package_cmd = f"electron-packager . {app_name} --out=../dist --overwrite {platform_map[platform]} --asar"
            
            if icon_path:
                if platform == "win" and icon_path.endswith(".ico"):
                    package_cmd += f" --icon={icon_path}"
                elif platform == "mac" and (icon_path.endswith(".icns") or icon_path.endswith(".png")):
                    package_cmd += f" --icon={icon_path}"
                elif platform == "linux" and icon_path.endswith(".png"):
                    package_cmd += f" --icon={icon_path}"
            
            # Update package.json with platform-specific command
            package_json["scripts"]["package"] = package_cmd
            with open(os.path.join(project_dir, "package.json"), "w") as f:
                json.dump(package_json, f, indent=2)
            
            self.log("Installing local dependencies...")
            process = subprocess.Popen(
                ["npm", "install"],
                cwd=project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            for line in process.stdout:
                self.log(line.strip())
            
            process.wait()
            
            self.log("Packaging application...")
            package_process = subprocess.Popen(
                ["npm", "run", "package"],
                cwd=project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            for line in package_process.stdout:
                self.log(line.strip())
            
            package_process.wait()
            
            if package_process.returncode == 0:
                self.log("\n✔ Conversion successful!")
                output_path = os.path.join(output_dir, "dist")
                self.log(f"Executable created in: {output_path}")
                
                # Clean up node_modules to save space
                node_modules = os.path.join(project_dir, "node_modules")
                if os.path.exists(node_modules):
                    shutil.rmtree(node_modules)
                
                messagebox.showinfo("Success", f"Application successfully converted!\nOutput directory: {output_path}")
            else:
                raise Exception("Packaging failed")
            
        except Exception as e:
            self.log(f"\n✖ Error: {str(e)}")
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
        finally:
            self.convert_btn.config(state=tk.NORMAL)
            self.install_btn.config(state=tk.NORMAL)
    
    def start_preview(self):
        if not self.html_dir.get():
            messagebox.showerror("Error", "Please select an HTML folder first")
            return
        
        html_dir = self.html_dir.get()
        
        if not os.path.exists(os.path.join(html_dir, "index.html")):
            messagebox.showerror("Error", "No index.html found in the selected folder")
            return
        
        # Stop any existing preview
        self.stop_preview()
        
        # Start HTTP server in a thread
        self.preview_server = Thread(target=self.run_preview_server, args=(html_dir,), daemon=True)
        self.preview_server.start()
        
        # Wait a moment for server to start
        time.sleep(1)
        
        # Update UI
        self.preview_label.config(text=f"Preview running at http://localhost:{self.preview_port}")
        
        # Start Electron preview
        try:
            main_js = self.generate_main_js()
            
            # Create temp directory for preview
            temp_dir = tempfile.mkdtemp()
            with open(os.path.join(temp_dir, "main.js"), "w") as f:
                f.write(main_js)
            
            # Create minimal package.json
            with open(os.path.join(temp_dir, "package.json"), "w") as f:
                json.dump({
                    "name": "preview",
                    "version": "1.0.0",
                    "main": "main.js",
                    "scripts": {
                        "start": "electron ."
                    }
                }, f)
            
            # Start Electron process
            self.preview_process = subprocess.Popen(
                ["electron", temp_dir],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start preview: {str(e)}")
    
    def run_preview_server(self, directory):
        os.chdir(directory)
        handler = http.server.SimpleHTTPRequestHandler
        
        with socketserver.TCPServer(("", self.preview_port), handler) as httpd:
            self.httpd = httpd
            httpd.serve_forever()
    
    def stop_preview(self):
        if hasattr(self, 'httpd') and self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd = None
        
        if self.preview_process:
            self.preview_process.terminate()
            try:
                self.preview_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.preview_process.kill()
            self.preview_process = None
        
        self.preview_label.config(text="Preview stopped")
    
    def open_in_browser(self):
        if self.preview_port:
            webbrowser.open(f"http://localhost:{self.preview_port}")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Set Windows style if available
    if sys.platform == "win32":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)

    
    app = HTMLtoEXEConverter(root)
    root.mainloop()
def run_gui():
    root = tk.Tk()
    app = HTMLtoEXEConverter(root)
    root.mainloop()