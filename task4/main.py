from parser import yaml_to_dict, from_dict_py_to_json

if __name__ == "__main__":
    with open('C://Users/denict/PycharmProjects/LabsAndEdu/Labs_inf/lab_inf_4/data/input.yml', 'r', encoding='utf-8') as file_yaml:
        yaml_string = file_yaml.read()

        dict_py = yaml_to_dict(yaml_string)
    with open('C://Users/denict/PycharmProjects/LabsAndEdu/Labs_inf/lab_inf_4/data/out4_parser.json', 'w', encoding="utf-8") as file_json:
        file_json.write(from_dict_py_to_json(dict_py))