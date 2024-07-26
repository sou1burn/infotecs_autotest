import unittest
import subprocess
import time
import requests
import numpy
from requests import HTTPError
import random
"""from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/run', methods=['GET', 'POST'])
def run_exe():
    if request.method == 'POST':
        try:
            result = subprocess.run(['C:/Users/spike/PycharmProjects/infotecs_autotest'], capture_output=True, text=True)
            return jsonify({'output' : result.stdout, 'error' : result.stderr}), 200
        except Exception as e:
            return jsonify({'Error' : result.stderr}), 500
    return jsonify({'message' : 'Send a post request to run'}), 200
"""

#Максимальное и минимальное значение диапазона допустимых чисел
int_min = numpy.iinfo(numpy.int32).min
int_max = numpy.iinfo(numpy.int32).max
#Базовый хост и порт для подключения к серверу через API
base_host = "127.0.0.1"
default_port = "17678"
#Лямбда-функция для подключения по другим хосту и порту
base_url = lambda host, port: f"http://{host}:{port}/api"
#Заполнение массива для тестов с различными числами
num_tests = 5
test_values = [(random.randint(int_min - 100, int_max + 100000000), random.randint(int_min - 100, int_max + 100)) for _ in range(num_tests)]
for_test_code_3 = 12,3
for_test_code_4 = int_max + 100

