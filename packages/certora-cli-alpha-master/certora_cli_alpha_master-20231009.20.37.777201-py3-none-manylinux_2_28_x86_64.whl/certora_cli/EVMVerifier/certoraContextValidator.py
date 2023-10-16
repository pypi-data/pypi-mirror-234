import json
import logging
import os
import re
import sys
import itertools
import time
from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Tuple, Set, Any

import EVMVerifier.certoraContext as Ctx
import EVMVerifier.certoraContextAttribute as Attr
import EVMVerifier.certoraValidateFuncs as Vf
from EVMVerifier.certoraContextClass import CertoraContext
from Shared import certoraUtils as Util

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))

validation_logger = logging.getLogger("validation")

KEY_ENV_VAR = "CERTORAKEY"


class CertoraContextValidator:
    def __init__(self, context: CertoraContext):
        self.context = context

    def validate(self) -> None:

        for arg in Attr.ContextAttribute:
            conf_key = arg.get_conf_key()
            attr = getattr(self.context, conf_key, None)
            if arg.value.deprecation_msg and attr:
                raise Util.CertoraUserInputError(arg.value.deprecation_msg)
            if attr is None or (attr is False and Attr.AttrArgType.BOOLEAN):
                continue
            if arg.value.arg_type == Attr.AttrArgType.STRING:
                self.validate_type_string(arg)
            elif arg.value.arg_type == Attr.AttrArgType.LIST_OF_STRINGS:
                self.validate_type_list_of_strings(arg)
            elif arg.value.arg_type == Attr.AttrArgType.BOOLEAN:
                self.validate_type_boolean(arg)
            elif arg.value.arg_type == Attr.AttrArgType.ANY:
                self.validate_type_any(arg)
            else:
                raise RuntimeError(f"{arg.value.arg_type} - unknown arg type")

    def __get_key_and_value(self, attr: Attr.ContextAttribute) -> Tuple[str, Any]:
        conf_key = attr.get_conf_key()
        value = getattr(self.context, conf_key, None)
        return conf_key, value

    def validate_type_list_of_strings(self, attr: Attr.ContextAttribute) -> None:
        conf_key, value = self.__get_key_and_value(attr)

        if value is None:
            raise RuntimeError(f"calling validate_type_list_of_strings with null value {conf_key}")
        if not isinstance(value, List):
            raise Util.CertoraUserInputError(f"value of {conf_key} {value} is not a list")
        for v in value:
            if not isinstance(v, str):
                raise Util.CertoraUserInputError(f"value in {conf_key} {v} in {value} is not a string")
            attr.validate_value(v)

    def validate_type_any(self, attr: Attr.ContextAttribute) -> None:
        conf_key, value = self.__get_key_and_value(attr)

        if value is None:
            raise RuntimeError(f"calling validate_type_any with null value {conf_key}")
        attr.validate_value(value)

    def validate_type_string(self, attr: Attr.ContextAttribute) -> None:
        conf_key, value = self.__get_key_and_value(attr)

        if value is None:
            raise RuntimeError(f"calling validate_type_string with null value {conf_key}")
        if not isinstance(value, str):
            raise Util.CertoraUserInputError(f"value of {conf_key} {value} is not a string")
        attr.validate_value(value)

    def validate_type_boolean(self, attr: Attr.ContextAttribute) -> None:
        conf_key, value = self.__get_key_and_value(attr)

        if value is None:
            raise RuntimeError(f"{conf_key}: calling validate_type_boolean with None")
        # for backward compatibility the value [] is considered true
        elif type(value) is list and len(value) == 0:
            setattr(self.context, conf_key, True)
        elif value not in [True, False]:
            raise Util.CertoraUserInputError(f"value of {conf_key} {value} is not a boolean (true/false)")


