# data-contract-playground
Playground site for creating/validating data contracts

[Try here.](https://data-catering.github.io/data-contract-playground/)

## Export

Given a data contract, export it to different formats.
Uses [datacontract-cli](https://github.com/datacontract/datacontract-cli) to export.
Current formats supported:
- Avro
- DBT
- DBT Sources
- DBT Staging SQL
- Go
- JSON Schema
- Open Data Contract Standard (ODCS)
- Protobuf
- Pydantic Model
- SodaCL
- SQL
- SQL Query
- Terraform

## Validate

Given a data contract, ensure it adheres to the specification selected.
[Specifications supported](#support).

## Support

Currently, it supports:

- [Open Data Contract Standard (ODCS)](https://github.com/bitol-io/open-data-contract-standard)
- [Data Contract Specification](https://github.com/datacontract/datacontract-specification)
- [Data Product Specification](https://github.com/datamesh-architecture/dataproduct-specification)
