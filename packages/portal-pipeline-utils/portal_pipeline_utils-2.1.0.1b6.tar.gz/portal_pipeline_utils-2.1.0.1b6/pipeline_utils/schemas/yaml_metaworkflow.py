from pipeline_utils.schemas import schema

yaml_metaworkflow_schema = {
    ## Schema #########################
    schema.SCHEMA: 'https://json-schema.org/draft/2020-12/schema',
    schema.ID: '/schemas/YAMLMetaWorkflow',
    schema.TITLE: 'YAMLMetaWorkflow',
    schema.DESCRIPTION: 'Schema to validate a YAML description of a MetaWorkflow',
    schema.TYPE: schema.OBJECT,
    schema.PROPERTIES: {

        ## MetaWorkflow information ###
        'name': {
            schema.DESCRIPTION: 'Name of the MetaWorkflow',
            schema.TYPE: schema.STRING
        },
        'title': {
            schema.DESCRIPTION: 'Title of the MetaWorkflow',
            schema.TYPE: schema.STRING
        },
        'description': {
            schema.DESCRIPTION: 'Description of the MetaWorkflow',
            schema.TYPE: schema.STRING
        },

        ## General input information ##
        'input': {
            schema.DESCRIPTION: 'Pipeline input, reference files, and general arguments',
            schema.TYPE: schema.OBJECT,
            schema.PATTERNPROPERTIES: {
                '.+': {schema.REF: '/schemas/argument'}
            }
        },

        # Workflows information ######
        'workflows': {
            schema.DESCRIPTION: 'Workflows information and their dependencies',
            schema.TYPE: schema.OBJECT,
            schema.PATTERNPROPERTIES: {
                '.+': {
                    schema.DESCRIPTION: 'Workflow information',
                    schema.TYPE: schema.OBJECT,
                    schema.PROPERTIES: {
                        'input': {
                            schema.DESCRIPTION: 'Workflow input and dependencies information',
                            schema.TYPE: schema.OBJECT,
                            schema.PATTERNPROPERTIES: {
                                '.+': {schema.REF: '/schemas/argument'}
                            }
                        },
                        'output': {
                            schema.DESCRIPTION: 'Workflow output information',
                            schema.TYPE: schema.OBJECT,
                            schema.PATTERNPROPERTIES: {
                                '.+': {schema.REF: '/schemas/argument-output'}
                            }
                        },
                        'version': {
                            schema.DESCRIPTION: 'Version to use for the Workflow',
                            schema.TYPE: schema.STRING
                        },
                        'dependencies': {
                            schema.DESCRIPTION: 'List of dependencies that need to be satisfied',
                            schema.TYPE: schema.ARRAY,
                            schema.ITEMS: {
                                schema.TYPE: schema.STRING
                            }
                        },
                        'shards': {
                            schema.DESCRIPTION: 'Shards structure to create for the step',
                            schema.TYPE: schema.ARRAY
                        }
                    },
                    schema.REQUIRED: ['input', 'config']
                }
            }
        }
    },
    schema.REQUIRED: ['name', 'description', 'input', 'workflows'],

    ## Sub-schemas ####################
    schema.DEFS: {
        'argument': {
            schema.SCHEMA: 'https://json-schema.org/draft/2020-12/schema',
            schema.ID: '/schemas/argument',
            schema.TYPE: schema.OBJECT,
            schema.PROPERTIES: {
                'argument_type': {
                    schema.TYPE: schema.STRING,
                    schema.PATTERN: '^file\..+|^parameter\..+'
                },
                'dimensionality': {
                    schema.TYPE: schema.NUMBER
                },
                'files': {
                    schema.TYPE: schema.ARRAY,
                    schema.ITEMS: {
                        schema.TYPE: schema.STRING,
                        schema.PATTERN: '.+\@.+' # check for <name>@<version>
                    }
                },
                'source': {
                    schema.TYPE: schema.STRING
                },
                'source_argument_name': {
                    schema.TYPE: schema.STRING
                },
                'scatter': {
                    schema.TYPE: schema.NUMBER
                },
                'gather': {
                    schema.TYPE: schema.NUMBER
                },
                'gather_input': {
                    schema.TYPE: schema.NUMBER
                },
                'input_dimension': {
                    schema.TYPE: schema.NUMBER
                },
                'extra_dimension': {
                    schema.TYPE: schema.NUMBER
                },
                'mount': {
                    schema.TYPE: schema.BOOLEAN
                },
                'rename': {
                    schema.TYPE: schema.STRING,
                    schema.PATTERN: '^formula\:.+'
                },
                'unzip': {
                    schema.TYPE: schema.STRING
                }
            },
            schema.REQUIRED: ['argument_type']
        },
        'argument-output': {
            schema.SCHEMA: 'https://json-schema.org/draft/2020-12/schema',
            schema.ID: '/schemas/argument-output',
            schema.TYPE: schema.OBJECT,
            schema.PROPERTIES: {
                'description': {
                    schema.TYPE: schema.STRING
                },
                'linkto_location': {
                    schema.TYPE: schema.ARRAY,
                    schema.ITEMS: {
                        schema.TYPE: schema.STRING
                    }
                },
                'file_type': {
                    schema.TYPE: schema.STRING
                },
                'higlass_file': {
                    schema.TYPE: schema.BOOLEAN
                },
                'variant_type': {
                    schema.TYPE: schema.STRING
                },
                'vcf_to_ingest': {
                    schema.TYPE: schema.BOOLEAN
                },
                's3_lifecycle_category': {
                    schema.TYPE: schema.STRING,
                    schema.PATTERN: 'short_term_access_long_term_archive|short_term_access|short_term_archive|long_term_access_long_term_archive|long_term_access|long_term_archive|no_storage|ignore'
                }
            },
            schema.REQUIRED: ['file_type']
        }
    }
}
