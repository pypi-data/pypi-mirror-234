import json

global_error_msg = "Something went wrong!"

class JsonModelData:
    def __init__(self, _model_name: str, _model_architecure, 
                 _model_optimizer, _model_training_data): 
        self._model_name = _model_name
        self._model_architecture = _model_architecure
        self._model_optimizer = _model_optimizer
        self._model_training_data = _model_training_data

    def set_model_state_dict(self):
        try:
            return self
        except:
            return None

    def set_model_optimizer(self):
        try:
            for var_name in self._model_optimizer:
                model_optimizer = self._model_optimizer[var_name]
                return model_optimizer
        except:
            return None

    def set_model_training_data(self):
        try:
            training_data = self._model_training_data
            return training_data
        except:
            return None

    def save_model_data(self):
            if self._model_name == "":
                raise ValueError("model_name param and file_path cannot be null")
            else:
                json_model_data = JsonModelData(self._model_name, self._model_architecture, 
                                                self._model_optimizer, self._model_training_data)
                __parse_model_data(json_model_data)

    def print_saved_model_data(self) -> bool:
        print(f"---------------------------------")
        print(f"\n--- Model Name: {self._model_name}")
        print(f"\n--- Model Architecture: {self._model_architecture}")
        print(f"\n--- Model Optimizer: {self._model_optimizer}")
        print(f"\n--- Model Traing Data: {self._model_training_data}")
        print(f"---------------------------------")

        return True

"""
Parses model architecture & model op
from a pytorch model to this json file: "model_data.json"
"""
def __parse_model_data(json_model_data: JsonModelData):
    model_data = {
            json_model_data._model_name: {
                "model_architecure": str(json_model_data._model_architecture),
                "model_optimizer": json_model_data._model_optimizer,
                "model_training_data": json_model_data._model_training_data,
                }
            }

    with open("json_data/json_model_data.json", "w+") as write_file:
        json.dump(model_data, write_file, indent=2)
