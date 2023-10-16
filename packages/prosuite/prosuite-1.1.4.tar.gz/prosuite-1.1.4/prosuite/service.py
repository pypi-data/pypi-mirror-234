import os
from typing import Union, Iterable
from prosuite.condition import Condition
from prosuite.perimeter import EnvelopePerimeter, EsriShapePerimeter, WkbPerimeter
from prosuite.parameter import Parameter
from prosuite.transformed_dataset import TransformedDataset
from prosuite.xml_specification import XmlSpecification
from prosuite.specification import Specification
from prosuite.verification_parameters import VerificationParameters
from prosuite.advanced_parameters import AdvancedParameters
import prosuite.generated.quality_verification_service_pb2 as service_util
import prosuite.generated.quality_verification_service_pb2_grpc as qa_service
import prosuite.generated.shared_qa_pb2 as shared_qa
import prosuite.generated.shared_types_pb2 as shared_types
from prosuite.verification_response import VerificationResponse
import grpc
import logging
import sys

from prosuite.dataset import Dataset

MAX_MESSAGE_LENGTH_MB = 1024

class Service:
    """
    The service class communicates on the http/2 channel with the server and initiates the 
    quality verifications.

    :param host_name: The name or IP address of the host running the quality verification service.
    :type host_name: str
    :param port_nr: The port used by the quality verification service.
    :type port_nr: int
    :param channel_credentials: The channel credentials to be used for TLS/SSL server 
        authentication, if required by the server (Default: None -> No TLS/SSL).

        Use :py:meth:`prosuite.utils.get_ssl_channel_credentials` to create the basic https 
        credentials if the appropria root certificates are in the windows certificate store.
        For advanced scenarios or credentials on a non-windows platform, see the gRPC Python docs
        (https://grpc.github.io/grpc/python/grpc.html).
    :type channel_credentials: grpc.ChannelCredentials  
    """

    ISSUE_GDB = "Issues.gdb"
    """The name of the issue File Geodatabase. 
        It will be written to the output_dir specified in the :py:meth:`prosuite.service.Service.verify` 
        method. This File Geodatabase contains the issues found during the verification and could 
        be used as the source for the Issue Worklist in the ProSuite QA Add-In for ArcGIS Pro.
    """

    XML_REPORT = "verification.xml"
    """The name of the xml verification report.
        It will be written to the output_dir specified in the :py:meth:`prosuite.service.Service.verify` 
        method.
    """

    HTML_REPORT = "verification.html"
    """The name of the html verification report.
        It will be written to the output_dir specified in the :py:meth:`prosuite.service.Service.verify` 
        method.
    """

    def __init__(self, host_name: str, port_nr: int, channel_credentials: grpc.ssl_channel_credentials = None):
        #:
        self.host_name = host_name
        """The host name.

        :meta private:
        """
        #:
        self.port_nr = port_nr
        """The port.

        :meta private:
        """
        #:
        self.ssl_channel_credentials: grpc.ssl_channel_credentials = channel_credentials
        """The TLS/SSL credentials.

        :meta private:
        """

    def verify(self, specification: Union[Specification, XmlSpecification],
               perimeter: Union[EnvelopePerimeter, EsriShapePerimeter, WkbPerimeter] = None, 
               output_dir: str = None, 
               parameters: VerificationParameters = None) -> Iterable[VerificationResponse]:
        """
        Executes a quality verification by running all the quality conditions defined in the 
        provided quality specification.
        Returns a collection of VerificationResponse objects, containing the verification
        messages.

        Please refer to the :ref:`samples <samples-link>` for more details.

        :param specification: The quality specification containing the conditions to be verified.
            It can be either a :py:class:`prosuite.specification.Specification` directly defined in 
            python code or a :py:class:`prosuite.xml_specification.XmlSpecification` from an XML 
            file, for example created by the XML export in the ProSuite Data Dictionary Editor.
        :param perimeter: The perimeter that defines the polygon or extent of the verification.
            Default: None -> Full extent of the verified datasets.
        :param output_dir: The output directory (must be writable / creatable by the service process).
            Default: No output is written by the server process.
        :param parameters: Additional optional verification parameters.
        :return: Iterator for looping over VerificationResponse objects. The verification response
            contains progress information, found issues and, in the final message, the verification results.
        :rtype: Iterator[VerificationResponse]
        """

        advanced_parameters = AdvancedParameters(
            specification, output_dir, perimeter, parameters)

        self._validate_params(advanced_parameters)

        channel = self._create_channel()

        client = qa_service.QualityVerificationGrpcStub(channel)

        request = self._create_request(advanced_parameters)

        for response_msg in client.VerifyStandaloneXml(request):
            yield VerificationResponse(
                message=response_msg.message.message,
                service_call_status=response_msg.service_call_status,
                message_level=response_msg.message.message_level
            )

    def _create_request(self, parameters: AdvancedParameters):
        if isinstance(parameters.specification, XmlSpecification):
            request = self._compile_xml_request(parameters)
        else:
            request = self._compile_request(parameters)
        return request

    def _create_channel(self):
        message_length = MAX_MESSAGE_LENGTH_MB * 1024 * 1024
        options=[('grpc.max_send_message_length', message_length),
                 ('grpc.max_receive_message_length', message_length)]
        
        if self.ssl_channel_credentials:
            channel = self._create_secure_channel(options)
        else:
            channel = grpc.insecure_channel(f'{self.host_name}:{self.port_nr}', options)
        return channel

    def _validate_params(self, params: AdvancedParameters):
        if params.output_dir is None:
            params.output_dir = ""            
            logging.warn("No output dir is defined")
        if params.specification is None:
            raise Exception(
                "No specification is defined. Please assign verification.specification.")

    def _compile_xml_request(self, parameters: AdvancedParameters):
        if not parameters.specification.specification_name:
            raise Exception(
                "The specification to be used is not defined. Please define XmlSpecification.specification_name")
        req = service_util.StandaloneVerificationRequest()
        req.output_directory = parameters.output_dir
        self._configure_verification_parameter_msg(req.parameters, parameters)
        self._configure_xml_quality_specification_msg(
            req.xml_specification, parameters.specification)
        return req

    def _compile_request(self, parameters: AdvancedParameters):
        req = service_util.StandaloneVerificationRequest()
        req.output_directory = parameters.output_dir
        self._configure_verification_parameter_msg(req.parameters, parameters)
        self._configure_condition_list_specification_msg(
            req.condition_list_specification, parameters.specification)
        return req

    def _create_secure_channel(self, options) -> grpc.Channel:
        channel = grpc.secure_channel(
            f'{self.host_name}:{self.port_nr}', self.ssl_channel_credentials, options)
        try:
            grpc.channel_ready_future(channel).result(timeout=5)
            logging.info(
                f'Successfully established secure channel to {self.host_name}')
        except:
            logging.exception(
                f'Timeout. Failed to establish secure channel to {self.host_name}')
        return channel

    def _configure_xml_quality_specification_msg(self, xml_specification_msg: shared_qa.XmlQualitySpecificationMsg, specification: XmlSpecification):
        xml_specification_msg.xml = specification.xml_string
        xml_specification_msg.selected_specification_name = specification.specification_name
        if specification.data_source_replacements:
            xml_specification_msg.data_source_replacements.extend(
                specification.data_source_replacements)
        return xml_specification_msg

    def _configure_condition_list_specification_msg(self,
                                                    cond_list_spec_msg: shared_qa.ConditionListSpecificationMsg, specification: Specification):
        cond_list_spec_msg.name = specification.name
        cond_list_spec_msg.description = specification.description
        for condition in specification.get_conditions():
            cond_list_spec_msg.elements.append(
                self._to_xml_quality_specification_element_msg(condition))

        data_sources = self._get_data_sources(specification)

        for key, value in data_sources.items():
            data_source_msg = shared_qa.DataSourceMsg()
            data_source_msg.id = key
            data_source_msg.model_name = key
            data_source_msg.catalog_path = value
            cond_list_spec_msg.data_sources.append(data_source_msg)

        return cond_list_spec_msg

    def _configure_shape_msg(self, shape_msg: shared_types.ShapeMsg, perimeter: Union[EnvelopePerimeter, WkbPerimeter, EsriShapePerimeter]):
        if isinstance(perimeter, EnvelopePerimeter):
            perimeter: EnvelopePerimeter
            shape_msg.envelope.x_min = perimeter.x_min
            shape_msg.envelope.x_max = perimeter.x_max
            shape_msg.envelope.y_min = perimeter.y_min
            shape_msg.envelope.y_max = perimeter.y_max
        if isinstance(perimeter, EsriShapePerimeter):
            perimeter: EsriShapePerimeter
            shape_msg.esri_shape = perimeter.esri_shape
        if isinstance(perimeter, WkbPerimeter):
            perimeter: WkbPerimeter
            shape_msg.wkb = bytes(perimeter.wkb)

    def _to_xml_quality_specification_element_msg(self, condition: Condition):
        spec_element = shared_qa.QualitySpecificationElementMsg()
        self._configure_quality_condition_msg(
            condition, spec_element.condition)
        spec_element.allow_errors = condition.allow_errors
        spec_element.category_name = condition.category
        # other props
        return spec_element

    def _configure_verification_parameter_msg(self, params_msg: shared_qa.VerificationParametersMsg, parameters: AdvancedParameters):
        params_msg.tile_size = parameters.tile_size
        params_msg.issue_file_gdb_path = os.path.join(
            parameters.output_dir, Service.ISSUE_GDB)
        params_msg.html_report_path = os.path.join(
            parameters.output_dir, Service.HTML_REPORT)
        params_msg.verification_report_path = os.path.join(
            parameters.output_dir, Service.XML_REPORT)
        if parameters.perimeter:
            self._configure_shape_msg(
                params_msg.perimeter, parameters.perimeter)

    def _configure_quality_condition_msg(self, condition: Condition, condition_msg: shared_qa.QualityConditionMsg):
        condition_msg.name = condition.name
        condition_msg.test_descriptor_name = condition.test_descriptor
        condition_msg.description = condition.description
        condition_msg.url = condition.url
        for param in condition.parameters:
            if param.contains_list_of_datasets:
                self._handle_dataset_list(condition_msg, param)
            else:
                condition_msg.parameters.append(self._to_parameter_mgs(param))

    def _handle_dataset_list(self, condition_msg: shared_qa.QualityConditionMsg, param: Parameter):
        """
        a Parameter value can be of type Dataset. Or it can be of type list[Dataset].
        if it is a Dataset list, each Dataset in the list should be treated as single Parameter
        """
        if param.contains_list_of_datasets:
            # in this case, param.dataset is actually a list of datasets. we need to unpack the list and create
            # single params for each dataset in the list
            if Parameter.value_is_list_of_datasets(param.dataset):
                for parameter in param.dataset:
                    ds_param = Parameter(param.name, parameter)
                    condition_msg.parameters.append(
                        self._to_parameter_mgs(ds_param))

    @staticmethod
    def _to_parameter_mgs(param: Parameter):
        param_msg = shared_qa.ParameterMsg()
        param_msg.name = param.name

        if isinstance(param.value, TransformedDataset):
            # handle transformed dataset here
            param_msg.where_clause = Service._none_to_emtpy_str(
                param.get_where_clause())
        else:
            param_msg.value = Service._none_to_emtpy_str(
                param.get_string_value())
            param_msg.where_clause = Service._none_to_emtpy_str(
                param.get_where_clause())
            param_msg.workspace_id = param.get_workspace_id()
            param_msg.used_as_reference_data = False

        return param_msg

    @staticmethod
    def _none_to_emtpy_str(value) -> str:
        if value is None:
            return ""
        return value

    def _get_data_sources(self, specification: Specification) -> dict:
        result = {}
        for condition in specification.get_conditions():
            for parameter in condition.parameters:
                if parameter.is_dataset_parameter():
                    if parameter.contains_list_of_datasets:
                        for dataset in parameter.dataset:
                            model = dataset.model
                            result[model.name] = model.catalog_path
                        pass
                    else:
                        model = parameter.dataset.model
                        result[model.name] = model.catalog_path
        return result
