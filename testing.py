import calculadora
import unittest
import random

#I wont write more test for time purposes
#But could be interesting add more unit tests
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

    #This test tries calculartor's thougtness by pressing random buttons
    #Note: Is terrybly slow, also my pc is a potato
    def test_random(self):
        button_history = []
        buf = ""
        
        with open("logfile.txt","w") as logfile:
            #With range > 100000 my pc takes 6+ hours
            #Should be a way to improve this
            button_list = list(self.calc.buttons)
            for i in range(1,100):
                button_history.append(random.choice(button_list))
                buf += str(button_history[-1]) + " "
                self.calc.buttons[button_history[-1]].invoke()
                if i % 48 == 0:
                    buf += '\n'
            logfile.write(buf)



if __name__ == "__main__":
    unittest.main()