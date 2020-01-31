import re
import ply.lex as lex

to_generate = {
    "MeasuredUnit"
    "ChoicePool",
    "ExclusiveChoice",
    "DatabaseEntryDescriptor",
    "DatabaseEntryReference",
    "CurrencyType"",
    "EntryCommon"",
    "RangeDescriptor"",
    "AbilityScoreValueDescriptor"",
    "CurrencyValue"",
    "DamageDescriptor"",
    "DiceDescriptor",
    "DiceType",
    "InfoDescriptor",
    "InventoryItemDescriptor",
    "ArmorClassDescriptor",
    "ArmorEquipmentDescriptor",
    "ArmorCategorySpecificDescriptor",
    "EquipmentEntryCommon",
    "AdventuringGearEquipmentDescriptor",
    "AdventuringGearCategorySpecificDescriptor",
    "MountEquipmentDescriptor",
    "MountCategorySpecificDescriptor",
    "LandAndAirMountEquipmentDescriptor",
    "WaterborneMountEquipmentDescriptor",
    "MountAccessoryEquipmentDescriptor",
    "ToolEquipmentDescriptor",
    "ToolCategorySpecificDescriptor",
    "WeaponEquipmentDescriptor",
    "WeaponCategorySpecificDescriptor",
    "BarbarianClassSpecificLevelDescriptor",
    "BardClassSpecificLevelDescriptor",
    "ClericClassSpecificLevelDescriptor",
    "DruidClassSpecificLevelDescriptor",
    "FighterClassSpecificLevelDescriptor",
    "MonkClassSpecificLevelDescriptor",
    "PaladinClassSpecificLevelDescriptor",
    "RangerClassSpecificLevelDescriptor",
    "RogueClassSpecificLevelDescriptor",
    "SorcererClassSpecificLevelDescriptor",
    "WarlockClassSpecificLevelDescriptor",
    "WizardClassSpecificLevelDescriptor",
    "DatabaseEntry",
    "AttributeEntry",
    "BackgroundEntry",
    "BackgroundFeatureEntry",
    "ClassEntry",
    "ConditionEntry",
    "DamageTypeEntry",
    "EquipmentCategoryEntry",
    "EquipmentEntry",
    "FeatureEntry",
    "LanguageEntry",
    "LevelEntry",
    "MagicSchoolsEntry",
    "ProficiencyEntry",
    "RaceEntry",
    "SkillEntry",
    "SpellcastingEntry",
    "SpellEntry",
    "StartingEquipmentEntry",
    "SubclassEntry",
    "SubraceEntry",
    "TraitEntry",
    "WeaponPropertyEntry",
}

built_ins = [
    "Maybe",
    "String",
    "Int",
    "Float",
    "Bool",
    "List",
    "Nothing",
    "Just",
    "Result",
    "Ok",
    "Err"
]

keywords = [
    "if",
    "then",
    "else",
    "case",
    "of",
    "let",
    "in",
    "type",
    "module",
    "where",
    "import",
    "exposing",
    "as",
    "port"
]

misc_symbols = [
    "--",
    "{--"
    "--}",
    "{",
    "}"
    "("
    ")",
    ":",
    ",",
    "|>",
    "<|",
    "//",
    "/",
    "\\",
    '|.',
    '|=',
    "=",
    "."
]

symbols = misc_symbols + keywords + built_ins

t_SINGLE_LINE_COMMENT = r'--'
t_MULTI_LINE_COMMENT_START = r'\{--'
t_MULTI_LINE_COMMENT_END = r'--\}'
t_OPEN_BRACKET = r"\{"
t_CLOSE_BRACKET = r"\}"
t_OPEN_PARENS = r'\('
t_CLOSE_PARENS = r'\)'
t_COLON = r":"
t_COMMA = r","
t_PIPE_RIGHT = r"\|>"
t_PIPE_LEFT = r"<\|"
t_DOUBLE_RIGHT_SLASH = r"//"
t_RIGHT_SLASH = r"/"
t_LEFT_SLASH = r"\\"
t_PIPE_AND_IGNORE = r"\|."
t_PIPE_AND_KEEP = r"\|="
t_EQUALS = r"="
t_DOT = r"\."


def split_at_caps(string):
    re.sub(r'([A-Z])', r' \1', string).split()


def make_t_identifier(string):
    return "t_" + "_".join((s.toupper(), split_at_caps(string)))


for value in (keywords):
    globals()[f"t_{make_t_identifier(value)}"] = value


#for value in to_generate:
#    globals()[f"t_{make_t_identifier(value)}"] = value


# def p_module_exposing_list(p):


to_ignore = '1234567890 \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += (t.value)


def t_error(t):
    t.lexer.skip(1)




if __name__ == '__main__':
    import os

    SCRIPT_DIR = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
    database_types_elm_file_path = os.path.join('../../elm/src/DatabaseTypes.elm')
    with open(database_types_elm_file_path) as database_types_elm_file:
        database_types_elm = database_types_elm_file.read()

    lexer = lex.lex()
    lexer.input(database_types_elm)

    is_ignoring_line = False
    is_handling_multi_line_comment = False
    last_line_num = -1

    def handle_type_alias_definition():

    def handle_type_definition():

    def handle_type_definition_generic():
        token = lexer.token()
        if token.value == t_ALIAS:
            return handle_type_alias_definition()

        return handle_type_definition()

    def main_loop():
        token = lexer.token()
        if not tok:
            return False

        line_delta = (lexer.lineno - last_line_num)
        last_line_num = lexer.lineno

        if line_delta != 0:
            is_ignoring_line = False

        elif is_ignoring_line:
            pass

        elif is_handling_multi_line_comment:
            is_handling_multi_line_comment = (t_MULTI_LINE_COMMENT_END == token.value)

        elif token.value == t_TYPE:
            return handle_type_definition_generic()

        else:
            is_ignoring_line = True

        return True

    while main_loop():
        pass
