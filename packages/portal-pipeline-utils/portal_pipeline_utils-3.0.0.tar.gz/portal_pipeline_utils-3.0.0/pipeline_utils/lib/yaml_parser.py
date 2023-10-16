#!/usr/bin/env python3

###########################################################
#
#   yaml_parser
#      classes to parse portal objects in YAML format
#
#   Michele Berselli - berselli.michele@gmail.com
#
###########################################################

import sys
import yaml
import itertools
from jsonschema import Draft202012Validator


###############################################################
#   Schemas
###############################################################
from pipeline_utils.schemas.yaml_workflow import yaml_workflow_schema
from pipeline_utils.schemas.yaml_metaworkflow import yaml_metaworkflow_schema
from pipeline_utils.schemas.yaml_software import yaml_software_schema
from pipeline_utils.schemas.yaml_file_reference import yaml_file_reference_schema
from pipeline_utils.schemas.yaml_file_format import yaml_file_format_schema


###############################################################
#   Functions
###############################################################
def load_yaml(file):
    """Return a generator to YAML documents in file.
    """
    with open(file) as stream:
        try:
            for d in yaml.safe_load_all(stream):
                yield d
        except yaml.YAMLError as exc:
            sys.exit(exc)

def peek(iterable):
    """Function to check if an iterable is empty.
    If not empty return the complete iterator, else return None.
    """
    try:
        first = next(iterable)
    except StopIteration:
        return None

    return itertools.chain([first], iterable)


###############################################################
#   ValidationError
###############################################################
class ValidationError(Exception):
    """Custom Exception for error tracking in schema validation.
    """

    def __init__(self, errors):
        """Constructor method.

            :param errors: Errors from jsonschema.Validator.iter_errors()
            :type errors: Iterable[jsonschema.exceptions.ValidationError]
        """
        errors, errors_ = itertools.tee(errors)
        super().__init__(self._message(errors))
        self.errors = errors_

    def _message(self, errors):
        """Helper to create error message.
        """
        message = 'YAML object failed schema validation.\n'
        for error in errors:
            message += 'ValidationError [{0}]: {1} in path={2}, schema={3}\n'.format(
                            error.validator,
                            error.message,
                            error.relative_path,
                            error.schema
                            )
        return message

###############################################################
#   YAMLTemplate
###############################################################
class YAMLTemplate(object):
    """Template class to work with YAML documents representing pipeline components.
    """

    # schema constants
    NAME_SCHEMA = 'name'
    TITLE_SCHEMA = 'title'
    DESCRIPTION_SCHEMA = 'description'
    ALIASES_SCHEMA = 'aliases'
    PROJECT_SCHEMA = 'project'
    INSTITUTION_SCHEMA = 'institution'
    VERSION_SCHEMA = 'version'
    ACCESSION_SCHEMA = 'accession'
    UUID_SCHEMA = 'uuid'
    ARGUMENT_TYPE_SCHEMA = 'argument_type'
    ARGUMENT_FORMAT_SCHEMA = 'argument_format'
    ARGUMENT_NAME_SCHEMA = 'argument_name'
    VALUE_TYPE_SCHEMA = 'value_type'
    WORKFLOW_ARGUMENT_NAME_SCHEMA = 'workflow_argument_name'
    INPUT_SCHEMA = 'input'
    STATUS_SCHEMA = 'status'
    SECONDARY_FILES_SCHEMA = 'secondary_files'
    SECONDARY_FORMATS_SCHEMA = 'secondary_formats'
    FILE_FORMAT_SCHEMA = 'file_format'
    SECONDARY_FILE_FORMATS_SCHEMA = 'secondary_file_formats'
    INSTITUTIONS_SCHEMA = 'institutions'
    PROJECTS_SCHEMA = 'projects'
    FILE_SCHEMA = 'file'
    FILES_SCHEMA = 'files'
    PARAMETER_SCHEMA = 'parameter'
    LICENSE_SCHEMA = 'license'
    WORKFLOW_TYPE_SCHEMA = 'Workflow'
    METAWORKFLOW_TYPE_SCHEMA = 'MetaWorkflow'
    FILEFORMAT_TYPE_SCHEMA = 'FileFormat'
    FILEREFERENCE_TYPE_SCHEMA = 'FileReference'
    SOFTWARE_TYPE_SCHEMA = 'Software'

    def __init__(self, data, schema):
        """Constructor method.
        """
        self.data = data
        self.schema = schema

    def _validate(self):
        """Helper to validate the document against schema.
        """
        draft202012validator = Draft202012Validator(self.schema)
        errors = draft202012validator.iter_errors(self.data)
        errors_ = peek(errors)
        if errors_:
            raise ValidationError(errors_)

    def _clean_newline(self, line):
        """Helper to clean multiline docstrings from YAML block style indicator "|".
        """
        if ' |' in line:
            line = line.replace(' |', '')
        elif '|' in line:
            line = line.replace('|', '')
        return line

    def _link_title(self, name, version):
        """Helper to create a "title" field.
        """
        title = getattr(self, self.TITLE_SCHEMA, None)
        if title:
            if version in title:
                return title
            else:
                return f'{title} [{version}]'
        else:
            return f'{name.replace("_", " ")} [{version}]'

    def _link_institution(self, institution):
        """Helper to create an "institution" field.
        """
        return f'/{self.INSTITUTIONS_SCHEMA}/{institution}/'

    def _link_project(self, project):
        """Helper to create a "project" field.
        """
        return f'/{self.PROJECTS_SCHEMA}/{project}/'


