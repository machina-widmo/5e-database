import json
import os


def Sanatize(raw_json_data, database_name):
    ''' Sanatize raw_json_data

    The main purpose of this method is to ensure some formatting and field
    consistency within the database.

    Namely:
        1. We except every database to be a list of objects.

        2. Each of these top level objects should have:
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

                    # If we have a URL value, then this is a reference to some other database entry.
                    # Do a quick sanity check to see if it conforms to our expected format.
                    if not is_top_level:
                        if "url" in value:
                            if "name" not in value:
                                print(f"Found object field '{key}' that appears to be a reference, but is missing name field. Database {database_name}.")
                            if len(value) != 2:
                                print(f"Found object field '{key}' that appears to be a reference, but has an incorrect number of fields (expects 2 found {len(value)}). Database {database_name}'")

        return cur_object

    index = 0
    for json_object in raw_json_data:
        index = index + 1
        json_object["index"] = index
        json_object["url"] = f"/api/{database_name}/{index}"

        if not "name" in json_object:
            json_object["name"] = f"Unnamed_Index{index}"

        description = json_object.get("desc", None)
        if not isinstance(description, list):
            json_object["desc"] = [] if description is None else [str(description)]
        elif len(description) > 0:
            json_object["desc"] = [str(desc_line) for desc_line in description]

    return [__SanatizeRecurse(entry) for entry in raw_json_data]


if __name__ == "__main__":
    SCRIPT_PATH = os.path.realpath(os.path.abspath(__file__))
    SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
    SUFFIX = ".json"
    PREFIX = "5e-SRD-"

    # Find all of our database JSON files, then load, sanatize, and save them.
    for file_name in os.listdir(SCRIPT_DIR):
        if file_name.endswith(SUFFIX) and file_name.startswith(PREFIX):
            
            # Read the file in, sanatize it, then dump it back out.
            json_file_name = os.path.join(SCRIPT_DIR, file_name)
            json_database_name = file_name.replace(SUFFIX, "").replace(PREFIX, "").lower()
            with open(json_file_name) as raw_json_file:
                raw_json_data = json.load(raw_json_file)

            sanatized_json_data = Sanatize(raw_json_data, json_database_name)

            with open(json_file_name, "w") as raw_json_file:
                json.dump(sanatized_json_data, raw_json_file, indent=4)

                