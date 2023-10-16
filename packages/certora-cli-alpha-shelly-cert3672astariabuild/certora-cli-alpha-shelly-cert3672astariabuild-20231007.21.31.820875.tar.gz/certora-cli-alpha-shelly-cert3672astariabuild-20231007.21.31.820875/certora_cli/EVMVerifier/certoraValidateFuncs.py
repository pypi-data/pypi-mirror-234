import sys
import argparse
import json
import json5
import logging
import os
import re
import shutil
import subprocess
import string
from pathlib import Path
from typing import Dict, Optional, Type, Union, IO, Any
from enum import auto, Enum

from Shared import certoraUtils as Util

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))


validation_logger = logging.getLogger("validation")


class CoverageInfoValue(Util.NoValEnum):
    """
    valid values for the --coverage_info flag.

    NONE: no unsat core analysis
    BASIC: less-precise but possibly much faster analysis (this allows for all the TAC simplificaitons/transformations
        we do)
    ADVANCE: precise but possibly slow analysis (this one turns off various TAC simplifications/transformations we do)

    """
    NONE = auto()
    BASIC = auto()
    ADVANCED = auto()


class RuleSanityValue(Util.NoValEnum):
    NONE = auto()
    BASIC = auto()
    ADVANCED = auto()


class FalseValue(Util.NoValEnum):
    FALSE = auto()


class OnOffValue(Util.NoValEnum):
    ON = auto()
    OFF = auto()


class MultiExampleValue(Util.NoValEnum):
    NONE = auto()
    BASIC = auto()
    ADVANCED = auto()


class RunSources(Util.NoValEnum):
    COMMAND = auto()
    VSCODE = auto()
    EQUIVALENCE = auto()
    MUTATION = auto()
    BENCHMARK = auto()
    LIGHT_TEST = auto()


class WaitForResultOptions(Util.NoValEnum):
    NONE = auto()
    ALL = auto()


def is_solc_file_valid(orig_filename: Optional[str]) -> str:
    """
    Verifies that a given --solc argument is valid:
        1. The file exists
        2. We have executable permissions for it
    :param orig_filename: Path to a solc executable file. If it is None, a default path is used instead,
                          which is also checked
    :return: Default solc executable if orig_filename was None, orig_filename is returned otherwise
    :raises argparse.ArgumentTypeException if the argument is invalid (including the default if it is used)
    """
    if orig_filename is None:
        filename = Util.DEFAULT_SOLC
        err_prefix = f'No --solc path given, but default solidity executable {Util.DEFAULT_SOLC} had an error. '
    else:
        filename = orig_filename
        err_prefix = ''

    if Util.is_windows() and not filename.endswith(".exe"):
        filename += ".exe"

    common_mistakes_suffixes = ['sol', 'conf', 'tac', 'spec', 'cvl']
    for suffix in common_mistakes_suffixes:
        if filename.endswith(f".{suffix}"):
            raise Util.CertoraUserInputError(f"wrong Solidity executable given: {filename}")

    # see https://docs.python.org/3.8/library/shutil.html#shutil.which. We use no mask to give a precise error
    solc_location = shutil.which(filename, os.F_OK)
    if solc_location is not None:
        solc_path = Path(solc_location)
        if solc_path.is_dir():
            raise Util.CertoraUserInputError(
                err_prefix + f"Solidity executable {filename} is a directory not a file: {solc_path}")
        if not os.access(solc_path, os.X_OK):
            raise Util.CertoraUserInputError(
                err_prefix + f"No execution permissions for Solidity executable {filename} at {solc_path}")
        return solc_path.as_posix()

    # given solc executable not found in path. Looking if the default solc exists
    if filename != Util.DEFAULT_SOLC:
        default_solc_path = shutil.which(Util.DEFAULT_SOLC)  # If it is not None, the file exists and is executable
        if default_solc_path is not None:
            try:
                run_res = subprocess.check_output([default_solc_path, '--version'], shell=False)
                default_solc_version = run_res.decode().splitlines()[-1]
            except Exception as e:
                # If we cannot invoke this command, we should not recommend the executable to the user
                validation_logger.debug(
                    f"Could not find the version of the default Solidity compiler {Util.DEFAULT_SOLC}\n{e}")
                default_solc_version = None

            if default_solc_version is not None:
                err_msg = f"Solidity executable {orig_filename} not found in path.\n" \
                          f"The default Solidity compiler was found at {default_solc_path} " \
                          f"with version {default_solc_version}. To use it, remove the --solc argument:\n"

                raise Util.CertoraUserInputError(err_msg)

    # Couldn't find the given solc nor the default solc
    raise Util.CertoraUserInputError(err_prefix + f"Solidity executable {filename} not found in path")