###############################################################
#   YAMLWorkflow, YAML Workflow
###############################################################
class YAMLWorkflow(YAMLTemplate):
    """Class to work with YAML documents representing Workflow objects.
    """

    # schema constants
    INPUT_FILE_SCHEMA = 'Input file'
    OUTPUT_PROCESSED_FILE_SCHEMA = 'Output processed file'
    OUTPUT_QC_FILE_SCHEMA = 'Output QC file'
    GENERIC_QC_FILE_SCHEMA = 'Generic QC file'
    OUTPUT_REPORT_FILE_SCHEMA = 'Output report file'
    QC_SCHEMA = 'qc'
    QUALITY_METRIC_GENERIC_SCHEMA = 'quality_metric_generic'
    REPORT_SCHEMA = 'report'
    ARGUMENT_TO_BE_ATTACHED_TO_SCHEMA = 'argument_to_be_attached_to'
    ZIPPED_SCHEMA = 'zipped'
    HTML_SCHEMA = 'html'
    JSON_SCHEMA = 'json'
    TABLE_SCHEMA = 'table'
    APP_NAME_SCHEMA = 'app_name'
    APP_VERSION_SCHEMA = 'app_version'
    SOFTWARE_SCHEMA = 'software'
    ARGUMENTS_SCHEMA = 'arguments'
    QC_TYPE_SCHEMA = 'qc_type'
    QC_ZIPPED_SCHEMA = 'qc_zipped'
    QC_HTML_SCHEMA = 'qc_html'
    QC_JSON_SCHEMA = 'qc_json'
    QC_TABLE_SCHEMA = 'qc_table'
    QC_ZIPPED_HTML_SCHEMA = 'qc_zipped_html'
    QC_ZIPPED_TABLES_SCHEMA = 'qc_zipped_tables'
    HTML_IN_ZIPPED_SCHEMA = 'html_in_zipped'
    TABLES_IN_ZIPPED_SCHEMA = 'tables_in_zipped'
    QC_ACL = 'qc_acl'
    QC_UNZIP_FROM_EC2 = 'qc_unzip_from_ec2'

    def __init__(self, data):
        """Constructor method.
        """
        super().__init__(data, yaml_workflow_schema)
        # validate data with schema
        self._validate()
        # load attributes
        for key, val in data.items():
            if key in [self.DESCRIPTION_SCHEMA, self.TITLE_SCHEMA]:
                val = self._clean_newline(val)
            setattr(self, key, val)

    def _arguments_input(self):
        """Helper to parse input arguments and map to expected JSON structure.
        """
        arguments = []
        for name, values in self.input.items():
            type, format = values[self.ARGUMENT_TYPE_SCHEMA].split('.')
            if type == self.FILE_SCHEMA:
                argument_type = self.INPUT_FILE_SCHEMA
            elif type == self.PARAMETER_SCHEMA:
                argument_type = self.PARAMETER_SCHEMA
            argument_ = {
                self.ARGUMENT_TYPE_SCHEMA: argument_type,
                self.WORKFLOW_ARGUMENT_NAME_SCHEMA: name
                }
            # add format to file argument, TODO
            #   this can be improved in schema to handle a list of formats so no placeholder is needed
            if type == self.FILE_SCHEMA and format not in ['any']:
                # handle format placeholders,
                #   if format is not a placeholder add format field to argument
                argument_[self.ARGUMENT_FORMAT_SCHEMA] = format
            arguments.append(argument_)

        return arguments

    def _arguments_output(self):
        """Helper to parse output arguments and map to expected JSON structure.
        """
        arguments = []
        for name, values in self.output.items():
            type, format = values[self.ARGUMENT_TYPE_SCHEMA].split('.')
            if type == self.FILE_SCHEMA:
                argument_type = self.OUTPUT_PROCESSED_FILE_SCHEMA
                argument_ = {
                    self.ARGUMENT_FORMAT_SCHEMA: format,
                    self.ARGUMENT_TYPE_SCHEMA: argument_type,
                    self.WORKFLOW_ARGUMENT_NAME_SCHEMA: name,
                    self.SECONDARY_FILE_FORMATS_SCHEMA: values.get(self.SECONDARY_FILES_SCHEMA, [])
                }
            elif type == self.QC_SCHEMA:
                # handle generic vs specific QC schema
                if format == self.QUALITY_METRIC_GENERIC_SCHEMA:
                    argument_type = self.GENERIC_QC_FILE_SCHEMA
                else:
                    argument_type = self.OUTPUT_QC_FILE_SCHEMA
                # create base QC argument
                argument_ = {
                    self.ARGUMENT_TYPE_SCHEMA: argument_type,
                    self.WORKFLOW_ARGUMENT_NAME_SCHEMA: name,
                    self.ARGUMENT_TO_BE_ATTACHED_TO_SCHEMA: values[self.ARGUMENT_TO_BE_ATTACHED_TO_SCHEMA],
                    self.QC_ZIPPED_SCHEMA: values.get(self.ZIPPED_SCHEMA, False),
                    self.QC_HTML_SCHEMA: values.get(self.HTML_SCHEMA, False),
                    self.QC_JSON_SCHEMA: values.get(self.JSON_SCHEMA, False),
                    self.QC_TABLE_SCHEMA: values.get(self.TABLE_SCHEMA, False)
                }
                # handle edge case for missing or generic QC type
                if format not in ['none', self.QUALITY_METRIC_GENERIC_SCHEMA]:
                    argument_[self.QC_TYPE_SCHEMA] = format
                # create argument format for generic QCs (JSON or ZIP)
                elif format == self.QUALITY_METRIC_GENERIC_SCHEMA:
                    if argument_[self.QC_JSON_SCHEMA]:
                        argument_[self.ARGUMENT_FORMAT_SCHEMA] = 'json'
                    else:
                        argument_[self.ARGUMENT_FORMAT_SCHEMA] = 'zip'
                # quality controls, TODO
                #   these fields are bad, need to rework how QCs work
                if values.get(self.HTML_IN_ZIPPED_SCHEMA):
                    argument_[self.QC_ZIPPED_HTML_SCHEMA] = values[self.HTML_IN_ZIPPED_SCHEMA]
                if values.get(self.TABLES_IN_ZIPPED_SCHEMA):
                    argument_[self.QC_ZIPPED_TABLES_SCHEMA] = values[self.TABLES_IN_ZIPPED_SCHEMA]
                if values.get(self.QC_ACL):
                    argument_[self.QC_ACL] = values[self.QC_ACL]
                if values.get(self.QC_UNZIP_FROM_EC2):
                    argument_[self.QC_UNZIP_FROM_EC2] = values[self.QC_UNZIP_FROM_EC2]
            elif type == self.REPORT_SCHEMA and format == self.FILE_SCHEMA:
                argument_type = self.OUTPUT_REPORT_FILE_SCHEMA
                argument_ = {
                    self.ARGUMENT_TYPE_SCHEMA: argument_type,
                    self.WORKFLOW_ARGUMENT_NAME_SCHEMA: name
                }
            arguments.append(argument_)

        return arguments

    def to_json(
               self,
               version,
               institution, # alias
               project, # alias
               wflbucket_url
               ):
        """Function to build the corresponding object in JSON format.
        """
        wfl_json = {}

        # common metadata
        wfl_json[self.APP_NAME_SCHEMA] = self.name # name
        wfl_json[self.APP_VERSION_SCHEMA] = version # version
        wfl_json[self.NAME_SCHEMA] = f'{self.name}_{version}'
        wfl_json[self.TITLE_SCHEMA] = self._link_title(self.name, version)
        wfl_json[self.ALIASES_SCHEMA] = [f'{project}:{self.WORKFLOW_TYPE_SCHEMA}-{wfl_json[self.NAME_SCHEMA]}']
        wfl_json[self.INSTITUTION_SCHEMA] = self._link_institution(institution)
        wfl_json[self.PROJECT_SCHEMA] = self._link_project(project)
        wfl_json[self.DESCRIPTION_SCHEMA] = self.description
        wfl_json[self.SOFTWARE_SCHEMA] = [f'{project}:{self.SOFTWARE_TYPE_SCHEMA}-{s.replace("@", "_")}' for s in getattr(self, self.SOFTWARE_SCHEMA, [])]
        wfl_json[self.ARGUMENTS_SCHEMA] = self._arguments_input() + self._arguments_output()

        # workflow language (TODO)
        #   we need to improve tibanna to have a unique general key for this
        language = self.runner.get('language')
        if not language or language.lower() == 'cwl':
            wfl_json['cwl_directory_url_v1'] = wflbucket_url
            wfl_json['cwl_main_filename'] = self.runner['main']
            wfl_json['cwl_child_filenames'] = self.runner.get('child', [])
        elif language.lower() == 'wdl':
            wfl_json['wdl_directory_url'] = wflbucket_url
            wfl_json['wdl_main_filename'] = self.runner['main']
            wfl_json['wdl_child_filenames'] = self.runner.get('child', [])
            wfl_json['workflow_language'] = 'wdl'

        # uuid, accession if specified
        if getattr(self, self.UUID_SCHEMA, None):
            wfl_json[self.UUID_SCHEMA] = self.uuid
        if getattr(self, self.ACCESSION_SCHEMA, None):
            wfl_json[self.ACCESSION_SCHEMA] = self.accession

        return wfl_json


