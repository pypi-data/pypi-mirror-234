import argparse
import hashlib
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))

from EVMVerifier.certoraContextClass import CertoraContext
from Shared import certoraUtils as Util
from EVMVerifier.certoraConfigIO import read_from_conf_file, current_conf_to_file
import EVMVerifier.certoraContextValidator as Cv
import EVMVerifier.certoraContextAttribute as Attr
import EVMVerifier.certoraValidateFuncs as Vf


context_logger = logging.getLogger("context")

CLI_DOCUMENTATION_URL = 'https://docs.certora.com/en/latest/docs/prover/cli/options.html'


def escape_string(string: str) -> str:
    """
    enclose string with double quotes if the string contains char that is not alphanum
    """
    pattern = re.compile('^[0-9a-zA-Z]+$')
    if pattern.match(string):
        return string
    else:
        return f"\"{string}\""


def collect_jar_args(context: CertoraContext) -> List[str]:
    """
    construct the jar flags. For each attribute with non-empty value in the context, we check if a jar flag was
    declared for that attribute. The jar command is a list of strings the first string is the flag (jar_flag). If
    the flag comes with a value we construct the value as the second string, based on the type of the attribute
    (Boolean, String or List of Strings)
    """
    return_list = []
    for arg in Attr.ContextAttribute:
        conf_key = arg.get_conf_key()
        attr = getattr(context, conf_key, None)
        if not attr or arg.value.jar_flag is None:
            continue
        return_list.append(arg.value.jar_flag)
        if not arg.value.jar_no_value:
            if isinstance(attr, list):
                return_list.append(','.join(attr))
            elif isinstance(attr, bool):
                return_list.append('true')
            elif isinstance(attr, str):
                return_list.append(escape_string(attr))
            else:
                raise RuntimeError(f"{arg.name}: {arg.value.arg_type} - unknown arg type")

    prover_args_values = getattr(context, Attr.ContextAttribute.PROVER_ARGS.get_conf_key(), None)
    if prover_args_values:
        for value in prover_args_values:
            return_list.extend(value.split())
    return return_list


def get_local_run_cmd(context: CertoraContext) -> str:
    """
    Assembles a jar command for local run
    @param context: A namespace including all command line input arguments
    @return: A command for running the prover locally
    """
    run_args = []
    if context.mode == Util.Mode.TAC or context.mode == Util.Mode.SOLANA:
        run_args.append(context.files[0])
    if context.cache is not None:
        run_args.extend(['-cache', context.cache])

    jar_args = collect_jar_args(context)
    run_args.extend(jar_args)

    run_args.extend(['-buildDirectory', str(Util.get_build_dir())])
    if context.jar is not None:
        jar_path = context.jar
    else:
        certora_root_dir = Util.get_certora_root_directory().as_posix()
        jar_path = f"{certora_root_dir}/emv.jar"

    """
    This flag prevents the focus from being stolen from the terminal when running the java process.
    Stealing the focus makes it seem like the program is not responsive to Ctrl+C.
    Nothing wrong happens if we include this flag more than once, so we always add it.
    """
    java_args = ""

    if context.java_args is not None:
        java_args = f"{context.java_args} {java_args}"

    cmd = " ".join(["java", java_args, "-jar", jar_path] + run_args)
    if context.test == str(Util.TestValue.LOCAL_JAR):
        raise Util.TestResultsReady(cmd)
    return cmd


class CertoraArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


def __get_argparser() -> argparse.ArgumentParser:

    def formatter(prog: Any) -> argparse.HelpFormatter:
        return argparse.HelpFormatter(prog, max_help_position=100, width=200)

    parser = CertoraArgumentParser(prog="certora-cli arguments and options", allow_abbrev=False,
                                   formatter_class=formatter,
                                   epilog="  -*-*-*   "
                                          "You can find detailed documentation of the supported options in "
                                          f"{CLI_DOCUMENTATION_URL}   -*-*-*")

    arg_groups = {i.name: parser.add_argument_group(i.value) for i in Attr.ArgGroups}

    args = list(Attr.ContextAttribute)

    for arg in args:
        flag = arg.get_flag()
        if arg.value.group is None:
            parser.add_argument(flag, help=arg.value.help_msg, **arg.value.argparse_args)
        else:
            arg_groups[arg.value.group.name].add_argument(flag, help=arg.value.help_msg, **arg.value.argparse_args)
    return parser