def warn_validate_file_args(files: List[str]) -> Tuple[Set[str], Set[str], Dict[str, str], Dict[str, Set[str]]]:
    """
    Verifies all file inputs are legal. If they are not, throws an exception.
    If there are any redundancies or duplication, warns the user.
    Otherwise, it returns a set of all legal contract names.
    @param files: A list of string of form: [contract.sol[:contract_name] ...]
    @return: (contracts, files, contract_to_file, file_to_contracts)
        contracts - a set of contract names
        files - a set of paths to files containing contracts
        contract_to_file - a mapping from contract name -> file containing it
        file_to_contracts - a mapping from a file path -> name of the contracts within it we verify
    """

    """
    The logic is complex, and better shown by examples.
    Legal use cases:
    1. A.sol B.sol
        ->  contracts=(A, B), files=(A.sol, B.sol), contract_to_file={'A': 'A.sol', 'B': 'B.sol'},
            file_to_contracts = {'A.sol': ['A'], 'B.sol': ['B']}
    2. A.sol:a B.sol:b C.sol
        ->  contracts=(a, b, C), files=(A.sol, B.sol, C.sol),
            contract_to_file={'a': 'A.sol', 'b': 'B.sol', 'C': 'C.sol'},
            file_to_contracts = {'A.sol': ['a'], 'B.sol': ['b'], 'C.sol': ['C']}
    3. A.sol:B B.sol:c
        ->  contracts=(B, c), files=(A.sol, B.sol),
            contract_to_file={'B': 'A.sol', 'c': 'B.sol'},
            file_to_contracts = {'A.sol': ['B'], 'B.sol': ['c']}
    4. A.sol:b A.sol:c
        ->  contracts=(b, c), files=(A.sol),
            contract_to_file={'b': 'A.sol', 'c': 'A.sol'},
            file_to_contracts = {'A.sol': ['b', 'c']}

    Warning cases:
    4. A.sol A.sol
        -> A.sol is redundant
    5. A.sol:a A.sol:a
        -> A.sol:a is redundant
    6. A.sol:A
        -> contract name A is redundant (it's the default name)

    Illegal cases:
    7. A.sol:a B.sol:a
        -> The same contract name cannot be used twice
    8. ../A.sol A.sol
        -> The same contract name cannot be used twice
    9. A.sol:B B.sol
        -> The same contract name cannot be used twice
    10. A.sol:a A.sol
        -> The same file cannot contain two different contracts
    11. A.sol A.sol:a
        -> The same file cannot contain two different contracts

    Warning are printed only if the input is legal
    @raise CertoraUserInputError in an illegal case (see above)
    """
    if len(files) == 1 and (files[0].endswith(".conf") or files[0].endswith(".tac")):
        return set(), set(), dict(), dict()  # No legal contract names

    declared_contracts = set()
    file_paths = set()
    all_warnings = set()

    contract_to_file: Dict[str, str] = dict()
    file_to_contracts: Dict[str, Set[str]] = dict()

    for f in files:

        default_contract_name = Util.get_trivial_contract_name(f)
        posix_path = os.path.relpath(Util.abs_posix_path_obj(f), Path.cwd())
        assert posix_path.count(':') < 2
        if ':' in posix_path:
            filepath_str, contract_name = posix_path.split(":")
            if contract_name == default_contract_name:
                all_warnings.add(f"contract name {contract_name} is the same as the file name and can be omitted "
                                 f"from {filepath_str}:{contract_name}")
        else:
            filepath_str = posix_path
            contract_name = default_contract_name

        if filepath_str in file_to_contracts:
            if contract_name in file_to_contracts[filepath_str]:
                all_warnings.add(f"file argument {f} appears more than once and is redundant")
                continue

        if contract_name in contract_to_file and contract_to_file[contract_name] != filepath_str:
            # A.sol:a B.sol:a
            raise Util.CertoraUserInputError(f"A contract named {contract_name} was declared twice for files "
                                             f"{contract_to_file[contract_name]}, {filepath_str}")

        contract_to_file[contract_name] = filepath_str
        file_to_contracts.setdefault(filepath_str, set()).add(contract_name)
        declared_contracts.add(contract_name)
        file_paths.add(filepath_str)

    for warning in all_warnings:
        validation_logger.warning(warning)

    return declared_contracts, file_paths, contract_to_file, file_to_contracts