###############################################################
#   YAMLMetaWorkflow, YAML MetaWorkflow
###############################################################
class YAMLMetaWorkflow(YAMLTemplate):
    """Class to work with YAML documents representing MetaWorkflow objects.
    """

    # schema constants
    DIMENSION_SCHEMA = 'dimension'
    WORKFLOW_SCHEMA = 'workflow'
    WORKFLOWS_SCHEMA = 'workflows'
    CUSTOM_PF_FIELDS_SCHEMA = 'custom_pf_fields'
    OUTPUT_SCHEMA = 'output'
    CONFIG_SCHEMA = 'config'
    DEPENDENCIES_SCHEMA = 'dependencies'
    SHARDS_SCHEMA = 'shards'
    PROBAND_ONLY_SCHEMA = 'proband_only'

    def __init__(self, data):
        """Constructor method.
        """
        super().__init__(data, yaml_metaworkflow_schema)
        # validate data with schema
        self._validate()
        # load attributes
        for key, val in data.items():
            if key in [self.DESCRIPTION_SCHEMA, self.TITLE_SCHEMA]:
                val = self._clean_newline(val)
            setattr(self, key, val)

    def _arguments(self, input, project):
        """Helper to parse arguments and map to expected JSON structure.
        """
        arguments = []
        for name, values in input.items():
            type, format = values[self.ARGUMENT_TYPE_SCHEMA].split('.')
            argument_ = {
                self.ARGUMENT_NAME_SCHEMA: name,
                self.ARGUMENT_TYPE_SCHEMA: type
            }
            if type == self.PARAMETER_SCHEMA:
                argument_[self.VALUE_TYPE_SCHEMA] = format
            for k, v in values.items():
                if k != self.ARGUMENT_TYPE_SCHEMA:
                    # handle files specifications, TODO
                    #   this system could be improved in how the schema works and deals with types
                    #
                    #   need to go from file name to dictionary of alias and dimension
                    #    files:
                    #        - foo@v1
                    #   ----- or -------
                    #        - foo@v1
                    #        - bar@v3
                    #   need to convert to:
                    #    files: [
                    #        {file: '<project>:FileReference-foo_v1'}
                    #       ]
                    #   ----- or -------
                    #    files: [
                    #        {file: '<project>:FileReference-foo_v1', dimension: '0'},
                    #        {file: '<project>:FileReference-bar_v3', dimension: '1'}
                    #       ]
                    if k == self.FILES_SCHEMA:
                        v_ = []
                        for i, name_ in enumerate(v):
                            v_.append({self.FILE_SCHEMA: f'{project}:{self.FILEREFERENCE_TYPE_SCHEMA}-{name_.replace("@", "_")}',
                                       self.DIMENSION_SCHEMA: str(i)})
                        # remove DIMENSION_SCHEMA field if only one file
                        if len(v_) == 1:
                            del v_[0][self.DIMENSION_SCHEMA]
                        argument_.setdefault(k, v_)
                    else:
                        argument_.setdefault(k, v)
            arguments.append(argument_)

        return arguments

    def _workflows(self, version, project):
        """Helper to parse workflow definitions and map to expected JSON structure.
        """
        workflows = []
        for name, values in self.workflows.items():
            # check if lock version
            #   if not use default version
            if values.get(self.VERSION_SCHEMA):
                version_ = values[self.VERSION_SCHEMA]
            else:
                version_ = version
            # basic JSON workflow structure
            workflow_ = {
                self.NAME_SCHEMA: name,
                self.WORKFLOW_SCHEMA: f'{project}:{self.WORKFLOW_TYPE_SCHEMA}-{name.split("@")[0]}_{version_}',
                                      # remove unique tag after @ to create the right alias to link
                self.INPUT_SCHEMA: self._arguments(values[self.INPUT_SCHEMA], project),
                self.CONFIG_SCHEMA: values[self.CONFIG_SCHEMA]
            }
            # file output can be optional
            #   QC workflows don't always have a file output
            if values.get(self.OUTPUT_SCHEMA):
                workflow_[self.CUSTOM_PF_FIELDS_SCHEMA] = values[self.OUTPUT_SCHEMA]
            # hard dependencies
            if values.get(self.DEPENDENCIES_SCHEMA):
                workflow_[self.DEPENDENCIES_SCHEMA] = values[self.DEPENDENCIES_SCHEMA]
            # fixed shards
            if values.get(self.SHARDS_SCHEMA):
                workflow_[self.SHARDS_SCHEMA] = values[self.SHARDS_SCHEMA]
            workflows.append(workflow_)

        return workflows

    def to_json(
               self,
               version,
               institution, # alias
               project # alias
               ):
        """Function to build the corresponding object in JSON format.
        """
        metawfl_json = {}

        # common metadata
        metawfl_json[self.NAME_SCHEMA] = self.name
        metawfl_json[self.VERSION_SCHEMA] = version # version
        metawfl_json[self.TITLE_SCHEMA] = self._link_title(self.name, version)
        metawfl_json[self.ALIASES_SCHEMA] = [f'{project}:{self.METAWORKFLOW_TYPE_SCHEMA}-{self.name}_{version}']
        metawfl_json[self.INSTITUTION_SCHEMA] = self._link_institution(institution)
        metawfl_json[self.PROJECT_SCHEMA] = self._link_project(project)
        metawfl_json[self.DESCRIPTION_SCHEMA] = self.description
        metawfl_json[self.INPUT_SCHEMA] = self._arguments(self.input, project)
        metawfl_json[self.WORKFLOWS_SCHEMA] = self._workflows(version, project)

        # proband_only field
        if getattr(self, self.PROBAND_ONLY_SCHEMA, None):
            metawfl_json[self.PROBAND_ONLY_SCHEMA] = self.proband_only

        # uuid, accession if specified
        if getattr(self, self.UUID_SCHEMA, None):
            metawfl_json[self.UUID_SCHEMA] = self.uuid
        if getattr(self, self.ACCESSION_SCHEMA, None):
            metawfl_json[self.ACCESSION_SCHEMA] = self.accession

        return metawfl_json


