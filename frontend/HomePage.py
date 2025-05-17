import customtkinter as ctk
import tkinter as tk

class HomePage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bluemoon Home")
        self.geometry("900x500")
        self.minsize(900, 500)
        self.configure(fg_color="#f5f6fa")
        
        # Header Frame
        header = ctk.CTkFrame(self, height=50, fg_color="white")
        header.pack(side="top", fill="x")

        # Logo bên trái header
        logo_label = ctk.CTkLabel(header, text="BLUEMOON", font=ctk.CTkFont(size=16, weight="bold"), text_color="#3742fa")
        logo_label.pack(side="left", padx=20)

        # User info bên phải header
        user_frame = ctk.CTkFrame(header, fg_color="transparent")
        user_frame.pack(side="right", padx=20)
        user_icon = ctk.CTkLabel(user_frame, text="👤", font=ctk.CTkFont(size=16))
        user_icon.pack(side="left")
        user_name = ctk.CTkLabel(user_frame, text="Admin", font=ctk.CTkFont(size=14))
        user_name.pack(side="left", padx=5)

        # Sidebar menu trái
        sidebar = ctk.CTkFrame(self, width=150, fg_color="white")
        sidebar.pack(side="left", fill="y")

        # Các nút menu sidebar
        btn_dancu = ctk.CTkButton(sidebar, text="🏠  Dân cư", anchor="w", fg_color="transparent", hover_color="#dfe4ea", border_width=0, font=ctk.CTkFont(size=14))
        btn_dancu.pack(fill="x", pady=(20, 10), padx=15)
        btn_khoanthu = ctk.CTkButton(sidebar, text="📋  Khoản thu", anchor="w", fg_color="transparent", hover_color="#dfe4ea", border_width=0, font=ctk.CTkFont(size=14))
        btn_khoanthu.pack(fill="x", pady=10, padx=15)

        # Main content area
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Tiêu đề Thống kê
        title = ctk.CTkLabel(main_frame, text="Thống kê", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(0, 20))

        # Frame chứa 2 card thông tin
        cards_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        cards_frame.pack(fill="both", expand=True)

        # Card 1: Số hộ khẩu
        card1 = ctk.CTkFrame(cards_frame, width=300, height=160, corner_radius=15, fg_color="#bdc3c7")
        card1.pack(side="left", padx=20, pady=10)
        card1.pack_propagate(False)

        icon_house = ctk.CTkLabel(card1, text="🏠", font=ctk.CTkFont(size=48))
        icon_house.pack(pady=(15, 5))

        label1 = ctk.CTkLabel(card1, 
                              text="Số hộ khẩu trong chung cư hiện tại là:", 
                              font=ctk.CTkFont(size=14), wraplength=280, justify="center")
        label1.pack()

        number1 = ctk.CTkLabel(card1, text="3", font=ctk.CTkFont(size=36, weight="bold"))
        number1.pack(pady=5)

        # Card 2: Số nhân khẩu
        card2 = ctk.CTkFrame(cards_frame, width=300, height=160, corner_radius=15, fg_color="#3867d6")
        card2.pack(side="left", padx=20, pady=10)
        card2.pack_propagate(False)

        icon_people = ctk.CTkLabel(card2, text="👪", font=ctk.CTkFont(size=48))
        icon_people.pack(pady=(15, 5))

        label2 = ctk.CTkLabel(card2, 
                              text="Số nhân khẩu trong chung cư hiện tại là:", 
                              font=ctk.CTkFont(size=14), wraplength=280, justify="center", text_color="white")
        label2.pack()

        number2 = ctk.CTkLabel(card2, text="7", font=ctk.CTkFont(size=36, weight="bold"), text_color="white")
        number2.pack(pady=5)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = HomePage()
    app.mainloop()
