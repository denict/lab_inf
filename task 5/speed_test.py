import time
from parser_row import yaml_to_json
from parser_lib import yaml_to_json_lib
from parser_regex import yaml_to_json_regex
from parser import yaml_to_dict, from_dict_py_to_json

# def test(f, string):
#     start_time = time.time()
#     for _ in range(100):
#         f(string)
#     return time.time() - start_time


with open('C://Users/denict/PycharmProjects/LabsAndEdu/Labs_inf/lab_inf_4/data/input.yml', 'r', encoding='utf-8') as f:
    data = f.read()
    start_time_row = time.time()
    for _ in range(100):
        yaml_to_json(data)
    print(f"Row parser: {time.time() - start_time_row} second")
    start_time_lib = time.time()
    for _ in range(100):
        yaml_to_json_lib(data)
    print(f"Lib parser: {time.time() - start_time_lib} second")

    start_time_regex = time.time()
    for _ in range(100):
        yaml_to_json_regex(data)
    print(f"Regex parser: {time.time() - start_time_regex} second")

    start_time_parser = time.time()
    for _ in range(100):
        from_dict_py_to_json(yaml_to_dict(data))
    print(f"My parser: {time.time() - start_time_parser} second")


