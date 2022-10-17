from tkinter import *
from tkinter import ttk

class Calculator:
    def __init__(self) -> None:
        self.root = Tk(baseName="Calculadora")
        self.mainframe = ttk.Frame(self.root)

        #Buffer contains current user input 
        #Sub buffer trace user input
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

        #Latches drives the main logic of calculator correctness
        self.equal_latch = False
        self.dot_latch = False
        self.function_latch = False

        self.createWidgets()
        self.setStyle()
        self.layoutWidgets()

    def createWidgets(self):
        self.operators = ["+", "-", "x", "/", "x²", "x³"]
        self.function_keys = ["M","Me"]
        self.special_keys = {
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
        for operator in self.operators:
            self.buttons[operator] = ttk.Button(
                self.mainframe,
                text=operator,
                command=lambda op=operator: self.putOperator(op),
            )
        # Function keys:
        for function in self.function_keys:
            self.buttons[function] = ttk.Button(
                self.mainframe,
                text=function,
                command=lambda op=function: self.putFunction(op),
            )
        # Special keys
        for key in self.special_keys:
            self.buttons[key] = ttk.Button(
                self.mainframe, text=key, command=lambda func=self.special_keys[key]: func()
            )

    def layoutWidgets(self):
        #Is a bunch of boilerplate code, but is necessary
        self.mainframe.grid()

        self.result.grid(row=1, column=0, columnspan=4, sticky=E + W)
        self.sub_result.grid(row=0, column=0, columnspan=4, sticky=E + W)

        # First we place all numeric buttons but 0
        for i in range(1, 10):
            self.buttons[i].grid(
                row=6 - (i - 1) // 3, column=(i - 1) % 3, padx=1, pady=1,sticky=N+S+W+E
            )
        self.buttons[0].grid(row=7, column=1, padx=1, pady=1, sticky=N+S+E+W)

        # Operators
        self.buttons["+"].grid(row=6, column=3, padx=1, pady=1,sticky=N+S+E+W)
        self.buttons["-"].grid(row=5, column=3, padx=1, pady=1,sticky=N+S+E+W)
        self.buttons["x"].grid(row=4, column=3, padx=1, pady=1,sticky=N+S+E+W)
        self.buttons["/"].grid(row=3, column=3, padx=1, pady=1,sticky=N+S+E+W)
        self.buttons["x²"].grid(row=3, column=2, padx=1, pady=1,sticky=N+S+E+W)
        self.buttons["x³"].grid(row=3, column=1, padx=1, pady=1,sticky=N+S+E+W)

        # Special keys
        self.buttons["="].grid(row=7, column=3, padx=1, pady=1,sticky=N+S+E+W)
        self.buttons["C"].grid(row=2, column=2, padx=1, pady=1,sticky=N+S+E+W)
        self.buttons["CE"].grid(row=2, column=1, padx=1, pady=1,sticky=N+S+E+W)
        self.buttons["B"].grid(row=2, column=3, padx=1, pady=1,sticky=N+S+E+W)
        self.buttons["⁺/-"].grid(row=7, column=0, padx=1, pady=1,sticky=N+S+E+W)
        self.buttons["."].grid(row=7, column=2, padx=1, pady=1,sticky=N+S+E+W)
        self.buttons[","].grid(row=3, column=0, padx=1, pady=1,sticky=N+S+E+W)

        #Function keys
        self.buttons["M"].grid(row=2, column=0, padx=1, pady=1,sticky=N+S+E+W)
        self.buttons["Me"].grid(row=8, column=0, padx=1, pady=1,sticky=N+S+E+W)

    def setStyle(self):
        #Style based on Dracula colorscheme
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
            foreground="#50FA7B",
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
            "Dracula3.TButton",
            foreground="#CAA9FA",
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

        self.mainframe.configure(style="Dracula1.TFrame")
        self.result.configure(style="Dracula1.TLabel")
        self.sub_result.configure(style="Dracula2.TLabel")

        for i in range(10):
            self.buttons[i].configure(style="Dracula1.TButton")
        for operator in self.operators:
            self.buttons[operator].configure(style="Dracula2.TButton")
        for special_key in self.special_keys:
            self.buttons[special_key].configure(style="Dracula2.TButton")
        for function_key in self.function_keys:
            self.buttons[function_key].configure(style="Dracula2.TButton")
        self.buttons["B"].configure(style="Dracula2.TButton")
        self.buttons["="].configure(style="Dracula3.TButton")
        

    def putNumber(self, number: str):
        #After get a result, we need make some cleanup
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
        functions = {"M" : self.mean, "Me" : self.median}
        temp = ""

        #Same cleanup, but we store the result as function first argument
        if self.equal_latch:
            temp = self.buffer.get()
            self.clear()
            self.equal_latch = False

        #For simplicity, I avoid function nesting
        if len(self.buffer.get()) > 0 or len(self.sub_buffer.get()) > 0:
            return

        self.function_latch = True

        if (len(temp) != 0):
            self.sub_buffer.set("self."+functions[function].__name__ + "(" + temp + ",")
        else:
            self.sub_buffer.set("self."+functions[function].__name__ + "(")

    #Probably these functions exist in the standard library
    #But i implemented for educational purposes
    def mean(self,*args):
        if len(args) == 0:
            return 0
        ret = 0
        for arg in args:
            ret += arg
        return ret/len(args)

    def median(self,*args):
        if len(args) == 0:
            return 0
        size = len(args)
        if size % 2 == 0:
            return (args[(size-1)//2] + args[size//2]) / 2
        else:
            return args[(size-1)//2]

    def backspace(self):
        temp = self.buffer.get()
        if temp and temp[-1] == ".":
            self.dot_latch = False
        self.buffer.set(temp[0:-1])

    def isUnary(self, operator: str):
        self.unary_operators = ("x²", "x³")
        return operator in self.unary_operators

    def dot(self):
        if self.dot_latch:
            return
        self.buffer.set(self.buffer.get() + ".")
        self.dot_latch = True

    def comma(self):
        #Comma is only usen to separate function args
        if not self.function_latch:
            return

        if len(self.buffer.get()) == 0 and not self.isUnary(self.last_operator):
            return

        temp = self.sub_buffer.get()
        #For first argumnet and operators we put comma on right side, otherwise to left side
        if temp[-1] == "(" or temp[-1] not in range(10):
            temp += self.buffer.get() + ","
        else:
            temp += "," + self.buffer.get()
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

        #Allow result-operator chaining
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
        self.last_operator = op
        self.sub_buffer.set(temp + self.buffer.get() + true_op)
        self.buffer.set("")
        self.dot_latch = False

    def equal(self):
        #Prevent to press equal button twice
        if self.equal_latch:
            return

        if len(self.sub_buffer.get()) == 0 or (
            len(self.buffer.get()) == 0 and not self.isUnary(self.last_operator)
        ):
            return

        temp = self.sub_buffer.get() + self.buffer.get()
        
        if self.function_latch:
            temp += ")"
        # if self.operator in ["x²","x³"]:
        #    self.rhs = int(self.buffer.get())

        self.buffer.set(str(round(eval(temp), 9)))
        self.sub_buffer.set(temp + "=")
        self.equal_latch = True
        self.dot_latch = True
        self.function_latch = False

    def clear(self):
        self.buffer.set("")
        self.sub_buffer.set("")
        self.equal_latch = False
        self.dot_latch = False
        self.function_latch = False
        self.last_operator = ""

    def cleanBuffer(self):
        self.buffer.set("")
        self.dot_latch = False

    def display(self):
        self.root.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.display()
