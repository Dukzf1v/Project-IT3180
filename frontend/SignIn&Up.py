import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LoginSignupApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login & Signup")
        self.geometry("800x500")
        self.resizable(False, False)
        self.configure(fg_color="#ffffff")

        # Container frame chứa cả login và signup
        self.container = ctk.CTkFrame(self, corner_radius=20, fg_color="white", width=400, height=450)
        self.container.place(relx=0.5, rely=0.5, anchor="center")


        # Tạo frame login và signup (ẩn signup mặc định)
        self.login_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.signup_frame = ctk.CTkFrame(self.container, fg_color="transparent")

        self.login_frame.pack(fill="both", expand=True)
        self.signup_frame.pack(fill="both", expand=True)
        self.signup_frame.pack_forget()  # Ẩn signup lúc đầu

        self.create_login_ui()
        self.create_signup_ui()

    def create_login_ui(self):
        # Login UI components
        ctk.CTkLabel(self.login_frame, text="Welcome back", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self.login_frame, text="Please enter your details to sign in.", font=ctk.CTkFont(size=12)).pack()

        ctk.CTkLabel(self.login_frame, text="Tên đăng nhập").pack(anchor="w", padx=30, pady=(20, 5))
        self.login_username = ctk.CTkEntry(self.login_frame, placeholder_text="Nhập tên đăng nhập")
        self.login_username.pack(fill="x", padx=30)

        ctk.CTkLabel(self.login_frame, text="Mật khẩu").pack(anchor="w", padx=30, pady=(20, 5))
        self.login_password = ctk.CTkEntry(self.login_frame, placeholder_text="Nhập mật khẩu", show="*")
        self.login_password.pack(fill="x", padx=30)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.handle_login)
        self.login_button.pack(pady=20)

        self.to_signup_btn = ctk.CTkButton(self.login_frame, text="Chưa có tài khoản? Đăng ký", fg_color="transparent", hover_color="lightblue", command=self.show_signup)
        self.to_signup_btn.pack()

    def create_signup_ui(self):
        # Signup UI components
        ctk.CTkLabel(self.signup_frame, text="Create account", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self.signup_frame, text="Please fill in the form to create an account.", font=ctk.CTkFont(size=12)).pack()

        ctk.CTkLabel(self.signup_frame, text="Tên đăng nhập").pack(anchor="w", padx=30, pady=(20, 5))
        self.signup_username = ctk.CTkEntry(self.signup_frame, placeholder_text="Nhập tên đăng nhập")
        self.signup_username.pack(fill="x", padx=30)

        ctk.CTkLabel(self.signup_frame, text="Email").pack(anchor="w", padx=30, pady=(20, 5))
        self.signup_email = ctk.CTkEntry(self.signup_frame, placeholder_text="Nhập email")
        self.signup_email.pack(fill="x", padx=30)

        ctk.CTkLabel(self.signup_frame, text="Mật khẩu").pack(anchor="w", padx=30, pady=(20, 5))
        self.signup_password = ctk.CTkEntry(self.signup_frame, placeholder_text="Nhập mật khẩu", show="*")
        self.signup_password.pack(fill="x", padx=30)

        ctk.CTkLabel(self.signup_frame, text="Xác nhận mật khẩu").pack(anchor="w", padx=30, pady=(20, 5))
        self.signup_password_confirm = ctk.CTkEntry(self.signup_frame, placeholder_text="Nhập lại mật khẩu", show="*")
        self.signup_password_confirm.pack(fill="x", padx=30)

        self.signup_button = ctk.CTkButton(self.signup_frame, text="Sign up", command=self.handle_signup)
        self.signup_button.pack(pady=20)

        self.to_login_btn = ctk.CTkButton(self.signup_frame, text="Đã có tài khoản? Đăng nhập", fg_color="transparent", hover_color="lightblue", command=self.show_login)
        self.to_login_btn.pack()

    def show_signup(self):
        self.login_frame.pack_forget()
        self.signup_frame.pack(fill="both", expand=True)

    def show_login(self):
        self.signup_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def handle_login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        if not username or not password:
            messagebox.showwarning("Warning", "Vui lòng nhập đầy đủ thông tin!")
            return
        # TODO: Gọi API login backend Django ở đây
        messagebox.showinfo("Login", f"Đăng nhập với username: {username}")

    def handle_signup(self):
        username = self.signup_username.get()
        email = self.signup_email.get()
        password = self.signup_password.get()
        password_confirm = self.signup_password_confirm.get()
        if not username or not email or not password or not password_confirm:
            messagebox.showwarning("Warning", "Vui lòng nhập đầy đủ thông tin!")
            return
        if password != password_confirm:
            messagebox.showerror("Error", "Mật khẩu xác nhận không khớp!")
            return
        # TODO: Gọi API đăng ký backend Django ở đây
        messagebox.showinfo("Signup", f"Đăng ký tài khoản: {username} - {email}")

if __name__ == "__main__":
    app = LoginSignupApp()
    app.mainloop()
