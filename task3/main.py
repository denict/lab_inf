from parser_regex import yaml_to_json_regex

if __name__ == "__main__":
    with open('C://Users/denict/PycharmProjects/LabsAndEdu/Labs_inf/lab_inf_4/data/input.yml', 'r', encoding='utf-8') as file_yaml:
        yaml_string = file_yaml.read()

        json_string = yaml_to_json_regex(yaml_string)
    with open('C://Users/denict/PycharmProjects/LabsAndEdu/Labs_inf/lab_inf_4/data/out3_regex.json', 'w', encoding="utf-8") as file_json:
        print(json_string, file=file_json)