def validate_non_negative_integer(string: str) -> str:
    """
    :param string: A string
    :return: The same string, if the string represents a non-negative integer
    :raises CertoraUserInputError if the string does not represent a non-negative integer
    """
    try:
        number = int(string)
        if number < 0:
            raise ValueError
    except ValueError as e:
        raise Util.CertoraUserInputError(f'expected a non-negative integer, instead given {string}') from e
    return string


def validate_non_negative_integer_or_minus_1(string: str) -> str:
    """
    :param string: A string
    :return: The same string, if the string represents a non-negative  integer
    :raises CertoraUserInputError if the string does not represent a non-negative  integer
    """
    try:
        number = int(string)
        if number != -1 and number < 0:
            raise ValueError
    except ValueError:
        raise Util.CertoraUserInputError(f'expected a non-negative integer or -1, instead given {string}')
    return string


def validate_positive_integer(string: str) -> str:
    """
    :param string: A string
    :return: The same string, if the string represents for positive integers
    :raises CertoraUserInputError if the string is not a positive integer
    """
    try:
        number = int(string)
        if number <= 0:
            raise ValueError
    except ValueError:
        raise Util.CertoraUserInputError(f'expected a positive integer, instead given {string}')
    return string


def validate_disallow_all_values(_: str) -> str:
    """
    :raises CertoraUserInputError always, as we cannot set the cloud's global timeout
    """
    raise Util.CertoraUserInputError("Cannot set the global timeout for the cloud. Use 'global_timeout' instead")


def validate_jar(filename: str) -> str:
    file_path = Path(filename)
    if not file_path.is_file():
        raise Util.CertoraUserInputError(f"file {filename} does not exist.")
    if not os.access(filename, os.X_OK):
        raise Util.CertoraUserInputError(f"no execute permission for jar file {filename}")

    basename = file_path.name  # extract file name from path.
    # NOTE: expects Linux file paths, all Windows file paths will fail the check below!
    if re.search(r"^[\w.-]+\.jar$", basename):
        # Base file name can contain only alphanumeric characters, underscores, or hyphens
        return filename

    raise Util.CertoraUserInputError(f"file {filename} is not of type .jar")


def validate_optional_readable_file(filename: str) -> str:
    """
    Verifies that if filename exists, it is a valid readable file.
    It is the responsibility of the consumer to check the file exists
    """
    file_path = Path(filename)
    if file_path.is_dir():
        raise Util.CertoraUserInputError(f"{filename} is a directory and not a file")
    elif not file_path.exists():
        raise Util.CertoraUserInputError(f"{filename} does not exists")
    elif file_path.exists() and not os.access(filename, os.R_OK):
        raise Util.CertoraUserInputError(f"no read permissions for {filename}")
    return filename  # It is okay if the file does not exist


def validate_spec_file(filename: str) -> str:
    return validate_readable_file(filename, (".spec", ".cvl"))


def validate_readable_file(filename: str, extensions: Union[str, tuple] = '') -> str:
    file_path = Path(filename)
    if not file_path.exists():
        raise Util.CertoraUserInputError(f"file {filename} not found")
    if file_path.is_dir():
        raise Util.CertoraUserInputError(f"{filename} is a directory and not a file")
    if not os.access(filename, os.R_OK):
        raise Util.CertoraUserInputError(f"no read permissions for {filename}")
    if extensions and not filename.lower().endswith(extensions):
        raise Util.CertoraUserInputError(f"{filename} does not end with {extensions}")

    return filename


def validate_resource_files(string: str) -> str:
    parts = string.split(':')
    if len(parts) == 2:
        validate_readable_file(parts[1])
    else:
        raise Util.CertoraUserInputError(f"resourceFiles format is <label>:<path>, got {string}")
    return string


def validate_dir(dirname: str) -> str:
    dir_path = Path(dirname)
    if not dir_path.exists():
        raise Util.CertoraUserInputError(f"path {dirname} does not exist")
    if dir_path.is_file():
        raise Util.CertoraUserInputError(f"{dirname} is a file and not a directory")
    if not os.access(dirname, os.R_OK):
        raise Util.CertoraUserInputError(f"no read permissions to {dirname}")
    return dir_path.resolve().as_posix()