def check_contract_name_arg_inputs(context: CertoraContext) -> None:
    """
    This function verifies that all options that expect to get contract names get valid contract names.
    If they do, nothing happens. If there is any error, an exception is thrown.
    @param context: Namespace containing all command line arguments
    @raise CertoraUserInputError if a contract name argument was expected, but not given.
    """
    contract_names, file_paths, contract_to_file, file_to_contract = warn_validate_file_args(context.files)
    context.contracts = contract_names
    context.file_paths = file_paths
    context.file_to_contract = file_to_contract
    context.contract_to_file = contract_to_file

    # we print the warnings at the end of this function, only if no errors were found. Each warning appears only once
    all_warnings = set()

    # Link arguments can be either: contractName:slot=contractName
    #   or contractName:slot=integer(decimal or hexadecimal)
    if context.link is not None:
        for link in context.link:
            executable = link.split(':')[0]
            executable = Util.get_trivial_contract_name(executable)
            if executable not in contract_names:
                __suggest_contract_name(f"link, {link}, doesn't match any contract name", executable, contract_names,
                                        contract_to_file)

            library_or_const = link.split('=')[1]
            try:
                parsed_int = int(library_or_const, 0)  # can be either a decimal or hexadecimal number
                if parsed_int < 0:
                    raise Util.CertoraUserInputError(f"slot number is negative at {link}")
            except ValueError:
                library_name = Util.get_trivial_contract_name(library_or_const)
                if library_name not in contract_names:
                    __suggest_contract_name(f"{library_name} in link '{link}' doesn't match any contract name",
                                            library_name, contract_names, contract_to_file)

        check_conflicting_link_args(context)

    context.verified_contract_files = []
    if context.assert_contracts is not None:
        for assert_arg in context.assert_contracts:
            contract = Util.get_trivial_contract_name(assert_arg)
            if contract not in contract_names:
                __suggest_contract_name(f"'assert' argument, {contract}, doesn't match any contract name", contract,
                                        contract_names, contract_to_file)
            else:
                context.verified_contract_files.append(contract_to_file[contract])

    context.spec_files = None

    if context.verify is not None:
        spec_files = set()
        contract, spec = context.verify.split(':')
        contract = Util.get_trivial_contract_name(contract)
        if contract not in contract_names:
            __suggest_contract_name(f"'verify' argument, {contract}, doesn't match any contract name", contract,
                                    contract_names, contract_to_file)
        spec_files.add(spec)
        context.verified_contract_files.append(contract_to_file[contract])
        context.spec_files = sorted(list(spec_files))

    contract_to_address = dict()
    if context.address:
        for address_str in context.address:
            contract = address_str.split(':')[0]
            if contract not in contract_names:
                __suggest_contract_name(f"unrecognized contract in 'address' argument {address_str}", contract,
                                        contract_names, contract_to_file)
            number = address_str.split(':')[1]
            if contract not in contract_to_address:
                contract_to_address[contract] = number
            elif contract_to_address[contract] != number:
                raise Util.CertoraUserInputError(f'contract {contract} was given two different addresses: '
                                                 f'{contract_to_address[contract]} and {number}')
            else:
                all_warnings.add(f'address {number} for contract {contract} defined twice')
    context.address = contract_to_address

    if context.struct_link:
        contract_slot_to_contract = dict()
        for link in context.struct_link:
            location = link.split('=')[0]
            destination = link.split('=')[1]
            origin = location.split(":")[0]
            if origin not in contract_names:
                __suggest_contract_name(
                    f"'struct_link' argument {link} is illegal: {origin} is not a defined contract name", origin,
                    contract_names, contract_to_file)
            if destination not in contract_names:
                __suggest_contract_name(
                    f"'struct_link' argument {link} is illegal: {destination} is not a defined contract name",
                    destination, contract_names, contract_to_file)

            if location not in contract_slot_to_contract:
                contract_slot_to_contract[location] = destination
            elif contract_slot_to_contract[location] == destination:
                all_warnings.add(f"'struct_link' argument {link} appeared more than once")
            else:
                raise Util.CertoraUserInputError(f"{location} has two different definitions in 'struct_link': "
                                                 f"{contract_slot_to_contract[location]} and {destination}")

    for warning in all_warnings:
        validation_logger.warning(warning)


