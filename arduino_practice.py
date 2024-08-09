import serial
import time
from tkinter import *
from tkinter import scrolledtext  

def read_data_from_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            numbers_str = line.split()
            numbers_int = [int(num) for num in numbers_str]
            data.append(numbers_int)
    return data

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Файл с путем {file_path} не был найден.")
    except IOError:
        print(f"Произошла ошибка во время чтения {file_path}.")

def create_list_of_lists(data_string):
    numbers = [int(num) for num in data_string.split()]
    return [numbers[i:i + 2] for i in range(0, len(numbers), 2)]

def compare_lists_element_by_element(list_file, list_arduino):
    result_message = ""
    errors = 0
    if len(list_file) != len(list_arduino):
        result_message = "Несовпадение наборов данных по длине"
        return result_message
    for sublist_file, sublist_arduino in zip(list_file, list_arduino):
        if sublist_file != sublist_arduino:
            result_message += f'Соединение некорректно - {sublist_file}, {sublist_arduino}\n'
            errors += 1 
    if errors == 0:
        result_message += 'Все соединения работают правильно'
    else:
        result_message += f'Число ошибок: {errors}\n'
    return result_message

def clear():
    txt.delete('1.0', END)
    txt_resume.delete('1.0', END)

def run_testing():
    try:
        ser = serial.Serial('COM3', 9600)
        lbl_port.configure(text = "Статус подключения - подключен (COM3)", background='green')
        time.sleep(2)    
        cycles = 0
        border = 42
        data_string = ""
        data_from_arduino_output = ""
        while cycles < 83:
            data = ser.readline().decode('utf-8')
            if cycles > border:
                data_from_arduino_output += data
            else:
                data_string += data
            time.sleep(0.1)
            cycles += 1    
            
        ser.close()
        txt.insert(INSERT, data_string)
        
        data_from_gui = create_list_of_lists(txt_pin_wire.get('1.0', END))
        data_from_arduino = create_list_of_lists(data_from_arduino_output)
        
        resume_message = compare_lists_element_by_element(data_from_gui, data_from_arduino)
        txt_resume.insert(INSERT, resume_message)
        lbl_port.configure(text = "Статус подключения - проверка \nзавершена (порт отключен)", background='gray')
        
    except:
        lbl_port.configure(text="Статус подключения - порт недоступен", background='red')

window = Tk()
window.title("Стенд по проверке проводов")  
window.geometry('1550x900')  
file_path = 'pin-wire-compliance.txt'

lbl_pin_wire = Label(window, text="Соответствия ПИН-ПРОВОД:")  
lbl_pin_wire.grid(column=0, row=2)  

btn_start = Button(window, text="Подключиться и начать проверку", command=run_testing)  
btn_start.grid(column=1, row=0) 

btn_clear = Button(window, text="Очистить поля вывода - X", command=clear) 
btn_clear.grid(column=2, row=2)

lbl_res = Label(window, text="Результат работы программы >>")  
lbl_res.grid(column=1, row=2)  

txt_pin_wire = scrolledtext.ScrolledText(window, width=24, height=46)  
txt_pin_wire.grid(column=0, row=3)
data_string = read_text_file(file_path)
txt_pin_wire.insert(INSERT, data_string)

txt_resume = scrolledtext.ScrolledText(window, width=43, height=46)  
txt_resume.grid(column=1, row=3) 

lbl_port = Label(window, text="Статус подключения - не подключен", background='red')  
lbl_port.grid(column=0, row=0)

txt = scrolledtext.ScrolledText(window, width=118, height=46)  
txt.grid(column=2, row=3) 

window.mainloop()