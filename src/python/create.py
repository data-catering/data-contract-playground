import js
import yaml
from datacontract.export.exporter_factory import exporter_factory
from datacontract.imports.importer_factory import importer_factory
from datacontract.lint import resolve
from datacontract.model.data_contract_specification import DataContractSpecification, Info
from pyodide.ffi import create_proxy
from pyscript import document, window
from pyweb import pydom

from src.python.common import set_options, set_editor_mode, input_option_id_prefix, output_option_id_prefix
from src.python.model import AvroDetails, DbtDetails, JsonSchemaDetails, SqlDetails, OdcsDetails, \
    DataContractSpecDetails, UnityDetails, BigQueryDetails

input_details = [
    AvroDetails(),
    BigQueryDetails(),
    DbtDetails(),
    JsonSchemaDetails(),
    SqlDetails(),
    UnityDetails()
]
output_details = [
    OdcsDetails(), DataContractSpecDetails()
]

convert_output_type = pydom["#convert-output-type"][0]
ace = window.ace
editor_input = ace.edit("input-yaml")
editor_output = ace.edit("output-text")
input_examples = {}
input_select_element = document.getElementById("convert-input-type")
output_select_element = document.getElementById("convert-output-type")


def init_select_options():
    set_options(input_details, input_select_element, input_option_id_prefix, editor_input, input_examples)
    js.createObject(create_proxy(input_examples), "input_examples")
    set_options(output_details, output_select_element, output_option_id_prefix, editor_output)


class MyInfo(Info):
    dbt_version: str = None


def import_to_output_type(e):
    input_type = input_select_element.value
    input_value = editor_input.getValue()
    file_name = "input.txt"
    f = open(file_name, "w")
    f.write(input_value)
    f.close()

    init_data_contract = resolve.resolve_data_contract(
        data_contract_location="https://datacontract.com/datacontract.init.yaml")
    data_contract = DataContractSpecification(info=MyInfo())
    data_contract.dataContractSpecification = init_data_contract.dataContractSpecification
    data_contract.id = init_data_contract.id
    data_contract.info.version = init_data_contract.info.version

    import_result = importer_factory.create(input_type).import_source(
        data_contract_specification=data_contract,
        source=file_name,
        import_args={}
    )
    # check if output type is odcs, if so, convert via export factory
    convert_result = export_to_data_contract(output_select_element.value, import_result)
    editor_output.session.setValue(convert_result)
    # based on the output type, change the editor_output mode
    set_editor_mode(output_option_id_prefix, convert_output_type.value, editor_output)


def export_to_data_contract(export_type, input_value):
    if export_type == "odcs":
        data_contract = export_odcs(input_value)
        # fix invalid values in odcs defaults
        update_api_version = data_contract.replace("apiVersion: 2.3.0", "apiVersion: v2.2.2")
        update_dataset_name = update_api_version.replace("datasetDomain: null",
                                                         "datasetDomain: default_domain\ndatasetName: default_name")
        update_quantum_name = update_dataset_name.replace("quantumName: null", "quantumName: default_quantum")
        return update_quantum_name
    else:
        dict_result = input_value.dict(exclude_defaults=True, exclude_none=True)
        return yaml.dump(dict_result, default_flow_style=False)


def export_odcs(data_contract: DataContractSpecification):
    return exporter_factory.create("odcs").export(
        data_contract=data_contract,
        model="postgres",
        server=None,
        sql_server_type="postgres",
        export_args={}
    )


init_select_options()