def check_mode_of_operation(context: CertoraContext) -> None:
    """
    Ascertains we have only one Util.Mode of operation in use and updates context.mode to store it as an enum.
    The Util.Modes are:
    1. There is a single .tac file
    2. There is a single .conf file
    3. There is a single .json file
    4. --assert
    5. --verify
    6. --bytecode - the only case in which files may be empty


    This function ascertains there is no overlap between the Util.Modes. The correctness of each
    Mode is checked in other functions.

    @param context: A namespace including all CLI arguments provided
    @raise an CertoraUserInputError when:
        1. .conf|.tac|.json file is used with --assert|--verify flags
        2. when both --assert and --verify flags were given
        3. when the file is not .tac|.conf|.json and neither --assert nor --verify were used
        4. If any file is provided with --bytecode flag
        5. If either --bytecode or --bytecode_spec was used without the other.
    """
    is_verifying = context.verify is not None and len(context.verify) > 0
    is_asserting = context.assert_contracts is not None and len(context.assert_contracts) > 0
    is_bytecode = context.bytecode_jsons is not None and len(context.bytecode_jsons) > 0
    has_bytecode_spec = context.bytecode_spec is not None

    if is_verifying and is_asserting:
        raise Util.CertoraUserInputError("only one option of 'assert_contracts' and 'verify' can be used")

    if has_bytecode_spec != is_bytecode:
        raise Util.CertoraUserInputError("Must use 'bytecode' together with 'bytecode_spec'")

    special_file_type = None
    files_len = len(context.files)

    if files_len == 0:
        if not is_bytecode:
            raise Util.CertoraUserInputError("Should always provide input files, unless 'bytecode_jsons' is used")
    else:
        if is_bytecode:
            raise Util.CertoraUserInputError("Cannot use 'bytecode_jsons' with other files")

        # We already checked that this is the only case where we might encounter CONF, TAC, or .o files
        input_file = context.files[0]
        for suffix in [".tac", ".conf", ".json", ".o", ".so"]:
            if input_file.endswith(suffix):
                special_file_type = suffix
                if len(context.files) > 1:
                    raise Util.CertoraUserInputError("No other files are allowed when one of the files ends with "
                                                     f"{suffix}")

            if special_file_type is not None:
                if is_asserting:
                    raise Util.CertoraUserInputError(
                        f"Option 'assert_contracts' cannot be used with a {special_file_type} file {input_file}")

    if special_file_type is None and not is_asserting and not is_verifying and not is_bytecode:
        raise Util.CertoraUserInputError(
            "You must use either 'assert_contracts' or 'verify' or 'bytecode' when running the Certora Prover")

    # If we made it here, exactly a single Util.Mode was used. We update the namespace entry Util.Mode accordingly:
    if is_verifying and special_file_type != '.conf':
        context.mode = Util.Mode.VERIFY
    elif is_asserting:
        context.mode = Util.Mode.ASSERT
    elif is_bytecode:
        context.mode = Util.Mode.BYTECODE
    elif special_file_type == '.conf':
        context.mode = Util.Mode.CONF
    elif special_file_type == '.tac':
        context.mode = Util.Mode.TAC
    elif special_file_type == '.o' or special_file_type == '.so':
        context.mode = Util.Mode.SOLANA
    else:
        raise ValueError(f"File {input_file} has unsupported file type {special_file_type}")


def check_packages_arguments(context: CertoraContext) -> None:
    """
    Performs checks on the --packages_path and --packages options.
    @param context: A namespace including all CLI arguments provided
    @raise an CertoraUserInputError if:
        1. both options --packages_path and --packages options were used
        2. in --packages the same name was given multiples paths
    """
    if context.packages_path is None:
        context.packages_path = os.getenv("NODE_PATH", f"{Path.cwd() / 'node_modules'}")
        validation_logger.debug(f"context.packages_path is {context.packages_path}")

    if context.packages is not None and len(context.packages) > 0:
        context.package_name_to_path = dict()
        for package_str in context.packages:
            package = package_str.split("=")[0]
            path = package_str.split("=")[1]
            if not Path(path).is_dir():
                raise Util.CertoraUserInputError(
                    f"package path {path} is not a directory")
            if package in context.package_name_to_path:
                raise Util.CertoraUserInputError(
                    f"package {package} was given two paths: {context.package_name_to_path[package]}, {path}")
            if path.endswith("/"):
                # emitting a warning here because here loggers are already initialized
                validation_logger.warning(
                    f"Package {package} is given a path ending with a `/`, which could confuse solc: {path}")
            context.package_name_to_path[package] = path

        context.packages = sorted(context.packages, key=str.lower)

    else:
        if check_if_dependencies_file_readable(Util.PACKAGE_FILE):
            try:
                with Util.PACKAGE_FILE.open() as package_json_file:
                    package_json = json.load(package_json_file)
                    deps = set(list(package_json["dependencies"].keys()) if "dependencies" in package_json else
                               list(package_json["devDependencies"].keys()) if "devDependencies" in package_json
                               else list())  # May need both

                    packages_path = context.packages_path
                    packages_to_path_list = [f"{package}={packages_path}/{package}" for package in deps]
                    context.packages = sorted(packages_to_path_list, key=str.lower)

            except EnvironmentError:
                ex_type, ex_value, _ = sys.exc_info()
                validation_logger.warning(f"Failed in processing {Util.PACKAGE_FILE}: {ex_type}, {ex_value}")
                handle_remappings_file(context)
        else:
            # if we failed with package.json, we try with remappings file
            handle_remappings_file(context)


def handle_remappings_file(context: CertoraContext) -> None:
    """"
    Tries to reach packages from remappings.txt
    """
    if check_if_dependencies_file_readable(Util.REMAPPINGS_FILE):
        try:
            with Util.REMAPPINGS_FILE.open() as remappings_file:
                context.packages = sorted(list(map(lambda x: x.strip(), remappings_file.readlines())), key=str.lower)
        except EnvironmentError:
            ex_type, ex_value, _ = sys.exc_info()
            validation_logger.warning(f"Failed in processing {Util.REMAPPINGS_FILE}: {ex_type}, {ex_value}")