def validate_build_dir(path_str: str) -> str:
    """
    Verifies the argument is not a path to an existing file/directory and that a directory can be created at that
    location
    """
    try:
        p = Path(path_str)
        if p.exists():
            raise Util.CertoraUserInputError(f"'build_dir' {path_str} already exists")
        # make sure the directory can be created
        p.mkdir(parents=True)
        shutil.rmtree(path_str)
    except OSError:
        raise Util.CertoraUserInputError(f"failed to create build directory - {path_str} ")

    return path_str


def validate_tool_output_path(filename: str) -> str:
    flag = '--tool_output'
    file_path = Path(filename)
    if file_path.is_dir():
        raise Util.CertoraUserInputError(f"{flag} {filename} is a directory")
    if file_path.is_file():
        validation_logger.warning(f"{flag} {filename} file already exists")
        if not os.access(filename, os.W_OK):
            raise Util.CertoraUserInputError(f'No permission to rewrite {flag} file {filename}')
    else:
        try:
            with file_path.open('w') as f:
                f.write('try')
            file_path.unlink()
        except (ValueError, IOError, OSError) as e:
            raise Util.CertoraUserInputError(f"could not create {flag} file {filename}. Error: {e}")

    return filename


def validate_conf_file(file_name: str) -> str:
    """
    Verifies that the file name has a .conf extension
    @param file_name: the file name
    @return: the name after confirming the .conf extension

    Will raise Util.CertoraUserInputError if the file name does end
    in .conf.
    """
    if not file_name.endswith('.conf'):
        raise Util.CertoraUserInputError(f"file name {file_name} does not end in .conf")

    # making sure the target file can be created and is accessible for writing
    with open(file_name, 'w') as f:
        f.write('try')
    os.remove(file_name)

    return file_name


def validate_exec_file(file_name: str) -> str:
    """
    Verifies that the file name is executable (including $path)
    @param file_name: the file name
    @return: the path to the executable file

    Will raise Util.CertoraUserInputError if the file is not executable
    """
    exec_file = shutil.which(file_name)
    if exec_file is None:
        raise Util.CertoraUserInputError(f"Could not find file name {file_name}")
    return file_name


def validate_input_file(file: str) -> str:
    # [file[:contractName] ...] or CONF_FILE.conf or TAC_FILE.tac

    if '.sol' in file:
        ext = '.sol'
    elif '.vy' in file:
        ext = '.vy'
    else:
        ext = None

    if ext is not None:
        """
        Regex explanation (suppose ext=.sol):
        The file path must ends with suffix .sol: ".+\\.sol"
        """

        if ':' in file:
            # We split by the last occurrence of sol: in the path, which was guaranteed by te regex
            try:
                basename_no_suffix, contract = file.rsplit(ext + ":", 1)
            except ValueError:
                raise Util.CertoraUserInputError(f"{file} is not a valid input file - <path>[:<contract>]") from None
            if not re.search(fr"^{Util.SOLIDITY_CONTRACT_NAME_RE}$", contract):
                raise Util.CertoraUserInputError(
                    f"{contract} should be a valid contract name (combination of alphanum, underscores"
                    " and dollar signs)")

            file_path = basename_no_suffix + ext
        else:
            basename = os.path.basename(file)
            basename_no_suffix, _ = os.path.splitext(basename)
            if not re.search(fr"^{Util.SOLIDITY_CONTRACT_NAME_RE}$", basename_no_suffix):
                raise Util.CertoraUserInputError(
                    f"file name {basename_no_suffix} should be a valid contract name (combination of alphanum, "
                    f"underscores and dollar signs) or use the <path>:<contract> format")

            file_path = file
        try:
            validate_readable_file(file_path)
        except Exception as e:
            raise Util.CertoraUserInputError(f"Cannot access file {file} : {e}")
        return file
    elif any(file.endswith(ext) for ext in ['.tac', '.conf', '.json', '.o', '.so']):
        validate_readable_file(file)
        return file

    raise Util.CertoraUserInputError(f"input file {file} is not in one of the supported types (.sol, .vy, .tac, .o, "
                                     ".so, .conf, .json)")


def validate_json_file(file: str) -> str:
    validate_readable_file(file, '.json')
    with open(file, 'r') as f:
        try:
            json.load(f)
        except Exception as e:
            raise Util.CertoraUserInputError(f"JSON file {file} cannot be parsed: {e}")
    return file