###############################################################
#   YAMLSoftware, YAML Software
###############################################################
class YAMLSoftware(YAMLTemplate):
    """Class to work with YAML documents representing Software objects.
    """

    # schema constants
    COMMIT_SCHEMA = 'commit'
    SOURCE_URL_SCHEMA = 'source_url'

    def __init__(self, data):
        """Constructor method.
        """
        super().__init__(data, yaml_software_schema)
        # validate data with schema
        self._validate()
        # load attributes
        for key, val in data.items():
            if key in [self.DESCRIPTION_SCHEMA, self.TITLE_SCHEMA]:
                val = self._clean_newline(val)
            setattr(self, key, val)

    def to_json(
               self,
               institution, # alias
               project # alias
               ):
        """Function to build the corresponding object in JSON format.
        """
        sftwr_json, version = {}, None

        # common metadata
        sftwr_json[self.NAME_SCHEMA] = self.name
        sftwr_json[self.INSTITUTION_SCHEMA] = self._link_institution(institution)
        sftwr_json[self.PROJECT_SCHEMA] = self._link_project(project)

        if getattr(self, self.VERSION_SCHEMA, None):
            sftwr_json[self.VERSION_SCHEMA] = self.version
            version = self.version
        else:
            sftwr_json[self.COMMIT_SCHEMA] = self.commit
            version = self.commit

        if getattr(self, self.DESCRIPTION_SCHEMA, None):
            sftwr_json[self.DESCRIPTION_SCHEMA] = self.description
        if getattr(self, self.SOURCE_URL_SCHEMA, None):
            sftwr_json[self.SOURCE_URL_SCHEMA] = self.source_url

        sftwr_json[self.TITLE_SCHEMA] = self._link_title(self.name, version)
        sftwr_json[self.ALIASES_SCHEMA] = [f'{project}:{self.SOFTWARE_TYPE_SCHEMA}-{self.name}_{version}']

        # uuid, accession if specified
        if getattr(self, self.UUID_SCHEMA, None):
            sftwr_json[self.UUID_SCHEMA] = self.uuid
        if getattr(self, self.ACCESSION_SCHEMA, None):
            sftwr_json[self.ACCESSION_SCHEMA] = self.accession

        # license
        if getattr(self, self.LICENSE_SCHEMA, None):
            sftwr_json[self.LICENSE_SCHEMA] = self.license

        return sftwr_json