def check_if_dependencies_file_readable(f: Path) -> bool:
    """
    Given a path to dependencies listings (aka package.json or remappings.txt), checks it is accessible.
    @returns True if f is accessible, False otherwise
    """
    if not f.exists():
        validation_logger.warning(
            f"Default package file {f} not found, external contract dependencies could be "
            f"unresolved. Ignore if solc invocation was successful"
        )
        return False
    elif not os.access(f, os.R_OK):
        validation_logger.warning(f"No read permissions for default package file {f}")
        return False

    return True


def check_solc_map(context: CertoraContext) -> None:
    """
    Executes all post-parsing checks of --solc and --solc_map arguments:
    1. --solc and --solc_map cannot be used together
    2. If both --solc and --solc_map were not used, and we are not in conf file Util.Mode,
       take the default solc and check its validity.
    3. If --solc_map is used, and we are not in .conf file mode:
       verify that every source file appears in the map and that every mapping has a valid file path as a
       key. Note: we rely on validate_solc_map() to guarantee that no file appears with conflicting values in the map
    For backwards compatibility reasons, we also allow the entry of contract names instead of files. If so, we fetch the
    source file that includes the contract and map it. We again check that there are no conflicts.
    @param context: A namespace including all CLI arguments provided
    @raise CertoraUserInputError if:
                1. both --solc and --solc_map options are present in context
                2. A key in the solc mapping is not a valid source file or a valid contract name
                3. Some source files do not appear as keys in the solc map
                4. If there are two or more contracts in the same source file with conflicting values
    """
    if context.solc is not None and context.solc_map is not None:
        raise Util.CertoraUserInputError("You cannot use both 'solc' and 'solc_map' arguments")

    if context.solc_map is None:
        context.solc = Vf.is_solc_file_valid(context.solc)
    else:  # we use solc_map, check its validity
        orphan_files = deepcopy(context.file_paths)
        normalized_solc_map = deepcopy(context.solc_map)  # The normalized map has only paths as keys, not contracts

        for (source_file, solc) in context.solc_map.items():
            # No need to call is_solc_file_valid(solc) as they are validated as a part of validate_solc_map()
            abs_src_file = str(Path(source_file).resolve())
            src_file_found = False
            for _file in context.file_paths:
                curr_abs_src_file = str(Path(_file).resolve())
                if abs_src_file == curr_abs_src_file:
                    if _file in orphan_files:
                        orphan_files.remove(_file)
                        src_file_found = True
                        break

            if not src_file_found:
                # it might be a contract name, for backwards compatibility reasons
                contract = source_file
                if contract not in context.contracts:
                    raise Util.CertoraUserInputError(
                        f"'solc_map' argument {source_file}={solc}: {source_file} is not a source file/contract")
                containing_source_file = context.contract_to_file[contract]
                if containing_source_file in normalized_solc_map:
                    if normalized_solc_map[containing_source_file] != solc:
                        raise Util.CertoraUserInputError(
                            f"Source file {containing_source_file} has two conflicting Solidity compiler versions in "
                            f"'solc_map', one of them is {contract}={solc}")
                else:
                    normalized_solc_map[containing_source_file] = solc
                    del normalized_solc_map[contract]
                    orphan_files.remove(containing_source_file)

        if len(orphan_files) > 0:
            raise Util.CertoraUserInputError(
                f"Some source files do not appear in 'solc_map': {', '.join(orphan_files)}")

        context.solc_map = normalized_solc_map


