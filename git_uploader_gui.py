# git_uploader_gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from git import Repo, GitCommandError
import os
import shutil
import threading
import time
import sys

class GitUploaderApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("GitHub Repository Manager")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6)
        self.style.configure("Title.TLabel", font=('Arial', 11, 'bold'))
        self.style.configure("Warning.TLabel", foreground='red', font=('Arial', 9))

        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="GitHub Repository Manager", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 15))

        # Repository Section
        repo_frame = ttk.LabelFrame(main_frame, text="Repository Configuration", padding="10")
        repo_frame.pack(fill=tk.X, pady=(0, 10))

        # Repo URL
        ttk.Label(repo_frame, text="GitHub Repository URL:*", style="Title.TLabel").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.repo_entry = ttk.Entry(repo_frame, width=70)
        self.repo_entry.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))
        
        # Personal Access Token
        ttk.Label(repo_frame, text="GitHub Personal Access Token:", style="Title.TLabel").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.token_entry = ttk.Entry(repo_frame, width=70, show="•")
        self.token_entry.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))
        ttk.Label(repo_frame, text="Required for private repositories", 
                 font=('Arial', 8), foreground='gray').grid(row=4, column=0, sticky=tk.W)

        # Local Path for Repo
        ttk.Label(repo_frame, text="Local Repository Path:*", style="Title.TLabel").grid(row=5, column=0, sticky=tk.W, pady=(0, 5))
        
        local_path_frame = ttk.Frame(repo_frame)
        local_path_frame.grid(row=6, column=0, columnspan=2, sticky=tk.EW, pady=(0, 5))
        
        self.local_entry = ttk.Entry(local_path_frame, width=60)
        self.local_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.browse_local_btn = ttk.Button(local_path_frame, text="Browse...", command=self.browse_directory)
        self.browse_local_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Warning label for directory requirement
        self.dir_warning_label = ttk.Label(repo_frame, 
                                          text="⚠️ Directory must be empty for cloning", 
                                          style="Warning.TLabel")
        self.dir_warning_label.grid(row=7, column=0, sticky=tk.W)
        
        self.clone_btn = ttk.Button(repo_frame, text="Clone Repository", command=self.start_clone_thread)
        self.clone_btn.grid(row=8, column=0, columnspan=2, pady=10)

        # File Upload Section
        upload_frame = ttk.LabelFrame(main_frame, text="File Upload", padding="10")
        upload_frame.pack(fill=tk.X, pady=(0, 10))

        # File selection
        ttk.Label(upload_frame, text="Select File to Upload:*", style="Title.TLabel").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        file_path_frame = ttk.Frame(upload_frame)
        file_path_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))
        
        self.file_entry = ttk.Entry(file_path_frame, width=60)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.browse_file_btn = ttk.Button(file_path_frame, text="Browse...", command=self.browse_file)
        self.browse_file_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Progress bar for upload
        self.progress_frame = ttk.Frame(upload_frame)
        self.progress_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=(5, 10))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, expand=True)
        
        self.progress_label = ttk.Label(self.progress_frame, text="Ready")
        self.progress_label.pack()

        self.upload_btn = ttk.Button(upload_frame, text="Upload File to Repository", command=self.start_upload_thread)
        self.upload_btn.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Status Section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.status_text = tk.Text(status_frame, height=6, wrap=tk.WORD, font=('Arial', 9))
        status_scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Clear status button
        clear_btn = ttk.Button(main_frame, text="Clear Status", command=self.clear_status)
        clear_btn.pack(anchor=tk.E)
        
        # Configure grid weights for responsive layout
        repo_frame.columnconfigure(0, weight=1)
        upload_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(0, weight=1)

        self.buttons = [self.browse_local_btn, self.clone_btn, self.browse_file_btn, self.upload_btn]
        
        # Bind events for directory validation
        self.local_entry.bind('<KeyRelease>', self.validate_directory)
        self.local_entry.bind('<FocusOut>', self.validate_directory)

    def browse_directory(self):
        """Opens a dialog to choose a directory and inserts it into the local_entry."""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.local_entry.delete(0, tk.END)
            self.local_entry.insert(0, dir_path)
            self.validate_directory()

    def browse_file(self):
        """Opens a dialog to choose a file and inserts it into the file_entry."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def validate_directory(self, event=None):
        """Validates if the directory exists and is empty"""
        path = self.local_entry.get().strip()
        if path and os.path.exists(path):
            if os.listdir(path):
                self.dir_warning_label.config(text="⚠️ Directory is NOT empty - cloning will be skipped", foreground='red')
            else:
                self.dir_warning_label.config(text="✓ Directory is empty - ready for cloning", foreground='green')
        else:
            self.dir_warning_label.config(text="⚠️ Directory must be empty for cloning", foreground='orange')

    def update_status(self, message, clear_first=False):
        """Updates the status text area with timestamp."""
        if clear_first:
            self.status_text.delete(1.0, tk.END)
        
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.status_text.insert(tk.END, formatted_message)
        self.status_text.see(tk.END)  # Auto-scroll to bottom
        self.root.update_idletasks()

    def update_progress(self, value, message=None):
        """Updates the progress bar and label."""
        self.progress_bar['value'] = value
        if message:
            self.progress_label.config(text=message)
        self.root.update_idletasks()

    def clear_status(self):
        """Clears the status text area."""
        self.status_text.delete(1.0, tk.END)
        self.update_status("Status cleared")

    def toggle_buttons(self, enabled):
        """Disables or enables all buttons to prevent multiple operations."""
        state = tk.NORMAL if enabled else tk.DISABLED
        for button in self.buttons:
            button.config(state=state)

    # --- Threaded Functions ---

    def start_clone_thread(self):
        """Starts the clone operation in a new thread."""
        self.toggle_buttons(False)
        self.update_status("Starting repository clone operation...", clear_first=True)
        thread = threading.Thread(target=self.clone_repo, daemon=True)
        thread.start()

    def start_upload_thread(self):
        """Starts the upload operation in a new thread."""
        self.toggle_buttons(False)
        self.update_status("Starting file upload operation...", clear_first=True)
        self.update_progress(0, "Initializing...")
        thread = threading.Thread(target=self.upload_file, daemon=True)
        thread.start()

    # --- Core Logic Functions ---

    def clone_repo(self):
        url = self.repo_entry.get().strip()
        path = self.local_entry.get().strip()
        token = self.token_entry.get().strip()

        if not url or not path:
            messagebox.showerror("Error", "Please enter both Repository URL and Local Path")
            self.toggle_buttons(True)
            self.update_status("Error: Missing required fields")
            return

        if token:
            url_parts = url.split("https://")
            if len(url_parts) == 2:
                url = f"https://{token}@{url_parts[1]}"

        try:
            if not os.path.exists(path):
                os.makedirs(path)
                self.update_status(f"Created directory: {path}")

            if not os.listdir(path):
                self.update_status(f"Cloning repository from: {url.split('@')[-1] if '@' in url else url}")
                Repo.clone_from(url, path)
                self.update_status("Repository cloned successfully!")
                messagebox.showinfo("Success", "Repository cloned successfully!")
            else:
                self.update_status("Directory is not empty - using existing repository")
                messagebox.showinfo("Info", "Directory is not empty; using existing repository.")
                
        except GitCommandError as e:
            error_msg = f"Git Error: Failed to clone repository\n{str(e)}"
            self.update_status(f"Error: {error_msg}")
            messagebox.showerror("Git Error", error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.update_status(f"Error: {error_msg}")
            messagebox.showerror("Error", error_msg)
        finally:
            self.toggle_buttons(True)

    def upload_file(self):
        repo_path = self.local_entry.get().strip()
        source_file = self.file_entry.get().strip()

        if not repo_path or not source_file:
            messagebox.showerror("Error", "Please provide both repository path and select a file.")
            self.toggle_buttons(True)
            self.update_status("Error: Missing repository path or file")
            self.update_progress(0, "Error: Missing fields")
            return

        try:
            self.update_progress(10, "Validating repository...")
            
            if not os.path.exists(repo_path) or not os.path.isdir(os.path.join(repo_path, '.git')):
                messagebox.showerror("Error", "The specified local path is not a valid Git repository!")
                self.update_status("Error: Not a valid Git repository")
                self.update_progress(0, "Error: Invalid repository")
                self.toggle_buttons(True)
                return

            dest_file = os.path.join(repo_path, os.path.basename(source_file))
            self.update_progress(30, "Copying file to repository...")
            self.update_status(f"Copying {os.path.basename(source_file)} to repository...")
            
            shutil.copy(source_file, dest_file)
            self.update_progress(50, "File copied successfully")

            repo = Repo(repo_path)
            
            self.update_progress(60, "Checking for changes...")
            if not repo.is_dirty(untracked_files=True):
                messagebox.showinfo("Info", "No changes to commit. The file may be identical or already tracked.")
                self.update_status("No changes detected - nothing to commit")
                self.update_progress(0, "No changes detected")
                self.toggle_buttons(True)
                return
            
            self.update_progress(70, "Staging files...")
            self.update_status("Adding files to Git staging area...")
            repo.git.add(A=True)
            
            self.update_progress(80, "Creating commit...")
            self.update_status("Committing changes...")
            commit_message = f"Add {os.path.basename(source_file)} via GitHub Uploader GUI"
            repo.index.commit(commit_message)
            
            self.update_progress(90, "Pushing to remote repository...")
            self.update_status("Pushing changes to remote repository...")
            origin = repo.remote(name='origin')
            origin.push()

            self.update_progress(100, "Upload completed successfully!")
            self.update_status("File uploaded and pushed successfully!")
            messagebox.showinfo("Success", "File uploaded and pushed successfully!")
            
        except GitCommandError as e:
            error_msg = f"Git Error: {str(e)}"
            self.update_status(f"Error: {error_msg}")
            self.update_progress(0, "Git operation failed")
            messagebox.showerror("Git Error", f"A Git command failed.\n\n{error_msg}")
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.update_status(f"Error: {error_msg}")
            self.update_progress(0, "Operation failed")
            messagebox.showerror("Error", error_msg)
        finally:
            self.toggle_buttons(True)
            # Reset progress bar after a delay
            self.root.after(3000, lambda: self.update_progress(0, "Ready"))

def main():
    # Check if required modules are installed
    try:
        import git
        import tkinter
    except ImportError as e:
        print(f"Missing required module: {e}")
        print("Please install required packages:")
        print("pip install GitPython tkinter")
        input("Press Enter to exit...")
        return

    root = tk.Tk()
    app = GitUploaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()