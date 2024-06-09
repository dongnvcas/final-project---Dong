import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import pandas as pd
import requests
from io import BytesIO
import matplotlib.pyplot as plt

class GiaoDienChuongTrinh:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý giao dịch Binance")
        self.df = pd.DataFrame()  # Khởi tạo DataFrame rỗng

        # Tạo menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Mở file", command=self.mo_file)
        self.file_menu.add_command(label="Lưu file", command=self.luu_file)
        
        # Tạo các nút chức năng
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)
        self.tong_quan_button = tk.Button(self.button_frame, text="Xem tổng quan", command=self.xem_tong_quan)
        self.tong_quan_button.pack(side=tk.LEFT)
        self.thong_ke_button = tk.Button(self.button_frame, text="Thống kê nắm giữ", command=self.thong_ke_nam_giu)
        self.thong_ke_button.pack(side=tk.LEFT)
        self.canh_bao_button = tk.Button(self.button_frame, text="Cảnh báo giá", command=self.canh_bao_gia)
        self.canh_bao_button.pack(side=tk.LEFT)
        self.phan_tich_button = tk.Button(self.button_frame, text="Phân tích lãi/lỗ", command=self.phan_tich_loi_lo)
        self.phan_tich_button.pack(side=tk.LEFT)
        self.them_giao_dich_button = tk.Button(self.button_frame, text="Thêm giao dịch", command=self.them_giao_dich)
        self.them_giao_dich_button.pack(side=tk.LEFT)
        self.xoa_giao_dich_button = tk.Button(self.button_frame, text="Xóa giao dịch", command=self.xoa_giao_dich)
        self.xoa_giao_dich_button.pack(side=tk.LEFT)

        # Tạo bảng hiển thị dữ liệu
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(expand=True, fill='both')

        # Tạo vùng hiển thị logo
        self.logo_frame = tk.Frame(self.root)
        self.logo_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.logo_label = tk.Label(self.logo_frame)
        self.logo_label.pack()

        # Gán sự kiện bàn phím
        self.root.bind("<Left>", self.xu_ly_phim)
        self.root.bind("<Right>", self.xu_ly_phim)

