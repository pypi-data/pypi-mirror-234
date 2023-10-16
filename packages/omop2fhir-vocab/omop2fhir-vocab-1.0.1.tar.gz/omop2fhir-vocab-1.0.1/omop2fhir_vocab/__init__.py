"""omop2fhir-vocab: Convert OMOP vocab to FHIR."""
from datetime import datetime

from omop2fhir_vocab.omop2fhir_vocab import cli


if __name__ == '__main__':
    t1 = datetime.now()
    cli()
    t2 = datetime.now()
    print(f'Finished in {(t2 - t1).seconds} seconds')