errors = {
    1: "Ошибка вычисления",
    2: "Не хватает ключей в теле запроса",
    3: "Одно из значений не является целым числом",
    4: "Превышен размер одного из значений",
    5: "Неправильный формат тела запроса"
}
#Функция подключения к серверу
def start_server(host = base_host, port = default_port):
    proc = subprocess.Popen(['webcalculator.exe', 'start', host, str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    return proc

#Функция выключения сервера
def shut_server(process):
    process.terminate()
    process.wait()

#Проверка ответа
def check_response(expected_status_code, response, expected_body):
    assert expected_status_code == response.status_code
    if response.status_code == 200:
        assert response.json() == expected_body
    else:
        raise AssertionError(f'Error: {response.status_code} - {response.text}')

#Проверка состояния сервера
def state_test(host, port):
    response = requests.get(f'{base_url(host, port)}/state')
    check_response(200, response, response.json())
    print(response.json())
    return response.json()

#Тест для сложения чисел
def add_test(x, y, host, port):
    try:
         response = requests.post(f'{base_url(host, port)}/addition', json={'x' : x, 'y' : y})
         if response.status_code == 200:
             check_response(200, response, response.json())
             print(response.json())
             return response.json()
         else:
             handle_error(response)
    except HTTPError as e:
        raise AssertionError(f"Error: {e.response.json()}")
    print(response.text)


#Тест для умножения чисел
def mult_test(x, y, host, port):
    try:
        response = requests.post(f'{base_url(host, port)}/multiplication', json={'x' : x, 'y' : y})
        if response.status_code == 200:
            check_response(200, response, response.json())
            print(response.json())
            return response.json()
        else:
            handle_error(response)
    except HTTPError as e:
        raise AssertionError(f"Error: {e.response.json()}")
    print(response.text)

#Тест для деления чисел нацело
def division_test(x, y, host, port):
    try:
        response = requests.post(f'{base_url(host, port)}/division', json={'x' : x, 'y' : y})
        if response.status_code == 200:
            check_response(200, response, response.json())
            print(response.json())
            return response.json()
        else:
            handle_error(response)
    except HTTPError as e:
        raise AssertionError(f"Error: {e.response.json()}")
    print(response.text)

#Тест для деления чисел с остатком
def remainder_test(x, y, host, port):
    try:
        response = requests.post(f'{base_url(host, port)}/remainder', json={'x' : x, 'y' : y})
        if response.status_code == 200:
            check_response(200, response, response.json())
            print(response.json())
            return response.json()
        else:
            handle_error(response)
    except HTTPError as e:
        raise AssertionError(f"Error: {e.response.json()}")
    print(response.text)

#Отлов ошибок
def handle_error(response):
    error_code = response.json().get('statusCode')
    error_msg = errors.get(error_code, "Error")
    raise AssertionError(f"Error occured: {error_code} - {error_msg}")

#Тесты для определения правильности приходящих кодов ошибок
def wrong_add_test(x, y, host, port):
    try:
         response = requests.post(f'{base_url(host, port)}/addition', json={'x' : x})
         if response.status_code == 200:
             check_response(200, response, response.json())
             print(response.json())
             return response.json()
         else:
             handle_error(response)
    except HTTPError as e:
        raise AssertionError(f"Error: {e.response.json()}")
    print(response.text)

def wrong_add_test_2(x, y, host, port):
    try:
         response = requests.post(f'{base_url(host, port)}/add', json={'x' : x, 'y': y})
         if response.status_code == 200:
             check_response(200, response, response.json())
             print(response.json())
             return response.json()
         else:
             handle_error(response)
    except HTTPError as e:
        raise AssertionError(f"Error: {e.response.json()}")
    print(response.text)


#Класс с реализованными тестами
class TestCases(unittest.TestCase):

    def test_start_server(self):
        start_server()
        print("Server started succesfully")

    def test_shut_server(self):
        shut_server(start_server())
        print("Server shut succesfully")

    def test_state(self):
        result = state_test(base_host, default_port)
        self.assertEqual(result, {'statusCode': 0, 'state': 'OК'})

    def test_add(self):
        for num1,num2 in test_values:
            if (num1 > int_max or num1 < int_min or num2 > int_max or num2 < int_min):
                raise AssertionError(
                    "Numbers outside of range: please enter numbers between -2147483648 and 2147483647")
            print(f"\nFirst num: {num1}, second: {num2}\n")
            result = add_test(num1, num2, base_host, default_port)
            if result['statusCode'] == 0:
                self.assertEqual(result['result'], num1 + num2)
            elif result['statusCode'] in errors:
                handle_error(result)
            else:
                pass


    def test_mul(self):
        for num1, num2 in test_values:
            if (num1 > int_max or num1 < int_min or num2 > int_max or num2 < int_min):
                raise AssertionError(
                    "Numbers outside of range: please enter numbers between -2147483648 and 2147483647")
            print(f"\nFirst num: {num1}, second: {num2}\n")
            result = mult_test(num1, num2, base_host, default_port)
            if result['statusCode'] == 0:
                self.assertEqual(result['result'], num1 * num2)
            elif result['statusCode'] in errors:
                handle_error(result)
            else:
                pass

    def test_div(self):
        for num1, num2 in test_values:
            if (num1 > int_max or num1 < int_min or num2 > int_max or num2 < int_min):
                raise AssertionError(
                    "Numbers outside of range: please enter numbers between -2147483648 and 2147483647")
            print(f"\nFirst num: {num1}, second: {num2}\n")
            result = division_test(num1, num2, base_host, default_port)
            if num2 == 0:
                self.assertEqual(result, {'statusCode': 1, 'statusMessage': 'Ошибка вычисления'})
            elif result['statusCode'] in errors:
                handle_error(result)
            else:
                self.assertEqual(result, {'statusCode': 0, 'result': num1 // num2})



    def test_rem(self):
        for num1, num2 in test_values:
            if (num1 > int_max or num1 < int_min or num2 > int_max or num2 < int_min):
                raise AssertionError(
                    "Numbers outside of range: please enter numbers between -2147483648 and 2147483647")
            print(f"\nFirst num: {num1}, second: {num2}\n")
            result = remainder_test(num1, num2, base_host, default_port)
            if num2 == 0:
                self.assertEqual(result, {'statusCode': 1, 'statusMessage': 'Ошибка вычисления'})
            elif result['statusCode'] in errors:
                handle_error(result)
            else:
                self.assertEqual(result, {'statusCode': 0, 'result': num1 % num2})

    def test_negative_answer_code_1(self):
        for num1, num2 in test_values:
            if (num1 > int_max or num1 < int_min or num2 > int_max or num2 < int_min):
                raise AssertionError(
                    "Numbers outside of range: please enter numbers between -2147483648 and 2147483647")
            print(f"\nFirst num: {num1}, second: {num2}\n")
            result = remainder_test(num1, num2, base_host, default_port)
            if num2 == 0:
                self.assertEqual(result, {'statusCode': 1, 'statusMessage': 'Ошибка вычисления'})
            elif result['statusCode'] in errors:
                handle_error(result)
            else:
                self.assertEqual(result, {'statusCode': 0, 'result': num1 % num2})


    def test_negative_answer_code_2(self):
        for num1, num2 in test_values:
            if (num1 > int_max or num1 < int_min or num2 > int_max or num2 < int_min):
                raise AssertionError(
                    "Numbers outside of range: please enter numbers between -2147483648 and 2147483647")
            print(f"\nFirst num: {num1}, second: {num2}\n")
            result = wrong_add_test(num1, num2, base_host, default_port)
            if result['statusCode'] == 0:
                self.assertEqual(result['result'], num1 + num2)
            elif result['statusCode'] in errors:
                handle_error(result)
            else:
                pass

    def test_negative_answer_code_3(self):
        for num1, num2 in test_values:
            if (num1 > int_max or num1 < int_min or num2 > int_max or num2 < int_min):
                raise AssertionError(
                    "Numbers outside of range: please enter numbers between -2147483648 and 2147483647")
        print(f"\nFirst num: {num1}, second: {num2}\n")
        result = add_test(num1, for_test_code_3, base_host, default_port)
        if result['statusCode'] == 0:
            self.assertEqual(result['result'], num1 + num2)
        elif result['statusCode'] in errors:
            handle_error(result)
        else:
            pass

    def test_negative_answer_code_4(self):
        for num1, num2 in test_values:
            print(f"\nFirst num: {num1}, second: {num2}\n")
            result = add_test(num1, for_test_code_4, base_host, default_port)
            if result['statusCode'] == 0:
                self.assertEqual(result['result'], num1 + num2)
            elif result['statusCode'] in errors:
                handle_error(result)
            else:
                pass

    def test_negative_answer_code_5(self):
        for num1, num2 in test_values:
            if (num1 > int_max or num1 < int_min or num2 > int_max or num2 < int_min):
                raise AssertionError(
                    "Numbers outside of range: please enter numbers between -2147483648 and 2147483647")
            print(f"\nFirst num: {num1}, second: {num2}\n")
            result = wrong_add_test_2(num1, num2, base_host, default_port)
            if result['statusCode'] == 0:
                self.assertEqual(result['result'], num1 + num2)
            elif result['statusCode'] in errors:
                handle_error(result)
            else:
                pass


    def test_change_host_port(self):
        new_host = "127.0.0.2"
        new_port = "17679"
        shut_server(start_server())
        proc = start_server(new_host, new_port)
        result = state_test(new_host, new_port)
        self.assertEqual(result, {'statusCode': 0, 'state': "OK"})
        shut_server(proc)
        process = start_server(base_host, default_port)

    def test_restart_server(self):
        shut_server(start_server(base_host, default_port))
        proc = start_server()
        result = state_test(base_host, default_port)
        self.assertEqual(result, {'statusCode': 0, 'state': "OK"})

#Запуск тестов с записью результата в файл
if __name__ == "__main__":
        unittest.main()

#division_test(1536558937, -1171856429)