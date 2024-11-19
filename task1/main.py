from parser_row import yaml_to_json
if __name__ == "__main__":
    with open('C://Users/denict/PycharmProjects/LabsAndEdu/Labs_inf/lab_inf_4/data/input.yml', 'r', encoding='utf-8') as input_yaml:
        string_yaml = input_yaml.read()
        output_string = yaml_to_json(string_yaml)
    with open('C://Users/denict/PycharmProjects/LabsAndEdu/Labs_inf/lab_inf_4/data/out1_row.json', 'w', encoding="utf-8") as file_json:
        file_json.write(output_string)