def get_args(args_list: Optional[List[str]] = None) -> Tuple[CertoraContext, Dict[str, Any]]:
    if args_list is None:
        args_list = sys.argv

    """
    Compiles an argparse.Namespace from the given list of command line arguments.
    Additionally returns the prettified dictionary version of the input arguments as generated by current_conf_to_file
    and printed to the .conf file in .lastConfs.

    Why do we handle --version before argparse?
    Because on some platforms, mainly CI tests, we cannot fetch the installed distribution package version of
    certora-cli. We want to calculate the version lazily, only when --version was invoked.
    We do it pre-argparse, because we do not care bout the input validity of anything else if we have a --version flag
    """
    handle_version_flag(args_list)

    pre_arg_fetching_checks(args_list)
    parser = __get_argparser()

    # if there is a --help flag, we want to ignore all parsing errors, even those before it:
    if any(string in [arg.strip() for arg in args_list] for string in ['--help', '-h']):
        parser.print_help()
        exit(0)

    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    args = parser.parse_args(args_list)
    context = CertoraContext(**vars(args))

    __remove_parsing_whitespace(args_list)
    format_input(context)

    Cv.check_mode_of_operation(context)  # Here context.mode is set

    if context.mode == Util.Mode.CONF:
        read_from_conf_file(context)

    validator = Cv.CertoraContextValidator(context)
    validator.validate()
    current_build_directory = Util.get_build_dir()
    if context.build_dir is not None and current_build_directory != context.build_dir:
        Util.reset_certora_internal_dir(context.build_dir)
        os.rename(current_build_directory, context.build_dir)

    # Store current options (including the ones read from .conf file)
    conf_options = current_conf_to_file(context)

    Cv.check_args_post_argparse(context)
    setup_cache(context)  # Here context.cache, context.user_defined_cache are set

    # Setup defaults (defaults are not recorded in conf file)
    if context.expected_file is None:
        context.expected_file = "expected.json"
    if context.run_source is None:
        context.run_source = Vf.RunSources.COMMAND.name.upper()

    context_logger.debug("parsed args successfully.")
    context_logger.debug(f"args= {context}")
    # the right way to stop at this point and check the args is using context.test and not context.check_args
    # since run_certora() that calls this function can run in a "library" mode throwing exception is the right
    # behaviour and not existing the script. --check_args will be removed once the old API will not be supported

    if context.check_args:
        sys.exit(0)
    if context.test == str(Util.TestValue.CHECK_ARGS):
        raise Util.TestResultsReady(context)
    return context, conf_options


def print_version() -> None:
    installed, package_name, version = Util.get_package_and_version()
    if installed:
        print(f"{package_name} {version}")
    else:
        print("local script version")


def handle_version_flag(args_list: List[str]) -> None:
    for arg in args_list:
        if arg == "--version":
            print_version()  # exits the program
            exit(0)


def __remove_parsing_whitespace(arg_list: List[str]) -> None:
    """
    Removes all whitespaces added to args by __alter_args_before_argparse():
    1. A leading space before a dash (if added)
    2. space between commas
    :param arg_list: A list of options as strings.
    """
    for idx, arg in enumerate(arg_list):
        arg_list[idx] = arg.strip().replace(', ', ',')


def __alter_args_before_argparse(args_list: List[str]) -> None:
    """
    some args value accept flags as value (e.g. java_args). The problem is that argparse treats this values
    as CLI arguments. The fix is to add a space before the dash artificially.

    NOTE: remove_parsing_whitespace() removes the added space
    :param args_list: A list of CLI options as strings
    """
    for idx, arg in enumerate(args_list):
        if isinstance(arg, str):
            pattern = r"^[\"\']*-[^-]"  # a string that starts 0 or more qoutes followed by a single hyphen
            if re.match(pattern, arg):
                arg = re.sub('-', " -", arg, count=1)
                args_list[idx] = arg


def pre_arg_fetching_checks(args_list: List[str]) -> None:
    """
    This function runs checks on the raw arguments before we attempt to read them with argparse.
    We also replace certain argument values so the argparser will accept them.
    NOTE: use remove_parsing_whitespace() on argparse.ArgumentParser.parse_args() output!
    :param args_list: A list of CL arguments
    :raises CertoraUserInputError if there are errors (see individual checks for more details):
        - There are wrong quotation marks “ in use
    """
    Cv.check_no_pretty_quotes(args_list)
    __alter_args_before_argparse(args_list)


def format_input(context: CertoraContext) -> None:
    """
    Formats the input as it was parsed by argParser. This allows for simpler reading and treatment of context
    * Removes whitespace from input
    * Flattens nested lists
    * Removes duplicate values in link
    :param context: Namespace containing all command line arguments, generated by get_args()
    """
    flatten_arg_lists(context)
    __dedup_link(context)


