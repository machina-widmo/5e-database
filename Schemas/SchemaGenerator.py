import json
import os
import re

to_generate = """
[
	{ "__name": "ConditionEntry",
    "__ref": "SimpleEntry"},
    { "__name": "DamageTypeEntry",
    "__ref": "SimpleEntry"},
    { "__name": "EquipmentCategoryEntry",
    "__ref": "SimpleEntry"},
    { "__name": "WeaponPropertyEntry",
    "__ref": "SimpleEntry"},
    { "__name": "MagicSchoolsEntry",
    "__ref": "SimpleEntry"},

    { "__name": "InventoryItemDescriptor"
    , "item" : "DatabaseEntryReference"
    , "quantity" : "Int"
    },


    { "__name": "AbilityScoreValueDescriptor"
    , "ability" : "DatabaseEntryReference"
    , "value" : "Int"
    },


    { "__name": "DatabaseEntryDescriptor"
    , "index" : "Int"
    , "name" : "String"
    , "description" : "List String"
    , "url" : "String"
    },


    { "__name": "SimpleEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    },


    { "__name": "DatabaseEntryReference"
    , "url" : "String"
    , "name" : "String"
    },

    { "__name": "ChoicePoolDatabaseEntryReference"
	, "numToChoose" : "Int"
    , "choiceType" : "String"
    , "chooseFrom" : "List DatabaseEntryReference"
    },


    { "__name": "AttributeEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "fullName" : "String"
    , "relatedSkills" : "List DatabaseEntryReference"
    },


    { "__name": "ClassEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "hitDie" : "Int"
    , "proficiencyChoices" : "List ChoicePoolDatabaseEntryReference"
    , "proficiencies" : "List DatabaseEntryReference"
    , "savingThrows" : "List DatabaseEntryReference"
    , "startingEquipment" : "DatabaseEntryReference"
    , "classLevels" : "DatabaseEntryReference"
    , "subclasses" : "List DatabaseEntryReference"
    , "spellcasting" : "Maybe DatabaseEntryReference"
    },


    { "__name": "SubclassEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "class" : "DatabaseEntryReference"
    , "subclassFlavor" : "String"
    , "features" : "List DatabaseEntryReference"
    },


    { "__name": "FeatureEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "class" : "Maybe DatabaseEntryReference"
    , "subclass" : "Maybe DatabaseEntryReference"
    , "level" : "Int"
    },


    { "__name": "LanguageEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "languageType" : "String"
    , "typicalSpeakers" : "List String"
    , "script" : "String"
    },


    { "__name": "TraitEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "races" : "List DatabaseEntryReference"
    , "subraces" : "List DatabaseEntryReference"
    },


    { "__name": "RaceEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "abilityScoreValues" : "List AbilityScoreValueDescriptor"
    , "abilityScoreValueOptions" : "Maybe ChoicePoolDatabaseEntryReference"
    , "startingProficiencies" : "List DatabaseEntryReference"
    , "startingProficiencyOptions" : "Maybe ChoicePoolDatabaseEntryReference"
    , "languages" : "List DatabaseEntryReference"
    , "languageOptions" : "Maybe ChoicePoolDatabaseEntryReference"
    , "traits" : "List DatabaseEntryReference"
    , "traitOptions" : "Maybe ChoicePoolDatabaseEntryReference"
    , "speed" : "Int"
    , "alignment" : "String"
    , "size" : "SizeDescriptor"
    , "sizeDescription" : "String"
    , "languageDescription" : "String"
    },


    { "__name": "SubraceEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "abilityScoreValuees" : "List AbilityScoreValueDescriptor"
    , "abilityScoreValueOptions" : "Maybe ChoicePoolDatabaseEntryReference"
    , "startingProficiencies" : "List DatabaseEntryReference"
    , "startingProficiencyOptions" : "Maybe ChoicePoolDatabaseEntryReference"
    , "languages" : "List DatabaseEntryReference"
    , "languageOptions" : "Maybe ChoicePoolDatabaseEntryReference"
    , "traits" : "List DatabaseEntryReference"
    , "traitOptions" : "Maybe ChoicePoolDatabaseEntryReference"
    , "race" : "DatabaseEntryReference"
    },


    { "__name": "StartingEquipmentEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "class" : "DatabaseEntryReference"
    , "startingEquipment" : "List InventoryItemDescriptor"
    , "choicesToMake" : "List (ExclusiveChoice InventoryItemDescriptor)"
    },


    { "__name": "SpellEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "higherLevels" : "Maybe (List String)"
    , "page" : "String"
    , "range" : "String"
    , "components" : "List String"
    , "material" : "List String"
    , "requiresRitual" : "Bool"
    , "requiresConcentration" : "Bool"
    , "duration" : "String"
    , "castingTime" : "String"
    , "level" : "Int"
    , "school" : "DatabaseEntryReference"
    , "classes" : "List DatabaseEntryReference"
    , "subclasses" : "List DatabaseEntryReference"
    },


    { "__name": "InfoDescriptor"
    , "name" : "String"
    , "description" : "List String"
    },


    { "__name": "SpellcastingEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "class" : "DatabaseEntryReference"
    , "level" : "Int"
    , "spellcastingAbility" : "DatabaseEntryReference"
    , "info" : "List InfoDescriptor"
    },


    { "__name": "SkillEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "ability" : "DatabaseEntryReference"
    },


    { "__name": "ProficiencyEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "proficiencyType" : "String"
    , "classes" : "List DatabaseEntryReference"
    , "races" : "List DatabaseEntryReference"
    },


    { "__name": "LevelEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "level" : "Int"
    , "class" : "DatabaseEntryReference"
    , "classSpecific" : "ClassSpecificLevelDescriptor"
    , "subclass" : "Maybe DatabaseEntryReference"
    , "abilityScoreBonus" : "Int"
    , "proficiencyBonus" : "Int"
    , "features" : "List DatabaseEntryReference"
    , "featureChoices" : "List DatabaseEntryReference"
    , "spellcasting" : "Maybe SpellcastingDescriptor"
    },


    { "__name": "SpellcastingDescriptor"
    , "cantripsKnown" : "Int"
    , "spellsKnown" : "Int"
    , "spellSlots" : "List Int"
    },


    { "__name": "BarbarianClassSpecificLevelDescriptor"
    , "rageCount" : "Int"
    , "rageDamageBonus" : "Int"
    , "brutalCriticalDice" : "Int"
    },


    { "__name": "BardClassSpecificLevelDescriptor"
    , "inspirationDie" : "Int"
    , "songOfRestDie" : "Int"
    , "magicalSecretsMax5" : "Int"
    , "magicalSecretsMax7" : "Int"
    , "magicalSecretsMax9" : "Int"
    },


    { "__name": "ClericClassSpecificLevelDescriptor"
    , "channelDivinityCharges" : "Int"
    , "destroyUndeadCrit" : "Float"
    },


    { "__name": "DruidClassSpecificLevelDescriptor"
    , "wilShapeMaxCrit" : "Float"
    , "wildShapeSwim" : "Bool"
    , "whileShapeFly" : "Bool"
    },


    { "__name": "FighterClassSpecificLevelDescriptor"
    , "actionSurges" : "Int"
    , "indomitableUses" : "Int"
    , "extraAttacks" : "Int"
    },


    { "__name": "MonkClassSpecificLevelDescriptor"
    , "kiPoints" : "Int"
    , "unarmoredMovement" : "Int"
    , "martialArts" : "DiceDescriptor"
    },


    { "__name": "PaladinClassSpecificLevelDescriptor"
    , "auraRange" : "Int"
    },


    { "__name": "RangerClassSpecificLevelDescriptor"
    , "favoredEnemies" : "Int"
    , "favoredTerrain" : "Int"
    },


    { "__name": "RogueClassSpecificLevelDescriptor"
    , "sneakAttack" : "DiceDescriptor"
    },


    { "__name": "SorcererClassSpecificLevelDescriptor"
    , "sorceryPoints" : "Int"
    , "metamagicKnown" : "Int"
    , "creatingSpellSlotsCost" : "List Int"
    },


    { "__name": "WarlockClassSpecificLevelDescriptor"
    , "invocationsKnown" : "Int"
    , "mysticArcanumLevel6" : "Int"
    , "mysticArcanumLevel7" : "Int"
    , "mysticArcanumLevel8" : "Int"
    , "mysticArcanumLevel9" : "Int"
    },


    { "__name": "WizardClassSpecificLevelDescriptor"
    , "arcaneRecoveryLevels" : "Int"
    },


    { "__name": "EquipmentEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "cost" : "CurrencyValue"
    , "equipmentCategory" : "DatabaseEntryReference"
    , "categorySpecific" : "CategorySpecificEquipmentDescriptor"
    },


    { "__name": "WeaponEquipmentDescriptor"
    , "weight" : "MeasuredUnit"
    , "weaponCategory" : "DatabaseEntryReference"
    , "weaponCategorySpecific" : "WeaponCategorySpecificDescriptor"
    , "weaponRange" : "String"
    , "categoryRange" : "String"
    , "damage" : "DamageDescriptor"
    , "range" : "RangeDescriptor"
    , "properties" : "List DatabaseEntryReference"
    },




    { "__name": "RangeDescriptor"
    , "normal" : "Maybe Int"
    , "long" : "Maybe Int"
    },


    { "__name": "DamageDescriptor"
    , "damageDice" : "String"
    , "damageBonus" : "Int"
    , "damageType" : "DatabaseEntryReference"
    },


    { "__name": "ArmorEquipmentDescriptor"
    , "weight" : "MeasuredUnit"
    , "armorCategory" : "DatabaseEntryReference"
    , "armorCategorySpecific" : "ArmorCategorySpecificDescriptor"
    , "armorClass" : "ArmorClassDescriptor"
    , "strengthMinimum" : "Int"
    , "stealthDisadvantage" : "Bool"
    },


    { "__name": "ArmorClassDescriptor"
    , "baseArmor" : "Int"
    , "dexterityBonus" : "Bool"
    , "bonusLimit" : "Maybe Int"
    },

 
    { "__name": "ToolEquipmentDescriptor"
    , "weight" : "MeasuredUnit"
    , "toolCategory" : "DatabaseEntryReference"
    , "toolCategorySpecific" : "ToolCategorySpecificDescriptor"
    },


    { "__name": "MountEquipmentDescriptor"
    , "mountCategory" : "DatabaseEntryReference"
    , "mountSpecific" : "MountCategorySpecificDescriptor"
    },




    { "__name": "LandAndAirMountEquipmentDescriptor"
    , "speed" : "MeasuredUnit"
    , "capacity" : "MeasuredUnit"
    },


    { "__name": "MountAccessoryEquipmentDescriptor"
    , "weight" : "MeasuredUnit"
    },


    { "__name": "WaterborneMountEquipmentDescriptor"
    , "speed" : "MeasuredUnit"
    },


    { "__name": "AdventuringGearEquipmentDescriptor"
    , "gearCategory" : "DatabaseEntryReference"
    , "gearCategorySpecific" : "AdventuringGearCategorySpecificDescriptor"
    },




    { "__name": "StandardGearDescriptor"
    , "weight" : "MeasuredUnit"
    },


    { "__name": "AmmunitionDescriptor"
    , "weight" : "MeasuredUnit"
    },


    { "__name": "HolySymbolDescriptor"
    , "weight" : "MeasuredUnit"
    },


    { "__name": "ArcaneFocusDescriptor"
    , "weight" : "MeasuredUnit"
    },


    { "__name": "DruidicFocusDescriptor"
    , "weight" : "MeasuredUnit"
    },


    { "__name": "KitDescriptor"
    , "weight" : "MeasuredUnit"
    },


    { "__name": "EquipmentPackDescriptor"
    , "contents" : "List InventoryItemDescriptor"
    },


    { "__name": "BackgroundEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "skills" : "List DatabaseEntryReference"
    , "suggestedOrigins" : "List String"
    , "languages" : "List DatabaseEntryReference"
    , "languageChoices" : "Maybe ChoicePoolDatabaseEntryReference"
    , "tools" : "List DatabaseEntryReference"
    , "toolChoices" : "Maybe ChoicePoolDatabaseEntryReference"
    , "feature" : "Maybe DatabaseEntryReference"
    , "featureChoices" : "Maybe ChoicePoolDatabaseEntryReference"
    , "equipment" : "List InventoryItemDescriptor"
    , "currency" : "List CurrencyValue"
    },


    { "__name": "BackgroundFeatureEntry"
    , "descriptor" : "DatabaseEntryDescriptor"
    , "background" : "DatabaseEntryReference"
    }
]
"""

