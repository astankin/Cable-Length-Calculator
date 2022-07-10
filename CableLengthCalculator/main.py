from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno
import pandas as pd

data = pd.read_csv('cables_data.csv')

class CableLengthCalculator:



    def error_message(self):
        messagebox.showerror('Грешка', 'Моля въведете правилен артикулен номер!')

    def confirm(self, tara_weight):
        self.tara_weight = tara_weight
        self.answer = askyesno(title='Confirmation',
                          message=f'Теглото на макарата {int(self.tara_weight)} грама ли е?')
        return self.answer

    # =================== Calculation of the length ===============

    def calculation(self, tara_weight, total_weight, weight_per_meter):
        self.tara_weight = tara_weight
        self.total_weight = total_weight
        self.weight_per_meter = weight_per_meter
        if self.total_weight <= self.tara_weight:
            self.length_meters = 0
        else:
            self.length_meters = (self.total_weight - self.tara_weight) / self.weight_per_meter
        text = f"{float(self.length_meters):.2f}  m."
        if self.article_num != "":
            self.print_result.delete(0, END)
            self.print_result.insert(0, text)

    # =================== New Tara Weight Input ===============

    def tara_input(self):
        def calc():
            self.new_tara_weight = float(self.new_tara.get())
            self.calculation(self.new_tara_weight, total_weight, weight_per_meter)

        self.new_window = Toplevel(self.root)
        self.new_window.iconbitmap("icon.ico")
        self.new_window.title("Tегло на макарата")
        self.new_window.maxsize(400, 200)
        self.new_window.minsize(400, 200)

        self.frame2 = LabelFrame(self.new_window, width=382, height=120, font=('verdana', 10, 'bold'),
                                 borderwidth=3, relief=RIDGE, highlightthickness=4, bg="white", highlightcolor="white",
                                 highlightbackground="white", fg="#248aa2")
        self.frame2.place(x=8, y=8)

        self.tara_weight_label = Label(self.frame2, text="Моля въведете \n тегло на макарата:", font=('verdana', 10, 'bold'), bg="white")
        self.tara_weight_label.place(x=10, y=25)
        self.new_tara = Entry(self.frame2, width=16, borderwidth=2, relief=SUNKEN)
        self.new_tara.place(y=35, x=190)
        self.grams = Label(self.frame2, text="грама.", font=('verdana', 10, 'bold'), bg="white")
        self.grams.place(x=300, y=35)

        self.calc_button2 = Button(self.new_window, text="Изчисли", relief=RAISED, width=15, borderwidth=2,
                                   font=('verdana', 10, 'bold'), bg='#248aa2', fg="white", command=calc)
        self.calc_button2.place(x=90, y=150)

        self.close = Button(self.new_window, text="Затвори", relief=RAISED, width=15, borderwidth=2,
                                    font=('verdana', 10, 'bold'), bg='#248aa2', fg="white", command=self.new_window.destroy)
        self.close.place(x=240, y=150)

        self.new_window.mainloop()

    def save_info(self):
        global weight_per_meter
        global total_weight
        searched_item = self.article_num.get()
        if self.net_weight.get() != "":
            total_weight = float(self.net_weight.get())
        else:
            total_weight = 0
        if searched_item not in data.values:
            self.error_message()
        else:
            weight_per_meter = float(data[data["Article Number"] == searched_item]["Weight per one meter"])
            self.tara_weight = float(data[data["Article Number"] == searched_item]["Tara weight"])
            if not self.confirm(self.tara_weight):
                self.tara_input()
            self.calculation(float(self.tara_weight), float(total_weight), float(weight_per_meter))

    # =================== Clear Fields ===============

    def clear(self):
        self.article_num.delete(0, "end")
        self.net_weight.delete(0, "end")
        self.print_result.delete(0, "end")

    # ========== end ========================

    def __init__(self):
        self.root = Tk()
        self.root.eval("tk::PlaceWindow . center")
        self.root.title("Cable Length Calculator")
        self.root.iconbitmap("icon.ico")
        self.root.maxsize(500, 300)
        self.root.minsize(500, 300)

        self.heading = Label(self.root, text="Cable Length Calculator ", font=('verdana', 20, 'bold'), fg="#a40000")
        self.heading.place(x=60, y=5)

        self.frame1 = LabelFrame(self.root, width=482, height=190, font=('verdana', 10, 'bold'),
                                 borderwidth=3, relief=RIDGE, highlightthickness=4, bg="white", highlightcolor="white",
                                 highlightbackground="white", fg="#248aa2")
        self.frame1.place(x=8, y=50)

        self.article_num_label = Label(self.frame1, text="Артикулен номер:", font=('verdana', 10, 'bold'), bg="white")
        self.article_num_label.place(x=20, y=25)
        self.article_num = Entry(self.frame1, width=35, borderwidth=2, relief=SUNKEN)
        self.article_num.place(y=25, x=230)

        self.net_weight_label = Label(self.frame1, text="Нетно тегло:", font=('verdana', 10, 'bold'), bg="white")
        self.net_weight_label.place(x=20, y=70)
        self.net_weight = Entry(self.frame1, width=16, borderwidth=2, relief=SUNKEN)
        self.net_weight.place(y=70, x=230)
        self.grams = Label(self.frame1, text="грама.", font=('verdana', 10, 'bold'), bg="white")
        self.grams.place(x=340, y=70)

        self.print_result_label = Label(self.frame1, text="Дължината на кабела е:", font=('verdana', 10, 'bold'),
                                        bg="white")
        self.print_result_label.place(x=20, y=115)
        self.print_result = Entry(self.frame1, width=35, borderwidth=2, relief=SUNKEN)
        self.print_result.place(y=115, x=230)

        self.calc_button1 = Button(self.root, text="Изчисли", relief=RAISED, width=15, borderwidth=2,
                                      font=('verdana', 10, 'bold'), bg='#248aa2', fg="white", command=self.save_info)
        self.calc_button1.place(x=190, y=250)

        self.clear_button1 = Button(self.root, text="Clear", relief=RAISED, width=15, borderwidth=2,
                                   font=('verdana', 10, 'bold'), bg='#248aa2', fg="white", command=self.clear)
        self.clear_button1.place(x=340, y=250)

        self.root.mainloop()


if __name__ == '__main__':
    CableLengthCalculator()
