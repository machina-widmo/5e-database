import fastjsonschema as fjs
import json
import os

SCRIPT_DIRECTORY = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
SCHEMA_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, "Schemas")


def load_json_file(path):
    with open(path) as json_file:
        return json.load(json_file)


DATABASES = {
    name: load_json_file(os.path.join(SCRIPT_DIRECTORY, name))
    for name in os.listdir(SCRIPT_DIRECTORY)
    if name.endswith(".json")
}

SCHEMAS = {
    name: load_json_file(os.path.join(SCHEMA_DIRECTORY, name))
    for name in os.listdir(SCHEMA_DIRECTORY)
    if name.endswith(".schema.json")
}

SCHEMA_NAMES_BY_DATABASE = {
    "5e-SRD-Ability-Scores.json": "AttributeEntry.schema.json",
    "5e-SRD-BackgroundFeatures.json": "BackgroundFeatureEntry.schema.json",
    "5e-SRD-Backgrounds.json": "BackgroundEntry.schema.json",
    "5e-SRD-Classes.json": "ClassEntry.schema.json",
    "5e-SRD-Conditions.json": "ConditionEntry.schema.json",
    "5e-SRD-Damage-Types.json": "DamageTypeEntry.schema.json",
    "5e-SRD-Equipment-Categories.json": "EquipmentCategoryEntry.schema.json",
    "5e-SRD-Equipment.json": "EquipmentEntry.schema.json",
    "5e-SRD-Features.json": "FeatureEntry.schema.json",
    "5e-SRD-Languages.json": "LanguageEntry.schema.json",
    "5e-SRD-Levels.json": "LevelEntry.schema.json",
    "5e-SRD-Magic-Schools.json": "MagicSchoolEntry.schema.json",
    "5e-SRD-Proficiencies.json": "ProficiencyEntry.schema.json",
    "5e-SRD-Races.json": "RaceEntry.schema.json",
    "5e-SRD-Skills.json": "SkillEntry.schema.json",
    "5e-SRD-StartingEquipment.json": "StartingEquipmentEntry.schema.json",
    "5e-SRD-Subclasses.json": "SubclassEntry.schema.json",
    "5e-SRD-Subraces.json": "SubraceEntry.schema.json",
    "5e-SRD-Traits.json": "TraitEntry.schema.json",
    "5e-SRD-Weapon-Properties.json": "WeaponPropertyEntry.schema.json",
    # TODO: Monsters
    # TODO: Spells
    # TODO: Spellcasting
    # TODO: Characters
}


handlers = {'': SCHEMAS.get}

for database in DATABASES.keys():
    schema = SCHEMA_NAMES_BY_DATABASE.get(database)
    if schema is not None:
        print(f'Validating database {database} with schema {schema}')
        database_schema = {
            "$schema": "http://json-schema.org/draft-07/schema",
            "type": "array",
            "items": {
                "$ref": f"{schema}"
            }
        }

        fjs.validate(database_schema, DATABASES[database], handlers=handlers)