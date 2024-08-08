from typing import Dict, List

import yaml
from datacontract.export.exporter_factory import exporter_factory
from datacontract.imports.odcs_importer import import_info, import_models, import_terms, import_servicelevels
from datacontract.lint import resolve
from datacontract.model.data_contract_specification import DataContractSpecification
from datacontract.model.exceptions import DataContractException
from pyscript import document, window
from pyweb import pydom

convert_output_type = pydom["#convert-output-type"][0]
ace = window.ace
editor_input = ace.edit("input-yaml")
editor_output = ace.edit("output-text")


class OptionDetails:
    name: str = None
    display_name: str = None
    is_default: bool = False
    additional_opts: Dict[str, str] = {}


class InputDetails(OptionDetails):
    additional_opts = {"is_import": False}


class OdcsInputDetails(InputDetails):
    name = "odcs"
    display_name = "Open Data Contract Standard (ODCS)"
    is_default = True
    additional_opts = {"is_import": True}


class DataContractSpecInputDetails(InputDetails):
    name = "dataContractSpecification"
    display_name = "Data Contract Specification"


class OutputDetails(OptionDetails):
    additional_opts = {"editor_mode": "yaml"}


class AvroOutput(OutputDetails):
    name = "avro"
    display_name = "Avro"
    additional_opts = {"editor_mode": "json"}


class AvroIdlOutput(OutputDetails):
    name = "avro-idl"
    display_name = "Avro IDL"
    additional_opts = {
        "editor_mode": "json"}  # TODO AttributeError: 'DataContractSpecification' object has no attribute 'model_copy'


class BigQueryOutput(OutputDetails):
    name = "bigquery"
    display_name = "BigQuery"
    additional_opts = {
        "editor_mode": "sql"}  # TODO Export to bigquery requires selecting a bigquery server from the data contract.


class DbmlOutput(OutputDetails):
    name = "dbml"
    display_name = "DBML"  # TODO Module dbml could not be loaded


class DbtOutput(OutputDetails):
    name = "dbt"
    display_name = "DBT"


class DbtSourcesOutput(OutputDetails):
    name = "dbt-sources"
    display_name = "DBT Sources"


class DbtStagingSqlOutput(OutputDetails):
    name = "dbt-staging-sql"
    display_name = "DBT Staging SQL"
    additional_opts = {"editor_mode": "sql"}


class GoOutput(OutputDetails):
    name = "go"
    display_name = "Go"
    additional_opts = {"editor_mode": "go"}  # TODO doesn't seem to use go mode


class GreatExpectationsOutput(OutputDetails):
    name = "great-expectations"
    display_name = "Great Expectations"
    additional_opts = {"editor_mode": "json"}


class HtmlOutput(OutputDetails):
    name = "html"
    display_name = "HTML"
    additional_opts = {"editor_mode": "html"}  # TODO Module html could not be loaded


class JsonSchemaOutput(OutputDetails):
    name = "jsonschema"
    display_name = "JSON Schema"
    additional_opts = {"editor_mode": "json"}


class OdcsOutput(OutputDetails):
    name = "odcs"
    display_name = "Open Data Contract Standard (ODCS)"


class ProtobufOutput(OutputDetails):
    name = "protobuf"
    display_name = "Protobuf"
    additional_opts = {"editor_mode": "protobuf"}  # TODO doesn't seem to use protobuf mode


class PydanticModelOutput(OutputDetails):
    name = "pydantic-model"
    display_name = "Pydantic Model"
    additional_opts = {"editor_mode": "python"}  # TODO doesn't seem to use python mode


class RdfOutput(OutputDetails):
    name = "rdf"
    display_name = "RDF"
    additional_opts = {"editor_mode": "xml"}  # TODO Module rdf could not be loaded.


class SodaClOutput(OutputDetails):
    name = "sodacl"
    display_name = "SodaCL"


class SparkOutput(OutputDetails):
    name = "spark"
    display_name = "Spark"  # TODO Module spark could not be loaded.


class SqlOutput(OutputDetails):
    name = "sql"
    display_name = "SQL"
    is_default = True
    additional_opts = {"editor_mode": "sql"}


class SqlQueryOutput(OutputDetails):
    name = "sql-query"
    display_name = "SQL Query"
    additional_opts = {"editor_mode": "sql"}


class TerraformOutput(OutputDetails):
    name = "terraform"
    display_name = "Terraform"  #TODO requires servers to be populated


input_details = [OdcsInputDetails(), DataContractSpecInputDetails()]
output_details = [
    AvroOutput(), AvroIdlOutput(), BigQueryOutput(), DbmlOutput(), DbtOutput(), DbtSourcesOutput(),
    DbtStagingSqlOutput(), GoOutput(), GreatExpectationsOutput(), HtmlOutput(), JsonSchemaOutput(),
    OdcsOutput(), ProtobufOutput(), PydanticModelOutput(), RdfOutput(), SodaClOutput(), SparkOutput(),
    SqlOutput(), SqlQueryOutput(), TerraformOutput()
]

data_contract_examples = {}
input_select_element = document.getElementById("convert-input-type")
output_select_element = document.getElementById("convert-output-type")


def init_select_options():
    set_options(input_details, input_select_element)
    set_options(output_details, output_select_element)


def set_options(options_list: List[OptionDetails], select_element):
    for opt in options_list:
        option_element = document.createElement("option")
        option_element.value = opt.name
        option_element.innerText = opt.display_name
        option_element.setAttribute("id", opt.name)
        if opt.additional_opts:
            for key, value in opt.additional_opts.items():
                option_element.setAttribute(key, value)
        if opt.is_default:
            option_element.setAttribute("selected", "")
        select_element.append(option_element)


def set_output_editor_mode(output_type):
    if output_type == "sql":
        editor_output.session.setMode("ace/mode/sql")
    elif output_type == "dbt" or output_type == "sodacl":
        editor_output.session.setMode("ace/mode/yaml")


def export_to_output_type(e):
    input_type = input_select_element.value
    input_option = document.getElementById(input_type)
    if input_option.getAttribute("is_import") == "true":
        # then need to import to data contract spec first then export
        converted_input = import_to_data_contract(input_type, editor_input.getValue())
        # pydantic 2.x cannot be imported as a package due to https://pyodide.org/en/stable/usage/faq.html#micropip-can-t-find-a-pure-python-wheel
        dict_input = converted_input.dict(exclude_defaults=True, exclude_none=True)
        input_value = yaml.dump(dict_input, default_flow_style=False)
    else:
        input_value = editor_input.getValue()

    data_contract = resolve.resolve_data_contract(data_contract_str=input_value)
    export_result = exporter_factory.create(convert_output_type.value).export(
        data_contract=data_contract,
        model="all",
        server=None,
        sql_server_type="postgres",  # TODO make this dynamic from input field
        export_args={}
    )
    editor_output.session.setValue(export_result)
    # based on the output type, change the editor_output mode
    set_output_editor_mode(convert_output_type.value)


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