###############################################################
#   YAMLFileReference, YAML FileReference
###############################################################
class YAMLFileReference(YAMLTemplate):
    """Class to work with YAML documents representing FileReference objects.
    """

    # schema constants
    EXTRA_FILES_SCHEMA = 'extra_files'

    def __init__(self, data):
        """Constructor method.
        """
        super().__init__(data, yaml_file_reference_schema)
        # validate data with schema
        self._validate()
        # load attributes
        for key, val in data.items():
            if key in [self.DESCRIPTION_SCHEMA]:
                val = self._clean_newline(val)
            setattr(self, key, val)

    def to_json(
               self,
               institution, # alias
               project # alias
               ):
        """Function to build the corresponding object in JSON format.
        """
        ref_json = {}

        # common metadata
        ref_json[self.INSTITUTION_SCHEMA] = self._link_institution(institution)
        ref_json[self.PROJECT_SCHEMA] = self._link_project(project)
        ref_json[self.DESCRIPTION_SCHEMA] = self.description
        ref_json[self.FILE_FORMAT_SCHEMA] = self.format
        ref_json[self.ALIASES_SCHEMA] = [f'{project}:{self.FILEREFERENCE_TYPE_SCHEMA}-{self.name}_{self.version}']
        ref_json[self.EXTRA_FILES_SCHEMA] = getattr(self, self.SECONDARY_FILES_SCHEMA, [])
        ref_json[self.STATUS_SCHEMA] = getattr(self, self.STATUS_SCHEMA, None) # this will be used during post/patch,
                                                           # if None:
                                                           #    - leave it as is if patch
                                                           #    - set to uploading if post

        # uuid, accession if specified
        if getattr(self, self.UUID_SCHEMA, None):
            ref_json[self.UUID_SCHEMA] = self.uuid
        if getattr(self, self.ACCESSION_SCHEMA, None):
            ref_json[self.ACCESSION_SCHEMA] = self.accession

        # license
        if getattr(self, self.LICENSE_SCHEMA, None):
            ref_json[self.LICENSE_SCHEMA] = self.license

        return ref_json


