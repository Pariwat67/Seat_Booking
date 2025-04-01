
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import simpledialog
from tabulate import tabulate


class Seat:
    def __init__(self, seat_number):
        self.seat_number = seat_number
        self.is_booked = False
        self.student_id = None
        self.student_name = None

    def book(self, student_id, student_name):
        if not self.is_booked:
            self.is_booked = True
            self.student_id = student_id
            self.student_name = student_name
            return True
        return False

    def cancel(self):
        if self.is_booked:
            self.is_booked = False
            self.student_id = None
            self.student_name = None
            return True
        return False

    def get_display_data(self):
        return [self.seat_number, "ว่าง" if not self.is_booked else f"{self.student_id} - {self.student_name}"]


class Booking:
    def __init__(self, total_seats=25):
        self.seats = [Seat(i + 1) for i in range(total_seats)]

    def get_seat_display(self):
        return [seat.get_display_data() for seat in self.seats]

    def book_seat(self, seat_number, student_id, student_name):
        if 1 <= seat_number <= len(self.seats):
            if self.seats[seat_number - 1].book(student_id, student_name):
                return True
        return False

    def cancel_seat(self, seat_number):
        if 1 <= seat_number <= len(self.seats):
            if self.seats[seat_number - 1].cancel():
                return True
        return False


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ระบบจองที่นั่งสอบ")
        self.geometry("600x600")
        self.config(bg="#87CEEB")  # สีฟ้า (SkyBlue) สำหรับพื้นหลัง

        self.booking_system = Booking()

        # Create header
        self.header_frame = tk.Frame(self, bg="#4caf50", bd=5)
        self.header_frame.pack(fill="x")
        self.header_label = tk.Label(self.header_frame, text="ระบบจองที่นั่งสอบ", font=("Helvetica", 18, "bold"), fg="white", bg="#4caf50")
        self.header_label.pack(padx=20, pady=10)

        # Create buttons with modern style
        self.create_button("แสดงที่นั่งทั้งหมด", self.show_seats)
        self.create_button("จองที่นั่ง", self.book_seat)
        self.create_button("ยกเลิกการจองที่นั่ง", self.cancel_seat)
        self.create_button("ออกจากโปรแกรม", self.quit)

        # Create Treeview for seat display
        self.tree = ttk.Treeview(self, columns=("Seat Number", "Status"), show="headings", height=10)
        self.tree.heading("Seat Number", text="หมายเลขที่นั่ง")
        self.tree.heading("Status", text="สถานะ")
        self.tree.column("Seat Number", width=100, anchor="center")
        self.tree.column("Status", width=300, anchor="center")

        self.tree.pack(pady=20, padx=20, fill="both", expand=True)

    def create_button(self, text, command):
        button = ttk.Button(self, text=text, command=command, style="TButton")
        button.pack(pady=10, fill="x", padx=40)

    def show_seats(self):
        # Clear the current Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        seats_data = self.booking_system.get_seat_display()
        for seat_data in seats_data:
            seat_number, status = seat_data
            # Adding colored rows
            if status == "ว่าง":
                self.tree.insert("", "end", values=(seat_number, status), tags=("available",))
            else:
                self.tree.insert("", "end", values=(seat_number, status), tags=("booked",))

        # Add style for the tags
        self.tree.tag_configure("available", background="#A3D4FC")  # สีฟ้าอ่อน
        self.tree.tag_configure("booked", background="#FFD54F")  # สีเหลือง

    def book_seat(self):
        seat_number = int(simpledialog.askstring("จองที่นั่ง", "กรอกหมายเลขที่นั่ง:"))
        student_id = simpledialog.askstring("จองที่นั่ง", "กรอกรหัสนักศึกษา:")
        student_name = simpledialog.askstring("จองที่นั่ง", "กรอกชื่อนักศึกษา:")

        if self.booking_system.book_seat(seat_number, student_id, student_name):
            messagebox.showinfo("สำเร็จ", f"จองที่นั่ง {seat_number} สำเร็จ")
            self.show_seats()  # อัปเดตตาราง
        else:
            messagebox.showerror("ผิดพลาด", "ที่นั่งถูกจองไปแล้วหรือหมายเลขที่นั่งไม่ถูกต้อง")

    def cancel_seat(self):
        seat_number = int(simpledialog.askstring("ยกเลิกการจอง", "กรอกหมายเลขที่นั่งที่ต้องการยกเลิก:"))

        if self.booking_system.cancel_seat(seat_number):
            messagebox.showinfo("สำเร็จ", f"ยกเลิกที่นั่ง {seat_number} เรียบร้อย")
            self.show_seats()  # อัปเดตตาราง
        else:
            messagebox.showerror("ผิดพลาด", "ที่นั่งนี้ยังไม่มีการจองหรือหมายเลขที่นั่งไม่ถูกต้อง")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
