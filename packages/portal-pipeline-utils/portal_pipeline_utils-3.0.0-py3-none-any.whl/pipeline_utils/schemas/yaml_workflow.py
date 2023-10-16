from pipeline_utils.schemas import schema

yaml_workflow_schema = {
    ## Schema #########################
    schema.SCHEMA: 'https://json-schema.org/draft/2020-12/schema',
    schema.ID: '/schemas/YAMLWorkflow',
    schema.TITLE: 'YAMLWorkflow',
    schema.DESCRIPTION: 'Schema to validate a YAML description of a Workflow',
    schema.TYPE: schema.OBJECT,
    schema.PROPERTIES: {

        ## Workflow information #######
        'name': {
            schema.DESCRIPTION: 'Name of the Workflow',
            schema.TYPE: schema.STRING
        },
        'title': {
            schema.DESCRIPTION: 'Title of the Workflow',
            schema.TYPE: schema.STRING
        },
        'description': {
            schema.DESCRIPTION: 'Description of the Workflow',
            schema.TYPE: schema.STRING
        },
        'runner': {
            schema.DESCRIPTION: 'Workflow description in standard language',
            schema.TYPE: schema.OBJECT,
            schema.PROPERTIES: {
                'language': {
                    schema.DESCRIPTION: 'Language used in Workflow description',
                    schema.TYPE: schema.STRING,
                    schema.PATTERN: '[wW][dD][lL]|[cC][wW][lL]'
                },
                'main': {
                    schema.DESCRIPTION: 'Main description file',
                    schema.TYPE: schema.STRING,
                    schema.PATTERN: '.+\.cwl|.+\.wdl'
                },
                'child': {
                    schema.DESCRIPTION: 'Supplementary description files used by main',
                    schema.TYPE: schema.ARRAY,
                    schema.ITEMS: {
                        schema.TYPE: schema.STRING,
                        schema.PATTERN: '.+\.cwl|.+\.wdl'
                    }
                }
            },
            schema.REQUIRED: ['language', 'main']
        },
        'software': {
            schema.DESCRIPTION: 'List of software used in the Workflow',
            schema.TYPE: schema.ARRAY,
            schema.ITEMS: {
                schema.TYPE: schema.STRING,
                schema.PATTERN: '.+\@.+' # check for <name>@<version>
            }
        },

        ## Input information ##########
        'input': {
            schema.DESCRIPTION: 'Input files and parameters',
            schema.TYPE: schema.OBJECT,
            schema.PATTERNPROPERTIES: {
                '.+': {schema.REF: '/schemas/argument'}
            }
        },

        ## Output information #########
        'output': {
            schema.DESCRIPTION: 'Output files and quality controls',
            schema.TYPE: schema.OBJECT,
            schema.PATTERNPROPERTIES: {
                '.+': {schema.REF: '/schemas/argument'}
            }
        }
    },
    schema.REQUIRED: ['name', 'description', 'runner', 'input', 'output'],

    ## Sub-schemas ####################
    schema.DEFS: {
        'argument': {
            schema.SCHEMA: 'https://json-schema.org/draft/2020-12/schema',
            schema.ID: '/schemas/argument',
            schema.TYPE: schema.OBJECT,
            schema.PROPERTIES: {
                'argument_type': {
                    schema.TYPE: schema.STRING,
                    schema.PATTERN: '^file\..+|^parameter\..+|^qc\..+|^report\..+'
                },
                'secondary_files': {
                    schema.TYPE: schema.ARRAY,
                    schema.ITEMS: {
                        schema.TYPE: schema.STRING
                    }
                }
            },
            schema.REQUIRED: ['argument_type'],

            ## qc specific ############
            schema.IF: {
                schema.TYPE: schema.OBJECT,
                schema.PROPERTIES: {
                    'argument_type': {
                        schema.PATTERN: '^qc\..+'
                    }
                },
            },
            schema.THEN: {
                schema.PROPERTIES: {
                    'argument_to_be_attached_to': {
                        schema.TYPE: schema.STRING
                    },
                    'zipped': {
                        schema.TYPE: schema.BOOLEAN
                    },
                    'html': {
                        schema.TYPE: schema.BOOLEAN
                    },
                    'json': {
                        schema.TYPE: schema.BOOLEAN
                    },
                    'table': {
                        schema.TYPE: schema.BOOLEAN
                    },
                    'html_in_zipped': {
                        schema.TYPE: schema.STRING
                    },
                    'tables_in_zipped': {
                        schema.TYPE: schema.ARRAY,
                        schema.ITEMS: {
                            schema.TYPE: schema.STRING
                        }
                    }
                },
                schema.REQUIRED: ['argument_to_be_attached_to']
            },
        }
    }
}
