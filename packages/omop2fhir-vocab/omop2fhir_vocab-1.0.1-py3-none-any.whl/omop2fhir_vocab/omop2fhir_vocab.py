"""omop2fhir-vocab: Convert OMOP vocab to FHIR."""
import os
from argparse import ArgumentParser
from datetime import datetime
from typing import Dict, List

# noinspection PyProtectedMember
from omop2owl_vocab.omop2owl_vocab import omop2owl
from owl_on_fhir.__main__ import owl_to_fhir


# TODO: consider cache for either package internals, or omop2owl outputs
#  use_cached_intermediaries  # not in CLI
def omop2fhir(
    concept_csv_path: str, concept_relationship_csv_path: str, vocabs: List[str] = [],
    relationships: List[str] = ['Is a'], out_dir: str = None, retain_intermediaries=False,
    vocab_outputs=True, combined_outputs=True, exclude_vocab_prefix=False,
    # Not in CLI
    include_codesystem=True,
    # TODO: temp until fixed: https://github.com/mapping-commons/sssom-py/issues/456
    include_conceptmap=False
):
    """Run program"""
    # OMOP2OWL
    print('--- Serializaing to intermediate format: OWL ---')
    d: Dict = omop2owl(
        concept_csv_path, concept_relationship_csv_path, vocabs=vocabs, relationships=relationships, outdir=out_dir,
        skip_semsql=True, retain_general_cache=False)

    # Manipulations
    d2 = {}
    if not exclude_vocab_prefix:
        for mode, mode_d in d.items():
            d2[mode] = {}
            for vocab_id, path in mode_d.items():
                d2[mode][f'OMOP-{vocab_id}'] = path
    d = d2

    # OWL2FHIR
    print('--- Converting to FHIR ---')
    # todo: code_system_url? (if not created automatically)
    try:
        if vocab_outputs:
            for vocab_id, path in d['vocab_outputs'].items():
                print(f'- converting vocab: "{vocab_id}"')
                owl_to_fhir(path, out_dir, code_system_id=vocab_id, include_codesystem=include_codesystem,
                            include_conceptmap=include_conceptmap)
        if combined_outputs:
            print('- creating combined output')
            _id, path = [x for x in d['combined_output'].items()][0]
            owl_to_fhir(path, out_dir, code_system_id=_id, include_codesystem=include_codesystem,
                        include_conceptmap=include_conceptmap)
    # - teardown
    finally:
        if not retain_intermediaries:
            for mode in d.values():
                for path in mode.values():
                    os.remove(path)


