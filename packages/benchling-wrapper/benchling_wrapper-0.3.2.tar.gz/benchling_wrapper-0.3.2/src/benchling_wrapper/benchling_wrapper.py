"""
Benchling Wrapper main module.
"""
import re

from benchling_api_client.v2.stable.models.dna_sequence import DnaSequence
from benchling_sdk.auth.client_credentials_oauth2 import ClientCredentialsOAuth2
from benchling_api_client.models.naming_strategy import NamingStrategy
from benchling_sdk.helpers.pagination_helpers import PageIterator
from benchling_sdk.helpers.serialization_helpers import fields
from benchling_sdk.helpers.retry_helpers import RetryStrategy
from benchling_sdk.benchling import Benchling
from benchling_sdk import models
from benchling_sdk.models import CustomEntity, AssayResult

from httpx import TransportError
from typing import Callable, Any
from math import log2
from time import sleep
import pandas as pd

_RETRY_STRATEGY_MAX_TRIES = 17  # 65535.5 secs
_REQUEST_STEP_BASE_DELAY = 60
REQUESTS_RETRY_COUNT = 623  # 23:58:05


def _with_retry(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        """
        Retry decorator for Benchling SDK methods.
        :param args:
        :param kwargs:
        :return:
        """
        for i in range(REQUESTS_RETRY_COUNT + 1):
            try:
                return func(*args, **kwargs)

            # TransportError: decorate Benchling Limitation
            except TransportError as e:
                if i == REQUESTS_RETRY_COUNT:
                    raise e
                delay = _REQUEST_STEP_BASE_DELAY + log2(i + 1) * 10
                # log here
                sleep(delay)

    return wrapper


class BenchlingWrapper:
    """
    Wrapper over Benchling SDK.
    Allow to initialize Benchling object, get entity by its id, by field value, update entity.

    Attributes
    ----------
    benchling: Type(benchling_sdk.benchling)
        determined in __init__(). Instance of Benchling SDK object

    benchling_url: str
        determined in config. URL of Benchling Tenant

    benchling_access_token: str
        determined in config. Access token for API of Benchling Tenant

    app_client_id: str
    determined in .env. App Client ID

    app_client_secret: str
        determined in .env. App Client Secret

    benchling_registry_id: str
        determined in __init__(). Benchling  registry  associates with tenant
        (such as bostongene). This parameter is common for all objects.

    """
    schema_ids = {'specimen_schema_id': 'ts_gKsAMR0K',
                  'sequencing_sample_schema_id': 'ts_F2lwLUBO',
                  'sequencing_run_schema_id': 'ts_QwANoEG2',
                  'extraction_schema_id': 'ts_AUVfUqaC',
                  'dna_extract_schema_id': 'ts_7TqxICm8',
                  'rna_extract_schema_id': 'ts_MG64TGbP',
                  'qc0_schema_id': 'assaysch_YXqsLth9',
                  'pre_cap_schema_id': 'assaysch_PTgssTON',
                  'post_cap_schema_id': 'assaysch_zfxOvuYe',
                  }

    def __init__(
            self,
            benchling_url: str,
            benchling_access_token: str,
            app_client_id: str,
            app_client_secret: str,
    ) -> None:
        self.benchling_url = benchling_url
        self.benchling_access_token = benchling_access_token
        self.app_client_id = app_client_id
        self.app_client_secret = app_client_secret

        """
        Get a Benchling object with the client credentials OAuth2 flow. Get registry id.
        """

        oauth2 = ClientCredentialsOAuth2(
            client_id=self.app_client_id,
            client_secret=self.app_client_secret,
            token_url=self.benchling_access_token,
        )  # Authentication with client credentials OAuth2 flow

        self.benchling = Benchling(
            url=self.benchling_url,
            auth_method=oauth2,
            retry_strategy=RetryStrategy(max_tries=_RETRY_STRATEGY_MAX_TRIES),
        )  # initialize Benchling object

        self.benchling_registry_id = self.benchling.registry.registries()[
            0
        ].id  # registry id

    @_with_retry
    def get_entity_by_name(self, entity_name: str) -> CustomEntity:
        """
        Get the entity for the given entity name.

        :param: entity_name - name of the entity.
        :return: entity - entity for the given entity name
        """
        return self.benchling.custom_entities.list(name=entity_name).first()

    @_with_retry
    def get_entities_by_names(self, entity_names: list[str]) -> list[CustomEntity]:
        """
        Get the entities for the given list of entity names.

        :param: entity_name - name of the entity.
        :return: entity - entity for the given entity name
        """
        result = []
        for chunk in chunking(entity_names):
            result.extend(
                flatten(self.benchling.custom_entities.list(names_any_of=chunk))
            )
        return result

    @_with_retry
    def get_entity_by_id(self, entity_id: str) -> CustomEntity:
        """
        Get the entity for the given entity id.

        :param: entity_id - id of the entity.
        :return: entity - entity for the given entity id
        """
        return self.benchling.custom_entities.get_by_id(entity_id)

    @_with_retry
    def get_entities_by_ids(self, entity_ids: list[str]) -> list[CustomEntity]:
        """
        Get the entity by the registry ids.

        :param: entity_registry_ids_any_of - list of registry ids
        :return: page iterator with entities - list of entities for the given registry ids
        """
        registry_id = self.benchling_registry_id
        result = []
        for chunk in chunking(entity_ids):
            result.extend(
                flatten(
                    self.benchling.custom_entities.list(
                        registry_id=registry_id, entity_registry_ids_any_of=chunk
                    )
                )
            )
        return result

    @_with_retry
    def get_sequence_by_name(self, entity_name: str) -> DnaSequence | None:
        """
        Get the entity for the given entity name.

        :param: entity_name - name of the entity.
        :return: entity - entity for the given entity name
        """
        return self.benchling.dna_sequences.list(name=entity_name).first()

    @_with_retry
    def get_sequence_by_id(self, entity_id: str) -> DnaSequence:
        """
        Get the entity for the given entity id.

        :param: entity_id - id of the entity.
        :return: entity - entity for the given entity id
        """
        return self.benchling.dna_sequences.get_by_id(entity_id)

    @_with_retry
    def get_sequences_by_ids(self, entity_ids: list[str]) -> list[DnaSequence]:
        """
        Get the entity for the given entity id.

        :param: entity_id - id of the entity.
        :return: entity - entity for the given entity id
        """
        registry_id = self.benchling_registry_id
        result = []
        for chunk in chunking(entity_ids):
            result.extend(
                flatten(
                    self.benchling.dna_sequences.list(
                        registry_id=registry_id, entity_registry_ids_any_of=chunk
                    )
                )
            )
        return result

    @_with_retry
    def get_entities_by_modified(
            self, schema_id: str, modified_at: str
    ) -> list[CustomEntity]:
        """
        Get the entity by the modified_at entity attribute.

        :param: schema_id - id of the schema
        :param: modified_at - modified_at attribute of the entity (datetime, RFC 3339 format)
        :return: page iterator with entities - list entity for the given (field name, field value) pair
        """
        return flatten(
            self.benchling.custom_entities.list(
                schema_id=schema_id, modified_at=f"> {modified_at}"
            )
        )

    @_with_retry
    def get_entity_by_schema_and_fields(
            self, schema_id: str, fields_dict: dict
    ) -> CustomEntity | None:
        """
        Get the entity by the schema id.

        :param: schema_id - id of the schema
        :return: page iterator with entities - list entity for the given schema id
        """
        return self.benchling.custom_entities.list(
            schema_id=schema_id, schema_fields=fields_dict, page_size=100
        ).first()

    @_with_retry
    def get_entities_by_schema_and_fields(
            self, schema_id: str, fields_dict: dict
    ) -> list[CustomEntity]:
        """
        Get the entity by the schema id.

        :param: schema_id - id of the schema
        :return: page iterator with entities - list entity for the given schema id
        """
        return flatten(
            self.benchling.custom_entities.list(
                schema_id=schema_id, schema_fields=fields_dict, page_size=100
            )
        )

    @_with_retry
    def get_results_by_schema_field(
            self, schema_id: str, entity_ids: list[str]
    ) -> PageIterator[AssayResult]:
        """
        Get the result by the schema and entity id.

        :param: schema_id - id of the schema
        :return: page iterator with entities - list entity for the given schema id
        """
        # result = []
        # for chunk in chunking(entity_ids):
        #     result.extend([*self.benchling.assay_results.list(schema_id=schema_id,
        #                                                       entity_ids=chunk)][0])
        # return result
        return self.benchling.assay_results.list(
            schema_id=schema_id, entity_ids=entity_ids
        )

    @_with_retry
    def get_results_by_schema_field_to_list(
            self, schema_id: str, entity_ids: list[str]
    ) -> list[AssayResult]:
        """
        Get the result by the schema and entity id.

        :param: schema_id - id of the schema
        :param: entity_ids - list of entity ids connected to the assay result
        :return: page iterator with entities - list entity for the given schema id
        """
        result = []
        for chunk in chunking(entity_ids):
            result.extend(
                flatten(
                    self.benchling.assay_results.list(
                        schema_id=schema_id, entity_ids=chunk
                    )
                )
            )
        return result

    @_with_retry
    def update_entity(
            self, entity: CustomEntity, fields_dict: dict, name: str = None
    ) -> None:
        """
        Update the entity with the given fields_dict.

        :param: entity - entity to update
        :param: fields_dict - fields to update in the format of {field_name: field_value}
        :param: name - new name of the entity
        :return: None
        """
        entity_id = entity.id
        if name is not None:
            update_entity = models.CustomEntityUpdate(
                fields=fields(fields_dict_converter(fields_dict)),
                name=name,
            )
        else:
            update_entity = models.CustomEntityUpdate(
                fields=fields(fields_dict_converter(fields_dict))
            )
        self.benchling.custom_entities.update(entity_id=entity_id, entity=update_entity)

    @_with_retry
    def update_entity_name(self, entity: CustomEntity, name: str) -> None:
        """
        Update the entity name.

        :param: entity - entity to update
        :param: name - new name of the entity
        :return: None
        """
        entity_id = entity.id
        update_entity = models.CustomEntityUpdate(name=name)
        self.benchling.custom_entities.update(entity_id=entity_id, entity=update_entity)

    def construct_entity(
            self,
            folder_id: str,
            schema_id: str,
            entity_name: str,
            fields_dict: dict,
            naming_strategy: NamingStrategy,
    ) -> models.CustomEntityCreate:
        """
        Construct the entity with the given schema_id and fields_dict for push to Benchling.
        :param: folder_id - id of the folder to push the entity to
        :param: schema_id - id of the entity schema
        :param: fields_dict - fields to update in the format of {field_name: field_value}
        :param: naming_strategy - naming strategy for the entity registration
        :return: entity - constructed entity
        """
        registry_id = self.benchling_registry_id
        entity = models.CustomEntityCreate(
            fields=fields(fields_dict_converter(fields_dict)),
            folder_id=folder_id,
            name=entity_name,
            registry_id=registry_id,
            naming_strategy=naming_strategy,
            schema_id=schema_id,
        )
        return entity

    @_with_retry
    def register_entity(self, entity: models.CustomEntityCreate) -> None:
        """
        Register the entity in Benchling.
        :param: entity - entity to register
        :return: None
        """
        self.benchling.custom_entities.create(entity=entity)

    @_with_retry
    def register_entities_by_ids(
            self, entities_ids: list[str], naming_strategy: NamingStrategy
    ) -> None:
        """
        Register the entities in Benchling.
        :param: entity - entity to register
        :return: None
        """
        registry_id = self.benchling_registry_id
        for chunk in chunking(entities_ids):
            self.benchling.registry.register(
                registry_id=registry_id,
                entity_ids=chunk,
                naming_strategy=naming_strategy,
            )

    @_with_retry
    def unregister_entities_by_ids(self, entity_ids: list[str], folder_id: str) -> None:
        """
        Unregister the entity in Benchling.
        :param: entity_id - id of the entity to unregister
        :return: None
        """
        registry_id = self.benchling_registry_id
        for chunk in chunking(entity_ids):
            self.benchling.registry.unregister(
                registry_id=registry_id, entity_ids=chunk, folder_id=folder_id
            )

    @_with_retry
    def get_dropdown_by_id(self, dropdown_id: str) -> models.Dropdown:
        """
        Get dropdown  by dropdown id.
        :param id: dropdown api id.
        :return: dropdown object with corresponding api ids.
        @rtype: models.Dropdown.
        """
        return self.benchling.dropdowns.get_by_id(dropdown_id)

    @_with_retry
    def get_dropdown_options(self, dropdown: models.Dropdown) -> dict:
        """
        Get dropdown variants by dropdown id.
        :param dropdown: dropdown object.
        @type dropdown: models.Dropdown.
        :return: dropdown options with corresponding api ids.
        @rtype: dict.
        """
        options = dropdown.options
        options = {option.name: option.id for option in options}
        return options

    @_with_retry
    def update_dropdown(self, dropdown_id: str, options_to_add: list) -> None:
        """
        Update a dropdown by dropdown_id with the given options.

        :param dropdown_id: id of a dropdown
        @type dropdown_id: str
        :param options_to_add: options to add
        @type options_to_add: list
        :return: None
        """
        dropdown = self.get_dropdown_by_id(dropdown_id)
        dropdown_options = self.get_dropdown_options(dropdown=dropdown)
        dropdown_options_for_upd = construct_dropdown_update(
            dropdown_options=dropdown_options
        )

        for option in options_to_add:
            dropdown_options_for_upd.append(models.DropdownOptionUpdate(name=option))

        self.benchling.dropdowns.update(
            dropdown_id=dropdown_id,
            dropdown=models.DropdownUpdate(options=dropdown_options_for_upd),
        )

    @_with_retry
    def register_assay_results(
            self, assay_results: list[models.AssayResultCreate]
    ) -> None:
        """
        Register the assay result in Benchling.
        :param: assay_result - assay result to register - accepts a list
        :return: None
        """
        for chunk in chunking(assay_results):
            self.benchling.assay_results.create(assay_results=chunk)

    def get_specimen_for_any_cases(self, case_list: list[str] = None) -> list[list[CustomEntity]]:
        """
        Get specimen objects for all types of cases from Benchling by a list of case names.
        e.g. ['RS005007', 'BG005074', 'CP000789']
        :param case_list: list of case names
        :return: list of specimen objects
        """

        if case_list is None:
            case_list = ['RS005007', 'BG005074', 'CP000789']

        specimen_list = []
        case_objects = self.get_entities_by_names(entity_names=case_list)
        for case in case_objects:
            if case.name.startswith('RS'):
                specimen_for_case = self.get_entities_by_schema_and_fields(
                    schema_id=self.schema_ids['specimen_schema_id'],
                    fields_dict={'R&D Case(s)': case.id})
            elif case.name.startswith('BG'):
                specimen_for_case = self.get_entities_by_schema_and_fields(
                    schema_id=self.schema_ids['specimen_schema_id'],
                    fields_dict={'Clinical Case(s)': case.id})
            elif case.name.startswith('CP'):
                specimen_for_case = self.get_entities_by_schema_and_fields(
                    schema_id=self.schema_ids['specimen_schema_id'],
                    fields_dict={'Collaboration Case(s)': case.id})
            else:
                raise ValueError(f"Unknown case name {case.name}")

            specimen_list.append(specimen_for_case)
        return specimen_list

    def get_extractions_for_specimen(self, specimen_object: CustomEntity) -> list[CustomEntity]:
        """
        Get Extraction objects for a specimen from Benchling.
        :param specimen_object:
        :return: a list of Extraction objects
        """
        extractions = self.get_entities_by_schema_and_fields(
            schema_id=self.schema_ids['extraction_schema_id'],
            fields_dict={'Specimen Lookup': specimen_object.id})

        extractions_dna = self.get_entities_by_schema_and_fields(
            schema_id=self.schema_ids['dna_extraction_schema_id'],
            fields_dict={'Specimen Lookup': specimen_object.id})

        extractions_rna = self.get_entities_by_schema_and_fields(
            schema_id=self.schema_ids['rna_extraction_schema_id'],
            fields_dict={'Specimen Lookup': specimen_object.id})

        extractions.extend(extractions_dna)
        extractions.extend(extractions_rna)
        return extractions

    def get_extractions_for_project(self, project_name: str) -> list[CustomEntity]:
        """
        Get Extraction objects for a project from Benchling.
        :param project_name:
        :return: a list of Extraction objects
        """
        # get project id in Benchling by project name
        project_id = self.get_entity_by_name(entity_name=project_name).id
        # get Extraction, DNA Extraction and RNA Extraction objects for the project
        extractions = self.get_entities_by_schema_and_fields(
            schema_id=self.schema_ids['extraction_schema_id'],
            fields_dict={'Project': project_id})
        extractions_dna = self.get_entities_by_schema_and_fields(
            schema_id=self.schema_ids['dna_extraction_schema_id'],
            fields_dict={'Project': project_id})
        extractions_rna = self.get_entities_by_schema_and_fields(
            schema_id=self.schema_ids['rna_extraction_schema_id'],
            fields_dict={'Project': project_id})
        extractions.extend(extractions_dna)
        extractions.extend(extractions_rna)
        return extractions

    def get_sequencing_samples_for_specimens(self, specimen_list: list[list[CustomEntity]]
                                             ) -> list[list[list[CustomEntity]]]:
        """
        Get sequencing samples for a list of specimens from Benchling.
        """

        sequencing_sample_list = []
        for specimen_for_case in specimen_list:
            for specimen in specimen_for_case:
                # 1 method using Starting NGS Sample field
                sequencing_sample_for_specimen_ngs_sample = self.get_entities_by_schema_and_fields(
                    schema_id=self.schema_ids['sequencing_sample_schema_id'],
                    fields_dict={'Starting NGS Sample': specimen.id})

                sequencing_sample_list.append(sequencing_sample_for_specimen_ngs_sample)

        return sequencing_sample_list

    def get_extraction_names_for_runs(
            self, run_names_benchling: list[str] = None
    ) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
        """
        Get Extraction names for every given run from Benchling.
        :param run_names_benchling:
        :return:
        """
        if run_names_benchling is None:
            run_names_benchling = ['230613_NovaB_XTHS2', '230617_NovaC_XTHS2']
        # getting run ids
        run_ids = [{run_object.name: run_object.id}
                   for run_object in
                   self.get_entities_by_names(entity_names=run_names_benchling)
                   ]

        # Getting the names of Extractions for every Seq Sample object
        seq_sample_extractions_names_dict = {}
        seq_sample_names_dict = {}

        for run_dict in run_ids:
            run_name, run_id = zip(*run_dict.items())
            run_name = run_name[0]

            sequencing_samples_for_run = flatten(list(
                self.get_entity_by_schema_and_fields(schema_id=self.schema_ids['sequencing_sample_schema_id'],
                                                     fields_dict={'Sequencing Run': run_id})))

            ss_ext_names = [ss.fields.additional_properties['Extraction(s)'].text_value for ss in
                            sequencing_samples_for_run]
            seq_sample_extractions_names_dict[run_name] = ss_ext_names

            ss_names = [ss.name for ss in sequencing_samples_for_run]
            seq_sample_names_dict[run_name] = ss_names
            print(f'{run_name} has {len(seq_sample_names_dict[run_name])} samples')

        return seq_sample_extractions_names_dict, seq_sample_names_dict

    def get_samples_filtered_by_project_names(self,
                                              seq_sample_extractions_names_dict: dict[str, list[str]],
                                              seq_sample_names_dict: dict[str, list[str]],
                                              run_names_benchling: list[str] = None,
                                              project_names_benchling: list[str] = None,
                                              mode: str = 'cfDNA'
                                              ) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
        """
        Filter out the samples from the list of Sequencing Sample names
        obtained from dicts of `get_extraction_names_for_runs()` function
        :param run_names_benchling: list of run names from Benchling, e.g. ['230613_NovaB_XTHS2', '230617_NovaC_XTHS2']
        :param project_names_benchling: list of project names from Benchling, e.g. ['cfDNA TMB references']
        :param seq_sample_extractions_names_dict: dict, where key - run name, value - list of Extraction names
        :param seq_sample_names_dict: dict, where key - run name, value - list of Sequencing Sample names
        :param mode: if 'cfDNA' string is passed, then it filters out all the samples with 'cfDNA' in the name
        :return: a dict filtered by given Projects, where key - run name, value - list of Sequencing Sample names
        """
        if run_names_benchling is None:
            run_names_benchling = ['230613_NovaB_XTHS2', '230617_NovaC_XTHS2']
        if project_names_benchling is None:
            project_names_benchling = ['cfDNA TMB references']

        filtered_seq_sample_names_dict = {}
        outlier_seq_sample_names_dict = {}
        seq_sample_extractions_objects_dict = {}
        sample_tracking_dict = {}

        for run_name in run_names_benchling:
            # replacing every Extraction name with the Extraction object
            extractions_for_run = self.get_entities_by_names(seq_sample_extractions_names_dict[run_name])
            seq_sample_extractions_objects_dict[run_name] = extractions_for_run
            # replacing every Extraction object with 1 if Extraction Project is in the list of projects
            # and 0 if not
            sample_tracking_dict[run_name] = [
                1 if ext.fields.additional_properties['Project'].text_value in project_names_benchling else 0 for ext in
                seq_sample_extractions_objects_dict[run_name]]
            # Iterating over Sequencing Sample names (seq_sample_names_dict) and
            # if sample_tracking_dict has 0 for this sample
            # we remove it from the list of Sequencing Sample names
            filtered_seq_sample_names_dict[run_name] = [seq_sample_names_dict[run_name][i] for i in
                                                        range(len(sample_tracking_dict[run_name])) if
                                                        sample_tracking_dict[run_name][i] == 1]
            outlier_seq_sample_names_dict[run_name] = [seq_sample_names_dict[run_name][i] for i in
                                                       range(len(sample_tracking_dict[run_name])) if
                                                       sample_tracking_dict[run_name][i] == 0]
            print(f'Number of samples filtered by project in {run_name} run:'
                  f' {len(filtered_seq_sample_names_dict[run_name])}')
            print(f'Number of outlier samples in {run_name} run: {len(outlier_seq_sample_names_dict[run_name])}')

            # filtering out all the samples with 'cfDNA' in the name
            if mode == 'cfDNA':
                filtered_seq_sample_names_dict[run_name] = [sample for sample in
                                                            filtered_seq_sample_names_dict[run_name]
                                                            if 'cfDNA' in sample]
                outlier_seq_sample_names_dict[run_name] = [sample for sample in outlier_seq_sample_names_dict[run_name]
                                                           if 'cfDNA' in sample]
                print(f'Number of samples filtered by project in {run_name} run after filtering out cfDNA: '
                      f'{len(filtered_seq_sample_names_dict[run_name])}')
                print(f'Number of outlier samples in {run_name} run after filtering out cfDNA: '
                      f'{len(outlier_seq_sample_names_dict[run_name])}')

        return filtered_seq_sample_names_dict, outlier_seq_sample_names_dict

    def get_run_names_by_project_name(self, project_name: str) -> tuple[list[str], dict[str, list[CustomEntity]]]:
        """
        By project name get run names and sequencing sample objects for these runs.
        :param project_name: name of the project
        :return: list of run names, dict of run names and sequencing sample objects for these runs
        """
        # get project id in Benchling by project name
        project_id = self.get_entity_by_name(entity_name=project_name).id
        # get Extraction, DNA Extraction and RNA Extraction objects for the project
        extractions = self.get_extractions_for_project(project_id)
        # get Sequencing Sample objects for the Extractions, DNA Extractions and RNA Extractions
        sequencing_samples = []
        for extraction in extractions:
            sequencing_samples_for_extraction = self.get_entities_by_schema_and_fields(
                schema_id=self.schema_ids['sequencing_sample_schema_id'],
                fields_dict={'Extraction(s)': extraction.id})
            sequencing_samples.extend(sequencing_samples_for_extraction)
        # sort Sequencing Sample objects by Sequencing Run in a dict
        sequencing_samples_by_run = {}
        for sequencing_sample in sequencing_samples:
            run_id = sequencing_sample.fields.additional_properties['Sequencing Run'].text_value
            if run_id not in sequencing_samples_by_run:
                sequencing_samples_by_run[run_id] = []
            sequencing_samples_by_run[run_id].append(sequencing_sample)
        # return run names and a dict of Sequencing Sample objects for runs
        return list(sequencing_samples_by_run.keys()), sequencing_samples_by_run

    def get_sequencing_sample_by_run_names_and_project_name(
            self, run_names: list[str], project_name: str = None
    ) -> pd.DataFrame:
        """
        Get sequencing sample objects for the given run names and project name.
        :param run_names: list of run names
        :param project_name: name of the project
        :return: dict of run names and sequencing sample objects for these runs and this project
        """
        # get Sequencing Runs ids in Benchling by run names
        run_ids = [run.id for run in self.get_entities_by_names(entity_names=run_names)]
        # get Sequencing Sample objects for the project and runs
        sequencing_samples = []
        for run_id in run_ids:
            sequencing_samples_for_run = self.get_entities_by_schema_and_fields(
                schema_id=self.schema_ids['sequencing_sample_schema_id'],
                fields_dict={'Sequencing Run': run_id})
            sequencing_samples.extend(sequencing_samples_for_run)
        # Filter Sequencing Sample objects by project
        # 1. getting Extractions to filter out the Sequencing Samples by project, which is stored in Extraction
        extractions_names = []
        for sequencing_sample in sequencing_samples:
            # get Extraction object for the Sequencing Sample
            extraction_name = sequencing_sample.fields.additional_properties['Extraction(s)'].text_value
            # append to the list of Extractions
            extractions_names.append(extraction_name)
        # 2. Getting Extraction objects by names
        extractions_objects = self.get_entities_by_names(entity_names=extractions_names)
        # 3. Filter Sequencing Samples from list by project using corresponding list of Extraction objects
        # or
        # if given Project is empty then just obtain project names for every Sequencing Sample
        sequencing_samples_projects = []
        sequencing_samples_specimen = []
        sequencing_samples_by_project = []

        if project_name is None:
            for sequencing_sample, extraction in zip(sequencing_samples, extractions_objects):
                sequencing_samples_projects.append(
                    extraction.fields.additional_properties['Project'].text_value)
                sequencing_samples_specimen.append(
                    extraction.fields.additional_properties['Starting NGS Sample'].text_value)
        else:
            for sequencing_sample, extraction in zip(sequencing_samples, extractions_objects):
                if extraction.fields.additional_properties['Project'].display_value == project_name:
                    sequencing_samples_by_project.append(sequencing_sample)
                    sequencing_samples_projects.append(
                        extraction.fields.additional_properties['Project'].text_value)
                    sequencing_samples_specimen.append(
                        extraction.fields.additional_properties['Starting NGS Sample'].text_value)
            sequencing_samples = sequencing_samples_by_project
        # 4. Fill the df with data
        final_df = pd.DataFrame(columns=['Sequencing Sample Name', 'Sample Sheet ID', 'Specimen',
                                         'Run Name', 'Project Name'])
        final_df['Sequencing Sample Name'] = [sequencing_sample.name for sequencing_sample in
                                              sequencing_samples]
        final_df['Sample Sheet ID'] = [sequencing_sample.fields.additional_properties[
                                           'Sample Sheet ID'].text_value for sequencing_sample in
                                       sequencing_samples]
        final_df['Run Name'] = [sequencing_sample.fields.additional_properties[
                                    'Sequencing Run'].text_value for sequencing_sample in
                                sequencing_samples]
        # get case name for every sequencing sample by cutting specimen name from start to the first underscore
        # if specimen is not None and not empty string, else add empty string
        final_df['Case'] = [specimen.split('_')[0] if specimen is not None and specimen != '' else ''
                            for specimen in sequencing_samples_specimen]
        final_df['Project Name'] = sequencing_samples_projects
        return final_df

    def get_qc_for_sequencing_samples(self, samples_df: pd.DataFrame) -> pd.DataFrame:
        """
        Get QC objects for the given sequencing samples.
        1. Extract names of the samples from dataframe
        2. Get QC result objects for the samples
        3. Fill the output dataframe with QC results: each row is a sample, each column is a QC result
        This function is easy to use with get_sequencing_sample_by_run_names_and_project_name() function output
        :param samples_df: dataframe with samples. Has to contain `Sequencing Sample Name` and `Sample Sheet ID` columns
        :return: dataframe with QC results
        """
        # creating output dataframe
        qc_df = pd.DataFrame(columns=['Sequencing Sample Name', 'Sample Sheet ID', 'Tissue', 'Input Material Type',
                                      'Library Probe Set Kit', 'Data Type', 'RNA_Distr_QC',
                                      'Tumor/Normal', 'Sequencing Date', 'Top-off',
                                      'Top-off Target Sample', 'Reseq'])
        # get Sample Sheet IDs and sample names from input dataframe
        sample_names = samples_df['Sequencing Sample Name'].tolist()
        sample_sheet_ids = samples_df['Sample Sheet ID'].tolist()
        # adding Sample Sheet UDs and Sample Names to the output dataframe
        qc_df['Sample Sheet ID'] = sample_sheet_ids
        qc_df['Sequencing Sample Name'] = sample_names
        # filling Data type column by cutting the Sample Sheet ID using regex:
        # from the start until first digit
        # then remove the last character which is additional hyphen.
        qc_df['Data Type'] = [re.search(r'^\D+', sample_sheet_id).group(0)[:-1]
                              for sample_sheet_id in sample_sheet_ids]

        # get samples as objects from Benchling
        sample_objects = self.get_entities_by_names(entity_names=sample_names)
        # getting data from the Sequencing Sample fields for the output dataframe
        # 1. getting Sequencing Date
        qc_df['Sequencing Date'] = [sample.fields.additional_properties['Date'].display_value
                                    for sample in sample_objects]
        # 2. getting Top-off.
        # if Top-off is None or empty string add No, else add Yes
        qc_df['Top-off'] = ['No'
                            if sample.fields.additional_properties['Top-off'].display_value is None
                               or
                               sample.fields.additional_properties['Top-off'].display_value == ''
                            else 'Yes'
                            for sample in sample_objects]
        # 3. getting Top-off Target Sample
        qc_df['Top-off Target Sample'] = [sample.fields.additional_properties['Top-off'].display_value
                                          for sample in sample_objects]
        # 4. getting Reseq
        # if Reseq is None or empty string add No, else add Yes
        qc_df['Reseq'] = ['No'
                          if sample.fields.additional_properties['Reseq'].display_value is None
                             or
                             sample.fields.additional_properties['Reseq'].display_value == ''
                          else 'Yes'
                          for sample in sample_objects]

        # getting Specimen objects from the Starting NGS Sample field of the Sequencing Sample
        specimen_objects = []
        for sample_object in sample_objects:
            specimen_objects.append(
                self.get_entity_by_name(entity_id=sample_object.fields.additional_properties[
                    'Starting NGS Sample'].display_value))
        # getting data from the Specimen fields for the output dataframe
        # 1. getting Tissue
        qc_df['Tissue'] = [specimen.fields.additional_properties['Tissue'].display_value
                           for specimen in specimen_objects]
        # 2. getting Input Material Type
        qc_df['Input Material Type'] = [specimen.fields.additional_properties['Specimen Type'].display_value
                                        for specimen in specimen_objects]
        # 3. getting Tumor/Normal
        qc_df['Tumor/Normal'] = [specimen.fields.additional_properties['Tumor/Normal'].display_value
                                 for specimen in specimen_objects]
        # getting Extraction objects from the Extraction(s) field of the Sequencing Sample
        extraction_objects = []
        for sample_object in sample_objects:
            extraction_objects.append(
                self.get_entity_by_name(entity_id=sample_object.fields.additional_properties[
                    'Extraction(s)'].display_value))
        # getting data from the Extraction fields for the output dataframe
        # 1. getting Library Probe Set Kit
        qc_df['Library Probe Set Kit'] = [extraction.fields.additional_properties['Probeset Used'].display_value
                                          for extraction in extraction_objects]
        # getting QC0 objects for every Sequencing Sample
        qc0_objects = []
        for sample_object in sample_objects:
            qc0_objects_for_sample = self.get_results_by_schema_field_to_list(
                schema_id=self.schema_ids['qc0_schema_id'],
                entity_ids=[sample_object.id],
            )
            if qc0_objects_for_sample:
                # getting the latest filled QC0 object
                qc0_latest_filled_object = get_first_object_with_filled_field(
                    qc0_objects_for_sample,
                    field_name='Index Distr',
                )
                qc0_objects.append(qc0_latest_filled_object)
            else:
                qc0_objects.append(None)
        # getting data from the QC0 fields for the output dataframe
        # 1. getting RNA_Distr_QC
        qc_df['RNA_Distr_QC'] = [qc0.fields.additional_properties['index_distr'].display_value
                                 if qc0 is not None
                                 else None
                                 for qc0 in qc0_objects]
        return qc_df

    def lab_qc_report(self, run_name: str) -> pd.DataFrame:
        """
        Get data from Benchling for Lab QC project.
        This functions calls several Benchling entities to obtain data for the Lab QC report.
        Entities being called:
         Sequencing Sample, Extraction, Specimen, Library, R&D Case, PreCap, PostCap, Extraction QC.
        :param run_name: name of the run in  Benchling
        :return: dataframe with LabQC data from Benchling
        """
        # create output dataframe
        lab_qc_df = pd.DataFrame(columns=['Sequencing Sample', 'Sequencing Run', 'Extraction', 'Library',
                                          'PreCap Conc, ng/ul', 'PostCap Conc, nM', 'PostCap Size, bp',
                                          'Patient', 'Case (RS)', 'Tumor/Normal', 'Input Material Type',
                                          'Project', 'Extraction Kit', 'Library Prep Kit', 'Library Probe Set Kit',
                                          'Specimen', 'Extraction conc, ng/ul', 'RIN/DIN', 'DV200',
                                          'Frag DNA Conc, ng/ul', 'Frag DNA Peak Size, bp',
                                          'Input Into Library Prep, ng'])
        # get Sequencing Sample objects for the given run name
        sequencing_samples = self.get_sequencing_samples_by_run_name(run_name=run_name)

        # get Sequencing Sample names
        sequencing_samples_names = [sequencing_sample.name for sequencing_sample in sequencing_samples]
        # get Extraction names for the Sequencing Samples
        extraction_names = get_field_from_objects_list(sequencing_samples, 'Extraction(s)')
        # get Library names for the Sequencing Samples
        library_names = get_field_from_objects_list(sequencing_samples, 'Library')
        # get Specimen names for the Sequencing Samples
        specimen_names = get_field_from_objects_list(sequencing_samples, 'Starting NGS Sample')
        # putting names into the output dataframe
        lab_qc_df['Sequencing Sample'] = sequencing_samples_names
        lab_qc_df['Sequencing Run'] = run_name
        lab_qc_df['Extraction'] = extraction_names
        lab_qc_df['Library'] = library_names

        # getting Library objects for the Sequencing Samples
        library_objects = self.get_entities_by_names(entity_names=library_names)
        # getting PreCap objects for the Sequencing Samples
        pre_cap_objects = self.getting_results_and_latest_filled_one_for_entities(
            library_objects,
            self.schema_ids['pre_cap_schema_id'],
            'd1000_conc_ngul',
        )
        # getting data from the PreCap fields for the output dataframe
        # 1. getting PreCap Conc, ng/ul
        lab_qc_df['PreCap Conc, ng/ul'] = get_field_from_objects_list(pre_cap_objects, 'd1000_conc_ngul')

        # getting PostCap objects for the Sequencing Samples for Conc
        post_cap_objects = self.getting_results_and_latest_filled_one_for_entities(
            library_objects,
            self.schema_ids['post_cap_schema_id'],
            'd1000_region_mol_nm',
        )
        # getting Post Cap Conc data from the PostCap fields for the output dataframe
        lab_qc_df['PostCap Conc, nM'] = get_field_from_objects_list(post_cap_objects, 'd1000_region_mol_nm')
        # getting PostCap objects for the Sequencing Samples for Size
        post_cap_objects = self.getting_results_and_latest_filled_one_for_entities(
            library_objects,
            self.schema_ids['post_cap_schema_id'],
            'd1000_size_bp',
        )
        # getting Post Cap Size data from the PostCap fields for the output dataframe
        lab_qc_df['PostCap Size, bp'] = get_field_from_objects_list(post_cap_objects, 'd1000_size_bp')

        # getting Specimen objects for the Sequencing Samples from list of Specimen names
        specimen_objects = self.get_entities_by_names(entity_names=specimen_names)

        # getting data from the Specimen fields for the output dataframe
        # 1. getting RS Case
        case_names = get_field_from_objects_list(specimen_objects, 'R&D Case')
        lab_qc_df['Case (RS)'] = case_names
        # 2. getting Patient from Case
        # getting Case objects for the Specimens
        case_objects = self.get_entities_by_names(entity_names=case_names)
        # getting Patient data from the Case fields for the output dataframe
        lab_qc_df['Patient'] = get_field_from_objects_list(case_objects, 'Patient')
        # 3. getting Tumor/Normal
        lab_qc_df['Tumor/Normal'] = get_field_from_objects_list(specimen_objects, 'Tumor/Normal')
        # 4. getting Input Material Type
        lab_qc_df['Input Material Type'] = get_field_from_objects_list(specimen_objects, 'Specimen Type')

        # getting Extraction objects for the Sequencing Samples from list of Extraction names
        extraction_objects = self.get_entities_by_names(entity_names=extraction_names)
        # getting data from the Extraction fields for the output dataframe
        # 1. getting Project
        lab_qc_df['Project'] = get_field_from_objects_list(extraction_objects, 'Project')
        # 2. getting Extraction Kit
        lab_qc_df['Extraction Kit'] = get_field_from_objects_list(extraction_objects, 'Extraction Protocol')
        # 3. getting Library Prep Kit
        lab_qc_df['Library Prep Kit'] = get_field_from_objects_list(extraction_objects, 'Library Protocol')
        # 4. getting Library Probe Set Kit
        lab_qc_df['Library Probe Set Kit'] = get_field_from_objects_list(extraction_objects, 'Probeset Used')
        # 5. getting Extraction conc, ng/ul
        lab_qc_df['Extraction conc, ng/ul'] = get_field_from_objects_list(extraction_objects, 'Extract Conc (ng/uL)')
        # 6. getting DV200
        lab_qc_df['DV200'] = get_field_from_objects_list(extraction_objects, 'DV200')
        # 7. getting Frag DNA Conc, ng/ul
        lab_qc_df['Frag DNA Conc, ng/ul'] = get_field_from_objects_list(extraction_objects, 'Frag DNA conc (ng/ul)')
        # 8. getting Frag DNA Peak Size, bp
        lab_qc_df['Frag DNA Peak Size, bp'] = get_field_from_objects_list(extraction_objects, 'Frag DNA peak size (bp')
        # 9. getting Input Into Library Prep, ng
        lab_qc_df['Input Into Library Prep, ng'] = get_field_from_objects_list(extraction_objects,
                                                                               'Input into library prep (ng)')
        # getting Extraction QC objects for the Sequencing Samples
        extraction_qc_objects = self.getting_results_and_latest_filled_one_for_entities(
            extraction_objects,
            self.schema_ids['extraction_qc_schema_id'],
            'rindin',
        )
        # getting data from the Extraction QC fields for the output dataframe
        # 1. getting RIN/DIN
        lab_qc_df['RIN/DIN'] = get_field_from_objects_list(extraction_qc_objects, 'rindin')
        return lab_qc_df

    def get_sequencing_samples_by_run_name(self, run_name=None) -> list[CustomEntity]:
        """
        Get Sequencing Sample names for the given run name.
        :param run_name: name of the run in  Benchling
        :return: list of Sequencing Sample names
        """
        # get run id in Benchling by run name
        run_id = self.get_entity_by_name(entity_name=run_name).id
        # get Sequencing Sample objects for the run
        sequencing_samples = self.get_entities_by_schema_and_fields(
            schema_id=self.schema_ids['sequencing_sample_schema_id'],
            fields_dict={'Sequencing Run': run_id})
        return sequencing_samples

    def getting_results_and_latest_filled_one_for_entities(
            self, input_objects: list, schema_id: str, field_name: str
    ) -> list[AssayResult | None]:
        """
        Get the list of field values from the list of objects.
        :param input_objects: list of entities to get the results for
        :param schema_id: id of the Results schema
        :param field_name: name of the field that should be filled in the Results
        :return:
        """
        output_objects = []
        for input_object in input_objects:
            output_objects_for_input_object = self.get_results_by_schema_field_to_list(
                schema_id=schema_id,
                entity_ids=[input_object.id],
            )
            if output_objects_for_input_object:
                # getting the latest filled Extraction QC object
                output_object_latest_filled = get_first_object_with_filled_field(
                    output_objects_for_input_object,
                    field_name=field_name,
                )
                output_objects.append(output_object_latest_filled)
            else:
                output_objects.append(None)
        return output_objects


def get_entity_name(entity: CustomEntity) -> str:
    """
    Get the name of the entity.

    :param: entity - benchling entity.
    :return: entity name - name of the entity
    """
    try:
        return entity.name
    except IndexError:
        raise ValueError("Can not get entity name")


def get_entity_id(entity: CustomEntity) -> str:
    """
    Get the entity id of the entity.

    :param: entity - benchling entity.
    :return: entity id - entity id of the entity
    """
    try:
        return entity.id
    except IndexError:
        raise ValueError("Can not get entity id")


def get_field_value(entity: CustomEntity, field_name: str) -> str:
    """
    Get the value of the field with the given name.

    :param: entity - benchling entity
    :param: field_name - name of the field.
    :return: field value - value of the field with the given name
    """
    try:
        return entity.fields.additional_properties[field_name].value
    except IndexError:
        raise ValueError(f"Can not get field value for {field_name}")


def get_display_field_value(entity: CustomEntity, field_name: str) -> str:
    """
    Get the display value of the field with the given name.

    :param: entity - benchling entity
    :param: field_name - name of the field.
    :return: field display value - display value of the field with the given name
    """
    try:
        return entity.fields.additional_properties[field_name].display_value
    except IndexError:
        raise ValueError(f"Can not get field display value for {field_name}")


def get_empty_entity_fields(entity: CustomEntity) -> list:
    """
    Get empty fields (value=None) for a given CustomEntity.

    :param entity: benchling custom entity
    @type entity: models.CustomEntity
    :return: names of the empty fields for a given entity
    @rtype: list
    """
    empty_entity_fields = []
    for field_name, field_value in entity.fields.to_dict().items():
        if field_value["value"] in (None, []):  # [] for multi-select fields
            empty_entity_fields.append(field_name)

    return empty_entity_fields


def fields_dict_converter(fields_dict: dict) -> dict:
    """
    Convert the fields_dict without "value" keyword
    to the format of {field_name: {'value': field_value}}.

    :param: fields_dict - fields to update in the format of {field_name: field_value}
    :return: converted fields_dict
    """
    converted_fields_dict = {}
    for field_name, field_value in fields_dict.items():
        converted_fields_dict[field_name] = {"value": field_value}
    return converted_fields_dict


def construct_dropdown_update(
        dropdown_options: dict,
) -> list[models.DropdownOptionUpdate]:
    """
    Construct the list of existing dropdown options for dropdown updating.

    :param dropdown_options: dict with key - option name, value - option api id
    @type dropdown_options: dict
    :return: list of existing dropdown options for dropdown updating
    @rtype: list[models.DropdownOptionUpdate]
    """
    return [
        models.DropdownOptionUpdate(id=id_, name=name)
        for name, id_ in dropdown_options.items()
    ]


def construct_assay_result(
        schema_id: str, fields_dict: dict, project_id: str
) -> models.AssayResultCreate:
    """
    Construct the assay result with the given schema_id and fields_dict for push to Benchling.
    :param: schema_id - id of the assay result schema
    :param: fields_dict - fields to update in the format of {field_name: field_value}
    :param: project_id - id of the project to push the assay result to
    :return: assay result - constructed assay result
    """
    assay_result = models.AssayResultCreate(
        schema_id=schema_id,
        fields=fields(fields_dict_converter(fields_dict)),
        project_id=project_id,
    )
    return assay_result


def chunking(lst: list):
    """
    Chunking the list into chunks of 100 elements.
    :param lst:
    """
    for i in range(0, len(lst), 100):
        yield lst[i: i + 100]


def flatten(list_of_lists: list | PageIterator):
    """
    Flatten a list of lists.
    :param list_of_lists:
    :return: flat list
    """
    return [item for sublist in list_of_lists for item in sublist]


def get_first_object_with_filled_field(
        entities: list, field_name: str
) -> CustomEntity | AssayResult | None:
    """
    Return first object from list with filled field
    :param entities: list of objects
    :param field_name: field name
    :return: first object from list with filled field
    """
    entities = sort_entities_by_modified(entities)
    # Objects are sorted by modified date field in ascending order,
    # so we have to reverse the list to get the latest object
    for ent in entities:
        # if requested field is not None
        field_value = ent.fields.additional_properties[field_name].text_value
        if field_value is not None and field_value != "":
            return ent
    return None


def sort_entities_by_modified(entities: list) -> list:
    """
    Sort entities by modified date field in ascending order
    :param entities: list of entities
    :return: list of entities sorted by modified date field in descending order: last modified entity is first.
    """

    sorted_entities = sorted(
        entities,
        key=lambda entity: entity.additional_properties["modifiedAt"],
        reverse=True,
    )
    return sorted_entities


# mapping specimen type to FF and FFPE
def map_sample_type_to_preservation_method(sample_type: list[str]) -> list[str]:
    """
    Maps the sample type to the preservation method
    :param sample_type:
    """
    specimen_type_mapping = {
        "FFPE": ["FPB",
                 "HE",
                 "FPS",
                 "FPR",
                 "FPSC",
                 "FPD"],

        "FF": ["FFLI",
               "FL",
               "FF",
               "WB",
               "PB",
               "BC",
               "S",
               "F",
               "R",
               "D",
               "PBL"]
    }

    sample_preservation_method = []
    # now we should iteratively map the sample type to the preservation method according to specimen_type_mapping
    # if the sample type is not found in the mapping, we will return the sample type as is
    for sample in sample_type:
        for preservation_method, sample_types in specimen_type_mapping.items():
            if sample in sample_types:
                sample_preservation_method.append(preservation_method)
                break
        else:
            sample_preservation_method.append(sample)

    return sample_preservation_method


def filter_sequencing_samples(sequencing_samples: list[list[list[CustomEntity]]], mode='cfDNA'
                              ) -> list[list[list[CustomEntity]]]:
    """
    Filter sequencing samples by the following criteria:
    If the .name of the  sequencing sample CustomEntity starts with cfDNA, then keep it.
    In other cases, remove the CustomEntity from the list.
    :param sequencing_samples:
    :param mode: which team needs the filtration
    :return:
    """
    if mode == 'cfDNA':
        filtered_sequencing_samples = []
        for sequencing_samples_for_case in sequencing_samples:
            filtered_sequencing_samples_for_case = []
            for sequencing_samples_for_specimen in sequencing_samples_for_case:
                filtered_sequencing_samples_for_specimen = []
                for sequencing_sample in sequencing_samples_for_specimen:
                    if sequencing_sample.name.startswith('cfDNA'):
                        filtered_sequencing_samples_for_specimen.append(sequencing_sample)
                filtered_sequencing_samples_for_case.append(filtered_sequencing_samples_for_specimen)
            filtered_sequencing_samples.append(filtered_sequencing_samples_for_case)
        return filtered_sequencing_samples
    else:
        return sequencing_samples


def get_sequencing_sample_names_and_runs(sequencing_samples: list[list[list[CustomEntity]]]
                                         ) -> tuple[list[list[list[str]]], list[list[list[str]]]]:
    """
    Get sequencing sample names and runs from Sequencing Sample objects.
    :param sequencing_samples:
    :return:
    """
    sequencing_sample_names = []
    sequencing_sample_runs = []
    for sequencing_samples_for_case in sequencing_samples:
        sequencing_sample_names_for_case = []
        sequencing_sample_runs_for_case = []
        for sequencing_samples_for_specimen in sequencing_samples_for_case:
            sequencing_sample_names_for_specimen = []
            sequencing_sample_runs_for_specimen = []
            for sequencing_sample in sequencing_samples_for_specimen:
                sequencing_sample_names_for_specimen.append(sequencing_sample.name)
                sequencing_sample_runs_for_specimen.append(
                    get_field_value(sequencing_sample, 'Sequencing Run'))
            sequencing_sample_names_for_case.append(sequencing_sample_names_for_specimen)
            sequencing_sample_runs_for_case.append(sequencing_sample_runs_for_specimen)
        sequencing_sample_names.append(sequencing_sample_names_for_case)
        sequencing_sample_runs.append(sequencing_sample_runs_for_case)
    return sequencing_sample_names, sequencing_sample_runs


def get_field_from_objects_list(objects: list[CustomEntity|AssayResult], field_name: str) -> list:
    """
    Get the list of field values from the list of objects.
    :param objects:
    :param field_name:
    :return:
    """
    field_values = [get_display_field_value(obj, field_name)
                    if get_display_field_value(obj, field_name) is not None
                       and get_display_field_value(obj, field_name) != ''
                    else None
                    for obj in objects]
    return field_values
