"""
2.	Создать собственный класс-исключение, обрабатывающий ситуацию деления на ноль. Проверить его работу на данных,
вводимых пользователем. При вводе нуля в качестве делителя программа должна корректно обработать эту ситуацию
и не завершиться с ошибкой.
"""
class MyException(Exception):

    def division_func(self, a, b):
        try:
            res = round(a / b, 2)
        except ZeroDivisionError:
            print(f"{a} / {b} -> на ноль делить нельзя!\n")
        else:
            print(f"{a} / {b} = {res} \n")


m_e = MyException()

m_e.division_func(5, 2)
m_e.division_func(6, 0)
m_e.division_func(4, 3)
m_e.division_func(0, 3)