def validate_verify_attr(contract: str) -> str:
    if not re.search(fr"^{Util.SOLIDITY_CONTRACT_NAME_RE}:[^:]+\.(spec|cvl)$", contract):
        # Regex: name has only one ':', has at least one letter before, one letter after and ends in .spec
        raise Util.CertoraUserInputError(f"argument {contract} for 'verify' option is in incorrect form. "
                                         "Must be formatted contractName:specName.spec")
    spec_file = contract.split(':')[1]
    validate_readable_file(spec_file)

    return contract


def validate_link_attr(link: str) -> str:
    if not re.search(fr"^{Util.SOLIDITY_CONTRACT_NAME_RE}:\w+={Util.SOLIDITY_CONTRACT_NAME_RE}$", link):
        raise Util.CertoraUserInputError(f"Link attribute {link} must be of the form contractA:slot=contractB or "
                                         f"contractA:slot=<number>")
    return link


def validate_prototype_attr(string: str) -> str:
    if not re.search(fr"^[0-9a-fA-F]+={Util.SOLIDITY_CONTRACT_NAME_RE}$", string):
        raise Util.CertoraUserInputError(f"Prototype attribute {string}"
                                         f" must be of the form bytecodeString=contractName")

    return string


def validate_struct_link(link: str) -> str:
    search_res = re.search(fr"^{Util.SOLIDITY_CONTRACT_NAME_RE}:([^:=]+)={Util.SOLIDITY_CONTRACT_NAME_RE}$", link)
    # We do not require firm form of slot number so we can give more informative warnings

    if search_res is None:
        raise Util.CertoraUserInputError(f"Struct link {link} must be of the form contractA:<field>=contractB")
    if search_res[1].isidentifier():
        return link
    try:
        parsed_int = int(search_res[1], 0)  # an integer or a hexadecimal
        if parsed_int < 0:
            raise Util.CertoraUserInputError(f"struct link slot number negative at {link}")
    except ValueError:
        raise Util.CertoraUserInputError(f"Struct link attribute {link} must be of the form contractA:number=contractB"
                                         f" or contractA:fieldName=contractB")
    return link


def validate_assert_contracts(contract: str) -> str:
    if not re.match(fr"^{Util.SOLIDITY_CONTRACT_NAME_RE}$", contract):
        raise Util.CertoraUserInputError(
            f"Contract name {contract} can include only alphanumeric characters, dollar signs or underscores")
    return contract


def validate_packages(package: str) -> str:
    if not re.search("^[^=]+=[^=]+$", package):
        raise Util.CertoraUserInputError("a package must have the form name=path")
    path = package.split('=')[1]
    if not os.path.isdir(path):
        raise Util.CertoraUserInputError(f"Package path {path} does not exist or is not a directory")
    if not os.access(path, os.R_OK):
        raise Util.CertoraUserInputError(f"No read permissions for for packages directory {path}")
    return package


def validate_settings_attr(settings: str) -> str:
    """
    Gets a string representing flags to be passed to the EVMVerifier jar via --settings,
    in the form '-a,-b=2,-c=r,q,[,..]'
    A flag can have several forms:
    1. A simple name, i.e. -foo
    2. A flag with a value, i.e. -foo=bar
    3. A flag with several values, i.e. -foo=bar,baz
    A value may be wrapped in quotes; if so, it is allowed to contain any non-quote character. For example:
    -foo="-bar,-baz=-foo" is legal
    -foo="-a",b ia also legal
    @raise Util.CertoraUserInputError
    """
    validation_logger.debug(f"settings pre-parsing= {settings}")

    if not isinstance(settings, str):
        raise Util.CertoraUserInputError(f"the settings attribute {settings} is not a string")

    settings = settings.lstrip()

    """
    Split by commas followed by a dash UNLESS it is inside quotes. Each setting must start with a dash.
    For example:
    "-b=2, -assumeUnwindCond, -rule="bounded_supply, -m=withdrawCollateral(uint256, uint256)", -regressionTest"

    will become:
    ['-b=2',
    '-assumeUnwindCond',
    '-rule="bounded_supply, -m=withdrawCollateral(uint256, uint256)"',
    '-regressionTest']
    """
    flags = Util.split_by_delimiter_and_ignore_character(settings, ', -', '"', last_delimiter_chars_to_include=1)

    validation_logger.debug("settings after-split= " + str(settings))
    for flag in flags:
        validation_logger.debug(f"checking setting {flag}")

        if not flag.startswith("-"):
            raise Util.CertoraUserInputError(f"illegal attribute in --settings: {flag}, must start with a dash")
        if flag.startswith("--"):
            raise Util.CertoraUserInputError(f"illegal attribute in --settings: {flag} starts with -- instead of -")

        eq_split = flag.split("=", 1)
        flag_name = eq_split[0][1:]
        if len(flag_name) == 0:
            raise Util.CertoraUserInputError(f"illegal attribute in --settings: {flag} has an empty name")

        if '"' in flag_name:
            raise Util.CertoraUserInputError(
                f'illegal attribute in --settings: {flag} contained an illegal character " in the flag name')

        if len(eq_split) > 1:  # the setting was assigned one or more values
            setting_val = eq_split[1]
            if len(setting_val) == 0:
                raise Util.CertoraUserInputError(f"illegal attribute in --settings: {flag} has an empty value")

            # Values are separated by commas, unless they are inside quotes
            setting_values = Util.split_by_delimiter_and_ignore_character(setting_val, ",", '"')
            for val in setting_values:
                val = val.strip()
                if val == "":
                    raise Util.CertoraUserInputError(f"--setting flag {flag_name} has a missing value after comma")

                # A value can be either entirely wrapped by quotes or contain no quotes at all
                if not val.startswith('"'):
                    if '=' in val:
                        raise Util.CertoraUserInputError(
                            f"--setting flag {flag_name} value {val} contains an illegal character =")
                    if '"' in val:
                        raise Util.CertoraUserInputError(
                            f'--setting flag {flag_name} value {val} contains an illegal character "')
                elif not val.endswith('"'):
                    raise Util.CertoraUserInputError(
                        f'--setting flag {flag_name} value {val} is only partially wrapped in "')

    return settings


