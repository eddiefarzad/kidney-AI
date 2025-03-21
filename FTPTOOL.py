import ftplib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class FTPClient:
    def __init__(self, root):
        self.root = root
        self.root.title("FTP Client")
        self.root.geometry("500x400")

        # Connection Frame
        self.frame = ttk.LabelFrame(root, text="FTP Connection")
        self.frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(self.frame, text="Host:").grid(row=0, column=0, padx=5, pady=5)
        self.host_entry = ttk.Entry(self.frame, width=30)
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        self.user_entry = ttk.Entry(self.frame, width=30)
        self.user_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        self.pass_entry = ttk.Entry(self.frame, width=30, show="*")
        self.pass_entry.grid(row=2, column=1, padx=5, pady=5)

        self.connect_btn = ttk.Button(self.frame, text="Connect", command=self.connect)
        self.connect_btn.grid(row=3, columnspan=2, pady=10)

        # File List
        self.file_listbox = tk.Listbox(root, height=15)
        self.file_listbox.pack(fill="both", padx=10, pady=5, expand=True)

        # Buttons
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(fill="x", padx=10, pady=5)

        self.upload_btn = ttk.Button(self.button_frame, text="Upload", command=self.upload_file)
        self.upload_btn.pack(side="left", expand=True)

        self.download_btn = ttk.Button(self.button_frame, text="Download", command=self.download_file)
        self.download_btn.pack(side="left", expand=True)

        self.disconnect_btn = ttk.Button(self.button_frame, text="Disconnect", command=self.disconnect)
        self.disconnect_btn.pack(side="left", expand=True)

        self.ftp = None

    def connect(self):
        try:
            host = self.host_entry.get()
            user = self.user_entry.get()
            password = self.pass_entry.get()
            
            self.ftp = ftplib.FTP(host)
            self.ftp.login(user, password)
            self.list_files()
            messagebox.showinfo("Success", "Connected to FTP server")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def list_files(self):
        if self.ftp:
            self.file_listbox.delete(0, tk.END)
            files = self.ftp.nlst()
            for file in files:
                self.file_listbox.insert(tk.END, file)

    def upload_file(self):
        if not self.ftp:
            messagebox.showerror("Error", "Not connected to FTP server")
            return
        
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, "rb") as file:
                    self.ftp.storbinary(f"STOR {file_path.split('/')[-1]}", file)
                self.list_files()
                messagebox.showinfo("Success", "File uploaded successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def download_file(self):
        if not self.ftp:
            messagebox.showerror("Error", "Not connected to FTP server")
            return
        
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            save_path = filedialog.asksaveasfilename(initialfile=selected_file)
            if save_path:
                try:
                    with open(save_path, "wb") as file:
                        self.ftp.retrbinary(f"RETR {selected_file}", file.write)
                    messagebox.showinfo("Success", "File downloaded successfully")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def disconnect(self):
        if self.ftp:
            self.ftp.quit()
            self.ftp = None
            self.file_listbox.delete(0, tk.END)
            messagebox.showinfo("Disconnected", "FTP session closed")

if __name__ == "__main__":
    root = tk.Tk()
    app = FTPClient(root)
    root.mainloop()
