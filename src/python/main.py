import yaml
from datacontract.export.exporter_factory import exporter_factory
from datacontract.imports.odcs_importer import import_info, import_models, import_terms, import_servicelevels
from datacontract.lint import resolve
from datacontract.model.data_contract_specification import DataContractSpecification
from datacontract.model.exceptions import DataContractException
from pyscript import document, window
from pyweb import pydom

from src.python.common import set_options, set_editor_mode, input_option_id_prefix, output_option_id_prefix
from src.python.model import OdcsDetails, DataContractSpecDetails, AvroDetails, AvroIdlDetails, BigQueryDetails, \
    DbmlDetails, DbtDetails, DbtSourcesDetails, DbtStagingSqlDetails, GoDetails, GreatExpectationsDetails, HtmlDetails, \
    JsonSchemaDetails, ProtobufDetails, PydanticModelDetails, RdfDetails, SodaClDetails, SparkDetails, SqlDetails, \
    SqlQueryDetails, TerraformDetails, DataContractSpec

convert_output_type = pydom["#convert-output-type"][0]
ace = window.ace
editor_input = ace.edit("input-yaml")
editor_output = ace.edit("output-text")

input_details = [OdcsDetails(), DataContractSpecDetails()]
output_details = [
    AvroDetails(), AvroIdlDetails(), BigQueryDetails(), DbmlDetails(), DbtDetails(), DbtSourcesDetails(),
    DbtStagingSqlDetails(), GoDetails(), GreatExpectationsDetails(), HtmlDetails(), JsonSchemaDetails(),
    OdcsDetails(), ProtobufDetails(), PydanticModelDetails(), RdfDetails(), SodaClDetails(), SparkDetails(),
    SqlDetails(), SqlQueryDetails(), TerraformDetails()
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
        # pydantic 2.x cannot be imported as a package due to https://pyodide.org/en/stable/usage/faq.html#micropip-can-t-find-a-pure-python-wheel
        dict_input = converted_input.dict(exclude_defaults=True, exclude_none=True)
        input_value = yaml.dump(dict_input, default_flow_style=False)
    else:
        input_value = editor_input.getValue()

    data_contract = resolve.resolve_data_contract(data_contract_str=input_value)
    contract_with_yaml = from_data_contract(data_contract)

    export_result = exporter_factory.create(convert_output_type.value).export(
        data_contract=contract_with_yaml,
        model="all",
        server=None,
        sql_server_type="postgres",  # TODO make this dynamic from input field
        export_args={}
    )
    editor_output.session.setValue(export_result)
    # based on the output type, change the editor_output mode
    set_editor_mode(output_option_id_prefix, convert_output_type.value, editor_output)


def import_to_data_contract(import_type, input_value):
    if import_type == "odcs":
        data_contract = import_odcs(input_value)
    else:
        data_contract = input_value
    return data_contract


def import_odcs(source: str) -> DataContractSpecification:
    data_contract_specification = resolve.resolve_data_contract(
        data_contract_location="https://datacontract.com/datacontract.init.yaml")

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

    data_contract_specification.id = odcs_contract["uuid"]
    data_contract_specification.info = import_info(odcs_contract)
    data_contract_specification.terms = import_terms(odcs_contract)
    data_contract_specification.servicelevels = import_servicelevels(odcs_contract)
    data_contract_specification.models = import_models(odcs_contract)

    return data_contract_specification


init_select_options()
