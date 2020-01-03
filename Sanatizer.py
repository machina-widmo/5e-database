#! venv/bin/python

import json
import os
import re
import sys
import logging

from fuzzywuzzy import fuzz, process

CUSTOM_DATABASE_SANATIZERS = {}
CUSTOM_DATABASE_SANATIZERS_POST_REF_FIXUP = {}

log = logging.getLogger(__file__)
log.setLevel(logging.ERROR)
log.addHandler(logging.StreamHandler(sys.stdout))

ENTRY_DESCRIPTOR = "entry_descriptor"


class DatabaseNameFinder():
    def __init__(self, databases_by_name):
        self.databases_by_name = databases_by_name
        self.database_name_list = list(databases_by_name.keys())
        self.names_by_database = {}

    @staticmethod
    def __EntryNameProcessor(entry):
            return entry if isinstance(entry, str) else entry[0]

    def FindBestEntryName(self, database_name, entry_name):
        entry_names = self.names_by_database.setdefault(database_name, [])
        if len(entry_names) == 0:
            entry_names = [
                (entry[ENTRY_DESCRIPTOR]["name"], enum_index)
                for enum_index, entry in enumerate(self.databases_by_name[database_name])
            ]

            self.names_by_database[database_name] = entry_names

        return process.extractOne(entry_name, entry_names, processor=DatabaseNameFinder.__EntryNameProcessor)

    def FindBestDatabaseName(self, database_name):
        return process.extractOne(database_name, self.database_name_list)

    def GetDatabaseFromName(self, database_name):
        return self.databases_by_name.get(database_name, None)

    def GetEntryFromUrl(self, url_parts):
        return self.databases_by_name[url_parts[1]][int(url_parts[2])]


def CustomDatabaseSanatizer(database_name):
    def Inner(func):
        def Wrapped(*args, **kwargs):
            assert database_name == args[1]
            return func(*args, **kwargs)

        CUSTOM_DATABASE_SANATIZERS[database_name] = Wrapped
        return Wrapped
    return Inner


def CustomDatabaseSanatizer_PostRefFixup(database_name):
    def Inner(func):
        def Wrapped(*args, **kwargs):
            assert database_name == args[1]
            return func(*args, **kwargs)

        CUSTOM_DATABASE_SANATIZERS_POST_REF_FIXUP[database_name] = Wrapped
        return Wrapped
    return Inner


def Noop(*args, **kwargs):
    return raw_json_data


@CustomDatabaseSanatizer("races")
def Sanatize_RacesDatabase(raw_json_data, database_name):
    for json_object in raw_json_data:
        ability_bonuses = json_object["ability_bonuses"]
        for ability_bonus in ability_bonuses:

            ability_bonus["ability"] = {}
            
            ability = ability_bonus["ability"]
            ability["name"] = ability_bonus["name"]
            ability["url"] = ability_bonus["url"]

            ability_bonus["value"] = ability_bonus["bonus"]
            del ability_bonus["name"]
            del ability_bonus["url"]
            del ability_bonus["bonus"]

    return raw_json_data

@CustomDatabaseSanatizer("features")
def Sanatize_FeaturesDatabase(raw_json_data, database_name):
    return raw_json_data

@CustomDatabaseSanatizer_PostRefFixup("traits")
def Sanatize_TraitsDatabase_PostRefFixup(raw_json_data, database_name, database_name_finder):
    pass


def FixupReference(field, field_name_scoped, database_name_finder):
    def GetScopeName():
        return ".".join(field_name_scoped)

    url = field['url']
    name = field['name']

    if not isinstance(url, str):
        log.info(f'{GetScopeName()} "url" field should be a string.')
        return

    if not isinstance(name, str):
        log.info(f'{GetScopeName()} "name" field should be a string."')
        return

    url_parts = url.split('/')
    if len(url_parts) > 0 and url_parts[0].strip() == '':
        url_parts = url_parts[1:]

    if not ((len(url_parts) == 3) and
            (url_parts[0] == 'api') and
            (url_parts[2].isnumeric())):
        log.info(f'{GetScopeName()} "url" ({url} should be in form /api/<database>/<entry_index>')

        new_url = None
        for index, part in enumerate(url_parts):
            if part == 'api':
                url_parts = url_parts[index:]
                new_url = "/" + "/".join(url_parts)
                break

        if new_url is None:
            log.info('Unable to fix url')
            return

        elif new_url != url:
            log.error(f'Replacing {url} with {new_url}')
            url = new_url
            field['url'] = new_url

    if len(url_parts) < 2:
        log.info('No usable database name, cannot fix reference')
        return
    
    database_name = url_parts[1]
    database = database_name_finder.GetDatabaseFromName(database_name)
    index = -1 if (len(url_parts) != 3 or (not url_parts[2].isnumeric())) else (int(url_parts[2]))

    if database is None:
        new_database_name, score = database_name_finder.FindBestDatabaseName(database_name)

        log.info(f'{GetScopeName()} "url" field does not name a valid database ({url})')
        log.info(f'Using "{new_database_name}" instead of "{database_name}"')
        field["url"] = f'/api/{new_database_name}/{index}'
        database_name = new_database_name
        database = database_name_finder.GetDatabaseFromName(database_name)

    if index >= len(database) or index < 0 or database[index][ENTRY_DESCRIPTOR]["name"] != name:
        log.info(f'{GetScopeName()} "url" field does not point to the correct entry.')

        if name == '_':
            found_entry = database_name_finder.GetEntryFromUrl(url_parts)
            print(found_entry)
            new_name = (found_entry["entry_descriptor"]["name"], int(url_parts[-1]))
            score = 100

        else:
            new_name, score = database_name_finder.FindBestEntryName(database_name, name)

        old_entry = dict(field.items())
        confidence = "exact" if score == 100 else "high" if score >= 85 else "low"

        if score != 100:
            log.info(f'{GetScopeName()} "name" field ({name}) does not match any entries, recommended: {new_name[0]}')

        field["name"] = new_name[0]
        field["url"] = f"/api/{database_name}/{new_name[1]}"
        log.debug(f'Swapping {old_entry} for {field}. Confidence is {confidence}')


