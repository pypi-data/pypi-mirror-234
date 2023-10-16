from pipeline_utils.schemas import schema

yaml_file_format_schema = {
    ## Schema #########################
    schema.SCHEMA: 'https://json-schema.org/draft/2020-12/schema',
    schema.ID: '/schemas/YAMLFileFormat',
    schema.TITLE: 'YAMLFileFormat',
    schema.DESCRIPTION: 'Schema to validate a YAML description of a FileFormat',
    schema.TYPE: schema.OBJECT,
    schema.PROPERTIES: {
        'name': {
            schema.DESCRIPTION: 'Name of the FileFormat',
            schema.TYPE: schema.STRING
        },
        'description': {
            schema.DESCRIPTION: 'Description of the FileFormat',
            schema.TYPE: schema.STRING
        },
        'extension': {
            schema.DESCRIPTION: 'Extension of the FileFormat',
            schema.TYPE: schema.STRING
        },
        'file_types': {
            schema.DESCRIPTION: 'File types that can use the FileFormat',
            schema.TYPE: schema.ARRAY,
            schema.ITEMS: {
                schema.TYPE: schema.STRING,
                schema.PATTERN: 'FileReference|FileProcessed|FileSubmitted|FileFastq'
            }
        },
        'status': {
            schema.TYPE: schema.STRING
        },
        'secondary_formats': {
            schema.DESCRIPTION: 'Secondary formats available for the FileFormat',
            schema.TYPE: schema.ARRAY,
            schema.ITEMS: {
                schema.TYPE: schema.STRING
            }
        }
    },
    schema.REQUIRED: ['name', 'description', 'extension']
}
