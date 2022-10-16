from tkinter import *
from tkinter import ttk
from tkinter import font


class Calculator:
    def __init__(self) -> None:
        self.root = Tk()
        self.mainframe = ttk.Frame(self.root)

        self.buffer = StringVar(self.mainframe)
        self.sub_buffer = StringVar(self.mainframe)

        self.result = ttk.Label(
            self.mainframe,
            textvariable=self.buffer,
        )
        self.sub_result = ttk.Label(
            self.mainframe,
            textvariable=self.sub_buffer,
        )

        self.unary_operators = ("x²", "x³")
        self.operator = None
        self.accumulator = 0
        self.operand_list = []

        self.equal_latch = False

        self.createWidgets()
        self.setStyle()
        self.layoutWidgets()
    
    def createWidgets(self):
        operators = ["+","-","x","/","x²","x³"]
        special_keys = {"C": self.clear, "CE" : self.clear, "=" : self.equal, "B" : self.backspace, "⁺/-" : self.sign}
        self.buttons = []

        #Numeric buttons 0-9
        for i in range(10):
            self.buttons.append(ttk.Button(self.mainframe,text=str(i),command=lambda x=str(i): self.putNumber(x)))
        #Operators
        for operator in operators:
            self.buttons.append(ttk.Button(self.mainframe,text=operator,command=lambda op=operator: self.putOperator(op)))
        #Special keys
        for key in special_keys:
            self.buttons.append(ttk.Button(self.mainframe,text=key,command=lambda func=special_keys[key]: func()))
    
    def layoutWidgets(self):
        self.mainframe.grid()

        self.result.grid(row=1,column=0,columnspan=4)
        self.sub_result.grid(row=0,column=0,columnspan=4)
        for i in range(len(self.buttons)):
            self.buttons[i].grid(row=7-i//4,column=i%4,padx=1,pady=1)
            

    def setStyle(self):
        self.style = ttk.Style()
        self.style.configure(
            "Dracula1.TButton",
            foreground="#9AEDFE",
            background="#282A36",
            font="Arial 12",
            height=10,
            width=4,
            activeforeground="blue",
            borderwidth=3,
            relief=FLAT,
            overrelief=FLAT,
        )
        self.style.configure(
            "Dracula2.TButton",
            foreground="blue",
            background="black",
            font="Arial 12",
        )
        self.style.configure(
            "Dracula1.TLabel",
            foreground="black",
            background="white",
            font="Arial 16",
            width=20,
            anchor=E,
        )
        self.style.configure(
            "Dracula2.TLabel",
            foreground="white",
            background="black",
            font="Arial 12",
            width=20,
            anchor=E,
        )

        self.result.configure(style="Dracula1.TLabel")
        self.sub_result.configure(style="Dracula2.TLabel")
        for button in self.buttons:
            button.configure(style="Dracula1.TButton")

    def putNumber(self, number: str):
        if self.equal_latch:
            self.clear()
            self.equal_latch = False

        sz = len(self.buffer.get())

        if not (sz == 5 or (number == "0" and sz == 0)):
            self.buffer.set(self.buffer.get() + number)

    def backspace(self):
        self.buffer.set(self.buffer.get()[0:-1])

    def isUnary(self, operator: str):
        return operator in self.unary_operators


    def sign(self):
        temp = self.buffer.get()
        if len(temp) == 0:
            return

        if temp[0] == "-":
            temp = temp[1:]
        else:
            temp = "-" + temp
        self.buffer.set(temp)

    def putOperator(self, op: str):
        if len(self.buffer.get()) == 0:
            return

        if self.equal_latch:
            self.sub_buffer.set("")
            self.equal_latch = False

        if op == "x²":
            true_op = "**2"
        elif op == "x³":
            true_op = "**3"
        elif op == "x":
            true_op = "*"
        else:
            true_op = op

        temp = self.sub_buffer.get()
        self.operator = op
        if len(temp) != 0:
            self.sub_buffer.set(temp + self.buffer.get() + true_op)
        else:
            self.sub_buffer.set(self.buffer.get() + true_op)
        self.buffer.set("")

        # These are unaries operator, so we can execute it immediatly, like windows calculator
        #if self.operator in self.unary_operators:
        #    self.equal()

    def equal(self):
        if self.equal_latch:
            return

        if len(self.sub_buffer.get()) == 0 or (
            len(self.buffer.get()) == 0 and self.operator not in self.unary_operators
        ):
            return

        temp = self.sub_buffer.get() + self.buffer.get()

        #if self.operator in ["x²","x³"]:
        #    self.rhs = int(self.buffer.get())

        self.buffer.set(str(round(eval(temp), 9)))
        self.sub_buffer.set(temp + "=")
        self.equal_latch = True

    def clear(self):
        self.buffer.set("")
        self.sub_buffer.set("")
        self.equal_latch = False

    def display(self):
        self.root.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.display()
