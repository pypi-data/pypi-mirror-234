import argparse
import logging
import sys
import re
from functools import lru_cache
from dataclasses import dataclass, field
from enum import unique, auto
from pathlib import Path
from typing import Optional, Dict, Any, Callable, List

from EVMVerifier import certoraValidateFuncs as Vf
from Shared import certoraUtils as Util

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))

# logger for issues regarding context
context_logger = logging.getLogger("context")


def validate_prover_args(value: str) -> str:

    strings = value.split()
    for arg in ContextAttribute:
        if arg.value.jar_flag is None:
            continue
        for string in strings:

            if string == arg.value.jar_flag:
                # globalTimeout will get a special treatment, because the actual arg is the wrong one
                if arg.value.jar_flag == ContextAttribute.CLOUD_GLOBAL_TIMEOUT.value.jar_flag:
                    actual_arg = ContextAttribute.GLOBAL_TIMEOUT
                else:
                    actual_arg = arg
                raise Util.CertoraUserInputError(f"Use CLI flag '{actual_arg.get_flag()}' "
                                                 f"instead of 'prover_args' with {string} as value")
    return value


def validate_solc_args(value: str) -> str:
    '''
    making sure no supported flags are set inside the --solc_arg flag
    '''
    strings = value.split()
    for string in strings:
        if string in ['--path', '--allow-paths', '--allow-path', '--solc_allow_path']:
            raise Util.CertoraUserInputError(f"the flag {string} should be set using 'solc_allow_path'")
        if string in ['--optimize', '--solc_optimize', '--optimize-runs']:
            raise Util.CertoraUserInputError(f"the flag {string} should be set using 'solc_optimize'")
        if string in ['--via_ir', '--solc_via_ir', '--via-ir']:
            raise Util.CertoraUserInputError(f"the flag {string} should be set using 'solc_via_ir'")
        if string in ['--evm_version', '--evm-version', '--solc_evm_version']:
            raise Util.CertoraUserInputError(f"the flag {string} should be set using 'solc_via_ir'")
    return value


def parse_struct_link(link: str) -> str:
    search_res = re.search(r'^\w+:([^:=]+)=\w+$', link)
    # We do not require firm form of slot number so we can give more informative warnings
    if search_res is None:
        raise Util.CertoraUserInputError(f"Struct link argument {link} must be of the form contractA:<field>=contractB")
    if search_res[1].isidentifier():
        return link
    try:
        parsed_int = int(search_res[1], 0)  # an integer or a hexadecimal
        if parsed_int < 0:
            raise Util.CertoraUserInputError(f"struct link slot number negative at {link}")
    except ValueError:
        raise Util.CertoraUserInputError(f"Struct link argument {link} must be of the form contractA:number=contractB"
                                         f" or contractA:fieldName=contractB")
    return link

APPEND = 'append'
STORE_TRUE = 'store_true'
STORE_FALSE = 'store_false'
VERSION = 'version'
SINGLE_OR_NONE_OCCURRENCES = '?'
MULTIPLE_OCCURRENCES = '*'
ONE_OR_MORE_OCCURRENCES = '+'


class AttrArgType(Util.NoValEnum):
    STRING = auto()
    BOOLEAN = auto()
    LIST_OF_STRINGS = auto()
    ANY = auto()


class ArgGroups(Util.NoValEnum):
    # The order of the groups is the order we want to show the groups in argParse's help
    MODE = "Mode of operation. Please choose one, unless using a .conf or .tac file"
    USEFUL = "Most frequently used options"
    RUN = "Options affecting the type of verification run"
    SOLIDITY = "Options that control the Solidity compiler"
    LOOP = "Options regarding source code loops"
    HASHING = "Options regarding handling of unbounded hashing"
    RUN_TIME = "Options that help reduce running time"
    LINKAGE = "Options to set addresses and link contracts"
    CREATION = "Options to model contract creation"
    INFO = "Debugging options"
    JAVA = "Arguments passed to the .jar file"
    PARTIAL = "These arguments run only specific parts of the tool, or skip parts"
    CLOUD = "Fine cloud control arguments"
    MISC_HIDDEN = "Miscellaneous hidden arguments"
    ENV = ""