def check_optimize_map(context: CertoraContext) -> None:
    """
    Executes all post-parsing checks of --optimize_map and --optimize arguments:
    1. --optimize and --optimize_map cannot be used together
    2. if --optimize_map is used and we are not in .conf file Util.Mode:
       Verify that every source file appears exactly once in the map and that every mapping has a valid source file as a
       key.
       Note: for backwards compatibility reasons, we allow using contract names as keys. It is not allowed to have two
       or more different contracts from the same source file with different optimizations.
    @param context: A namespace including all CLI arguments provided
    @raise CertoraUserInputError if:
                1. Both --optimize and --optimize_map options are present in context.
                2. A key in the mapping is not a valid source file or contract.
                3. Some source files do not appear as keys in the map and none of their contracts appear as keys either.
                4. A file has two or more contracts with conflicting optimization values.
    """
    if context.optimize is not None and context.optimize_map is not None:
        raise Util.CertoraUserInputError("You cannot use both 'optimize' and 'optimize_map' arguments")

    if context.optimize_map is not None:

        # See if any source file is missing a number of runs in the map
        orphan_files = deepcopy(context.file_paths)
        normalized_opt_map = deepcopy(context.optimize_map)  # The normalized map has only paths as keys not contracts

        for (source_file, num_runs) in context.optimize_map.items():
            abs_src_file = str(Path(source_file).resolve())
            src_file_found = False
            for _file in context.file_paths:
                curr_abs_src_file = str(Path(_file).resolve())
                if abs_src_file == curr_abs_src_file:
                    if _file in orphan_files:
                        orphan_files.remove(_file)
                        src_file_found = True
                        break

            if not src_file_found:
                # it might be a contract name, for backwards compatibility reasons
                contract = source_file
                if contract not in context.contracts:
                    raise Util.CertoraUserInputError(
                        f"'optimize_map' argument {source_file}={num_runs}: {source_file} is not a source "
                        "file/contract")
                containing_source_file = context.contract_to_file[contract]
                if containing_source_file in normalized_opt_map:
                    if normalized_opt_map[containing_source_file] != num_runs:
                        raise Util.CertoraUserInputError(
                            f"Source file {containing_source_file} has two conflicting number of runs optimizations in "
                            f"'optimize_map', one of them is {contract}={num_runs}")
                else:
                    normalized_opt_map[containing_source_file] = num_runs
                    del normalized_opt_map[contract]
                    orphan_files.remove(containing_source_file)

        if len(orphan_files) > 0:
            raise Util.CertoraUserInputError(
                f"Some source files do not appear in 'optimize_map': {', '.join(orphan_files)}")

        # See that there is no --optimize-runs inside --solc_args
        if context.solc_args is not None:
            if '--optimize-runs' in context.solc_args:
                raise Util.CertoraUserInputError(
                    "You cannot use both 'optimize_map' and the 'solc_args' argument 'optimize-runs'")

        context.optimize_map = normalized_opt_map


def check_solc_optimize_map(context: CertoraContext) -> None:
    """
    Called only by the new API

    Executes all post-parsing checks of --solc_optimize_map and --solc_optimize arguments:
    1. --solc_optimize and --solc_optimize_map cannot be used together
    2. if --solc_optimize_map is used and we are not in .conf file Util.Mode:
       Verify that every source file appears exactly once in the map and that every mapping has a valid source file as a
       key. Note: we rely on validate_solc_optimize_map() to guarantee that no source file appears with conflicting
       values.
       Note: for backwards compatibility reasons, we allow using contract names as keys. It is not allowed to have two
       or more different contracts from the same source file with different optimizations.
    @param context: A namespace including all CLI arguments provided
    @raise CertoraUserInputError if:
                1. Both --solc_optimize and --solc_optimize_map options are present in context.
                2. A key in the mapping is not a valid source file or contract.
                3. Some source files do not appear as keys in the map and none of their contracts appear as keys either.
                4. A file has two or more contracts with conflicting optimization values.
    """
    if context.solc_optimize is not None and context.solc_optimize_map is not None:
        raise Util.CertoraUserInputError("You cannot use both 'solc_optimize' and 'solc_optimize_map' arguments")

    if context.solc_optimize_map is not None:

        # See if any source file is missing a number of runs in the map
        orphan_files = deepcopy(context.file_paths)
        normalized_opt_map = deepcopy(context.solc_optimize_map)  # The map has only paths as keys not contracts

        for (source_file, num_runs) in context.solc_optimize_map.items():
            abs_src_file = str(Path(source_file).resolve())
            src_file_found = False
            for _file in context.file_paths:
                curr_abs_src_file = str(Path(_file).resolve())
                if abs_src_file == curr_abs_src_file:
                    if _file in orphan_files:
                        orphan_files.remove(_file)
                        src_file_found = True
                        break

            if not src_file_found:
                # it might be a contract name, for backwards compatibility reasons
                contract = source_file
                if contract not in context.contracts:
                    raise Util.CertoraUserInputError(
                        f"'solc_optimize_map' argument {source_file}={num_runs}: {source_file} "
                        "is not a source file/contract")
                containing_source_file = context.contract_to_file[contract]
                if containing_source_file in normalized_opt_map:
                    if normalized_opt_map[containing_source_file] != num_runs:
                        raise Util.CertoraUserInputError(
                            f"Source file {containing_source_file} has two conflicting number of runs optimizations in "
                            f"solc_optimize_map, one of them is {contract}={num_runs}")
                else:
                    normalized_opt_map[containing_source_file] = num_runs
                    del normalized_opt_map[contract]
                    orphan_files.remove(containing_source_file)

        if len(orphan_files) > 0:
            raise Util.CertoraUserInputError(
                f"Some source files do not appear in 'solc_optimize_map': {', '.join(orphan_files)}")

        context.solc_optimize_map = normalized_opt_map


