from tkinter import *
from tkinter import ttk


class Calculator:
    def __init__(self) -> None:
        self.root = Tk(baseName="Calculadora")
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
        self.operator = ""
        self.accumulator = 0
        self.operand_list = []

        self.equal_latch = False
        self.dot_latch = False

        self.createWidgets()
        self.setStyle()
        self.layoutWidgets()

    def createWidgets(self):
        operators = ["+", "-", "x", "/", "x²", "x³"]
        special_keys = {
            "C": self.clear,
            "CE": self.cleanBuffer,
            "=": self.equal,
            "B": self.backspace,
            "⁺/-": self.sign,
            ".": self.dot,
            ",": self.comma,
        }
        self.buttons = {}

        # Numeric buttons 0-9
        for i in range(10):
            self.buttons[i] = ttk.Button(
                self.mainframe, text=str(i), command=lambda x=str(i): self.putNumber(x)
            )
        # Operators
        for operator in operators:
            self.buttons[operator] = ttk.Button(
                self.mainframe,
                text=operator,
                command=lambda op=operator: self.putOperator(op),
            )
        # Special keys
        for key in special_keys:
            self.buttons[key] = ttk.Button(
                self.mainframe, text=key, command=lambda func=special_keys[key]: func()
            )

    def layoutWidgets(self):
        self.mainframe.grid()

        self.result.grid(row=1, column=0, columnspan=4, sticky=E + W)
        self.sub_result.grid(row=0, column=0, columnspan=4, sticky=E + W)

        # First we place all numeric buttons but 0
        for i in range(1, 10):
            self.buttons[i].grid(
                row=6 - (i - 1) // 3, column=(i - 1) % 3, padx=1, pady=1
            )
        self.buttons[0].grid(row=7, column=1, padx=1, pady=1)

        # Operators
        self.buttons["+"].grid(row=6, column=3, padx=1, pady=1)
        self.buttons["-"].grid(row=5, column=3, padx=1, pady=1)
        self.buttons["x"].grid(row=4, column=3, padx=1, pady=1)
        self.buttons["/"].grid(row=3, column=3, padx=1, pady=1)
        self.buttons["x²"].grid(row=3, column=2, padx=1, pady=1)
        self.buttons["x³"].grid(row=3, column=1, padx=1, pady=1)
        self.buttons[","].grid(row=7, column=2, padx=1, pady=1)
        self.buttons["."].grid(row=3, column=0, padx=1, pady=1)

        # Special keys
        self.buttons["="].grid(row=7, column=3, padx=1, pady=1)
        self.buttons["C"].grid(row=2, column=2, padx=1, pady=1)
        self.buttons["CE"].grid(row=2, column=1, padx=1, pady=1)
        self.buttons["B"].grid(row=2, column=3, padx=1, pady=1)
        self.buttons["⁺/-"].grid(row=7, column=0, padx=1, pady=1)

    #        for i in range(len(self.buttons)):
    #            self.buttons[i].grid(row=7-i//4,column=i%4,padx=1,pady=1)

    def setStyle(self):
        self.style = ttk.Style()
        self.style.configure("Dracula1.TFrame", background="#4D4D4D")
        self.style.configure(
            "Dracula1.TButton",
            foreground="#9AEDFE",
            background="#282A36",
            font="Arial 12",
            height=11,
            width=3,
            activeforeground="blue",
            borderwidth=3,
            relief=FLAT,
            overrelief=FLAT,
        )
        self.style.configure(
            "Dracula2.TButton",
            foreground="blue",
            background="#CAA9FA",
            font="Arial 12",
        )
        self.style.configure(
            "Dracula1.TLabel",
            foreground="white",
            background="#282A36",
            font="Arial 16",
            anchor=E,
        )
        self.style.configure(
            "Dracula2.TLabel",
            foreground="white",
            background="#282A36",
            font="Arial 12",
            anchor=E,
        )

        self.mainframe.configure(style="Dracula1.TFrame")
        self.result.configure(style="Dracula1.TLabel")
        self.sub_result.configure(style="Dracula2.TLabel")
        for button in self.buttons.values():
            button.configure(style="Dracula1.TButton")

    def putNumber(self, number: str):
        if self.equal_latch:
            self.clear()
            self.equal_latch = False

        sz = len(self.buffer.get())

        if self.isUnary(self.operator):
            return

        if not (sz == 5 or (number == "0" and sz == 0)):
            self.buffer.set(self.buffer.get() + number)

    def backspace(self):
        self.buffer.set(self.buffer.get()[0:-1])

    def isUnary(self, operator: str):
        return operator in self.unary_operators

    def dot(self):
        if self.dot_latch:
            return
        self.buffer.set(self.buffer.get() + ".")
        self.dot_latch = True

    def comma(self):
        pass

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
        if len(self.buffer.get()) == 0 and not self.isUnary(self.operator):
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

        self.dot_latch = False

    def equal(self):
        if self.equal_latch:
            return

        if len(self.sub_buffer.get()) == 0 or (
            len(self.buffer.get()) == 0 and self.operator not in self.unary_operators
        ):
            return

        temp = self.sub_buffer.get() + self.buffer.get()

        # if self.operator in ["x²","x³"]:
        #    self.rhs = int(self.buffer.get())

        self.buffer.set(str(round(eval(temp), 9)))
        self.sub_buffer.set(temp + "=")
        self.equal_latch = True

    def clear(self):
        self.buffer.set("")
        self.sub_buffer.set("")
        self.equal_latch = False

    def cleanBuffer(self):
        self.buffer.set("")

    def display(self):
        self.root.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.display()
