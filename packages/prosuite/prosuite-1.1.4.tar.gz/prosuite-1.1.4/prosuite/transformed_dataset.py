from prosuite.dataset import BaseDataset
from prosuite.parameter import Parameter
from prosuite.model import Model
from typing import List


class TransformedDataset(BaseDataset):
    def __init__(self, name: str, filter_expression: str = ""):
        super().__init__(name, filter_expression)

        #:
        self.parameters: List[Parameter] = []