also_to_generate = """
[
    [
        ["ClassSpecificLevelDescriptor", "class", "class_specific"]
        , ["BarbarianLevel", "BarbarianClassSpecificLevelDescriptor", "Barbarian"]
        , ["BardLevel", "BardClassSpecificLevelDescriptor", "Bard"]
        , ["ClericLevel", "ClericClassSpecificLevelDescriptor", "Cleric"]
        , ["DruidLevel", "DruidClassSpecificLevelDescriptor", "Druid"]
        , ["FighterLevel", "FighterClassSpecificLevelDescriptor", "Fighter"]
        , ["MonkLevel", "MonkClassSpecificLevelDescriptor", "Monk"]
        , ["PaladinLevel", "PaladinClassSpecificLevelDescriptor", "Paladin"]
        , ["RangerLevel", "RangerClassSpecificLevelDescriptor", "Ranger"]
        , ["RogueLevel", "RogueClassSpecificLevelDescriptor", "Rogue"]
        , ["SorcererLevel", "SorcererClassSpecificLevelDescriptor", "Sorcerer"]
        , ["WarlockLevel", "WarlockClassSpecificLevelDescriptor", "Warlock"]
        , ["WizardLevel", "WizardClassSpecificLevelDescriptor", "Wizard"]
    ],
    [
        ["CategorySpecificEquipmentDescriptor", "equipment_category", "category_specific"]
        , ["Weapon", "WeaponEquipmentDescriptor", "Weapon"]
        , ["Armor", "ArmorEquipmentDescriptor", "Armor"]
        , ["Tool", "ToolEquipmentDescriptor", "Tools"]
        , ["Mount", "MountEquipmentDescriptor", "Mounts and Vehicles"]
        , ["AdventuringGear", "AdventuringGearEquipmentDescriptor", "Adventuring Gear"]
    ],
    [
        ["MountCategorySpecificDescriptor", "mount_category", "category_specific"]
        , ["LandAndAirMount", "LandAndAirMountEquipmentDescriptor", "Mounts and Other Animals"]
        , ["WaterborneMount", "WaterborneMountEquipmentDescriptor", "Waterborne Vehicles"]
        , ["MountAccessory", "MountAccessoryEquipmentDescriptor", "Tack, Harness, and Drawn Vehicles"]
    ],
    [
        ["AdventuringGearCategorySpecificDescriptor", "gear_category", "category_specific"]
        , ["StandardGear", "StandardGearDescriptor", "Standard Gear"]
        , ["Ammunition", "AmmunitionDescriptor", "Ammunition"]
        , ["HolySymbol", "HolySymbolDescriptor", "Holy Symbol"]
        , ["ArcaneFocus", "ArcaneFocusDescriptor", "Druidic Focus"]
        , ["DruidicFocus", "DruidicFocusDescriptor", "Arcane Focus"]
        , ["Kit", "KitDescriptor", "Kits"]
        , ["EquipmentPack", "EquipmentPackDescriptor", "Equipment Packs"]
    ],
    [
        ["WeaponCategorySpecificDescriptor", "weapon_category", "category_specific"]
        , ["SimpleWeapon", "Simple Weapons"]
        , ["MartialWeapon", "Martial Weapons"]
    ],
    [
        ["ArmorCategorySpecificDescriptor", "armor_category", "category_specific"]
        , ["LightArmor", "Light Armor"]
        , ["MediumArmor", "Medium Armor"]
        , ["HeavyArmor", "Heavy Armor"]
        , ["Shield", "Shields"]
    ],
    [
        ["ToolCategorySpecificDescriptor", "tool_category", "category_specific"]
        , ["ArtisansTool", "Artisan's Tools"]
        , ["GamingSet", "Gaming Sets"]
        , ["MusicalInstrument", "Musical Instruments"]
        , ["OtherTool", "Other Tools"]
    ]
]
"""

