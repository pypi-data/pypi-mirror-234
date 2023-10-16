# OMOP2FHIR-vocab
Convert OMOP vocab to FHIR.

## Prerequisites
* [Python 3.9+](https://www.python.org/downloads/)
* [Java 11+](https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html)

## Installation
`pip install omop2fhir-vocab`

## Running
Run: `omop2fhir-vocab OPTIONS`

### CLI
```
omop2fhir-vocab --help
usage: omop2fhir-vocab [-h] -c CONCEPT_CSV_PATH -r CONCEPT_RELATIONSHIP_CSV_PATH [-v VOCABS [VOCABS ...]] [-R RELATIONSHIPS [RELATIONSHIPS ...]] [-o OUT_DIR]
                       [-I]

Convert OMOP vocab to FHIR.

options:
  -h, --help            show this help message and exit
  -c CONCEPT_CSV_PATH, --concept-csv-path CONCEPT_CSV_PATH
                        Path to CSV of OMOP concept table.
  -r CONCEPT_RELATIONSHIP_CSV_PATH, --concept-relationship-csv-path CONCEPT_RELATIONSHIP_CSV_PATH
                        Path to CSV of OMOP concept_relationship table.
  -v VOCABS [VOCABS ...], --vocabs VOCABS [VOCABS ...]
                        Which vocabularies to include in the output? Usage: --vocabs "Procedure Type" "Device Type"
  -R RELATIONSHIPS [RELATIONSHIPS ...], --relationships RELATIONSHIPS [RELATIONSHIPS ...]
                        Which relationship types from the concept_relationship table's relationship_id field to include? Default is "Is a" only. Passing "ALL"
                        includes everything. Usage: --realationships "Is a" "Maps to"
  -o OUT_DIR, --out-dir OUT_DIR
                        Output directory. Defaults to current working directory.
  -I, --retain-intermediaries
                        Retain intermediary OWL files created during conversion process?
```