def default_validation(x: Any) -> Any:
    return x

@dataclass
class CertoraArgument:
    flag: Optional[str] = None  # override the 'default': option name
    group: Optional[ArgGroups] = None  # name of the arg parse (see ArgGroups above)
    attr_validation_func: Callable = default_validation
    deprecation_msg: Optional[str] = None
    jar_flag: Optional[str] = None  # the flag that is sent to the jar (if attr is sent to the jar)
    jar_no_value: Optional[bool] = False  # if true, flag is sent with no value
    help_msg: str = argparse.SUPPRESS

    # args for argparse's add_attribute passed as is
    argparse_args: Dict[str, Any] = field(default_factory=dict)
    arg_type: AttrArgType = AttrArgType.STRING

    def get_dest(self) -> Optional[str]:
        return self.argparse_args.get('dest')


class UniqueStore(argparse.Action):
    """
    This class makes the argparser throw an error for a given flag if it was inserted more than once
    """

    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: Any,  # type: ignore
                 option_string: str) -> None:
        if getattr(namespace, self.dest, self.default) is not self.default:
            parser.error(f"{option_string} appears several times.")
        setattr(namespace, self.dest, values)


@unique
class ContextAttribute(Util.NoValEnum):
    """
    This enum class must be unique. If 2 args have the same value we add the 'flag' attribute to make sure the hash
    value is not going to be the same

    The order of the attributes is the order we want to show the attributes in argParse's help

    """
    FILES = CertoraArgument(
        attr_validation_func=Vf.validate_input_file,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="contract files for analysis, a conf file or SOLANA_FILE.so",
        flag='files',
        argparse_args={
            'nargs': MULTIPLE_OCCURRENCES
        }
    )

    VERIFY = CertoraArgument(
        group=ArgGroups.MODE,
        attr_validation_func=Vf.validate_verify_attr,
        arg_type=AttrArgType.STRING,
        help_msg="Matches a specification file to a contract",
        argparse_args={
            'action': UniqueStore
        }
    )

    # something is definitely under-tested here, because I changed this to take
    # a string instead of list of strings and everything just passed!
    ASSERT_CONTRACTS = CertoraArgument(
        group=ArgGroups.MODE,
        attr_validation_func=Vf.validate_assert_contracts,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND,
        }
    )

    BYTECODE_JSONS = CertoraArgument(
        group=ArgGroups.MODE,
        attr_validation_func=Vf.validate_json_file,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        jar_flag='-bytecode',
        help_msg="List of EVM bytecode json descriptors",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    BYTECODE_SPEC = CertoraArgument(
        group=ArgGroups.MODE,
        attr_validation_func=Vf.validate_spec_file,
        jar_flag='-spec',
        help_msg="Spec to use for the provided bytecodes",
        argparse_args={
            'action': UniqueStore
        }
    )

    MSG = CertoraArgument(
        group=ArgGroups.USEFUL,
        attr_validation_func=Vf.validate_msg,
        help_msg="Adds a message description to your run",
        argparse_args={
            'action': UniqueStore
        }
    )

    #  RULE option is for both --rule and --rules
    RULE = CertoraArgument(
        group=ArgGroups.USEFUL,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        attr_validation_func=Vf.validate_rule,
        jar_flag='-rule',
        help_msg="Filters the list of rules/invariants to verify",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    PROTOCOL_NAME = CertoraArgument(
        group=ArgGroups.USEFUL,
        help_msg="Adds the protocol's name for easy filtering in the dashboard",
        argparse_args={
            'action': UniqueStore
        }
    )

    PROTOCOL_AUTHOR = CertoraArgument(
        group=ArgGroups.USEFUL,
        help_msg="Adds the protocol's author for easy filtering in the dashboard",
        argparse_args={
            'action': UniqueStore
        }
    )

    MULTI_ASSERT_CHECK = CertoraArgument(
        group=ArgGroups.RUN,
        arg_type=AttrArgType.BOOLEAN,
        jar_no_value=True,
        jar_flag='-multiAssertCheck',
        help_msg="Checks each assertion statement that occurs in a rule, separately",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    SAVE_VERIFIER_RESULTS = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        arg_type=AttrArgType.BOOLEAN,
        jar_no_value=True,
        jar_flag='-saveVerifierResults',
        argparse_args={
            'action': STORE_TRUE
        }
    )

    INCLUDE_EMPTY_FALLBACK = CertoraArgument(
        group=ArgGroups.RUN,
        arg_type=AttrArgType.BOOLEAN,
        jar_flag='-includeEmptyFallback',
        argparse_args={
            'action': STORE_TRUE
        }
    )

    RULE_SANITY = CertoraArgument(
        group=ArgGroups.RUN,
        attr_validation_func=Vf.validate_sanity_value,
        help_msg="Selects the type of sanity check that will be performed during execution",
        jar_flag='-ruleSanityChecks',
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'action': UniqueStore,
            'default': None,  # 'default': when no --rule_sanity given
            'const': Vf.RuleSanityValue.BASIC.name.lower()  # 'default': when empty --rule_sanity is given
        }
    )

    MULTI_EXAMPLE = CertoraArgument(
        group=ArgGroups.RUN,
        attr_validation_func=Vf.validate_multi_example_value,
        help_msg="Sets the required multi example mode",
        jar_flag='-multipleCEX',
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'action': UniqueStore,
            'default': None,  # 'default': when no --multi_example given
            'const': Vf.MultiExampleValue.BASIC.name.lower()
        }
    )

    SHORT_OUTPUT = CertoraArgument(
        group=ArgGroups.RUN,
        arg_type=AttrArgType.BOOLEAN,
        jar_flag='-ciMode',
        help_msg="Reduces verbosity",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    NO_CALLTRACE_STORAGE_INFORMATION = CertoraArgument(
        group=ArgGroups.RUN,
        arg_type=AttrArgType.BOOLEAN,
        jar_flag='-noCalltraceStorageInformation',
        argparse_args={
            'action': STORE_TRUE
        }
    )

    CALLTRACE_REMOVE_EMPTY_LABELS = CertoraArgument(
        group=ArgGroups.RUN,
        arg_type=AttrArgType.BOOLEAN,
        jar_flag='-calltraceRemoveEmptyLabels',
        argparse_args={
            'action': STORE_TRUE
        }
    )

    TYPECHECK_ONLY = CertoraArgument(
        group=ArgGroups.RUN,
        arg_type=AttrArgType.BOOLEAN,
        argparse_args={
            'action': STORE_TRUE
        }
    )

    SEND_ONLY = CertoraArgument(
        group=ArgGroups.RUN,
        arg_type=AttrArgType.BOOLEAN,
        deprecation_msg="'send_only' is deprecated and is now the default. In CI, use 'wait_for_results false' instead",
        help_msg="Makes the request to the prover but does not wait for verifications results",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    WAIT_FOR_RESULTS = CertoraArgument(
        group=ArgGroups.RUN,
        attr_validation_func=Vf.validate_wait_for_results,
        help_msg="Wait for verification results before terminating the run",
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'action': UniqueStore,
            'default': None,  # 'default': when --wait_for_results was not used
            'const': str(Vf.WaitForResultOptions.ALL)  # when --wait_for_results was used without an argument
        }
    )

    SOLC = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=Vf.validate_exec_file,
        help_msg="Path to the Solidity compiler executable file",
        argparse_args={
            'action': UniqueStore
        }
    )

    SOLC_ARGS = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=validate_solc_args,
        help_msg="Sends flags directly to the Solidity compiler",
        argparse_args={
            'action': UniqueStore,
        }
    )

    SOLC_VIA_IR = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        arg_type=AttrArgType.BOOLEAN,
        help_msg="Instructs the solidity compiler to use intermediate representation instead of EVM opcode",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    SOLC_EVM_VERSION = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        help_msg="Intructs the Solidity compiler to use a specific EVM version",
        argparse_args={
            'action': UniqueStore
        }
    )

    SOLC_MAP = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=Vf.validate_solc_map,
        arg_type=AttrArgType.ANY,
        help_msg="Matches each Solidity file with a Solidity compiler executable",
        argparse_args={
            'action': UniqueStore,
            'type': lambda value: Vf.parse_dict('solc_map', value)
        }
    )

    SOLC_ALLOW_PATH = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=Vf.validate_dir,
        help_msg="Sets the base path for loading Solidity files",
        argparse_args={
            'action': UniqueStore
        }
    )

    SOLC_OPTIMIZE = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=Vf.validate_non_negative_integer_or_minus_1,
        help_msg="Tells the Solidity compiler to optimize the gas costs of the contract for a given number of runs, "
                 "if number of runs is not defined the Solidity compiler default is used",
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'action': UniqueStore,
            'const': '-1'
        }
    )

    SOLC_OPTIMIZE_MAP = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=Vf.validate_solc_optimize_map,
        arg_type=AttrArgType.ANY,
        help_msg="Matches each Solidity source file with a number of runs to optimize for",
        argparse_args={
            'action': UniqueStore,
            'type': lambda value: Vf.parse_dict('solc_optimize_map', value)
        }
    )

    PACKAGES_PATH = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=Vf.validate_dir,
        help_msg="Path to a directory including the Solidity packages",
        argparse_args={
            'action': UniqueStore
        }
    )

    PACKAGES = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=Vf.validate_packages,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="Maps packages to their location in the file system",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    OPTIMISTIC_LOOP = CertoraArgument(
        group=ArgGroups.LOOP,
        arg_type=AttrArgType.BOOLEAN,
        jar_flag='-assumeUnwindCond',
        jar_no_value=True,
        help_msg="After unrolling loops, assume the loop halt conditions hold",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    LOOP_ITER = CertoraArgument(
        group=ArgGroups.LOOP,
        attr_validation_func=Vf.validate_non_negative_integer,
        jar_flag='-b',
        help_msg="Maximum number of loop iterations we verify for",
        argparse_args={
            'action': UniqueStore
        }
    )

    OPTIMISTIC_HASHING = CertoraArgument(
        group=ArgGroups.HASHING,
        arg_type=AttrArgType.BOOLEAN,
        help_msg="Bounds the length of data (with potentially unbounded length) to the value given in "
                 "--hashing_length_bound",
        jar_flag='-optimisticUnboundedHashing',
        argparse_args={
            'action': STORE_TRUE
        }
    )

    HASHING_LENGTH_BOUND = CertoraArgument(
        group=ArgGroups.HASHING,
        attr_validation_func=Vf.validate_non_negative_integer,
        jar_flag='-hashingLengthBound',
        help_msg="Maximum length of otherwise unbounded data chunks that are being hashed",
        argparse_args={
            'action': UniqueStore
        }
    )

    METHOD = CertoraArgument(
        group=ArgGroups.RUN_TIME,
        jar_flag='-method',
        help_msg="Filters methods to be verified by their signature",
        argparse_args={
            'action': UniqueStore
        }
    )

    CACHE = CertoraArgument(
        group=ArgGroups.RUN_TIME,
        argparse_args={
            'action': UniqueStore
        }
    )

    SMT_TIMEOUT = CertoraArgument(
        group=ArgGroups.RUN_TIME,
        attr_validation_func=Vf.validate_positive_integer,
        jar_flag='-t',
        argparse_args={
            'action': UniqueStore
        }
    )

    LINK = CertoraArgument(
        group=ArgGroups.LINKAGE,
        attr_validation_func=Vf.validate_link_attr,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="Links a slot in a contract with another contract",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    ADDRESS = CertoraArgument(
        group=ArgGroups.LINKAGE,
        attr_validation_func=Vf.validate_address,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="Sets the address of a contract to a given address",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    STRUCT_LINK = CertoraArgument(
        group=ArgGroups.LINKAGE,
        attr_validation_func=Vf.validate_struct_link,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="Links a slot in a struct with another contract",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND,
        }
    )

    PROTOTYPE = CertoraArgument(
        group=ArgGroups.CREATION,
        attr_validation_func=Vf.validate_prototype_attr,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="Prototype defines that for a constructor bytecode prefixed by the given string, we generate an "
                 "instance of the given contract",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    DYNAMIC_BOUND = CertoraArgument(
        group=ArgGroups.CREATION,
        attr_validation_func=Vf.validate_non_negative_integer,
        jar_flag='-dynamicCreationBound',
        help_msg="Maximum times a contract will be cloned",
        argparse_args={
            'action': UniqueStore
        }
    )

    DYNAMIC_DISPATCH = CertoraArgument(
        group=ArgGroups.CREATION,
        arg_type=AttrArgType.BOOLEAN,
        jar_flag='-dispatchOnCreated',
        help_msg="Automatically apply the DISPATCHER summary on newly created instances",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    DEBUG = CertoraArgument(
        group=ArgGroups.INFO,
        arg_type=AttrArgType.BOOLEAN,
        argparse_args={
            'action': STORE_TRUE
        }
    )

    SHOW_DEBUG_TOPICS = CertoraArgument(
        group=ArgGroups.INFO,
        arg_type=AttrArgType.BOOLEAN,
        flag='--show_debug_topics',  # added to prevent dup with DEBUG
        argparse_args={
            'action': STORE_TRUE
        }
    )

    DEBUG_TOPICS = CertoraArgument(
        group=ArgGroups.INFO,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    VERSION = CertoraArgument(
        group=ArgGroups.INFO,
        arg_type=AttrArgType.BOOLEAN,
        help_msg="Shows the tool version",
        argparse_args={
            'action': VERSION,
            'version': 'This message should never be reached'
        }
    )

    JAR = CertoraArgument(
        group=ArgGroups.JAVA,
        attr_validation_func=Vf.validate_jar,
        argparse_args={
            'action': UniqueStore
        }
    )

    JAVA_ARGS = CertoraArgument(
        group=ArgGroups.JAVA,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        argparse_args={
            'action': APPEND,
        }
    )

    CHECK_ARGS = CertoraArgument(
        group=ArgGroups.PARTIAL,
        arg_type=AttrArgType.BOOLEAN,
        flag='--check_args',  # added to prevent dup with DISABLE_LOCAL_TYPECHECKING
        argparse_args={
            'action': STORE_TRUE
        }
    )

    BUILD_ONLY = CertoraArgument(
        group=ArgGroups.PARTIAL,
        arg_type=AttrArgType.BOOLEAN,
        flag='--build_only',  # added to prevent dup with CHECK_ARGS
        argparse_args={
            'action': STORE_TRUE
        }
    )

    BUILD_DIR = CertoraArgument(
        group=ArgGroups.PARTIAL,
        attr_validation_func=Vf.validate_build_dir,
        argparse_args={
            'action': UniqueStore
        }
    )

    DISABLE_LOCAL_TYPECHECKING = CertoraArgument(
        group=ArgGroups.PARTIAL,
        arg_type=AttrArgType.BOOLEAN,
        argparse_args={
            'action': STORE_TRUE
        }
    )

    NO_COMPARE = CertoraArgument(
        group=ArgGroups.PARTIAL,
        arg_type=AttrArgType.BOOLEAN,
        flag='--no_compare',  # added to prevent dup with CHECK_ARGS
        argparse_args={
            'action': STORE_TRUE
        }
    )

    EXPECTED_FILE = CertoraArgument(
        group=ArgGroups.PARTIAL,
        attr_validation_func=Vf.validate_optional_readable_file,
        argparse_args={
            'action': UniqueStore
        }
    )

    QUEUE_WAIT_MINUTES = CertoraArgument(
        group=ArgGroups.CLOUD,
        attr_validation_func=Vf.validate_non_negative_integer,
        flag='--queue_wait_minutes',  # added to prevent dup with MAX_POLL_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    MAX_POLL_MINUTES = CertoraArgument(
        group=ArgGroups.CLOUD,
        attr_validation_func=Vf.validate_non_negative_integer,
        flag='--max_poll_minutes',  # added to prevent dup with QUEUE_WAIT_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    LOG_QUERY_FREQUENCY_SECONDS = CertoraArgument(
        group=ArgGroups.CLOUD,
        attr_validation_func=Vf.validate_non_negative_integer,
        flag='--log_query_frequency_seconds',  # added to prevent dup with QUEUE_WAIT_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    MAX_ATTEMPTS_TO_FETCH_OUTPUT = CertoraArgument(
        group=ArgGroups.CLOUD,
        attr_validation_func=Vf.validate_non_negative_integer,
        flag='--max_attempts_to_fetch_output',  # added to prevent dup with QUEUE_WAIT_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    DELAY_FETCH_OUTPUT_SECONDS = CertoraArgument(
        group=ArgGroups.CLOUD,
        attr_validation_func=Vf.validate_non_negative_integer,
        flag='--delay_fetch_output_seconds',  # added to prevent dup with QUEUE_WAIT_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    PROCESS = CertoraArgument(
        group=ArgGroups.CLOUD,
        argparse_args={
            'action': UniqueStore,
            'default': 'emv'
        }
    )

    """
    The content of prover_args is added as is to the jar command without any flag. If jar_flag was set to None, this
    attribute would have been skipped altogether. setting jar_flag to empty string ensures that the value will be added
    to the jar as is
    """
    PROVER_ARGS = CertoraArgument(

        group=ArgGroups.MISC_HIDDEN,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        attr_validation_func=validate_prover_args,
        help_msg="Sends flags directly to the prover",
        argparse_args={
            'action': APPEND
        }
    )

    COMMIT_SHA1 = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_git_hash,
        argparse_args={
            'action': UniqueStore
        }
    )

    DISABLE_AUTO_CACHE_KEY_GEN = CertoraArgument(
        flag='--disable_auto_cache_key_gen',  # added to prevent dup with SKIP_PAYABLE_ENVFREE_CHECK
        group=ArgGroups.MISC_HIDDEN,
        arg_type=AttrArgType.BOOLEAN,
        argparse_args={
            'action': STORE_TRUE
        }
    )

    DISABLE_PER_RULE_CACHE = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_false,
        jar_flag='-usePerRuleCache',
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'action': UniqueStore,
            'default': None,
            'const': 'false'
        }
    )

    UNUSED_SUMMARY_HARD_FAIL = CertoraArgument(
        attr_validation_func=Vf.validate_on_off,
        group=ArgGroups.MISC_HIDDEN,
        jar_flag='-unusedSummaryHardFail',
        argparse_args={
            'action': UniqueStore
        }
    )

    MAX_GRAPH_DEPTH = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_non_negative_integer,
        jar_flag='-graphDrawLimit',
        argparse_args={
            'action': UniqueStore
        }
    )

    TOOL_OUTPUT = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_tool_output_path,
        jar_flag='-json',
        argparse_args={
            'action': UniqueStore,
        }
    )

    CLOUD_GLOBAL_TIMEOUT = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_disallow_all_values,
        jar_flag='-globalTimeout',
        argparse_args={
            'action': UniqueStore
        }
    )

    GLOBAL_TIMEOUT = CertoraArgument(
        group=ArgGroups.RUN_TIME,
        attr_validation_func=Vf.validate_non_negative_integer,
        jar_flag='-userGlobalTimeout',
        argparse_args={
            'action': UniqueStore
        }
    )

    INTERNAL_FUNCS = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_json_file,
        argparse_args={
            'action': UniqueStore
        }
    )

    COINBASE_MODE = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        arg_type=AttrArgType.BOOLEAN,
        jar_flag='-coinbaseFeaturesMode',
        argparse_args={
            'action': STORE_TRUE
        }
    )

    CONF_OUTPUT_FILE = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        argparse_args={
            'action': UniqueStore
        }
    )

    SKIP_PAYABLE_ENVFREE_CHECK = CertoraArgument(
        flag='--skip_payable_envfree_check',  # added to prevent dup with DISABLE_AUTO_CACHE_KEY_GEN
        group=ArgGroups.MISC_HIDDEN,
        jar_flag='-skipPayableEnvfreeCheck',
        arg_type=AttrArgType.BOOLEAN,
        jar_no_value=True,
        argparse_args={
            'action': STORE_TRUE
        }
    )

    RUN_SOURCE = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_run_source,
        argparse_args={
            'action': UniqueStore
        }
    )

    ASSERT_AUTOFINDERS_SUCCESS = CertoraArgument(
        flag="--assert_autofinder_success",
        group=ArgGroups.MISC_HIDDEN,
        arg_type=AttrArgType.BOOLEAN,
        argparse_args={
            'action': STORE_TRUE
        }
    )

    PROVER_VERSION = CertoraArgument(
        group=ArgGroups.ENV,
        help_msg="Instructs the prover to use a build that is not the default",
        argparse_args={
            'action': UniqueStore
        }
    )

    SERVER = CertoraArgument(
        group=ArgGroups.ENV,
        attr_validation_func=Vf.validate_server_value,
        argparse_args={
            'action': UniqueStore
        }
    )
    # resource files are string of the form <label>:<path> the client will add the file to .certora_sources
    # and will change the path from relative/absolute path to
    PROVER_RESOURCE_FILES = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_resource_files,
        jar_flag='-resourceFiles',
        arg_type=AttrArgType.LIST_OF_STRINGS,
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    TEST = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_test_value,
        argparse_args={
            'action': UniqueStore
        }
    )

    COVERAGE_INFO = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_coverage_info,
        jar_flag='-coverageInfo',
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'action': UniqueStore,
            'default': None,  # 'default': when no --coverage_info given
            'const': Vf.CoverageInfoValue.BASIC.name.lower()  # 'default': when empty --coverage_info is given
        }
    )

    FE_VERSION = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_fe_value,
        argparse_args={
            'action': UniqueStore
        }
    )

    MUTATION_TEST_ID = CertoraArgument(
        flag='--mutation_test_id',  # added to prevent dup with CONF_OUTPUT_FILE
        group=ArgGroups.MISC_HIDDEN,
        argparse_args={
            'action': UniqueStore
        }
    )

    def to_csv(self) -> str:
        """

        This function is good for generating attributes reports

        dump attributes of an input option to a row in a csv file where the separator is ampersand & and not a comma (,)
        For example,

        --link & list_of_strings & linkage &   &   & Links a slot in a contract with another contract & regular

        Note that empty strings and None values are recorded as well

        @return: value as a string with & as separator
        """
        row = [
            self.get_flag(),  # name
            self.value.arg_type.name.lower() if self.value.arg_type is not None else ' ',  # type
            self.value.group.name.lower() if self.value.group is not None else ' ',  # group
            self.value.deprecation_msg.lower() if self.value.deprecation_msg is not None else ' ',  # deprecation_msg
            self.value.jar_flag if self.value.jar_flag is not None else ' ',  # jar_flag
            self.value.help_msg if self.value.help_msg != '==SUPPRESS==' else ' ',  # help_msg
        ]
        return ' & '.join(row)

    @staticmethod
    def csv_dump(file_path: Path) -> None:
        with file_path.open('w') as f:
            f.write("sep=&\n")
            f.write("name & type & argparse group & status & deprecation_msg & jar_flag & help_msg\n ")
            for attr in ContextAttribute:
                f.write(f"{attr.to_csv()}\n")

    def validate_value(self, value: str) -> None:
        if self.value.attr_validation_func is not None:
            try:
                self.value.attr_validation_func(value)
            except Util.CertoraUserInputError as e:
                raise Util.CertoraUserInputError(f'{self.get_flag()}: {e}') from None

    def get_flag(self) -> str:
        return self.value.flag if self.value.flag is not None else '--' + str(self)

    def get_conf_key(self) -> str:
        dest = self.value.get_dest()
        return dest if dest is not None else self.get_flag().lstrip('--')

    def __str__(self) -> str:
        return self.name.lower()


@lru_cache(maxsize=1, typed=False)
def all_context_keys() -> List[str]:
    return [attr.get_conf_key() for attr in ContextAttribute if attr is not ContextAttribute.CONF_OUTPUT_FILE]