def cli():
    """Command line interface.

    This package is mostly a wrapper around other packages. As such, arguments will be passed down."""
    parser = ArgumentParser(prog='omop2fhir-vocab', description='Convert OMOP vocab to FHIR.')

    # omop2owl-vocab only args -----------------------------------------------------------------------------------------
    # Required
    parser.add_argument(
        '-c', '--concept-csv-path', required=True, help='Path to CSV of OMOP concept table.')
    parser.add_argument(
        '-r', '--concept-relationship-csv-path', required=True,
        help='Path to CSV of OMOP concept_relationship table.')
    # Optional
    parser.add_argument(
        '-v', '--vocabs', required=False, nargs='+',
        help='Which vocabularies to include in the output?  Usage: --vocabs "Procedure Type" "Device Type"')
    parser.add_argument(
        '-R', '--relationships', required=False, nargs='+', default=['Is a'],
        help='Which relationship types from the concept_relationship table\'s relationship_id field to include? '
             'Default is "Is a" only. Passing "ALL" includes everything. Usage: --realationships "Is a" "Maps to"')

    # Common arguments -------------------------------------------------------------------------------------------------
    # todo: mark anywhere where verbiage differs
    #  - Ideally, while doing so, fix it so that owl2fhir and omop2owl have same verbiage
    parser.add_argument(
        '-o', '--out-dir', required=False, default=os.getcwd(),
        help='Output directory. Defaults to current working directory.')
    # parser.add_argument(  # omop2owl version
    #     '-O', '--outdir', required=False, default=os.getcwd(), help='Output directory.')
    # - not implemented
    #   - caching: it is parameterized differently in eaach package
    # todo: consider adding: codesys-id/ontology-id: very similar but may be worth 2 params
    # parser.add_argument(
    #     '-s', '--code-system-id', required=True, default=False,
    #     help="The code system ID to use for identification on the server uploaded to. "
    #          "See: https://hl7.org/fhir/resource-definitions.html#Resource.id")
    # # parser.add_argument(  # omop2owl version. should this be exposed separately?
    #     '-I', '--ontology-id', required=False, default='OMOP',  # add str(randint(100000, 999999))?
    #     help='Identifier for ontology. Used to generate a pURL and file name.')
    # - todo: expose any of these?
    # parser.add_argument(
    #     '-C', '--use-cache', required=False, action='store_true',
    #     help='Of outputs or intermediates already exist, use them.')
    # parser.add_argument(  # I think this is useful for omop2owl because of semsql, but we don't use that output here
    #     '-M', '--memory', required=False, default=100, help='The amount of Java memory (GB) to allocate.')
    # parser.add_argument(
    #     '-o', '--output-type', required=False, default='merged-post-split',
    #     choices=['merged', 'split', 'merged-post-split', 'rxnorm'],
    #     help='What output to generate? If "merged" will create an ONTOLOGY_ID.db file with all concepts of all vocabs '
    #          'merged into one. If "split" will create an ONTOLOGY_ID-*.db file for each vocab. "merged-post-split" '
    #          'output will be as if running both "split" and  "merged", but the merging implementation is different. '
    #          'Use this option if running out of memory. If using "rxnorm", will create a specifically customized '
    #          'ONTOLOGY_ID-RxNorm.db.')
    # - not useful
    # parser.add_argument(
    #     '-S', '--skip-semsql', required=False, action='store_true',
    #     help='In addition to .owl, also convert to a SemanticSQL .db? This is always True except when --output-type is '
    #          'all-merged-post-split and it is creating initial .owl files to be merged.')
    # parser.add_argument(
    #     '-e', '--exclude-singletons', required=False, action='store_true',
    #     help='Exclude terms that do not have any relationships. This only applies to --method robot.')
    # parser.add_argument(
    #     '-s', '--semsql-only', required=False, action='store_true',
    #     help='Use this if the .owl already exists and you just want to create a SemanticSQL .db.')

    # New args ---------------------------------------------------------------------------------------------------------
    parser.add_argument(
        '-I', '--retain-intermediaries', action='store_true', default=False, required=False,
        help='Retain intermediary OWL files created during conversion process?')
    parser.add_argument(
        '-V', '--vocab-outputs', action='store_true', default=True, required=False,
        help='Create set of artefacts (CodeSystem, ConceptMap) for each vocabulary?')
    parser.add_argument(
        '-C', '--combined-outputs', action='store_true', default=True, required=False,
        help='Create set of artefacts (CodeSystem, ConceptMap) for all of OMOP vocabulary combined?')
    parser.add_argument(
        '-e', '--exclude-vocab-prefix', action='store_true', default=False, required=False,
        help='With this flag absent, the identifiers and file names for each vocabulary will be prefixed "OMOP".')

    # owl2fhir only args -----------------------------------------------------------------------------------------------
    # - todo: expose any of these?
    # parser.add_argument(
    #     '-S', '--code-system-url', required=True, default=False,
    #     help="Canonical URL for the code system. "
    #          "See: https://hl7.org/fhir/codesystem-definitions.html#CodeSystem.url")
    # parser.add_argument(
    #     '-t', '--intermediary-type', choices=INTERMEDIARY_TYPES, default='obographs', required=False,
    #     help='Which type of intermediary to use? First, we convert OWL to that intermediary format, and then we '
    #          'convert that to FHIR.')
    # parser.add_argument(
    #     '-c', '--use-cached-intermediaries', action='store_true', required=False, default=False,
    #     help='Use cached intermediaries if they exist? Also will save intermediaries to owl-on-fhir\'s cache/ dir.')
    # parser.add_argument(
    #     '-r', '--retain-intermediaries', action='store_true', default=False, required=False,
    #     help='Retain intermediary files created during conversion process (e.g. Obograph JSON)?')
    # parser.add_argument(
    #     '-I', '--convert-intermediaries-only', action='store_true', default=False, required=False,
    #     help='Convert intermediaries only?')
    # - not useful
    # parser.add_argument('-i', '--input-path-or-url', required=True, help='URL or path to OWL file to convert.')
    # parser.add_argument(  # covered by omop2owl --relationships
    #     '-p', '--include-only-critical-predicates', action='store_true', required=False, default=False,
    #     help='If present, includes only critical predicates (is_a/parent) rather than all predicates in '
    #          'CodeSystem.property and CodeSystem.concept.property.')
    # parser.add_argument(
    #     '-d', '--dev-oak-path', default=False, required=False,
    #     help='If you want to use a local development version of OAK, specify the path to the OAK directory here. '
    #          'Must be used with --dev-oak-interpreter-path.')
    # parser.add_argument(
    #     '-D', '--dev-oak-interpreter-path', default=False, required=False,
    #     help='If you want to use a local development version of OAK, specify the path to the Python interpreter where '
    #          'its dependencies are installed (i.e. its virtual environment). Must be used with --dev-oak-path.')
    # parser.add_argument(
    #     '-u', '--native-uri-stems', required=True, nargs='+',
    #     help='A comma-separated list of URI stems that will be used to determine whether a concept is native to '
    #          'the CodeSystem. For example, for OMIM, the following URI stems are native: '
    #          'https://omim.org/entry/,https://omim.org/phenotypicSeries/PS". '
    #          'As of 2023-01-15, there is still a bug in the Obographs spec and/or `robot` where certain nodes are not'
    #          ' being converted. This converter adds back the nodes, but to know which ones belong to the CodeSystem '
    #          'itself and are not foreign concepts, this parameter is necessary. OAK also makes use of this parameter. '
    #          'See also: https://github.com/geneontology/obographs/issues/90')

    d: Dict = vars(parser.parse_args())
    omop2fhir(**d)


if __name__ == '__main__':
    t1 = datetime.now()
    cli()
    t2 = datetime.now()
    print(f'Finished in {(t2 - t1).seconds} seconds')