def FixupReferences(database_name_finder):
    def IsReference(field):
        return isinstance(field, dict) and (len(field) == 2) and ('url' in field) and ('name' in field)

    def FixupReferenceRecurse(field, field_name_scoped=[]):
        if IsReference(field):
            FixupReference(field, field_name_scoped, database_name_finder)

        elif isinstance(field, list):
            for index, item in enumerate(field):
                FixupReferenceRecurse(item, field_name_scoped + [f"{index}"])
                
        elif isinstance(field, dict):
            for name, field in field.items():
                FixupReferenceRecurse(field, field_name_scoped + [name])

    for database_name, database in database_name_finder.databases_by_name.items():
        FixupReferenceRecurse(database, [database_name])


def PostFixupReferences(database_name_finder):
    for database_name, database in database_name_finder.databases_by_name.items():
        CUSTOM_DATABASE_SANATIZERS_POST_REF_FIXUP.get(database_name, Noop)(database, database_name, database_name_finder)

def Sanatize(raw_json_data, database_name):
    ''' Sanatize raw_json_data

    The main purpose of this method is to ensure some formatting and field
    consistency within the database.

    Namely:
        1. We except every database to be a list of objects.

        2. Each of these top level objects should have an entryDescriptor field
            which is an object that contains the following fields:
            - Name: A short descriptive way to refer to the entry.

            - Url: A url in the form /api/<database>/<index>.
                    This is primarily used as a uniform way to reference other entries.

            - Description: A textual / long form description of the item.
                    This is represented as a list of strings, where each string is a line.

            - Index: An ID used to unambiguously refer to the entry within the database.
                    Usually the index where it is in the database list (1-based).

        3. There are no empty objects within the database.
            To help with parsing, objects will either be wellformed or null.

        4. All objects (nested or otherwise) in a given database shall have the same format.
                In any case where additional or optional fields are required, the object
                should have some type specifier (not specified here) and the polymorphic
                data should be placed in a nested subobject.

        5. References to other objects in the database should have a consistent form.
            They should be an object with only 2 fields:
                {"name": "referenced-entry-name", "url": "referenced-entry-url"}
    '''
    assert isinstance(raw_json_data, list)
    assert len(raw_json_data) > 0
    log.info(database_name)

    def __SanatizeRecurse(cur_object, is_top_level=True):
        for key, value in cur_object.items():
            if isinstance(value, list):
                if len(value) > 0 and isinstance(value[0], dict):
                    cur_object[key] = [__SanatizeRecurse(sub_value, is_top_level=False) for sub_value in value]

            elif isinstance(value, dict):
                if len(value) == 0:
                    cur_object[key] = None
                else:
                    cur_object[key] = __SanatizeRecurse(value, is_top_level=False)

                    if len(value) == 2:
                        if 'unit' in value and 'quantity' in value:
                            value['quantity'] = float(value['quantity'])

        return cur_object

    index = 0
    for json_object in raw_json_data:
        entry_descriptor = json_object.setdefault(ENTRY_DESCRIPTOR, {})
        for field_to_move in ["index", "url", "name", "desc"]:
            value = json_object.get(field_to_move, None)
            if value is not None:
                del json_object[field_to_move]
                entry_descriptor[field_to_move] = value

        entry_descriptor["index"] = index
        entry_descriptor["url"] = f"/api/{database_name}/{index}"

        if not "name" in entry_descriptor:
            entry_descriptor["name"] = f"Unnamed_Index{index}"

        description = entry_descriptor.get("desc", None)
        if not isinstance(description, list):
            entry_descriptor["desc"] = [] if description is None else [str(description)]

        elif len(description) > 0:
            entry_descriptor["desc"] = [str(desc_line) for desc_line in description]

        index += 1

    raw_json_data = [__SanatizeRecurse(entry) for entry in raw_json_data]

    return CUSTOM_DATABASE_SANATIZERS.get(database_name, Noop)(raw_json_data, database_name)


if __name__ == "__main__":
    SCRIPT_PATH = os.path.realpath(os.path.abspath(__file__))
    SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
    SUFFIX = ".json"
    PREFIX = "5e-SRD-"

    databases = {}

    # Find all of our database JSON files, then load, sanatize, and save them.
    for file_name in os.listdir(SCRIPT_DIR):
        if file_name.endswith(SUFFIX) and file_name.startswith(PREFIX):
            
            # Read the file in, sanatize it, then dump it back out.
            json_file_name = os.path.join(SCRIPT_DIR, file_name)
            json_database_name = file_name.replace(SUFFIX, "").replace(PREFIX, "").lower()
            with open(json_file_name) as raw_json_file:
                raw_json_data = json.load(raw_json_file)

            databases[json_file_name] = (json_database_name, Sanatize(raw_json_data, json_database_name))

    database_name_finder = DatabaseNameFinder(dict(databases.values()))
    FixupReferences(database_name_finder)
    PostFixupReferences(database_name_finder)

    for file_name, database_name_and_database in databases.items():
        database_name, database = database_name_and_database
        with open(file_name, "w") as new_json_file:
            json.dump(database, new_json_file, indent=4)