def check_rule(context: CertoraContext) -> None:
    """
    Checks that we do not use both --rule (or --settings -rule) in any other Mode than --verify
    @param context: a namespace containing command line arguments
    @raises ArgumentTypeError when a user chose a rule with --rule or --settings -rule when not in verify mode
    """
    if context.rule is None:
        return

    if not context.verify and context.bytecode_spec is None:
        raise Util.CertoraUserInputError(
            "checking for a specific rule is only supported with 'verify' and 'bytecode_spec'")


def check_args_post_argparse(context: CertoraContext) -> None:
    """
    Performs checks over the arguments after basic argparse parsing

    argparse parses option one by one. This is the function that checks all relations between different options and
    arguments. We assume here that basic syntax was already checked.
    @param context: A namespace including all CLI arguments provided
    @raise CertoraUserInputError if input is illegal
    """
    if context.solc_allow_path is None:
        context.solc_allow_path = str(__default_path())

    check_files_input(context.files)
    check_contract_name_arg_inputs(context)  # Here context.contracts is set
    check_packages_arguments(context)
    check_solc_map(context)
    check_solc_optimize_map(context)

    check_rule(context)
    certora_root_dir = Util.get_certora_root_directory().as_posix()
    default_jar_path = Path(certora_root_dir) / "emv.jar"
    if context.jar is not None or (default_jar_path.is_file() and not context.server):
        context.local = True
    else:
        context.local = False

    if context.java_args is not None:
        context.java_args = ' '.join(context.java_args).replace('"', '').replace("'", '')

    if context.typecheck_only and context.disable_local_typechecking:
        raise Util.CertoraUserInputError("cannot use both 'typecheck_only' and 'disable_local_typechecking'")

    if context.typecheck_only and context.build_only:
        raise Util.CertoraUserInputError("cannot use both 'typecheck_only' and 'build_only'")

    if context.local and context.typecheck_only:
        raise Util.CertoraUserInputError("cannot use 'typecheck_only' in local tool runs")

    if context.rule_sanity and context.multi_assert_check:
        raise Util.CertoraUserInputError("cannot run with both 'rule_sanity' and 'multi_assert_check'")

    if context.wait_for_results is not None:
        if context.local:
            validation_logger.warning("'wait_for_results' has no effect in local tool runs")

    # packages must be in a normal form (no unneeded . or ..)
    if context.packages:
        for idx, el in enumerate(context.packages):
            key, path = el.split('=')
            abs_path = os.path.abspath(path)
            context.packages[idx] = '='.join([key, os.path.relpath(abs_path, os.getcwd())])

    if context.debug_topics is not None or context.show_debug_topics:
        context.debug = True

    # if --fe_version was not set then if the package is alpha/beta we set it to latest else we set it to production
    if not context.fe_version:
        if Util.get_package_and_version()[1] in [Util.ALPHA_PACKAGE_NAME, Util.BETA_PACKAGE_NAME]:
            context.fe_version = str(Util.FeValue.LATEST)
        else:
            context.fe_version = str(Util.FeValue.PRODUCTION)

    check_conflicting_branch_and_hash(context)
    set_wait_for_results_default(context)


def __default_path() -> Path:
    path = Path.cwd() / "contracts"
    if path.is_dir():
        return path.resolve()
    return Path.cwd().resolve()


def check_no_pretty_quotes(args_list: List[str]) -> None:
    """
    :param args_list: A list of CL arguments
    :raises CertoraUserInputError if there are wrong quotation marks “ in use (" are the correct ones)
    """
    for arg in args_list:
        if '“' in arg:
            raise Util.CertoraUserInputError('Please replace “ with " quotation marks')


def __suggest_contract_name(err_msg: str, contract_name: str, all_contract_names: Set[str],
                            contract_to_file: Dict[str, str]) -> None:
    err_str = err_msg
    suggestions = Util.get_closest_strings(contract_name, list(all_contract_names), max_suggestions=1)

    if len(suggestions) == 1:
        suggested_contract = suggestions[0]
        err_str = f'{err_str}. Maybe you meant contract {suggested_contract} ' \
                  f'(found in file {contract_to_file[suggested_contract]})?'
    err_str += ' \nNote: To specify a contract in a differently-named sol file, you can ' \
               'provide the contract name explicitly, ie: certoraRun sol_file.sol:XYZcontract ' \
               '--verify XYZcontract:spec_file.spec'

    """
    Why do we raise from None?
    We run this function from an except block. We explicitly want to discard the context of the exception caught in the
    wrapping except block. If we do not discard the previous exception context, we see the following confusing pattern:
        "During handling of the above exception, another exception occurred:"
    """
    raise Util.CertoraUserInputError(err_str) from None  # ignore prev exception context


