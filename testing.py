import calculadora
import unittest
import random

class calculatorTests(unittest.TestCase):
    def setUp(self):
        self.calc = calculadora.Calculator()

    def test_simple(self):
        self.calc.putNumber("2")
        self.calc.putOperator("+")
        self.calc.putNumber("2")
        self.calc.equal()
        self.assertEqual(self.calc.getResult(),4)

    def test_unary_operator(self):
        self.calc.putNumber("2")
        self.calc.putOperator("x³")
        self.calc.equal()
        self.assertEqual(self.calc.getResult(),8)

    def test_random(self):
        button_history = []
        buf = ""
        
        with open("logfile.txt","w") as logfile:
            for i in range(1,100000):
                button_history.append(random.choice(list(self.calc.buttons)))
                buf += str(button_history[-1]) + " "
                self.calc.buttons[button_history[-1]].invoke()
                if i % 48 == 0:
                    buf += '\n'
            logfile.write(buf)



if __name__ == "__main__":
    unittest.main()
