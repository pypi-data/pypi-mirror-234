import csv
import json
import os
import subprocess
from abc import ABCMeta
from enum import Enum, unique, auto
import sys
import platform
import shlex
import shutil
import re
import queue
import math
from typing import Any, Callable, Dict, List, Optional, Set, Union, Generator, Tuple, Iterable
from pathlib import Path
scripts_dir_path = Path(__file__).parent.parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))
from contextlib import contextmanager
from Shared.ExpectedComparator import ExpectedComparator
import logging
import random
import time
import tempfile
from datetime import datetime

io_logger = logging.getLogger("file")
# logger for issues calling/shelling out to external functions
process_logger = logging.getLogger("rpc")
# messages from the verification results
verification_logger = logging.getLogger("verification")
# errors handling csvs (???)
csv_logger = logging.getLogger("csv")
# logger for issues regarding type checking
typecheck_logger = logging.getLogger("type_check")
context_logger = logging.getLogger("context")
LEGAL_CERTORA_KEY_LENGTHS = [32, 40]

# bash colors
BASH_ORANGE_COLOR = "\033[33m"
BASH_END_COLOR = "\033[0m"
BASH_GREEN_COLOR = "\033[32m"
BASH_RED_COLOR = "\033[31m"
BASH_PURPLE_COLOR = "\033[35m"

VERIFICATION_ERR_MSG_PREFIX = "Prover found violations:"
VERIFICATION_SUCCESS_MSG = "No errors found by Prover!"

DEFAULT_SOLC = "solc"
ENVVAR_CERTORA = "CERTORA"
PUBLIC_KEY = "795ebbac71ae5fd6a19e7a214a524b064e33ff05"
CERTORA_INTERNAL_ROOT = Path(".certora_internal")
PRODUCTION_PACKAGE_NAME = "certora-cli"
BETA_PACKAGE_NAME = "certora-cli-beta"
DEV_PACKAGE_NAME_PREFIX = f"{PRODUCTION_PACKAGE_NAME}-"
CERTORA_BUILD_DIRECTORY = Path("")
CERTORA_JARS = Path("certora_jars")
CERTORA_BINS = Path("certora_bins")
CERTORA_CLI_VERSION_METADATA = Path("CERTORA-CLI-VERSION-METADATA.json")
PRE_AUTOFINDER_BACKUP_DIR = Path(".pre_autofinders")
POST_AUTOFINDER_BACKUP_DIR = Path(".post_autofinders")

PACKAGE_FILE = Path("package.json")
REMAPPINGS_FILE = Path("remappings.txt")
RECENT_JOBS_FILE = Path(".certora_recent_jobs.json")
LAST_CONF_FILE = Path("run.conf")

ALPHA_PACKAGE_NAME = 'certora-cli-alpha-master'
BETA_PACKAGE_NAME = 'certora-cli-beta'
SOLIDITY_CONTRACT_NAME_RE = r"[\w_\$]+"  # contract names in solidity consists of alphnums, underscores and dollar signs

VYPER = 'vyper'
NEW_LINE = '\n'  # for new lines in f strings

# Type alias definition, not a variable
CompilerVersion = Tuple[int, int, int]


@unique
class SupportedServers(Enum):
    """
    mapping between servers and their url
    """
    STAGING = 'https://vaas-stg.certora.com'
    PRODUCTION = 'https://prover.certora.com'


def get_build_dir() -> Path:
    return CERTORA_BUILD_DIRECTORY


def get_random_build_dir() -> Path:
    for tries in range(3):
        build_uuid = f"{datetime.now().strftime('%y_%m_%d_%H_%M_%S')}_{random.randint(0, 999):03d}"
        build_dir = CERTORA_INTERNAL_ROOT / Path(build_uuid)
        if not build_dir.exists():
            return build_dir
        time.sleep(0.5)
    raise Exception('Unable to generate random build directory')


def reset_certora_internal_dir(build_dir_str: Optional[str] = None) -> None:
    """
    build_dir_str constraints are defined in type_build_dir (basically not an existing file/dir and open for creating
    a new directory
    """
    global CERTORA_BUILD_DIRECTORY
    if build_dir_str is None:
        build_dir = get_random_build_dir()
        safe_create_dir(CERTORA_INTERNAL_ROOT)  # create, allow generating symlink to latest when directory is empty
        if is_windows():
            build_dir = Path(".")
    else:
        build_dir = Path(build_dir_str)

    CERTORA_BUILD_DIRECTORY = Path(build_dir)
    if build_dir_str is None:
        # We are using the default dir, with the BUILD_UUID. Add a symlink to the last one to run, for ease of use.
        # Note that when running concurrently 'latest' may not be well defined, but for local usage it could be useful.
        last_build = build_dir.parent / 'latest'

        try:
            last_build.unlink(missing_ok=True)
            last_build.symlink_to(build_dir.relative_to(build_dir.parent), target_is_directory=True)
        except Exception as e:
            # This is a nice-to-have thing, so if we fail for some reason (e.g. permission error)
            # we'll just continue without it.
            io_logger.warning(f"Failed to create the '{last_build}' symlink. {e}")


def path_in_certora_internal(path: Path) -> Path:
    return path if (path.parent == get_build_dir()) else get_build_dir() / path


def get_certora_config_dir() -> Path:
    return path_in_certora_internal(Path(".certora_config"))