def mo_file(self):
    # Yêu cầu người dùng chọn file để mở
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if file_path:
        # Đọc dữ liệu từ file Excel
        self.df = pd.read_excel(file_path)
        # Hiển thị dữ liệu lên giao diện
        self.hien_thi_du_lieu()
        self.current_file_path = file_path  # Lưu lại đường dẫn file hiện tại


    def luu_file(self):
        # Lưu dữ liệu vào file Excel
        if hasattr(self, 'current_file_path'):
            self.df.to_excel(self.current_file_path, index=False)
            messagebox.showinfo("Lưu file", "Dữ liệu đã được lưu thành công!")
        else:
            messagebox.showerror("Lưu file", "Không có file nào được mở để lưu!")

    def hien_thi_du_lieu(self):
        # Đặt tên các cột cho bảng hiển thị
        self.tree["columns"] = list(self.df.columns)
        self.tree["show"] = "headings"
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        # Xóa dữ liệu cũ trong bảng
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Thêm dữ liệu mới vào bảng
        for index, row in self.df.iterrows():
            self.tree.insert("", index, values=list(row))
        # Gán sự kiện khi chọn một hàng trong bảng
        self.tree.bind("<ButtonRelease-1>", self.hien_logo_coin)

    def hien_logo_coin(self, event):
        # Lấy tên đồng coin từ hàng được chọn
        selected_item = self.tree.selection()[0]
        selected_market = self.tree.item(selected_item, "values")[1]
        selected_coin = selected_market.split('USDT')[0]  # Lấy tên đồng coin từ cặp giao dịch
        # URL để tải logo của đồng coin
        coin_logo_url = f"https://cryptoicons.org/api/icon/{selected_coin.lower()}/200"
        response = requests.get(coin_logo_url)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((100, 100), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)
        # Hiển thị logo lên giao diện
        self.logo_label.config(image=img_tk)
        self.logo_label.image = img_tk

    def xem_tong_quan(self):
        # Hiển thị thông báo tổng quan
        messagebox.showinfo("Tổng quan", f"Có tổng cộng {len(self.df)} giao dịch trong dữ liệu.")

    def thong_ke_nam_giu(self):
        # Thống kê số lượng nắm giữ của mỗi đồng coin
        buy_data = self.df[self.df['Type'].str.lower() == 'buy']
        sell_data = self.df[self.df['Type'].str.lower() == 'sell']
        thong_ke = buy_data.groupby('Market')['Amount'].sum() - sell_data.groupby('Market')['Amount'].sum()
        thong_ke_str = "\n".join([f"{market}: {quantity}" for market, quantity in thong_ke.items()])
        messagebox.showinfo("Thống kê nắm giữ", thong_ke_str)

    def canh_bao_gia(self):
        # Thiết lập cảnh báo giá cho đồng coin
        market = simpledialog.askstring("Cảnh báo giá", "Nhập tên cặp giao dịch (e.g., BTCUSDT):")
        gia_canh_bao = simpledialog.askfloat("Cảnh báo giá", "Nhập giá cảnh báo:")
        current_price = simpledialog.askfloat("Cảnh báo giá", f"Nhập giá hiện tại của {market}:")
        
        if current_price >= gia_canh_bao:
            messagebox.showinfo("Cảnh báo giá", f"Giá của {market} đã đạt mức cảnh báo {gia_canh_bao} USD!")
        else:
            messagebox.showinfo("Cảnh báo giá", f"Giá của {market} chưa đạt mức cảnh báo {gia_canh_bao} USD.")

    def phan_tich_loi_lo(self):
        # Phân tích lãi/lỗ theo thời gian
        market = simpledialog.askstring("Phân tích lãi/lỗ", "Nhập tên cặp giao dịch (e.g., BTCUSDT):")
        gia_hien_tai = simpledialog.askfloat("Phân tích lãi/lỗ", f"Nhập giá hiện tại của {market}:")
        
        # Lọc dữ liệu theo cặp giao dịch
        market_data = self.df[self.df['Market'] == market]
        market_data['Date(UTC)'] = pd.to_datetime(market_data['Date(UTC)'])
        market_data = market_data.sort_values('Date(UTC)')
        market_data['Cumulative Amount'] = market_data.apply(lambda x: x['Amount'] if x['Type'].lower() == 'buy' else -x['Amount'], axis=1).cumsum()
        market_data['Current Value'] = market_data['Cumulative Amount'] * gia_hien_tai
        
        # Vẽ biểu đồ
        plt.figure(figsize=(10, 6))
        plt.plot(market_data['Date(UTC)'], market_data['Current Value'], marker='o')
        plt.title(f'Biểu đồ lãi/lỗ của {market} theo thời gian')
        plt.xlabel('Ngày')
        plt.ylabel('Giá trị hiện tại (USD)')
        plt.grid(True)
        plt.show()

    def them_giao_dich(self):
        # Thêm giao dịch mới
        ngay_giao_dich = simpledialog.askstring("Thêm giao dịch", "Nhập ngày giao dịch (yyyy-mm-dd):")
        market = simpledialog.askstring("Thêm giao dịch", "Nhập tên cặp giao dịch (e.g., BTCUSDT):")
        loai_giao_dich = simpledialog.askstring("Thêm giao dịch", "Nhập loại giao dịch (buy/sell):")
        so_luong = simpledialog.askfloat("Thêm giao dịch", "Nhập số lượng:")
        gia = simpledialog.askfloat("Thêm giao dịch", "Nhập giá (USD):")
        tong = so_luong * gia
        phi = simpledialog.askfloat("Thêm giao dịch", "Nhập phí (USD):")
        phi_coin = simpledialog.askstring("Thêm giao dịch", "Nhập loại coin phí (e.g., BNB):")

        # Thêm giao dịch mới vào DataFrame
        new_data = pd.DataFrame([[ngay_giao_dich, market, loai_giao_dich, gia, so_luong, tong, phi, phi_coin]], columns=self.df.columns)
        self.df = pd.concat([self.df, new_data], ignore_index=True)
        
        # Cập nhật bảng hiển thị
        self.hien_thi_du_lieu()

    def xoa_giao_dich(self):
        # Xóa giao dịch được chọn
        selected_item = self.tree.selection()
        if selected_item:
            for item in selected_item:
                index = self.tree.index(item)
                self.df = self.df.drop(index).reset_index(drop=True)
            self.hien_thi_du_lieu()
            messagebox.showinfo("Xóa giao dịch", "Giao dịch đã được xóa.")
        else:
            messagebox.showwarning("Xóa giao dịch", "Vui lòng chọn giao dịch cần xóa.")

    def xu_ly_phim(self, event):
        if event.keysym == "Left":
            print("Phím Left được nhấn")
        elif event.keysym == "Right":
            print("Phím Right được nhấn")

if __name__ == "__main__":
    root = tk.Tk()
    app = GiaoDienChuongTrinh(root)
    root.mainloop()