inline_schema_selectors = {}


def sanatize_property_name(name):
    return '_'.join((
        word.lower()
        for word in re.sub(r'([A-Z])', r' \1', name).split(' ')
    ))


def generate_property_type(value):
    value_parts = value.split(' ')

    value = None
    while len(value_parts) > 0:
        processing = value_parts.pop()

        if "Maybe" == processing:
            value = {
                "oneOf": [
                    {"type": "null"},
                    value
                ]
            }

        elif "List" == processing:
            value = {
                "type": "array",
                "items": value
            }

        elif "String" == processing:
            value = {"type": "string"}

        # TODO: Ideally we validate these to Ints or Floats,
        #       or have Elm use Numerics
        elif "Int" == processing or "Float" == processing:
            value = {"type": "number"}

        elif "Bool" == processing:
            value = {"type": "boolean"}

        elif processing in inline_schema_selectors:
            value = inline_schema_selectors[processing]

        else:
            value = {"$ref": f"{processing}.schema.json"}

    return value


def generate_object_schema(value):
    output = {
        "$schema": "http://json-schema.org/draft-07/schema",
        "$id": f"{value['__name']}.schema.json",
        "title": f"{value['__name']}",
        "type": "object",
    }

    del value["__name"]

    if "__ref" in value:
        output["$ref"] = f"{value['__ref']}.schema.json"

    else:
        output["required"] = [sanatize_property_name(prop_name) for prop_name in value.keys()]
        output["properties"] = {
            sanatize_property_name(prop_name): generate_property_type(prop_type)
            for prop_name, prop_type in value.items()
        }

    return output



json_data = json.loads(also_to_generate)
for value in json_data:
    name = value[0][0]
    reference = value[0][1]
    field = value[0][2]

    def generate_if_else_for_value(inner_value):
        value_to_match = inner_value.pop()
        if len(inner_value) > 1:
            field_value = {
                "$ref": f"{inner_value[1]}.schema.json"
            }
        else:
            field_value = {
                "type": "null"
            }

        return {
            "if": {
                "properties": {
                    reference: {
                        "properties": {
                            "name": {
                                "const": value_to_match
                            }
                        }
                    }
                }
            },
            "then": {
                "properties": {
                    field: field_value
                }
            }
        }

    output = {
        "oneOf": [generate_if_else_for_value(inner_value) for inner_value in value[1:]]
    }

    inline_schema_selectors[name] = output

json_data = json.loads(to_generate)
base_path = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
for value in json_data:
    with open(os.path.join(base_path, f"{value['__name']}.schema.json"), 'w') as out_schema_file:
        json.dump(generate_object_schema(value), out_schema_file, indent=4)