def get_certora_sources_dir() -> Path:
    return path_in_certora_internal(Path(".certora_sources"))


def get_certora_build_file() -> Path:
    return path_in_certora_internal(Path(".certora_build.json"))


def get_certora_verify_file() -> Path:
    return path_in_certora_internal(Path(".certora_verify.json"))


def get_certora_metadata_file() -> Path:
    return path_in_certora_internal(Path(".certora_metadata.json"))


def get_resource_errors_file() -> Path:
    return path_in_certora_internal(Path("resource_errors.json"))


def get_debug_log_file() -> Path:
    return path_in_certora_internal(Path("certora_debug_log.txt"))


def get_extension_info_file() -> Path:
    return path_in_certora_internal(Path(".vscode_extension_info.json"))


def get_zip_output_url_file() -> Path:
    return CERTORA_INTERNAL_ROOT / '.zip-output-url.txt'


def get_recent_jobs_file() -> Path:
    return CERTORA_INTERNAL_ROOT / RECENT_JOBS_FILE


def get_last_conf_file() -> Path:
    return path_in_certora_internal(LAST_CONF_FILE)


class SolcCompilationException(Exception):
    pass


class CertoraUserInputError(ValueError):
    pass


MIN_JAVA_VERSION = 11  # minimal java version to run the local type checker jar


def __colored_text(txt: str, color: str) -> str:
    return color + txt + BASH_END_COLOR


def orange_text(txt: str) -> str:
    return __colored_text(txt, BASH_ORANGE_COLOR)


def purple_text(txt: str) -> str:
    return __colored_text(txt, BASH_PURPLE_COLOR)


def red_text(txt: str) -> str:
    return __colored_text(txt, BASH_RED_COLOR)


def green_text(txt: str) -> str:
    return __colored_text(txt, BASH_GREEN_COLOR)


def print_completion_message(txt: str, flush: bool = False) -> None:
    print(green_text(txt), flush=flush)


def print_progress_message(txt: str, flush: bool = False) -> None:
    if not is_ci_or_git_action():
        print(txt, flush=flush)


def is_ci_or_git_action() -> bool:
    if os.environ.get("GITHUB_ACTIONS", False) or os.environ.get("CI", False):
        return True
    return False


def remove_file(file_path: Union[str, Path]) -> None:  # TODO - accept only Path
    if isinstance(file_path, str):
        try:
            os.remove(file_path)
        except OSError:
            pass
    else:
        try:
            # When we upgrade to Python 3.8, we can use unlink(missing_ok=True) and remove the try/except clauses
            file_path.unlink()
        except FileNotFoundError:
            pass


def get_package_and_version() -> Tuple[bool, str, str]:
    """
    @return: A tuple (is insatlled package, package name, version)
    is installed package - True if we run an installed package, false if we run as a local script
    package name - either certora-cli / certora-cli-beta, or certora-cli-alpha-master and others
    version - the python package version in format X.Y.Z if found
    """
    # Note: the most common reason not to have an installed package is in circleci
    version_metadata_file = get_package_resource(CERTORA_JARS / CERTORA_CLI_VERSION_METADATA)
    if not version_metadata_file.exists():
        return False, "", ""

    try:
        with open(version_metadata_file) as version_metadata_handle:
            version_metadata = json.load(version_metadata_handle)
            if "name" in version_metadata and "version" in version_metadata:
                return True, version_metadata["name"], version_metadata["version"]
            else:
                raise Exception(f"Invalid format for {version_metadata_file}, got {version_metadata}")
    except OSError as e:  # json errors - better to just propagate up
        raise Exception(f"Failed to open {version_metadata_file}: {e.strerror}")


def check_results_from_file(output_path: str, expected_filename: str) -> bool:
    with open(output_path) as output_file:
        actual = json.load(output_file)
        return check_results(actual, expected_filename)


def check_results(actual: Dict[str, Any], expected_filename: str) -> bool:
    actual_results = actual
    if os.path.exists(expected_filename):  # compare actual results with expected
        with open(expected_filename) as expected_file:
            expected = json.load(expected_file)
        if 'rules' in actual_results and 'rules' in expected:
            comparator = ExpectedComparator(actual_results["rules"], expected["rules"], {}, {})
            if comparator.has_violations:
                verification_logger.error(f'{VERIFICATION_ERR_MSG_PREFIX}')
                print(comparator.get_violations_table())
                return False
        if ('rules' not in actual_results) ^ ('rules' not in expected):
            verification_logger.error(f'{VERIFICATION_ERR_MSG_PREFIX}')
            return False

        print_completion_message(f"{VERIFICATION_SUCCESS_MSG} (based on {expected_filename})")
        return True
    # if expected results are not defined
    # traverse results and look for violation
    errors = []
    result = True

    if "rules" not in actual_results:
        errors.append("No rules in results")
        result = False
    elif len(actual_results["rules"]) == 0:
        errors.append("No rule results found. Please make sure you wrote the rule and method names correctly.")
        result = False
    else:
        for rule in actual_results["rules"].keys():
            rule_result = actual_results["rules"][rule]
            if isinstance(rule_result, str) and rule_result != 'SUCCESS':
                errors.append("[rule] " + rule)
                result = False
            elif isinstance(rule_result, dict):
                # nested rule - ruleName: {result1: [functions list], result2: [functions list] }
                nesting = rule_result
                violating_functions = ""
                for method in nesting.keys():
                    if method != 'SUCCESS' and len(nesting[method]) > 0:
                        violating_functions += '\n  [func] ' + '\n  [func] '.join(nesting[method])
                        result = False
                if violating_functions:
                    errors.append("[rule] " + rule + ":" + violating_functions)

    if not result:
        verification_logger.error(VERIFICATION_ERR_MSG_PREFIX)
        verification_logger.error('\n'.join(errors))
        return False

    print_completion_message(VERIFICATION_SUCCESS_MSG)
    return True