###############################################################
#   YAMLFileFormat, YAML FileFormat
###############################################################
class YAMLFileFormat(YAMLTemplate):
    """Class to work with YAML documents representing FileFormat objects.
    """

    # schema constants
    STANDARD_FILE_EXTENSION_SCHEMA = 'standard_file_extension'
    VALID_ITEM_TYPES_SCHEMA = 'valid_item_types'
    EXTRAFILE_FORMATS_SCHEMA = 'extrafile_formats'
    FILE_TYPES_SCHEMA = 'file_types'

    def __init__(self, data):
        """Constructor method.
        """
        super().__init__(data, yaml_file_format_schema)
        # validate data with schema
        self._validate()
        # load attributes
        for key, val in data.items():
            if key in [self.DESCRIPTION_SCHEMA]:
                val = self._clean_newline(val)
            setattr(self, key, val)

    def to_json(
               self,
               institution, # alias
               project # alias
               ):
        """Function to build the corresponding object in JSON format.
        """
        frmt_json = {}

        # common metadata
        frmt_json[self.FILE_FORMAT_SCHEMA] = self.name
        frmt_json[self.ALIASES_SCHEMA] = [f'{project}:{self.FILEFORMAT_TYPE_SCHEMA}-{self.name}']
        frmt_json[self.INSTITUTION_SCHEMA] = self._link_institution(institution)
        frmt_json[self.PROJECT_SCHEMA] = self._link_project(project)
        frmt_json[self.DESCRIPTION_SCHEMA] = self.description
        frmt_json[self.STANDARD_FILE_EXTENSION_SCHEMA] = self.extension
        frmt_json[self.VALID_ITEM_TYPES_SCHEMA] = getattr(self, self.FILE_TYPES_SCHEMA, ['FileReference', 'FileProcessed'])
        frmt_json[self.EXTRAFILE_FORMATS_SCHEMA] = getattr(self, self.SECONDARY_FORMATS_SCHEMA, [])
        frmt_json[self.STATUS_SCHEMA] = getattr(self, self.STATUS_SCHEMA, 'shared')

        # uuid, accession if specified
        if getattr(self, self.UUID_SCHEMA, None):
            frmt_json[self.UUID_SCHEMA] = self.uuid
        if getattr(self, self.ACCESSION_SCHEMA, None):
            frmt_json[self.ACCESSION_SCHEMA] = self.accession

        return frmt_json
