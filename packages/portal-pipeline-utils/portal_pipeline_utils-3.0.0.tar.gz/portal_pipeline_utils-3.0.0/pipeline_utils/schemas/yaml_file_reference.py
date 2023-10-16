from pipeline_utils.schemas import schema

yaml_file_reference_schema = {
    ## Schema #########################
    schema.SCHEMA: 'https://json-schema.org/draft/2020-12/schema',
    schema.ID: '/schemas/YAMLFileReference',
    schema.TITLE: 'YAMLFileReference',
    schema.DESCRIPTION: 'Schema to validate a YAML description of a FileReference',
    schema.TYPE: schema.OBJECT,
    schema.PROPERTIES: {
        'name': {
            schema.DESCRIPTION: 'Name of the FileReference',
            schema.TYPE: schema.STRING
        },
        'description': {
            schema.DESCRIPTION: 'Description of the FileReference',
            schema.TYPE: schema.STRING
        },
        'format': {
            schema.DESCRIPTION: 'Format of the FileReference',
            schema.TYPE: schema.STRING
        },
        'version': {
            schema.DESCRIPTION: 'Version of the FileReference',
            schema.TYPE: schema.STRING
        },
        'status': {
            schema.DESCRIPTION: 'Status of the upload of the FileReference',
            schema.TYPE: schema.STRING,
            schema.PATTERN: 'uploading|uploaded'
        },
        'secondary_files': {
            schema.DESCRIPTION: 'Secondary files for the FileReference',
            schema.TYPE: schema.ARRAY,
            schema.ITEMS: {
                schema.TYPE: schema.STRING
            }
        },
        'license': {
            schema.DESCRIPTION: 'License of the FileReference',
            schema.TYPE: schema.STRING
        }
    },
    schema.REQUIRED: ['name', 'description', 'format', 'version']
}