def is_windows() -> bool:
    return platform.system() == 'Windows'


def replace_file_name(old_file: str, new_file_name: str) -> str:
    """
    :param old_file: the full original path
    :param new_file_name: the new base name of the file
    :return: file_with_path with the base name of the file replaced with new_file_name,
             preserving the file extension and the base path
    """
    old_file_path = Path(old_file)
    return str(old_file_path.parent / f'{new_file_name}')


def safe_create_dir(path: Path) -> None:
    if path.is_dir():
        io_logger.debug(f"directory {path} already exists")
        return
    path.mkdir(parents=True, exist_ok=True)


def safe_copy_folder(source: Path, dest: Path, ignore_patterns: Callable[[str, List[str]], Iterable[str]]) -> None:
    """
    Safely copy source to dest. Assume dest does not exists.
    On certain OS/kernels/FS, copying a folder f into a subdirectory of f will
    send copy tree into an infinite loop. This sidesteps the problem by first copying through a temporary folder.
    See https://github.com/Certora/EVMVerifier/pull/3982 for details.
    """
    copy_temp = tempfile.mkdtemp()
    shutil.copytree(source, copy_temp, ignore=ignore_patterns, dirs_exist_ok=True)
    shutil.copytree(copy_temp, dest)
    shutil.rmtree(copy_temp, ignore_errors=True)


def as_posix(path: str) -> str:
    """
    Converts path from windows to unix
    :param path: Path to translate
    :return: A unix path
    """
    return path.replace("\\", "/")


def normalize_double_paths(path: str) -> str:
    """
    Handles an oddity of paths from absolutePath nodes in solc AST,
    specifically "//" instead of just "/"
    """
    return path.replace("//", "/")


def abs_posix_path(path: Union[str, Path]) -> str:
    """
    Returns the absolute path, unix style
    :param path: Path to change
    :return: A posix style absolute path string
    """
    return as_posix(str(abs_posix_path_obj(path)))


def abs_posix_path_obj(path: Union[str, Path]) -> Path:
    """
    Returns the absolute path, unix style
    :param path: Path to change
    :return: A posix style absolute Path, resolving symlinks
    """
    sanitized_path = as_posix(str(path))  # Windows works with / as file separator, so we always convert
    abs_path = Path(sanitized_path).expanduser().resolve()
    return abs_path


def abs_posix_path_relative_to_root_file(rel_path: Path, root_file: Path) -> Path:
    """
     Returns the absolute path, unix style
     :param rel_path: Relative path to change.
     :param root_file: rel_path is assumed to be relative to the directory of the file root_file.
     :return: A posix style absolute path
    """
    root_dir = root_file.parent
    file_path = root_dir / rel_path
    return Path(abs_posix_path(file_path))


def convert_path_for_solc_import(path: Union[Path, str]) -> str:
    """
    Converts a path to a solc-compatible import.
    Solc paths only accept / as a file separator, and do not accept drives in path
    :param path: A path to convert
    :return: the converted path
    """
    unix_file_sep_path = abs_posix_path(path)
    driveless_path = re.sub("^[a-zA-Z]:", "", unix_file_sep_path)
    return as_posix(os.path.abspath(driveless_path))


