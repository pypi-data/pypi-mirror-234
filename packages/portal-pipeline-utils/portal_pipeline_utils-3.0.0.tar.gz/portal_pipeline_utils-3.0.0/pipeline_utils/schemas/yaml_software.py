from pipeline_utils.schemas import schema

yaml_software_schema = {
    ## Schema #########################
    schema.SCHEMA: 'https://json-schema.org/draft/2020-12/schema',
    schema.ID: '/schemas/YAMLSoftware',
    schema.TITLE: 'YAMLSoftware',
    schema.DESCRIPTION: 'Schema to validate a YAML description of a Software',
    schema.TYPE: schema.OBJECT,
    schema.PROPERTIES: {
        'name': {
            schema.DESCRIPTION: 'Name of the Software',
            schema.TYPE: schema.STRING
        },
        'title': {
            schema.DESCRIPTION: 'Title of the Software',
            schema.TYPE: schema.STRING
        },
        'source_url': {
            schema.DESCRIPTION: 'Source url of the Software',
            schema.TYPE: schema.STRING,
            schema.FORMAT: 'uri',
            schema.PATTERN: '^https?\:.+'
        },
        'description': {
            schema.DESCRIPTION: 'Description of the Software',
            schema.TYPE: schema.STRING
        },
        'version': {
            schema.DESCRIPTION: 'Version of the Software',
            schema.TYPE: schema.STRING
        },
        'commit': {
            schema.DESCRIPTION: 'Commit of the Software',
            schema.TYPE: schema.STRING
        },
        'license': {
            schema.DESCRIPTION: 'License of the Software',
            schema.TYPE: schema.STRING
        }
    },
    schema.REQUIRED: ['name'],
    schema.ONEOF: [
        {schema.REQUIRED: ['version']},
        {schema.REQUIRED: ['commit']}
    ]
}