def check_conflicting_link_args(context: CertoraContext) -> None:
    """
    Detects contradicting definitions of slots in link and throws.
    DOES NOT check for file existence, format legality, or anything else.
    We assume the links contain no duplications.
    @param context: A context object, where context.link includes a list of strings that are the link arguments
    @raise CertoraUserInputError if a slot was given two different definitions
    """
    pair_list = itertools.permutations(context.link, 2)
    for pair in pair_list:
        link_a = pair[0]
        link_b = pair[1]
        slot_a = link_a.split('=')[0]
        slot_b = link_b.split('=')[0]
        if slot_a == slot_b:
            raise Util.CertoraUserInputError(f"slot {slot_a} was defined multiple times: {link_a}, {link_b}")


def check_conflicting_branch_and_hash(context: CertoraContext) -> None:
    """
    A run can be sent to either a specific branch or a specific commit hash, but never both
    @param context: A context object
    @raise CertoraUserInputError if both a branch and a specific commit hash were specified
    """
    commit_hash = context.commit_sha1
    if commit_hash:
        staging_branch = context.prover_version
        if context.local:
            raise Util.CertoraUserInputError("Cannot run on a specific commit in local runs. ")
        elif Ctx.is_staging(context) and bool(staging_branch):
            raise Util.CertoraUserInputError(f"Cannot run on both a specific branch {staging_branch} "
                                             f"and a specific commit {commit_hash}")


def validate_certora_key() -> str:
    f"""
    Checks that the environment variable {KEY_ENV_VAR} is legal and returns a valid Certora key.
    If the environment variable {KEY_ENV_VAR} is undefined or empty, the public key is returned.
    If the environment variable {KEY_ENV_VAR} has a different legal value, returns it.
    @raise RuntimeError if {KEY_ENV_VAR} has an illegal value.
    """
    key = os.environ.get(KEY_ENV_VAR, "")
    if not key:
        is_ci = os.environ.get("CI", "") == "true"
        if is_ci:
            txt = f"""You are using a demo version of the tool in a CI environment.
                     If you have a premium Certora key, please set it as the environment variable {KEY_ENV_VAR}.
                  """
            raise Util.CertoraUserInputError(txt)
        key = Util.PUBLIC_KEY
        print('\n')
        txt_1 = "You are using the demo version of the tool. Therefore, the tool has limited resources."
        validation_logger.warning(f'{Util.red_text(txt_1)}')
        txt_2 = f'If you have a premium Certora key, please set it as the environment variable {KEY_ENV_VAR}.'
        validation_logger.warning(f"{Util.red_text(txt_2)}\n")
        time.sleep(1)

    if not re.match(r'^[0-9A-Fa-f]+$', key):  # checks if the key is a hexadecimal number (without leading 0x)
        raise Util.CertoraUserInputError(f"environment variable {KEY_ENV_VAR} has an illegal value")
    if not len(key) in Util.LEGAL_CERTORA_KEY_LENGTHS:
        raise Util.CertoraUserInputError(f"environment variable {KEY_ENV_VAR} has an illegal length")
    return key


def check_files_input(file_list: List[str]) -> None:
    """
    Verifies that correct input was inserted as input to files.
    As argparser verifies the files exist and the correctness of the format, we only check if only a single operation
    mode was used.
    The allowed disjoint cases are:
    1. Use a single .conf file
    2. Use a single .tac file
    3. Use a single .o or .so file
    4. Use any number of [contract.sol:nickname ...] (at least one is guaranteed by argparser)
    @param file_list: A list of strings representing file paths
    @raise CertoraUserInputError if more than one of the modes above was used
    """
    num_files = len(file_list)
    if num_files > 1:  # if there is a single file, there cannot be a mix between file types
        for file in file_list:
            if '.tac' in file:
                raise Util.CertoraUserInputError(f'When using the tool in TAC Util.Mode by providing .tac file {file}, '
                                                 f'you can only provide a single file. {num_files} files were given')
            if '.conf' in file:
                raise Util.CertoraUserInputError(
                    f'When using the tool in CONF Util.Mode by providing .conf file {file}, '
                    f'you can only provide a single file. {num_files} files were given')
            if file.endswith(".o") or file.endswith(".so"):
                raise Util.CertoraUserInputError(
                    f'When using the tool in SOLANA Util.mode by providing .conf file {file}, '
                    f'you can only provide a single file. {num_files} files were given')


def set_wait_for_results_default(context: CertoraContext) -> None:
    if context.wait_for_results is None:
        if Util.is_ci_or_git_action():
            context.wait_for_results = str(Vf.WaitForResultOptions.ALL)
        else:
            context.wait_for_results = str(Vf.WaitForResultOptions.NONE)