def remove_and_recreate_dir(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    safe_create_dir(path)


def prepare_call_args(cmd: str) -> List[str]:
    """
    Takes a command line as a string and returns a list of strings that consist that line.
    Importantly, does not interpret forward slashes used for newline continuation as a word.
    We replace a call to a Python script with a call to the Python executable first.
    We also fix the path to the certora root directory
    :param cmd - the command line we split. We assume it contains no comments!
    :return - a list of words that make up the command line given
    """
    if is_windows():
        """
        There is no good shlex alternative to Windows, but quoting works well, and spaces should work too
        see https://stackoverflow.com/questions/33560364/python-windows-parsing-command-lines-with-shlex
        """
        split = cmd.split()
    else:
        # Using shlex here is necessary, as otherwise quotes are not handled well especially in lists like "a/path",.
        split = shlex.split(cmd)
    if split[0].endswith('.py'):
        # sys.executable returns a full path to the current running python, so it's good for running our own scripts
        certora_root = get_certora_root_directory()
        args = [sys.executable, (certora_root / split[0]).as_posix()] + split[1:]
    else:
        args = split
    return args


def get_certora_root_directory() -> Path:
    return Path(os.getenv(ENVVAR_CERTORA, os.getcwd()))


def get_certora_envvar() -> str:
    return os.getenv(ENVVAR_CERTORA, "")


def get_certora_dump_config() -> str:
    return os.getenv("CERTORA_DUMP_CONFIG", "")


def which(filename: str) -> Optional[str]:
    if is_windows() and not filename.endswith(".exe"):
        filename += ".exe"

    # TODO: find a better way to iterate over all directories in $Path
    for dirname in os.environ['PATH'].split(os.pathsep) + [os.getcwd()]:
        candidate = os.path.join(dirname, filename)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return filename

    return None


def read_json_file(file_name: Path) -> Dict[str, Any]:
    with file_name.open() as json_file:
        json_obj = json.load(json_file)
        return json_obj


def write_json_file(data: Union[Dict[str, Any], List[Dict[str, Any]]], file_name: Path) -> None:
    with file_name.open("w+") as json_file:
        json.dump(data, json_file, indent=4)


def output_to_csv(filename: str, fieldnames: List[str], row: Dict[str, Any]) -> bool:
    """
        Creates and appends the row to csv file

        @param filename: csv filename without the extension
        @param fieldnames: headers of the csv file
        @param row: data to append (as a row) to the csv file

        @return: true if completed successfully
    """
    try:
        csv_path = Path(f'{filename}.csv')
        if csv_path.exists():
            with csv_path.open("a") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(row)
        else:
            with csv_path.open('a+') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(row)
        return True
    except ValueError as e:  # when the row contains fields not in fieldnames (file header)
        csv_logger.error("value conversion failed", exc_info=e)
        return False


class NoValEnum(Enum):
    """
    A class for an enum where the numerical value has no meaning.
    """

    def __repr__(self) -> str:
        """
        Do not print the value of this enum, it is meaningless
        """
        return f'<{self.__class__.__name__}.{self.name}>'

    @classmethod
    def values(cls) -> List[str]:
        return list(map(lambda c: str(c), cls))  # type: ignore

    def __str__(self) -> str:
        return self.name.lower()

class Mode(NoValEnum):
    """
    Mode of operation - the modes are mutually exclusive:

    1. CLI parameters consist of a single .tac file.
        We check the verification condition given by that file.
    2. CLI parameters consist of a single .conf file.
        A .conf file is created on each tool run inside the .certora_config directory. It contains the command line
        options that were used for the run (in a parsed format).
        We take the options given from that file as a basis for this run; additionally given command line options
        override options given in the .conf file.
    3. CLI parameters consist of one or more Solidity (.sol) files and the `--verify` option is set (the option takes
        an additional .spec/.cvl file).
        We use the given .spec/.cvl file to create and check verification conditions for the given Solidity contracts.
    4. CLI parameters consist of one or more Solidity (.sol) files and the `--assert_contracts` option is set.
        We create and check verification conditions based on the `assert` statements in the given Solidity contracts.
    5. CLI parameters consist of 0 files but all are provided in --bytecode.
        The bytecode files are in JSON, and adhere to a format given by blockchain scrapers.
        --bytecode_spec must be specified as well if this mode is used.
        The spec will be checked against the first bytecode provided, with the other bytecodes serving as auxiliary.
    7. CLI parameters consist of one object (.o|so) file. The object file already contains `assert` statements.
    """
    TAC = "a single .tac file"
    CONF = "a single .conf file"
    VERIFY = "using --verify"
    ASSERT = "using --assert_contracts"
    BYTECODE = "using --bytecode"
    SOLANA = "a single .o or .so file"


def mode_has_spec_file(mode: Mode) -> bool:
    return mode not in [Mode.ASSERT, Mode.TAC]


def is_hex_or_dec(s: str) -> bool:
    """
    @param s: A string
    @return: True if it is a decimal or hexadecimal number
    """
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def is_hex(number: str) -> bool:
    """
    @param number: A string
    @return: True if the number is a hexadecimal number:
        - Starts with 0
        - Second character is either x or X
        - All other characters are digits 0-9, or letters a-f or A-F
    """
    match = re.search(r'^0[xX][0-9a-fA-F]+$', number)
    return match is not None


def hex_str_to_cvt_compatible(s: str) -> str:
    """
    @param s: A string representing a number in base 16 with '0x' prefix
    @return: A string representing the number in base 16 but without the '0x' prefix
    """
    assert is_hex(s)
    return re.sub(r'^0[xX]', '', s)


def decimal_str_to_cvt_compatible(s: str) -> str:
    """
    @param s: A string representing a number in base 10
    @return: A string representing the hexadecimal representation of the number, without the '0x' prefix
    """
    assert s.isnumeric()
    return re.sub(r'^0[xX]', '', hex(int(s)))


def split_by_delimiter_and_ignore_character(input_str: str, delimiter: str, ignore_splitting_char: str,
                                            last_delimiter_chars_to_include: int = 0) -> List[str]:
    """
    Splits a string by a given delimiter, ignoring anything between a special pair of characters.

    For example, if the delimiter is a comma, and the ignore splitting character is an asterisk, then the input:
    hello,we,dislike*splitting,if,*it,is,complex
    Will return:
    ['hello', 'we', 'dislike*splitting,if,*it', 'is', 'complex']

    If we want to include some of the last characters of the delimiter in the preceding substring, we should specify a
    positive number for the parameter last_delimiter_chars_to_include. A negative number will not include that amount
    of characters after the delimiter in the substrings.

    A more complex example, for delimiter ", -", ignore character ", the input string:

    "-b=2, -assumeUnwindCond, -rule=bounded_supply, -m=withdrawCollateral(uint256, (bool, bool)), -regressionTest,
         -solvers=bitwuzla, yices"

    will return:
    ['-b=2',
    '-assumeUnwindCond',
    '-rule=bounded_supply',
    '-m=withdrawCollateral(uint256, (bool, bool))',
    '-regressionTest',
    '-solvers=bitwuzla, yices']

    Assumptions:
    - We do not check for the validity of the last_delimiter_chars_to_include parameter. If it is too large or too
    small, we will get an out-of-bounds error.

    Notes:
    - We currently do not support a different character to start and end an ignored section, like an opening and
    closing parenthesis.

    @param input_str a string we want to split to substrings
    @param delimiter a sequence of characters by which we split
    @param ignore_splitting_char a character that must appear an even amount of times in the string. Between every
           pair of appearances, we skip splitting
    @param last_delimiter_chars_to_include a number of characters from the end of the delimeter to include in the
           following substring. See above.
    @returns a list of strings that represents individual settings to pass to the jar. They might have illegal syntax.
    """

    if input_str.count(ignore_splitting_char) % 2 != 0:
        raise ValueError(f'Uneven number of {ignore_splitting_char} in {input_str}')

    substrings = []  # type: List[str]

    i = 0
    substring_start_index = 0
    ignore_splitting = False  # if we are between the two ignore characters, we skip splitting

    while i < len(input_str):
        if input_str[i] == ignore_splitting_char:
            ignore_splitting = not ignore_splitting
        elif not ignore_splitting:
            if i + len(delimiter) < len(input_str):
                if input_str[i:i + len(delimiter)] == delimiter:
                    substrings.append(input_str[substring_start_index:i])
                    i += len(delimiter)
                    substring_start_index = i - last_delimiter_chars_to_include
                    continue
        i += 1

    if substring_start_index < len(input_str):
        substrings.append(input_str[substring_start_index:])

    return substrings


def string_distance_function(input_str: str, dictionary_str: str) -> float:
    """
    Calculates a modified levenshtein distance between two strings. The distance function is modified to penalize less
    for more common user mistakes.
    Each subtraction, insertion or replacement of a character adds 1 to the distance of the two strings, unless:
    1. The input string is a prefix of the dictionary string or vice versa - the distance is 0.1 per extra letter.
    2. The replacement is between two equal letter except casing - adds nothing to the distance
    3. The subtraction/addition is of an underscore, adds 0.1 to the distance
    4. Repeated characters cost nothing, e.g. 'balloon', 'baloon' and 'balllllloooonn' have distance 0 from each other

    :param input_str: the string the user gave as input, error-prone
    :param dictionary_str: a legal string we compare the wrong input to
    :return a distance measure between the two string. A low number indicates a high probably the user to give the
            dictionary string as input
    """
    # treat special cases first:

    input_str = input_str.lower()
    dictionary_str = dictionary_str.lower()

    if input_str == dictionary_str:
        return 0
    if dictionary_str.startswith(input_str) or input_str.startswith(dictionary_str):
        diff = abs(len(input_str) - len(dictionary_str))
        return 0.1 * diff

    """
    We are calculating the Levenshtein distance with a dynamic programming algorithm based on
    https://en.wikipedia.org/wiki/Levenshtein_distance

    Each matrix value distance_matrix[row][col] we calculate represent the distance between the two prefix substrings
    input_str[0..row-1] and dictionary_str[0..col-1]

    NOTE: our implementation differs from the classic implementation in that the cost of deletions/insertions is not
    constant
    """

    # Initialize matrix of zeros
    rows = len(input_str) + 1
    cols = len(dictionary_str) + 1

    distance_matrix = []
    for row in range(rows):
        column = []
        for j in range(cols):
            column.append(0.0)
        distance_matrix.append(column)

    # Populate matrix of zeros with the indices of each character of both strings
    for i in range(1, rows):
        distance_matrix[i][0] = i
    for k in range(1, cols):
        distance_matrix[0][k] = k

    # Calculate modified Levenshtein distance
    for col in range(1, cols):
        for row in range(1, rows):
            if input_str[row - 1] == dictionary_str[col - 1]:
                # No cost if the characters are the same up to casing in the two strings
                cost: float = 0
            elif input_str[row - 1] == '_' or dictionary_str[col - 1] == '_':
                # common mistake
                cost = 0.1
            else:
                # full cost
                cost = 1
            distance_matrix[row][col] = min(distance_matrix[row - 1][col] + cost,         # Cost of deletions
                                            distance_matrix[row][col - 1] + cost,         # Cost of insertions
                                            distance_matrix[row - 1][col - 1] + cost)     # Cost of substitutions

    return distance_matrix[rows - 1][cols - 1]


def get_closest_strings(input_word: str, word_dictionary: List[str],
                        distance: Callable[[str, str], float] = string_distance_function,
                        max_dist: float = 4, max_dist_ratio: float = 0.5, max_suggestions: int = 2,
                        max_delta: float = 0.2) -> List[str]:
    """
    Gets an input word, which doesn't belong to a dictionary of predefined words, and returns a list of the closest
    words from the dictionary, with respect to a distance function.

    :param input_word: The word we look for closest matches of.
    :param word_dictionary: A collection of words to suggest matches from.
    :param distance: The distance function we use to measure proximity of words.
    :param max_dist: The maximal distance between words, over which no suggestions will be made.
    :param max_dist_ratio: A maximal ratio between the distance and the input word's length. No suggestions will be made
                           over this ratio.
    :param max_suggestions: The maximal number of suggestions to return.
    :param max_delta: We stop giving suggestions if the next best suggestion is worse than the one before it by more
                      than the maximal delta.
    :return: A list of suggested words, ordered from the best match to the worst.
    """
    distance_queue: queue.PriorityQueue = queue.PriorityQueue()  # Ordered in a distance ascending order

    for candidate_word in word_dictionary:
        dist = distance(input_word, candidate_word)
        distance_queue.put((dist, candidate_word))

    all_suggestions: List[str] = []
    last_dist = None

    while not distance_queue.empty() and len(all_suggestions) <= max_suggestions:
        suggested_dist, suggested_rule = distance_queue.get()
        if suggested_dist > max_dist or suggested_dist / len(input_word) > max_dist_ratio:
            break  # The distances are monotonically increasing
        if (last_dist is None) or (suggested_dist - last_dist <= max_delta):
            all_suggestions.append(suggested_rule)
            last_dist = suggested_dist

    return all_suggestions


def get_readable_time(milliseconds: int) -> str:
    # calculate (and subtract) whole hours
    milliseconds_in_hour = 3600000  # 1000 * 60 * 60
    hours = math.floor(milliseconds / milliseconds_in_hour)
    milliseconds -= hours * milliseconds_in_hour

    # calculate (and subtract) whole minutes
    milliseconds_in_minute = 60000  # 1000 * 60
    minutes = math.floor(milliseconds / milliseconds_in_minute)
    milliseconds -= minutes * milliseconds_in_minute

    # seconds
    seconds = math.floor(milliseconds / 1000)

    milliseconds -= seconds * 1000
    duration = ""

    if hours > 0:
        duration += f"{hours}h "
    duration += f"{minutes}m {seconds}s {milliseconds}ms"
    return duration


def flush_stdout() -> None:
    print("", flush=True)


def flatten_nested_list(nested_list: List[list]) -> list:
    """
    @param nested_list: A list of lists: [[a], [b, c], []]
    @return: a flat list, in our example [a, b, c]. If None was entered, returns None
    """
    return [item for sublist in nested_list for item in sublist]


def flatten_set_list(set_list: List[Set[Any]]) -> List[Any]:
    """
    Gets a list of sets, returns a list that contains all members of all sets without duplicates
    :param set_list: A list containing sets of elements
    :return: A list containing all members of all sets. There are no guarantees on the order of elements.
    """
    ret_set = set()
    for _set in set_list:
        for member in _set:
            ret_set.add(member)
    return list(ret_set)


def is_relative_to(path1: Path, path2: Path) -> bool:
    """certora-cli currently requires python3.8 and it's the last version without support for is_relative_to.
    Shamelessly copying.
    """
    # return path1.is_relative_to(path2)
    try:
        path1.relative_to(path2)
        return True
    except ValueError:
        return False


def find_jar(jar_name: str) -> Path:
    # if we are a dev running certoraRun.py (local version), we want to get the local jar
    # if we are a dev running an installed version of certoraRun, we want to get the installed jar
    # how would we know? if $CERTORA is not empty, __file__ is relative to $CERTORA,
    # and we have a local jar, then we need the local jar. Otherwise we take the installed one.
    # A regular user should not have $CERTORA enabled, or the local jar doesn't exist.
    # if $CERTORA is set to site-packages, it should be fine too. (but let's hope nobody does that.)
    certora_home = get_certora_envvar()

    if certora_home != "":
        local_certora_path = Path(certora_home) / CERTORA_JARS / jar_name
        if is_relative_to(Path(__file__), Path(certora_home)) and local_certora_path.is_file():
            return local_certora_path

    return get_package_resource(CERTORA_JARS / jar_name)


def get_package_resource(resource: Path) -> Path:
    """
    Returns a resource installed in the package. Since we are in
    `site-packages/certora_cli/Shared/certoraUtils.py`, we go 3 parents up, and then can access, e.g.,
    - certora_jars (sibling to certora_cli)
    """
    return Path(__file__).parents[2] / resource


def run_typechecker(typechecker_name: str, with_typechecking: bool, rules_to_check: Optional[List[str]] = None,
                    suppress_output: bool = False) -> int:
    """
    Runs a spec typechecker or syntax checker and returns an integer for the success/failure as detailed below:
    @param typechecker_name - the name of the jar that we should run for running typechecking
    @param with_typechecking - True if we want full typechecking including build (Solidity outputs) file,
                                False if we run only the leaner syntax checking.
    @param rules_to_check - A list of rules that will be verified to exist in the spec
    @param suppress_output - True if we do not wish to redirect the typechecker's output to the screen.
    @returns int - -1 if could not find the typechecker jar,
                   otherwise returns the exit code returned by the typechecker.
    """
    # Find path to typechecker jar
    path_to_typechecker = find_jar(typechecker_name)

    typecheck_logger.info(f"Path to typechecker is {path_to_typechecker}")
    # if typechecker jar does not exist, we just skip this step
    if not path_to_typechecker.is_file():
        typecheck_logger.error(f"Could not run type checker locally: file not found {path_to_typechecker}")
        return -1

    # args to typechecker
    typecheck_cmd = f"java -jar {path_to_typechecker} " \
                    f'-buildDirectory "{get_build_dir().resolve()}"'
    if with_typechecking:
        typecheck_cmd = f"{typecheck_cmd} -typeCheck"
    if rules_to_check:
        typecheck_cmd = f"{typecheck_cmd} -rule '{','.join(rules_to_check).replace(' ', '')}'"

    # run it - exit with code 1 if failed
    if not suppress_output:
        exit_code = run_jar_cmd(typecheck_cmd, False,
                                custom_error_message=f"Failed to compile spec file in "
                                                     f"{get_certora_build_file().parent.resolve()}",
                                logger_topic="type_check")
    else:
        exit_code = run_jar_cmd(typecheck_cmd, False, print_err=False)

    return exit_code


def run_local_spec_check(with_typechecking: bool, rules_to_check: Optional[List[str]] = None) -> int:
    """
    Runs the local type checker in one of two modes: (1) syntax only,
        and (2) including full typechecking after building the contracts
    :param with_typechecking: True if we want the full check, false for a quick CVL syntax check
    :param rules_to_check: A list of rules that will be verified to exist in the spec
    @return 0 on success or if the type checking was skipped, an error exit code otherwise
    """
    # Check if java exists on the machine
    java = which("java")
    if java is None:
        print(
            f"`java` is not installed. Installing Java version {MIN_JAVA_VERSION} or later will enable faster "
            f"CVL specification syntax checking before uploading to the cloud.")
        return 0  # if user doesn't have java installed, user will have to wait for remote type checking

    try:
        java_version_str = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode()
        major_java_version = re.search(r'version \"(\d+).*', java_version_str).groups()[0]  # type: ignore[union-attr]
        if int(major_java_version) < MIN_JAVA_VERSION:
            print(f"Installed Java version is too old to check CVL specification files locally. Installing Java version"
                  f" {MIN_JAVA_VERSION} or later will enable faster CVL syntax checking before uploading to the cloud.")
            # if user doesn't have a valid version of java installed, user will have to wait for remote CVL syntax
            # checking
            return 0
    except (subprocess.CalledProcessError, AttributeError):
        print("Couldn't find the installed Java version. Skipping local CVL specification checking")
        # if user doesn't have a valid version of java installed, user will have to wait for remote CVL syntax
        # checking
        return 0

    exit_code = run_typechecker("Typechecker.jar", with_typechecking, rules_to_check=rules_to_check)
    return exit_code


def run_jar_cmd(jar_cmd: str, override_exit_code: bool, custom_error_message: Optional[str] = None,
                logger_topic: Optional[str] = "run", print_output: bool = False, print_err: bool = True) -> int:
    """
    @return: 0 on success, an error exit code otherwise
    @param override_exit_code if true, always returns 0 (ignores/overrides non-zero exit codes of the jar subprocess)
    @param custom_error_message if specified, determines the header of the error message printed for non-zero exit codes
    @param logger_topic the topic of the logger being used
    @param print_output If True, the process' standard output will be printed on the screen
    @param print_err If True, the process' standard error will be printed on the screen
    @param jar_cmd a command line that runs a jar file (EVMVerifier or Typechecker)

    One may be confused why we need both override_exit_code and print_err, that have a similar effect:
    logs are not printed if either override_exit_code is enabled or print_err is disabled.

    The difference is that override_exit_code also controls the return value of this function and print_err
    only affects the logging.

    The use case for setting override_exit_code is the comparison of expected files instead of the Prover's default
    exit code which is failure in any case of not all-successful rules.

    """
    logger = logging.getLogger(logger_topic)
    try:
        args = prepare_call_args(jar_cmd)
        logger.info(f"running {args}")
        if print_output:
            stdout_stream = None
        else:
            stdout_stream = subprocess.DEVNULL

        run_result = \
            subprocess.run(args, shell=False, universal_newlines=True, stderr=subprocess.PIPE, stdout=stdout_stream)

        return_code = run_result.returncode
        if return_code:

            default_msg = f"Execution of command \"{' '.join(args)}\" terminated with exitcode {return_code}."
            err_msg_header = custom_error_message if custom_error_message is not None else default_msg
            if print_err:
                logger.error(err_msg_header)
            else:
                logger.info(err_msg_header)

            # We log all lines in stderr, as they contain useful information we do not want the
            # Python loggers to miss
            # specifically, the errors go only to the log if we disabled printing of errors or exit code override is on
            log_level = logging.INFO if (override_exit_code or not print_err) else logging.CRITICAL
            stderr_lines = run_result.stderr.splitlines()
            for line in stderr_lines:
                logger.log(log_level, line)

            if not override_exit_code:  # else, we return 0
                return return_code

        return 0
    except Exception as e:
        logger.error(e)
        return 1


def print_failed_to_run(cmd: str) -> None:
    print()
    print(f"Failed to run {cmd}")
    if is_windows() and cmd.find('solc') != -1 and cmd.find('exe') == -1:
        print("did you forget the .exe extension for solcXX.exe??")
    print()


# TODO move to CompilerCollectorFactory.py
def run_compiler_cmd(compiler_cmd: str, output_file_name: str, config_path: Path, wd: Path,
                     compiler_input: Optional[bytes] = None) -> None:
    """
    @param compiler_cmd The command that runs the smart contract compiler, i.e. solc/vyper executable
    @param output_file_name the name of the .stdout and .stderr file
    @param config_path the directory of the generated files
    @param wd the working directory for the compiler
    @param compiler_input input to the compiler subprocess
    """
    process_logger.debug(f"Running cmd {compiler_cmd}")
    build_start = time.perf_counter()

    stdout_name = config_path / f'{output_file_name}.stdout'
    stderr_name = config_path / f'{output_file_name}.stderr'
    process_logger.debug(f"stdout, stderr = {stdout_name}, {stderr_name}")

    with stdout_name.open('w+') as stdout:
        with stderr_name.open('w+') as stderr:
            try:
                args = prepare_call_args(compiler_cmd)
                exitcode = subprocess.run(args, stdout=stdout, stderr=stderr, input=compiler_input, cwd=wd).returncode
                if exitcode:
                    msg = f"Failed to run {compiler_cmd}, exit code {exitcode}"
                    with open(stderr_name, 'r') as stderr_read:
                        for line in stderr_read:
                            print(line)
                    raise Exception(msg)
                else:
                    process_logger.debug(f"Exitcode {exitcode}")
            except Exception as e:
                print(f"Error: {e}")
                print_failed_to_run(compiler_cmd)
                raise

    build_end = time.perf_counter()
    time_run = round(build_end - build_start, 4)
    process_logger.debug(f"Solc run {compiler_cmd} time: {time_run}")


@contextmanager
def change_working_directory(path: Union[str, os.PathLike]) -> Generator[None, None, None]:
    """
    Changes working directory and returns to previous on exit.
    Note: the directory will return to the previous even if an exception is thrown, for example: if path does not exist
    """
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def file_is_not_empty(file_path: Path) -> bool:
    return file_path.exists() and file_path.stat().st_size != 0


class Singleton(type):
    """
    This is intended to be used as a metaclass to enforce only a single instance of a class can be created
    """
    __instancesinstances: Dict[Any, Any] = {}  # Mapping from a class type to its instance

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """
        returns the instance of a class if exists, otherwise constructs it
        """
        if cls not in cls.__instancesinstances:
            cls.__instancesinstances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instancesinstances[cls]


class AbstractAndSingleton(Singleton, ABCMeta):
    pass


def match_path_to_mapping_key(path: Path, m: Dict[str, str]) -> Optional[str]:
    """
    Matches the path to the best match in the dictionary's keys.
    For example, given an absolute path `/Users/JohnDoe/Path/ToSolc/a.sol`, if the map contains
    `b/a.sol` and `ToSolc/a.sol`, it will match on `ToSolc/a.sol`.
    It is assumed the map does not contain any ambiguities, e.g. both `a.sol` and `ToSolc/a.sol`.
    @param path: the path to match against
    @param m: the map whose keys we're searching
    @return: the value from the map that best matches the path, None if not found.
    """
    resolved_abs_path = path.resolve()
    for k, v in m.items():
        if Path(k).resolve() == resolved_abs_path:
            return v
    return None


def find_in(dir_path: Path, file_to_find: Path) -> Optional[Path]:
    """
    Given a directory dir_path and a file we wish to find within that directory,
    we iterate by trimming the prefix of file_to_find.
    Use case: since .certora_sources is a common root of paths we copy, we wish to resolve
    the original files inside .certora_sources.
    Note that file_to_find should not have directory traversals.
    Also, the result must not be an absolute path.

    @param dir_path: A path to root the new file in
    @param file_to_find: The file to re-root
    @return The path of file_to_find rooted in dir_path, and None if it is not there
    """

    num_parts = len(file_to_find.parts)
    if file_to_find.is_absolute():
        start = 1  # we must trim the `/` so that we do not return absolute paths
    else:
        start = 0

    for i in range(start, num_parts):
        candidate_path = Path(*file_to_find.parts[i:])
        if (dir_path / candidate_path).is_file():
            return candidate_path

    return None


def find_filename_in(dir_path: Path, filename_to_find: str) -> Optional[str]:
    res = find_in(dir_path, Path(filename_to_find))
    if res is not None:
        return str(res)
    else:
        return None


def get_trivial_contract_name(contract: str) -> str:
    """
    Gets a path to a .sol file and returns its trivial contract name. The trivial contract name is the basename of the
    path of the file, without file type suffix.
    For example: for 'file/Test/opyn/vault.sol', the trivial contract name is 'vault'.
    @param contract: A path to a .sol file
    @return: The trivial contract name of a file
    """
    return abs_posix_path_obj(contract).stem

def version_triplet_regex(prefix: str = "", suffix: str = "") -> str:
    """
    @return: the regex pattern for a version triplet (xx.yy.zz)
    """
    return fr'^{prefix}(\d+)\.(\d+)\.(\d+){suffix}'


class TestValue(NoValEnum):
    """
    valid values for the --test flag. The values in command line are in lower case (e.g. --test local_jar). The value
    determines the chekpoint where the execution will halt. The exception TestResultsReady will be thrown. The value
    will also determine what object will be attached to the exception for inspection by the caller
    """
    LOCAL_JAR = auto()
    CHECK_ARGS = auto()
    AFTER_BUILD = auto()
    CHECK_SOLC_OPTIONS = auto()
    CHECK_AUTH_DATA = auto()


class FeValue(NoValEnum):
    PRODUCTION = auto()
    LATEST = auto()


class TestResultsReady(Exception):
    def __init__(self, data: Any):
        super().__init__()
        self.data = data
