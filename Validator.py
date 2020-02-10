import fastjsonschema as fjs
import json
import os
import sys
import traceback

SCRIPT_DIRECTORY = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
DATABASE_SCHEMA_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, "Schemas/DatabaseSchemas")
MISC_SCHEMA_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, "Schemas/SupportingSchemas")


def load_json_file(path):
    print(path)
    with open(path) as json_file:
        return json.load(json_file)


DATABASES = {
    name: load_json_file(os.path.join(SCRIPT_DIRECTORY, name))
    for name in os.listdir(SCRIPT_DIRECTORY)
    if name.endswith(".json")
}

DATABASE_SCHEMAS = {
    name: load_json_file(os.path.join(DATABASE_SCHEMA_DIRECTORY, name))
    for name in os.listdir(DATABASE_SCHEMA_DIRECTORY)
    if name.endswith(".schema.json")
}

MISC_SCHEMAS = {
    name: load_json_file(os.path.join(MISC_SCHEMA_DIRECTORY, name))
    for name in os.listdir(MISC_SCHEMA_DIRECTORY)
    if name.endswith(".schema.json")
}

def get_schema(schema_name):
    # print(schema_name)
    schema_name = schema_name.split('/')[-1]
    if schema_name in MISC_SCHEMAS:
        return MISC_SCHEMAS[schema_name]

    elif schema_name in DATABASE_SCHEMAS:
        return DATABASE_SCHEMAS[schema_name]

    raise Exception(f'Unable to find schema {schema_name}')

handlers = {'': get_schema}

for database_name, database in DATABASES.items():
    database_base_name = database_name.replace('.json', '')
    database_schema_name = database_base_name + '.schema.json'
    database_schema = DATABASE_SCHEMAS.get(database_schema_name)

    if not database_schema:
        print(f'No schema for {database_name}, skipping validation.')
        continue

    try:
        fjs.validate(database_schema, database, handlers=handlers)

    except fjs.JsonSchemaException as jsce:
        print(f'Validating database {database_name} with schema {database_schema_name}')
        with open(os.path.join(SCRIPT_DIRECTORY, 'generated'), 'w') as tmp_gen:
            tmp_gen.write(fjs.compile_to_code(database_schema, handlers=handlers))
        traceback.print_exc()
        print(f'path={jsce.path}')
        print()

    except Exception as e:
        print(f'Validating database {database_name} with schema {database_schema_name}')
        traceback.print_exc()
        print()
