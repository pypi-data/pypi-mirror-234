from typing import Union
from prosuite.perimeter import EnvelopePerimeter, EsriShapePerimeter, WkbPerimeter
from prosuite.verification_parameters import VerificationParameters
from prosuite.specification import Specification
from prosuite.xml_specification import XmlSpecification


class AdvancedParameters(VerificationParameters):
    def __init__(self, specification, output_dir, perimeter, verification_params: VerificationParameters = None) -> None:

        self.specification:  Union[Specification,
                                   XmlSpecification] = specification
        self.perimeter: Union[EnvelopePerimeter,
                              EsriShapePerimeter, WkbPerimeter] = perimeter
        self.output_dir: str = output_dir
        self.tile_size: int = 5000
        self.user_name: str = None
        if (verification_params):
            self.tile_size = verification_params.tile_size
            self.user_name = verification_params.user_name
