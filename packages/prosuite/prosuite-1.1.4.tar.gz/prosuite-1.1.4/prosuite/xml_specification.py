import typing
from typing import List
import prosuite.utils as utils


class XmlSpecification:
    """
    Represents a specification defined in the xml specification schema:

    :param specification_file: path to the xml specification file
    :type specification_file: str
    :param specification_name: name of the specification (in the xml file) that should be executed. If not defined in the constructor, it needs to be defined later.
    :type specification_name: str
    :param data_source_replacements: a list containing a list with two string elements. these represent a workspace id, and the path to the workspace
    :type data_source_replacements: [[str]] example: [["TLM_Production", "C:/temp/user@topgist.sde"]]
    """

    def __init__(self, specification_file: str, specification_name: str = None,
                 data_source_replacements: List[List[str]] = None):

        self.specification_name: str = None
        self.data_source_replacements = XmlSpecification._parse_datasource_replacements(data_source_replacements)
        self._specification_msg = None
        self.xml_string = XmlSpecification._read_file_as_string(specification_file)
        self.specification_file = specification_file
        self.specification_name = specification_name

    @staticmethod
    def _read_file_as_string(file_path) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
            return data

    @staticmethod
    def _parse_datasource_replacements(data_source_replacements: List[List[str]]):
        result = []
        for pair in data_source_replacements:
            result.append(f"{pair[0]}|{pair[1]}")
        return result

    @staticmethod
    def get_specification_names(specification_file: str) -> typing.List[str]:
        """
        Returns a list of the specification names of all specifications in all categories of the xml-specifications doc.

        :param specification_file: path of xml specification file.
        :type specification_file: str
        :return: List of specification names
        :rtype: [str]
        """
        specification_names = []
        xml = utils.objectify_xml(specification_file)
        for cat in xml.Categories:
            for qs in cat.Category.QualitySpecifications:
                name = utils.try_get_lxml_attrib(qs.QualitySpecification, 'name')
                if name:
                    specification_names.append(name)
        return specification_names