def flatten_arg_lists(context: CertoraContext) -> None:
    """
    Flattens lists of lists arguments in a given namespace.
    For example,
    [[a], [b, c], []] -> [a, b, c]

    This is applicable to all options that can be used multiple times, and each time get multiple arguments.
    For example: --assert and --link
    @param context: Namespace containing all command line arguments, generated by get_args()
    """
    for arg_name in vars(context):
        arg_val = getattr(context, arg_name)
        # We assume all list members are of the same type
        if isinstance(arg_val, list) and len(arg_val) > 0 and isinstance(arg_val[0], list):
            flat_list = Util.flatten_nested_list(arg_val)
            flat_list.sort()
            setattr(context, arg_name, flat_list)


def __dedup_link(context: CertoraContext) -> None:
    try:
        context.link = list(set(context.link))
    except TypeError:
        pass


def setup_cache(context: CertoraContext) -> None:
    """
    Sets automatic caching up, unless it is disabled (only relevant in VERIFY and ASSERT modes).
    The list of contracts, optimistic loops and loop iterations are determining uniquely a cache key.
    If the user has set their own cache key, we will not generate an automatic cache key, but we will also mark it
    as a user defined cache key.

    This function first makes sure to set user_defined_cache to either True or False,
    and then if necessary, sets up the cache key value.
    """

    # we have a user defined cache key if the user provided a cache key
    context.user_defined_cache = context.cache is not None
    if not context.disable_auto_cache_key_gen and not os.environ.get("CERTORA_DISABLE_AUTO_CACHE") is not None:
        if context.mode == Util.Mode.VERIFY or context.mode == Util.Mode.ASSERT or context.mode == Util.Mode.CONF:
            # in local mode we don't want to create a cache key if not such is given
            if (context.cache is None) and (not context.local):
                optimistic_loop = context.optimistic_loop
                loop_iter = context.loop_iter
                files = sorted(context.files)
                context.cache = hashlib.sha256(bytes(str(files), 'utf-8')).hexdigest() + \
                    f"-optimistic{optimistic_loop}-iter{loop_iter}"

                """
                We append the cloud env and the branch name (or None) to the cache key to make it different across
                branches to avoid wrong cloud cache collisions.
                """
                branch = context.prover_version if context.prover_version else ''
                context.cache += f'-{context.server}-{branch}'
                is_installed, package, version = Util.get_package_and_version()
                if is_installed:
                    context.cache += f'-{package}-{version}'
                # sanitize so we don't create nested "directories" in s3
                context.cache = context.cache.replace("/", "-").replace(" ", "-")
                context_logger.debug(f"setting cache key to {context.cache}")


def write_output_conf_to_path(json_content: Dict[str, Any], path: Path) -> None:
    """
    Write the json object to the path
    @param json_content: the json object
    @param path: the location of the output path
    @:return: None
    """
    with path.open("w+") as out_file:
        json.dump(json_content, out_file, indent=4, sort_keys=True)


def handle_flags_in_args(args: List[str]) -> None:
    """
    For argparse flags are strings that start with a dash. Some arguments get flags as value.
    The problem is that argparse will not treat the string as a value but rather as a new flag. There are different ways
    to prevent this. One way that was used in the past in certoraRun was to surround the string value with single
    quotes, double quotes or both. This technique complicates the value syntax and is error prune. A different technique
    is to precede the dash with a white space. That is something the tool can do for the user. In addition, if the user
    did add quotes (single or double) around a value they will be removed. Examples:

        --java_args '-d'
        --java_args "-d"
        --java_args '"-d"'

    Will all be converted to " -d"

    """

    all_flags = list(map(lambda member: member.get_flag(), Attr.ContextAttribute))

    def surrounded(string: str, char: str) -> bool:
        if len(string) < 2:
            return False
        return string[0] == char and string[-1] == char

    for index, arg in enumerate(args):
        if arg in all_flags:
            continue

        while True:
            if arg and (surrounded(arg, '\'') or surrounded(arg, '\"')):
                arg = arg[1:-1]
            else:
                break
        if len(arg) > 0 and arg[0] == '-' and (args[index - 1] == Attr.ContextAttribute.JAVA_ARGS.get_flag()):
            arg = f" {arg}"
        if arg != args[index]:
            args[index] = arg


def is_staging(context: CertoraContext) -> bool:
    if context.server is None:
        return False
    return context.server.upper() == Util.SupportedServers.STAGING.name


def __rename_key(context: CertoraContext, old_key: str, new_key: str) -> None:
    if old_key in vars(context):
        value = getattr(context, old_key)
        setattr(context, new_key, value)
        context.delete_key(old_key)
