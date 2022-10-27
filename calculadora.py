from tkinter import *
from tkinter import ttk
from sys import platform
from math import gcd


class Calculator:
    def __init__(self) -> None:
        self.root = Tk(className="Calculator")
        self.root.resizable(False, False)
        self.mainframe = ttk.Frame(self.root)

        # Buffer contains current user input
        # Sub buffer trace user input
        self.buffer = StringVar(self.mainframe)
        self.sub_buffer = StringVar(self.mainframe)
        self.eval_buffer = ""

        self.result = ttk.Label(
            self.mainframe,
            textvariable=self.buffer,
        )
        self.sub_result = ttk.Label(
            self.mainframe,
            textvariable=self.sub_buffer,
        )

        self.last_operator = ""

        # Latches drives the main logic of calculator correctness
        self.equal_latch = False
        self.dot_latch = False
        self.function_latch = False

        self.setStyles()
        self.createWidgets()
        self.setKeybindings()
        self.layoutWidgets()

    def createWidgets(self):
        self.operators = ["+", "-", "x", "/", "x²", "x³"]
        self.function_keys = ["M", "Me", "LCM", "GCD"]
        self.special_keys = {
            "C": self.clear,
            "CE": self.cleanBuffer,
            "=": self.equal,
            "←": self.backspace,
            "⁺/-": self.sign,
            ".": self.dot,
            ",": self.comma,
            "?": self.help,
        }
        self.buttons = {}

        if not platform.startswith("win32"):
            # Numeric buttons 0-9
            for i in range(10):
                self.buttons[i] = ttk.Button(
                    self.mainframe,
                    text=str(i),
                    command=lambda x=str(i): self.putNumber(x),
                    style="Dracula1.TButton",
                )
            # Operators
            for operator in self.operators:
                self.buttons[operator] = ttk.Button(
                    self.mainframe,
                    text=operator,
                    command=lambda op=operator: self.putOperator(op),
                    style="Dracula2.TButton",
                )
            # Function keys:
            for function in self.function_keys:
                self.buttons[function] = ttk.Button(
                    self.mainframe,
                    text=function,
                    command=lambda op=function: self.putFunction(op),
                    style="Dracula4.TButton",
                )
            # Special keys
            for key in self.special_keys:
                self.buttons[key] = ttk.Button(
                    self.mainframe,
                    text=key,
                    command=lambda func=self.special_keys[key]: func(),
                    style="Dracula3.TButton",
                )
        else:
            for i in range(10):
                self.buttons[i] = Button(
                    self.mainframe,
                    text=str(i),
                    command=lambda x=str(i): self.putNumber(x),
                    **self.style_button_common,
                    **self.style_button_dracula1
                )
            # Operators
            for operator in self.operators:
                self.buttons[operator] = Button(
                    self.mainframe,
                    text=operator,
                    command=lambda op=operator: self.putOperator(op),
                    **self.style_button_common,
                    **self.style_button_dracula2
                )
            # Function keys:
            for function in self.function_keys:
                self.buttons[function] = Button(
                    self.mainframe,
                    text=function,
                    command=lambda op=function: self.putFunction(op),
                    **self.style_button_common,
                    **self.style_button_dracula4
                )
            # Special keys
            for key in self.special_keys:
                self.buttons[key] = Button(
                    self.mainframe,
                    text=key,
                    command=lambda func=self.special_keys[key]: func(),
                    **self.style_button_common,
                    **self.style_button_dracula3
                )

    def layoutWidgets(self):
        # Is a bunch of boilerplate code, but is necessary
        button_common = {"padx": 1, "pady": 1, "sticky": N + S + E + W}
        self.mainframe.grid()
        self.result.grid(row=1, column=0, columnspan=4, sticky=E + W)
        self.sub_result.grid(row=0, column=0, columnspan=4, sticky=E + W)

        # First we place all numeric buttons but 0
        for i in range(1, 10):
            self.buttons[i].grid(
                row=7 - (i - 1) // 3,
                column=(i - 1) % 3,
                padx=1,
                pady=1,
                sticky=N + S + W + E,
            )
        self.buttons[0].grid(row=8, column=1, **button_common)

        # Operators
        self.buttons["+"].grid(row=7, column=3, **button_common)
        self.buttons["-"].grid(row=6, column=3, **button_common)
        self.buttons["x"].grid(row=5, column=3, **button_common)
        self.buttons["/"].grid(row=4, column=3, **button_common)
        self.buttons["x²"].grid(row=4, column=2, **button_common)
        self.buttons["x³"].grid(row=4, column=1, **button_common)

        # Special keys
        self.buttons["="].grid(row=8, column=3, **button_common)
        self.buttons["C"].grid(row=2, column=2, **button_common)
        self.buttons["CE"].grid(row=2, column=1, **button_common)
        self.buttons["←"].grid(row=2, column=3, **button_common)
        self.buttons["⁺/-"].grid(row=8, column=0, **button_common)
        self.buttons["."].grid(row=8, column=2, **button_common)
        self.buttons[","].grid(row=4, column=0, **button_common)
        self.buttons["?"].grid(row=2, column=0, **button_common)

        # Function keys
        self.buttons["M"].grid(row=3, column=0, **button_common)
        self.buttons["Me"].grid(row=3, column=1, **button_common)
        self.buttons["LCM"].grid(row=3, column=2, **button_common)
        self.buttons["GCD"].grid(row=3, column=3, **button_common)

    def setStyles(self):
        if platform.startswith("win32"):
            self.__setStylesWin32()
        else:
            self.__setStyles()
        
    def __setStyles(self):
        style_common = {
            "background": "#282A36",
            "font": "Arial 12",
            "relief": FLAT,
            "overrelief": FLAT,
            "height": 2,
        }
        # Style based on Dracula colorscheme
        self.style = ttk.Style()
        self.style.configure("Dracula1.TFrame", background="#4D4D4D")
        self.style.configure("TkDefault.TButton", background="#282a36")
        self.style.configure(
            "Dracula1.TButton",
            **style_common,
            foreground="#9AEDFE",
        )
        self.style.configure(
            "Dracula2.TButton",
            **style_common,
            foreground="#50FA7B",
        )
        self.style.configure(
            "Dracula3.TButton",
            **style_common,
            foreground="#CAA9FA",
        )
        self.style.configure(
            "Dracula4.TButton",
            **style_common,
            foreground="#F1FA8C",
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
            foreground="gray",
            background="#282A36",
            font="Arial 12",
            anchor=E,
        )
        self.style.map(
            "Dracula1.TButton",
            background=[("pressed", "#9AEDFE"), ("active", "#9AEDFE")],
            foreground=[("pressed", "white"), ("active", "white")],
        )
        self.style.map(
            "Dracula2.TButton",
            background=[("pressed", "#50FA7B"), ("active", "#50FA7B")],
            foreground=[("pressed", "white"), ("active", "white")],
        )
        self.style.map(
            "Dracula3.TButton",
            background=[("pressed", "#CAA9FA"), ("active", "#CAA9FA")],
            foreground=[("pressed", "white"), ("active", "white")],
        )
        self.style.map(
            "Dracula4.TButton",
            background=[("pressed", "#F1FA8C"), ("active", "#F1FA8C")],
            foreground=[("pressed", "white"), ("active", "white")],
        )

        self.mainframe.configure(style="Dracula1.TFrame")
        self.result.configure(style="Dracula1.TLabel")
        self.sub_result.configure(style="Dracula2.TLabel")

    def __setStylesWin32(self):
        self.style_button_common = {
            "background": "#282A36",
            "font": "Arial 14",
            "height": 2,
            "width": 5,
            "borderwidth": 0,
            "relief": FLAT,
            "activeforeground": "white",
            "highlightbackground": "#282A36",
            "highlightcolor": "blue",
        }
        self.style_button_dracula1 = {
            "foreground": "#9AEDFE",
            "activebackground": "#9AEDFE",
        }
        self.style_button_dracula2 = {
            "foreground": "#50FA7B",
            "activebackground": "#50FA7B",
        }
        self.style_button_dracula3 = {
            "foreground": "#CAA9FA",
            "activebackground": "#CAA9FA",
        }
        self.style_button_dracula4 = {
            "foreground": "#F1FA8C",
            "activebackground": "#F1FA8C",
        }
        self.style = ttk.Style()
        self.style.configure(
            "Dracula1.TLabel",
            foreground="white",
            background="#282A36",
            font="Arial 18",
            anchor=E,
        )
        self.style.configure(
            "Dracula2.TLabel",
            foreground="gray",
            background="#282A36",
            font="Arial 14",
            anchor=E,
        )
        self.style.configure(
            "Dracula1.TFrame", background="#4D4D4D", foreground="#4D4D4D"
        )
        self.mainframe.configure(style="Dracula1.TFrame")
        self.result.configure(style="Dracula1.TLabel")
        self.sub_result.configure(style="Dracula2.TLabel")

    def setKeybindings(self):
        for i in range(10):
            self.root.bind(str(i), lambda event, x=str(i): self.putNumber(x))
            self.root.bind(
                "<KP_" + str(i) + ">", lambda event, x=str(i): self.putNumber(x)
            )

        self.root.bind("+", lambda event: self.buttons["+"].invoke())
        self.root.bind("-", lambda event: self.buttons["-"].invoke())
        self.root.bind("*", lambda event: self.buttons["x"].invoke())
        self.root.bind("/", lambda event: self.buttons["/"].invoke())
        self.root.bind("<KP_Add>", lambda event: self.buttons["+"].invoke())
        self.root.bind("<KP_Subtract>", lambda event: self.buttons["-"].invoke())
        self.root.bind("<KP_Multiply>", lambda event: self.buttons["x"].invoke())
        self.root.bind("<KP_Divide>", lambda event: self.buttons["/"].invoke())

        self.root.bind(".", lambda event: self.buttons["."].invoke())
        self.root.bind("<KP_Decimal>", lambda event: self.buttons["."].invoke())
        self.root.bind(",", lambda event: self.buttons[","].invoke())

        self.root.bind("<Return>", lambda event: self.buttons["="].invoke())
        self.root.bind("<KP_Enter>", lambda event: self.buttons["="].invoke())
        self.root.bind("<BackSpace>", lambda event: self.backspace())
        self.root.bind("<Delete>", lambda event: self.clear())

    def putNumber(self, number: str):
        # After get a result, we need make some cleanup
        if self.equal_latch:
            self.clear()
            self.equal_latch = False

        if self.isUnary(self.last_operator):
            return

        sz = len(self.buffer.get())
        input_limit = 5
        if not (sz == input_limit or (number == "0" and sz == 0)):
            self.buffer.set(self.buffer.get() + number)

    def putFunction(self, function: str):
        functions = {
            "M": self.mean,
            "Me": self.median,
            "LCM": self.LCM,
            "GCD": self.GCD,
        }
        temp = ""

        # Same cleanup, but we store the result as function first argument
        if self.equal_latch:
            temp = self.buffer.get()
            self.clear()
            self.equal_latch = False

        # For simplicity, I avoid function nesting
        if len(self.buffer.get()) > 0 or len(self.sub_buffer.get()) > 0:
            return

        self.function_latch = True

        if len(temp) != 0:
            self.sub_buffer.set(functions[function].__name__ + "(" + temp + ",")
            self.eval_buffer = "self." + functions[function].__name__ + "(" + temp + ","
        else:
            self.sub_buffer.set(functions[function].__name__ + "(")
            self.eval_buffer = "self." + functions[function].__name__ + "("

    def GCD(self, *args):
        return gcd(*args)

    def backspace(self):
        temp = self.buffer.get()
        if temp and temp[-1] == ".":
            self.dot_latch = False

        if len(temp) == 2 and temp[0] == "-":
            self.buffer.set("")
        else:
            self.buffer.set(temp[0:-1])

    def isUnary(self, operator: str):
        self.unary_operators = ("²", "³")
        return operator in self.unary_operators

    def dot(self):
        if self.dot_latch or not self.buffer.get():
            return
        self.buffer.set(self.buffer.get() + ".")
        self.dot_latch = True

    def comma(self):
        # Comma is only usen to separate function args
        if not self.function_latch:
            return

        if len(self.buffer.get()) == 0 and not self.isUnary(self.last_operator):
            return

        temp = self.sub_buffer.get()
        # For first argumnet and operators we put comma on right side, otherwise to left side
        if temp[-1] == "(" or temp[-1] not in range(10):
            temp += self.buffer.get() + ","
            self.eval_buffer += self.buffer.get() + ","
        else:
            temp += "," + self.buffer.get()
            self.eval_buffer += "," + self.eval_buffer
        self.sub_buffer.set(temp)
        self.buffer.set("")
        self.dot_latch = False
        self.last_operator = ","

    def sign(self):
        temp = self.buffer.get()
        if not temp:
            return

        if temp[0] == "-":
            temp = temp[1:]
        else:
            temp = "-" + temp
        self.buffer.set(temp)

    def putOperator(self, op: str):
        if len(self.buffer.get()) == 0 and not self.isUnary(self.last_operator):
            return

        # Allow result-operator chaining
        if self.equal_latch:
            self.sub_buffer.set("")
            self.eval_buffer = ""
            self.equal_latch = False

        if op == "x²":
            op = "²"
            true_op = "**2"
        elif op == "x³":
            op = "³"
            true_op = "**3"
        elif op == "x":
            true_op = "*"
        else:
            true_op = op

        temp = self.sub_buffer.get()
        self.last_operator = op
        self.sub_buffer.set(temp + self.buffer.get() + op)
        self.eval_buffer += self.buffer.get() + true_op
        self.buffer.set("")
        self.dot_latch = False

    def equal(self):
        # Prevent to press equal button twice
        if self.equal_latch:
            return

        if len(self.sub_buffer.get()) == 0 or (
            len(self.buffer.get()) == 0 and not self.isUnary(self.last_operator)
        ):
            return

        temp = self.sub_buffer.get() + self.buffer.get()
        self.eval_buffer += self.buffer.get()

        if self.function_latch:
            temp += ")"
            self.eval_buffer += ")"
        # if self.operator in ["x²","x³"]:
        #    self.rhs = int(self.buffer.get())
        self.buffer.set(str(round(eval(self.eval_buffer), 9)))
        self.sub_buffer.set(temp + "=")
        self.equal_latch = True
        self.dot_latch = True
        self.function_latch = False

    def clear(self):
        self.buffer.set("")
        self.sub_buffer.set("")
        self.eval_buffer = ""
        self.equal_latch = False
        self.dot_latch = False
        self.function_latch = False
        self.last_operator = ""

    def cleanBuffer(self):
        self.buffer.set("")
        self.dot_latch = False

    def mean(self, *args):
        if len(args) == 0:
            return 0
        ret = 0
        for arg in args:
            ret += arg
        return ret / len(args)

    def median(self, *args):
        if len(args) == 0:
            return 0
        size = len(args)
        if size % 2 == 0:
            return (args[(size - 1) // 2] + args[size // 2]) / 2
        else:
            return args[(size - 1) // 2]

    # TODO:Not implemented yet
    def LCM(self, *args):
        return len(args)

    def getResult(self):
        return float(self.buffer.get())

    def help(self):
        pass

    def display(self):
        self.root.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.display()
