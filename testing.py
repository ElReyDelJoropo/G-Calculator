import calculadora
import unittest
import random

# I wont write more test for time purposes
# But could be interesting add more unit tests
class calculatorTests(unittest.TestCase):
    def setUp(self):
        self.calc = calculadora.Calculator()

    def test_simple(self):
        self.calc.putNumber("2")
        self.calc.putOperator("+")
        self.calc.putNumber("2")
        self.calc.equal()
        self.assertEqual(self.calc.getResult(), 4)

    def test_mean(self):
        self.calc.putFunction("M")
        self.calc.putNumber("2")
        self.calc.comma()
        self.calc.putNumber("8")
        self.calc.putOperator("+")
        self.calc.putNumber("3")
        self.calc.sign()
        self.calc.equal()
        self.assertEqual(self.calc.getResult(), 3.5)

    def test_unary_operator(self):
        self.calc.putNumber("2")
        self.calc.putOperator("x³")
        self.calc.equal()
        self.assertEqual(self.calc.getResult(), 8)

    # This test tries calculartor's thougtness by pressing random buttons
    def test_random(self):
        button_history = []
        buf = ""
        button_list = list(self.calc.buttons)

        with open("logfile.txt", "w", encoding="utf-8") as logfile:
            # Calculator have a quirk with eval function when exceeds certarin amount number width
            # Should be a way to improve this
            # I dont fully understand python exception handling
            # In C++ things are much simpler
            for i in range(1, 100000):
                button_history.append(random.choice(button_list))
                buf += str(button_history[-1]) + " "
                if len(self.calc.eval_buffer) > 6:
                    self.calc.clear()
                self.calc.buttons[button_history[-1]].invoke()

                if i % 16 == 0:
                    buf += "\n"
            logfile.write(buf)


if __name__ == "__main__":
    unittest.main()
