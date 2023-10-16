from prosuite.dataset import Dataset


class Parameter:
    """
    A parameter configures a quality condition. Parameters can represent Datasets (dataset parameter) or scalar values
    (scalar parameters). Parameters have a name and a value.

    Dataset parameters: value is of type dataset. the parameter can retrieve the workspace id (model name) and the where
    clause (filter expression) of the dataset.

    Scalar parameters: value is a simple type (number, string, bool). .
    """
    def __init__(self, name: str, value):
        self.contains_list_of_datasets = False
        if self._value_type_is_dataset(value):
            self.dataset = value
        else:
            self.dataset = None

        self.name: str = name
        self.value = value

    def get_string_value(self) -> str:
        if self.dataset:
            if self.contains_list_of_datasets:
                return self.dataset[0].name
            else:
                return self.dataset.name
        else:
            if self.value is None:
                return ""
            else:
                return str(self.value)

    def is_dataset_parameter(self) -> bool:
        if self.dataset:
            return True
        else:
            return False

    def get_workspace_id(self):
        if not self.dataset:
            return ""
        return self.dataset.model.name

    def get_where_clause(self):
        if not self.dataset:
            return ""
        if self.contains_list_of_datasets:
            return self.dataset[0].filter_expression
        else:
            return self.dataset.filter_expression

    @staticmethod
    def value_is_list_of_datasets(value):
        if isinstance(value, list):
            if all(isinstance(x, Dataset) for x in value):
                return True
        return False

    def _value_type_is_dataset(self, value):
        if Parameter.value_is_list_of_datasets(value):
            self.contains_list_of_datasets = True
            return True
        if isinstance(value, Dataset):
            return True
        return False
