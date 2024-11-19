import yaml
import json
def yaml_to_json_lib(yaml_string: str):
    dict_py = yaml.load(yaml_string, Loader=yaml.FullLoader)
    json_string = json.dumps(dict_py, ensure_ascii=False, indent=2)


# if __name__ == "__main__":
#     with open('C://Users/denict/PycharmProjects/LabsAndEdu/Labs_inf/lab_inf_4/data/input.yml', 'r',
#               encoding='utf-8') as file_yaml:
#         dict_py = yaml.load(file_yaml, Loader=yaml.FullLoader)
#     with open('C://Users/denict/PycharmProjects/LabsAndEdu/Labs_inf/lab_inf_4/data/out2_lib.json', 'w', encoding="utf-8") as file_json:
#         json.dump(dict_py, file_json, ensure_ascii=False, indent=2)