def validate_address(address: str) -> str:
    if not re.search(r'^[^:]+:[0-9A-Fa-fxX]+$', address):
        # Regex: name has a single ':', has at least one character before and one alphanumeric character after
        raise Util.CertoraUserInputError(f"Argument {address} of 'address' is in incorrect form. "
                                         "Must be formatted <contractName>:<non-negative number>")
    return address


def validate_solc_optimize_map(args: Dict[str, str]) -> None:
    if not isinstance(args, dict):
        raise Util.CertoraUserInputError("'solc_optimize_map' should be stored as a map "
                                         f"(type was {type(args).__name__})")

    for contract, num_runs in args.items():
        validate_non_negative_integer(num_runs)

    if len(set(args)) == 1:
        validation_logger.warning(f"All contracts are optimized for the same number of runs in --solc_optimize_map."
                                  f" --optimize {list(args)[0]} can be used instead")


def validate_solc_map(args: Dict[str, str]) -> None:
    """
    Checks that the argument is a dictionary of the form <sol_file_1>=<solc_1>,<sol_file_2>=<solc_2>,..
    and if all solc files are valid: they were found, and we have execution permissions for them.

    :param args: argument of --solc_map
    :raises CertoraUserInputError if the format is wrong
    """
    if not isinstance(args, dict):
        raise Util.CertoraUserInputError(f"'solc_map' should be stored as a map (type was {type(args).__name__})")

    for source_file, solc_file in args.items():
        is_solc_file_valid(solc_file)  # raises an exception if file is bad
    value_set = set(args.values())
    if len(value_set) == 1:
        validation_logger.warning(f"All Solidity source files will be compiled with the same Solidity compiler"
                                  f" in --solc_map. --solc {value_set.pop()} can be used instead")


def validate_git_hash(git_hash: str) -> str:
    """
    Validates that correct input was inserted as a git commit hash. It must be between 1 and 40 hexadecimal digits.
    :param git_hash - the string we validate
    :raise CertoraUserInputError if the hash is illegal
    :return the same string if it is a legal git hash
    """
    if not all(c in '0123456789abcdefABCDEF' for c in git_hash):
        raise Util.CertoraUserInputError("Git hash contains non-hexadecimal characters")
    if len(git_hash) < 1 or len(git_hash) > 40:
        raise Util.CertoraUserInputError("Git hash must consist of between 1 and 40 characters")
    return git_hash


def validate_rule(rule: str) -> str:
    """
    validates that rules starts with letter or underscore followed by digits, letters or underscores
    :return: the rule (if no exception was raised)
    """
    regex = r'^[A-Za-z_][A-Za-z0-9_]*$'

    if not re.match(regex, rule):
        raise Util.CertoraUserInputError(f"invalid rule \"{rule}\": rule must starts with a letter or underscore"
                                         " followed only by letters, digits or underscores")
    return rule


MAX_MSG_LEN: int = 256


