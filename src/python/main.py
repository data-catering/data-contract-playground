from typing import Any, Dict
import yaml
from datacontract.export.exporter_factory import exporter_factory
from datacontract.imports.odcs_v3_importer import import_models, import_terms, import_servicelevels, import_odcs_v3_from_str
from datacontract.lint import resolve
from datacontract.model.data_contract_specification import DataContractSpecification
from datacontract.model.exceptions import DataContractException
from pyscript import document, window
from pyweb import pydom

from src.python.common import set_options, set_editor_mode, input_option_id_prefix, output_option_id_prefix
from src.python.model import MyInfo, OdcsDetails, DataContractSpecDetails, AvroDetails, AvroIdlDetails, BigQueryDetails, \
    DbmlDetails, DbtDetails, DbtSourcesDetails, DbtStagingSqlDetails, GoDetails, GreatExpectationsDetails, HtmlDetails, \
    JsonSchemaDetails, ProtobufDetails, PydanticModelDetails, RdfDetails, SodaClDetails, SparkDetails, SqlDetails, \
    SqlQueryDetails, SqlAlchemyDetails, TerraformDetails, DataContractSpec, DataCatererDetails

convert_output_type = pydom["#convert-output-type"][0]
ace = window.ace
editor_input = ace.edit("input-yaml")
editor_output = ace.edit("output-text")

input_details = [OdcsDetails(), DataContractSpecDetails()]
output_details = [
    AvroDetails(), AvroIdlDetails(), BigQueryDetails(), DataCatererDetails(), DbmlDetails(), DbtDetails(), DbtSourcesDetails(),
    DbtStagingSqlDetails(), GoDetails(), GreatExpectationsDetails(), HtmlDetails(), JsonSchemaDetails(),
    OdcsDetails(), ProtobufDetails(), PydanticModelDetails(), RdfDetails(), SodaClDetails(), SparkDetails(),
    SqlDetails(), SqlQueryDetails(), SqlAlchemyDetails(), TerraformDetails()
]

data_contract_examples = {}
input_select_element = document.getElementById("convert-input-type")
output_select_element = document.getElementById("convert-output-type")


def from_data_contract(data_contract: DataContractSpecification):
    dict_input = data_contract.dict(exclude_defaults=True, exclude_none=True)
    return DataContractSpec(**dict_input)


def init_select_options():
    set_options(input_details, input_select_element, input_option_id_prefix, editor_input)
    set_options(output_details, output_select_element, output_option_id_prefix, editor_output)


def export_to_output_type(e):
    input_type = input_select_element.value
    input_option = document.getElementById(f"{input_option_id_prefix}{input_type}")
    if input_option.getAttribute("is_import") == "true":
        # then need to import to data contract spec first then export
        converted_input = import_to_data_contract(input_type, editor_input.getValue())
    else:
        converted_input = resolve.resolve_data_contract(data_contract_str=editor_input.getValue(), schema_location="datacontract/schemas/datacontract-1.1.0.schema.json")

    # data_contract = resolve.resolve_data_contract(data_contract_str=input_value)
    contract_with_yaml = from_data_contract(converted_input)

    export_result = exporter_factory.create(convert_output_type.value).export(
        data_contract=contract_with_yaml,
        model="all",
        server=None,
        sql_server_type="postgres",  # TODO make this dynamic from input field
        export_args={}
    )
    
    # Handle dictionary results (like protobuf) vs direct string results
    if isinstance(export_result, dict):
        # For protobuf and potentially other formats that return a dict
        output_content = export_result.get(convert_output_type.value, '')
    else:
        # For formats that return a string directly
        output_content = export_result
        
    editor_output.session.setValue(output_content)
    # based on the output type, change the editor_output mode
    set_editor_mode(output_option_id_prefix, convert_output_type.value, editor_output)


def import_to_data_contract(import_type, input_value):
    if import_type == "odcs":
        data_contract = import_odcs(input_value)
    else:
        data_contract = input_value
    return data_contract


def import_info(odcs_contract: Dict[str, Any]) -> MyInfo:
    info = MyInfo()

    info.title = odcs_contract.get("name") if odcs_contract.get("name") is not None else "My contract title"

    if odcs_contract.get("version") is not None:
        info.version = odcs_contract.get("version")

    # odcs.description.purpose => datacontract.description
    if odcs_contract.get("description") is not None and odcs_contract.get("description").get("purpose") is not None:
        info.description = odcs_contract.get("description").get("purpose")

    # odcs.domain => datacontract.owner
    if odcs_contract.get("domain") is not None:
        info.owner = odcs_contract.get("domain")

    # add dataProduct as custom property
    if odcs_contract.get("dataProduct") is not None:
        info.dataProduct = odcs_contract.get("dataProduct")

    # add tenant as custom property
    if odcs_contract.get("tenant") is not None:
        info.tenant = odcs_contract.get("tenant")

    return info


def import_odcs(source: str) -> DataContractSpecification:
    data_contract_specification = DataContractSpecification(info=MyInfo())
    data_contract_specification.dataContractSpecification = "1.1.0"
    # data_contract_specification = import_odcs_v3_from_str(data_contract_specification, source)

    try:
        odcs_contract = yaml.safe_load(source)

    except Exception as e:
        raise DataContractException(
            type="schema",
            name="Parse ODCS contract",
            reason=f"Failed to parse odcs contract from {source}",
            engine="datacontract",
            original_exception=e,
        )

    # print(odcs_contract)
    odcs_contract["dataProduct"] = None
    odcs_contract["tenant"] = None
    odcs_contract["schema"][0]["quality"] = None
    odcs_contract["schema"][0]["properties"][2]["quality"] = None
    odcs_contract["schema"][0]["properties"][1]["nullable"] = False
    data_contract_specification.id = odcs_contract["id"]
    data_contract_specification.info = import_info(odcs_contract)
    data_contract_specification.terms = import_terms(odcs_contract)
    data_contract_specification.servicelevels = import_servicelevels(odcs_contract)
    data_contract_specification.models = import_models(odcs_contract)

    return data_contract_specification


init_select_options()
