import copy
from typing import Dict

import yaml
from datacontract.model.data_contract_specification import DataContractSpecification, Contact, Info, Terms, Field, Model


class MyContact(Contact):
    @property
    def model_fields(self):
        return self.__fields__


class MyInfo(Info):
    contact: MyContact = None
    model_extra: dict = {}


class MyTerms(Terms):
    model_extra: dict = {}

    @property
    def model_fields(self):
        return self.__fields__


class MyField(Field):
    model_extra: dict = {}

    @property
    def model_fields(self):
        return self.__fields__


class MyModel(Model):
    fields: Dict[str, MyField] = {}


class DataContractSpec(DataContractSpecification):
    info: MyInfo = MyInfo()
    terms: MyTerms = MyTerms()
    models: Dict[str, MyModel] = {}

    def to_yaml(self):
        dict_input = self.dict(exclude_defaults=True, exclude_none=True)
        return yaml.dump(dict_input, default_flow_style=False)

    def model_copy(self):
        return copy.deepcopy(self)


class DataSourceDetails:
    name: str = None
    display_name: str = None
    is_default: bool = False
    example_file: str = None
    additional_opts: Dict[str, str] = {"editor_mode": "yaml"}


class AvroDetails(DataSourceDetails):
    name = "avro"
    display_name = "Avro"
    example_file = "example/avro/orders.avsc"
    additional_opts = {"editor_mode": "json"}


class AvroIdlDetails(DataSourceDetails):
    name = "avro-idl"
    display_name = "Avro IDL"
    additional_opts = {"editor_mode": "json"}


class BigQueryDetails(DataSourceDetails):
    name = "bigquery"
    display_name = "BigQuery"
    example_file = "example/bigquery/complete_table_schema.json"
    additional_opts = {"editor_mode": "json"}
    # TODO Export to bigquery requires selecting a bigquery server from the data contract.


class DataContractSpecDetails(DataSourceDetails):
    name = "dataContractSpecification"
    display_name = "Data Contract Specification"


class DbmlDetails(DataSourceDetails):
    name = "dbml"
    display_name = "DBML"
    example_file = "example/dbml/dbml.txt"


class DbtDetails(DataSourceDetails):
    name = "dbt"
    display_name = "DBT"
    example_file = "example/dbt/manifest_jaffle_duckdb.json"


class DbtSourcesDetails(DataSourceDetails):
    name = "dbt-sources"
    display_name = "DBT Sources"


class DbtStagingSqlDetails(DataSourceDetails):
    name = "dbt-staging-sql"
    display_name = "DBT Staging SQL"
    additional_opts = {"editor_mode": "sql"}


class GoDetails(DataSourceDetails):
    name = "go"
    display_name = "Go"
    additional_opts = {"editor_mode": "go"}


class GreatExpectationsDetails(DataSourceDetails):
    name = "great-expectations"
    display_name = "Great Expectations"
    additional_opts = {"editor_mode": "json"}


class HtmlDetails(DataSourceDetails):
    name = "html"
    display_name = "HTML"
    additional_opts = {"editor_mode": "html"}


class JsonSchemaDetails(DataSourceDetails):
    name = "jsonschema"
    display_name = "JSON Schema"
    example_file = "example/jsonschema/orders_union-types.json"
    additional_opts = {"editor_mode": "json"}


class OdcsDetails(DataSourceDetails):
    name = "odcs"
    display_name = "Open Data Contract Standard (ODCS)"
    is_default = True
    additional_opts = {"is_import": True}


class ProtobufDetails(DataSourceDetails):
    name = "protobuf"
    display_name = "Protobuf"
    additional_opts = {"editor_mode": "protobuf"}


class PydanticModelDetails(DataSourceDetails):
    name = "pydantic-model"
    display_name = "Pydantic Model"
    additional_opts = {"editor_mode": "python"}


class RdfDetails(DataSourceDetails):
    name = "rdf"
    display_name = "RDF"
    additional_opts = {"editor_mode": "xml"}


class SodaClDetails(DataSourceDetails):
    name = "sodacl"
    display_name = "SodaCL"


class SparkDetails(DataSourceDetails):
    name = "spark"
    display_name = "Spark"
    additional_opts = {"editor_mode": "sql", "disabled": ""}
    # TODO Module spark could not be loaded.


class SqlDetails(DataSourceDetails):
    name = "sql"
    display_name = "SQL"
    is_default = True
    example_file = "example/sql/customer.sql"
    additional_opts = {"editor_mode": "sql"}


class SqlQueryDetails(DataSourceDetails):
    name = "sql-query"
    display_name = "SQL Query"
    additional_opts = {"editor_mode": "sql"}


class SqlAlchemyDetails(DataSourceDetails):
    name = "sqlalchemy"
    display_name = "SQLAlchemy"
    additional_opts = {"editor_mode": "sql"}


class TerraformDetails(DataSourceDetails):
    name = "terraform"
    display_name = "Terraform"
    # TODO requires servers to be populated


class UnityDetails(DataSourceDetails):
    name = "unity"
    display_name = "Unity Catalog"
    example_file = "example/unity/unity_table_schema.json"
    additional_opts = {"editor_mode": "json"}