def validate_msg(msg: str) -> str:
    if len(msg) > MAX_MSG_LEN:
        raise Util.CertoraUserInputError(f"'msg' can't accept a message longer than {MAX_MSG_LEN} chars")

    additional_chars = {'(', ' ', ',', '/', '[', "'", '-', '"', '_', ']', '.', ')', ':', '\\', '='}
    valid_chars = set(string.ascii_letters) | set(string.digits) | additional_chars
    invalid_chars = set(msg) - valid_chars
    if len(invalid_chars) > 0:
        raise Util.CertoraUserInputError(f"{invalid_chars} not allowed in 'msg'")
    return msg


def __validate_enum_value(string: str, enum_class: Type[Enum]) -> str:
    legal_values = [e.name.lower() for e in enum_class]
    if string.lower() not in legal_values:
        raise Util.CertoraUserInputError(f"{string} is not a valid value. Possible values are: {legal_values}.")
    return string


def validate_sanity_value(value: str) -> str:
    return __validate_enum_value(value, RuleSanityValue)


def validate_test_value(value: str) -> str:
    return __validate_enum_value(value, Util.TestValue)


def validate_coverage_info(value: str) -> str:
    return __validate_enum_value(value, CoverageInfoValue)


def validate_fe_value(value: str) -> str:
    return __validate_enum_value(value, Util.FeValue)


def validate_run_source(string: str) -> str:
    """
    Returns the run source string as uppercase, as that is what the cloud expects.
    We allow the user to insert the run source in any casing they want
        (e.g., we accept command, Command, COMMAND and CoMmAnD, but always send COMMAND)
    """
    return __validate_enum_value(string, RunSources).upper()


def validate_multi_example_value(value: str) -> str:
    return __validate_enum_value(value, MultiExampleValue)


def validate_server_value(value: str) -> str:
    """
    A server may consist only of letters, numbers, dashes and underscores
    """
    if not re.match(r"^[a-zA-Z_0-9\-]+$", value):
        raise Util.CertoraUserInputError(f"illegal 'server' argument {value}")
    return value


def validate_false(value: str) -> str:
    """
    This is used when there's a jar flag with a default value of true that we want to set to
    false through a CLI flag. We'll create a string argument that when specified can only hold
    the value 'false'.
    """
    return __validate_enum_value(value, FalseValue)


def validate_on_off(value: str) -> str:
    return __validate_enum_value(value, OnOffValue)


def parse_dict(conf_key: str, input_string: str) -> Dict[str, str]:
    """
    convert conf attribute string of the form <key>=<value>,<key>=<value>,.. to a Dict.
    Keys with different values raise an exception
    """
    input_string = input_string.replace(' ', '')  # remove whitespace

    """
    Regex explanation:
    ([^=,]+=[^=,]+) describes a single key-value pair in the map. It must contain a single = sign, something before
    and something after.
    We allow more than one, as long as all but the last are followed by a comma hence ([^=,]+=[^=,]+,)*
    We allow nothing else inside the argument, so all is wrapped by ^ and $
    """
    matches = re.search(r'^([^=,]+=[^=,]+,)*([^=,]+=[^=,]+)$', input_string)

    if matches is None:
        raise argparse.ArgumentTypeError(f"{conf_key} argument {input_string} is of wrong format. Must be of format:"
                                         f"<key>=<value>[,..]")

    return_dict = {}  # type: Dict[str, str]

    for match in input_string.split(','):
        key, value = match.split('=')
        if key in return_dict:
            if return_dict[key] == value:
                validation_logger.warning(f"in {conf_key} {key}={value} appears multiple times and is redundant")
            else:
                raise argparse.ArgumentTypeError(f"key {key} was given two different values: "
                                                 f"{return_dict[key]} and {value}") from None
        else:
            return_dict[key] = value

    validation_logger.debug(f"{conf_key} = {return_dict}")
    return return_dict


def validate_wait_for_results(value: str) -> str:
    return __validate_enum_value(value, WaitForResultOptions)


def validate_for_conf_file_duplicates(conf_file: IO[str]) -> None:

    def detect_duplicates(ordered_pairs: Dict) -> None:
        result: Dict[str, Any] = {}
        for key, val in ordered_pairs:
            if key in result:
                vals = f"values: '{val}' and {result[key]}" if val and result[key] else ""
                raise Util.CertoraUserInputError(f"Duplicate key specified for key {key}. {vals}")
            result[key] = val

    json5.load(conf_file, object_pairs_hook=detect_duplicates)
    conf_file.seek(0)
