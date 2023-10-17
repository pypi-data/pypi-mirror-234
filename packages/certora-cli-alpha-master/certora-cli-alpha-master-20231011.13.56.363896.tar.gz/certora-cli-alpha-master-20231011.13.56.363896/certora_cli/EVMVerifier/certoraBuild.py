import enum
import json
import logging
import os
import re
import shutil
import sys
import typing
from collections import OrderedDict
from enum import Enum
from functools import lru_cache, reduce
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional, Set, BinaryIO, Iterator
from Crypto.Hash import keccak
from sly import Lexer  # type: ignore[import]
from sly import Parser  # type: ignore[import]
from sly.lex import Token  # type: ignore[import]
from sly.yacc import YaccProduction  # type: ignore[import]

scripts_dir_path = Path(__file__).parent.parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))
from EVMVerifier.Compiler.CompilerCollector import CompilerLang, CompilerCollector
from EVMVerifier.Compiler.CompilerCollectorSol import CompilerCollectorSol, CompilerLangSol
from EVMVerifier.Compiler.CompilerCollectorVy import CompilerLangVy
from EVMVerifier.Compiler.CompilerCollectorFactory import CompilerCollectorFactory, \
    get_relevant_compiler, get_compiler_lang
from EVMVerifier.certoraNodeFilters import NodeFilters as Nf
import EVMVerifier.certoraType as CT

from EVMVerifier.certoraContextClass import CertoraContext
import EVMVerifier.certoraContextAttribute as Attr
from Shared import certoraUtils as Util

BUILD_IS_LIBRARY = False
AUTO_FINDER_PREFIX = "autoFinder_"
CONF_FILE_ATTR = 'conf_file'
INTERNALTYPE = "internalType"
TYPE = "type"
SOL = ".sol"
VY = ".vy"
INPUTS = "inputs"
OUTPUTS = "outputs"
FUNCTION = "function"
CONTRACTS = "contracts"
STATEMUT = "stateMutability"
NAME = "name"

FunctionSig = Tuple[str, List[str], List[str], str]

# logger for building the abstract syntax tree
ast_logger = logging.getLogger("ast")
# logger for issues calling/shelling out to external functions
process_logger = logging.getLogger("rpc")
# logger for running the Solidity compiler and reporting any errors it emits
compiler_logger = logging.getLogger("compiler")
# logger for instrumentation for the function finder
instrumentation_logger = logging.getLogger("finder_instrumentation")
# logger of the build configuration
build_logger = logging.getLogger("build_conf")


def fatal_error(logger: logging.Logger, msg: str) -> None:
    logger.fatal(msg)
    raise Exception(msg)


class MutationType(object):
    def insert(self, what: str, expected: bytes, file: BinaryIO) -> int:
        raise NotImplementedError("Did not implement insertion")


class InsertBefore(MutationType):
    def __init__(self) -> None:
        pass

    def insert(self, what: str, expected: bytes, file: BinaryIO) -> int:
        file.write(bytes(what, "utf-8"))
        file.write(expected)
        return 0


class InsertAfter(MutationType):
    def __init__(self) -> None:
        pass

    def insert(self, what: str, expected: bytes, file: BinaryIO) -> int:
        file.write(expected)
        file.write(bytes(what, "utf-8"))
        return 0


class Replace(MutationType):
    def __init__(self, amt: int) -> None:
        self.to_delete = amt

    def insert(self, what: str, expected: bytes, file: BinaryIO) -> int:
        to_read = self.to_delete - len(expected)
        file.write(bytes(what, "utf-8"))
        return to_read


class Instrumentation:
    def __init__(self, expected: bytes, mut: MutationType, to_ins: str) -> None:
        self.expected = expected
        self.mut = mut
        self.to_ins = to_ins


class InputConfig:
    def __init__(self, context: CertoraContext) -> None:
        """
        A class holding relevant attributes for the build string.
        :param context: command line input argument in an argparse.Namespace
        """

        # populate fields relevant for build, handle defaults
        self.files = sorted(list(context.file_paths))
        self.solc = context.solc
        self.solc_args = context.solc_args
        self.packages = context.packages
        self.verify = context.verify
        self.assert_contracts = context.assert_contracts
        self.path = context.solc_allow_path
        self.link = context.link
        self.struct_link = context.struct_link
        self.function_finders = context.internal_funcs

        if context.solc_map is not None:
            self.solc_mappings = context.solc_map  # type: Dict[str, str]
        else:
            self.solc_mappings = {}

        optimize_map_attr = context.solc_optimize_map
        if optimize_map_attr is not None:
            self.optimize_map = optimize_map_attr  # type: Dict[str, str]
        else:
            self.optimize_map = {}

        if context.address is not None:
            self.address = context.address  # type: Dict[str, int]
        else:
            self.address = dict()

        self.fileToContractName = context.file_to_contract
        self.contract_to_file = context.contract_to_file

        self.prototypes = self.handle_prototypes(context)

    def __str__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def handle_prototypes(context: CertoraContext) -> Dict[str, List[str]]:
        to_ret: Dict[str, List[str]] = dict()
        if context.prototype is None:
            return to_ret
        for proto in context.prototype:
            (sig, nm) = proto.split("=")
            if nm not in to_ret:
                to_ret[nm] = []
            to_ret[nm].append(sig)
        return to_ret


class FinderGenerator(object):
    def __init__(self, internal_id: int):
        self.internal_id = internal_id
        self.alpha_renamings: List[str] = []

    def gen_key(self, flag: int) -> str:
        return f'0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff{"%0.4x" % self.internal_id}{"%0.4x" % flag}'

    @staticmethod
    def is_decomposed(arg_ty: CT.TypeInstance) -> bool:
        if isinstance(arg_ty.type, CT.ArrayType):
            return arg_ty.location == CT.TypeLocation.CALLDATA and not arg_ty.type.is_static_array()

        if isinstance(arg_ty.type, CT.PackedBytes) or isinstance(arg_ty.type, CT.StringType):
            return arg_ty.location == CT.TypeLocation.CALLDATA

        return False

    def normalize_arg(self, idx: int, ty: CT.TypeInstance, arg_name: str) -> Optional[str]:
        if not FinderGenerator.is_opcode(v_name=arg_name):
            return arg_name
        renamed = f"certoraRename{self.internal_id}_{idx}"
        if ty.get_source_str() is None:
            instrumentation_logger.debug(f"Need to rename {arg_name} with type {ty}, but"
                                         f" it doesn't have a type declaration")
            return None
        self.alpha_renamings.append(f"{ty.get_source_and_location_str()} {renamed} = {arg_name};")
        return renamed

    @staticmethod
    def is_opcode(v_name: str) -> bool:
        return v_name in {"stop", "add", "sub", "mul", "div", "sdiv", "mod", "smod", "exp", "not", "lt", "gt",
                          "slt", "sgt", "eq", "iszero", "and", "or", "xor", "byte", "shl", "shr", "sar", "addmod",
                          "mulmod", "signextend", "keccak256", "pc", "pop", "mload", "mstore", "mstore8", "sload",
                          "sstore", "msize", "gas", "address", "balance", "selfbalance", "caller", "callvalue",
                          "calldataload", "calldatasize", "calldatacopy", "codesize", "codecopy", "extcodesize",
                          "extcodecopy", "returndatasize", "returndatacopy", "extcodehash", "create", "create2",
                          "call", "callcode", "delegatecall", "staticcall", "return", "revert", "selfdestruct",
                          "invalid", "log0", "log1", "log2", "log3", "log4", "chainid", "basefee", "origin",
                          "gasprice", "blockhash", "coinbase", "timestamp", "number", "difficulty", "gaslimit"}

    def renaming(self) -> str:
        return " ".join(self.alpha_renamings)


class Func:
    def __init__(self,
                 name: str,
                 fullArgs: List[CT.TypeInstance],
                 paramNames: List[str],
                 returns: List[CT.TypeInstance],
                 sighash: str,
                 notpayable: bool,
                 fromLib: bool,  # actually serialized
                 isConstructor: bool,  # not serialized
                 stateMutability: str,
                 visibility: str,
                 implemented: bool,  # does this function have a body? (false for interface functions)
                 overrides: bool,  # does this function override an interface declaration or super-contract definition?
                 ast_id: Optional[int],
                 where: Optional[Tuple[str, str]] = None  # 1st element: source file name, 2nd element: location string
                 ):
        self.name = name
        self.fullArgs = fullArgs
        self.paramNames = paramNames
        self.returns = returns
        self.sighash = sighash
        self.notpayable = notpayable
        self.fromLib = fromLib
        self.isConstructor = isConstructor
        self.stateMutability = stateMutability
        self.visibility = visibility
        self.where = where
        self.implemented = implemented
        self.ast_id = ast_id
        self.overrides = overrides

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "paramNames": self.paramNames,
            "fullArgs": list(map(lambda x: x.as_dict(), self.fullArgs)),
            "returns": list(map(lambda x: x.as_dict(), self.returns)),
            "sighash": self.sighash,
            "notpayable": self.notpayable,
            STATEMUT: self.stateMutability,
            "visibility": self.visibility,
            "isLibrary": self.fromLib
        }

    def __repr__(self) -> str:
        return repr(self.as_dict())

    def __lt__(self, other: Any) -> bool:
        return self.source_code_signature() < other.source_code_signature()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Func):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.source_code_signature() == other.source_code_signature() and self.signature() == other.signature()

    def __hash__(self) -> int:
        return int(self.sighash, 16)

    def signature(self) -> str:
        """
        Returns the ABI-conforming version of the signature
        """
        return Func.compute_signature(self.name, self.fullArgs, lambda x: x.get_abi_canonical_string(self.fromLib))

    def source_code_signature(self) -> str:
        """
        Returns the signature of the function in non-ABI format; The argument types are not
        encoded to the ABI version (e.g. an argument of type 'struct S' will show the struct
        name, not the destructered tuple the ABI uses)
        """
        return Func.compute_signature(self.name, self.fullArgs, lambda x: x.get_source_str())

    @staticmethod
    def compute_signature(name: str, args: List[CT.TypeInstance], signature_getter: Any) -> str:
        return name + "(" + ",".join([signature_getter(x) for x in args]) + ")"

    def same_internal_signature_as(self, other: 'Func') -> bool:
        if self.name != other.name:
            return False
        args_match = len(self.fullArgs) == len(other.fullArgs) and \
            all([my_arg.matches(other_arg) for my_arg, other_arg in zip(self.fullArgs, other.fullArgs)])

        rets_match = len(self.returns) == len(other.returns) and \
            all([my_ret.matches(other_ret) for my_ret, other_ret in zip(self.returns, other.returns)])
        return args_match and rets_match

    @staticmethod
    def compute_getter_signature(variable_type: CT.TypeInstance) -> Tuple[List[CT.TypeInstance], List[CT.TypeInstance]]:
        """
        Computes the signature of a contract's (public) state-variable getter function
        :param variable_type: the storage variable whose getter parameter signature we are calculating
        :return: The param types and return types for a getter of a storage variable of type variable_type
        """
        curr = variable_type.type
        params: List[CT.TypeInstance] = []
        while True:
            if isinstance(curr, CT.MappingType):
                params.append(CT.TypeInstance(curr.domain))
                curr = curr.codomain
            elif isinstance(curr, CT.ArrayType):
                params.append(CT.TypeInstance(CT.PrimitiveType("uint256", "uint256")))
                curr = curr.elementType
            else:
                break

        # In case of the variable returned is a struct, the getter skips any struct members that are
        # of mapping or array type.
        # See https://docs.soliditylang.org/en/v0.8.17/contracts.html#getter-functions
        if isinstance(curr, CT.StructType):
            returns = [CT.TypeInstance(t.type)
                       for t in curr.members if not isinstance(t.type, (CT.MappingType, CT.ArrayType))]
        else:
            returns = [CT.TypeInstance(curr)]
        return params, returns


class InternalFunc:
    def __init__(self, fileName: str, contractName: str, func: Func):
        self.canonical_id = f"{fileName}|{contractName}"
        self.declaringContract = contractName
        self.func = func

    def as_dict(self) -> Dict[str, Any]:
        return {
            "canonicalId": self.canonical_id,
            "declaringContract": self.declaringContract,
            "method": self.func.as_dict()
        }


class ImmutableReference:
    def __init__(self, offset: str, length: str, varname: str):
        self.offset = offset
        self.length = length
        self.varname = varname

    def as_dict(self) -> Dict[str, Any]:
        return {
            "offset": self.offset,
            "length": self.length,
            "varname": self.varname
        }

    def __repr__(self) -> str:
        return repr(self.as_dict())


class PresetImmutableReference(ImmutableReference):
    def __init__(self,
                 offset: str,
                 length: str,
                 varname: str,
                 value: str
                 ):
        ImmutableReference.__init__(self, offset, length, varname)
        self.value = value

    def as_dict(self) -> Dict[str, Any]:
        _dict = ImmutableReference.as_dict(self)
        _dict["value"] = self.value
        return _dict

    def __repr__(self) -> str:
        return repr(self.as_dict())


# Python3.5 to which we maintain backward-compatibility due to CI's docker image, does not support @dataclass
class ContractInSDC:
    def __init__(self, name: str, source_file: str, lang: str,
                 report_source_file: str, address: str,
                 methods: Set[Func], bytecode: str,
                 constructor_bytecode: str,
                 srcmap: str, varmap: Any, constructor_srcmap: str,
                 storageLayout: Any, immutables: List[ImmutableReference],
                 function_finders: Dict[str, InternalFunc], internal_funcs: Set[Func], public_funcs: Set[Func],
                 all_funcs: List[Func],
                 types: List[CT.Type],
                 compiler_collector: Optional[CompilerCollector] = None,
                 source_bytes: Tuple[int, int] = (0, 0)):
        self.name = name
        self.original_file = source_file
        self.lang = lang
        self.report_source_file = report_source_file
        self.address = address
        self.methods = methods
        self.bytecode = bytecode
        self.constructor_bytecode = constructor_bytecode
        self.srcmap = srcmap
        self.varmap = varmap
        self.constructorSrcmap = constructor_srcmap
        self.storageLayout = storageLayout
        self.immutables = immutables
        # function finder: a mapping from external function ids to
        # the ids of the internal functions they are "finding" for us
        self.function_finders = function_finders
        # the internal functions of the contract NOT including imported library functions
        self.internal_funcs = internal_funcs
        # the public functions of the contract (this EXCLUDES external functions)
        self.public_funcs = public_funcs
        # all function types floating around (unique by internal signature), any AST location/ids from
        # these should not be used
        self.all_funcs = all_funcs
        self.types = types
        # the start and end source bytes of the contract
        self.source_bytes = source_bytes
        self.original_file_name = Path(source_file).name
        self.compiler_collector = compiler_collector

    def as_dict(self) -> Dict[str, Any]:
        """
        :return: A dictionary representation of this SDC, including all attributes and their values
        """
        if not self.compiler_collector:
            compiler_version = ""
        elif self.compiler_collector.smart_contract_lang == CompilerLangVy():
            compiler_version = typing.cast(str, self.compiler_collector.compiler_version)
        else:
            assert isinstance(self.compiler_collector.compiler_version, tuple), \
                f"Expected the compiler version to be a tuple of three integers, " \
                f"but got {self.compiler_collector.compiler_version}"
            compiler_version = '.'.join(str(e) for e in self.compiler_collector.compiler_version)
        return {
            "name": self.name,
            "original_file": Util.find_filename_in(Util.get_certora_sources_dir(), self.original_file),
            "lang": self.lang,
            "file": self.report_source_file,
            "address": self.address,
            "methods": list(map(lambda x: x.as_dict(), self.methods)),
            "bytecode": self.bytecode,
            "constructorBytecode": self.constructor_bytecode,
            "srcmap": self.srcmap,
            "varmap": self.varmap,
            "constructorSrcmap": self.constructorSrcmap,
            "storageLayout": self.storageLayout,
            "immutables": list(map(lambda x: x.as_dict(), self.immutables)),
            # the function finder field
            # why are we using this and not the normal list of functions?
            "internalFunctions": {key: method.as_dict() for key, method in self.function_finders.items()},
            # this doesn't even have all functions
            "allMethods": [f.as_dict() for f in self.all_funcs],
            "types": list(),
            "solidityTypes": [x.as_dict() for x in self.types],
            "compilerName": "" if not self.compiler_collector else self.compiler_collector.compiler_name,
            "compilerVersion": compiler_version,
        }

    def as_printable_dict(self) -> Dict[str, Any]:
        """
        :return: A dictionary representation of this SDC meant for printing to logs.
        It does not include long, hard-to-read attributes: bytecodes and srcmaps of the contract and the constructor.
        """
        return {
            "name": self.name,
            "original_file": self.original_file,
            "lang": self.lang,
            "file": self.report_source_file,
            "address": self.address,
            "methods": list(map(lambda x: x.as_dict(), self.methods)),
            "storageLayout": self.storageLayout,
            "immutables": list(map(lambda x: x.as_dict(), self.immutables)),
            "internalFunctions": {k: method.as_dict() for k, method in self.function_finders.items()}
        }

    def __repr__(self) -> str:
        return repr(self.as_printable_dict())


class SDC:
    """
    'Single Deployed Contracts' the solidity file whose contracts comprise a single bytecode of interest
    """

    def __init__(self, primary_contract: str, compiler_collector: CompilerCollector, primary_contract_address: str,
                 sdc_origin_file: str, original_srclist: Dict[Any, Any], report_srclist: Dict[Any, Any], sdc_name: str,
                 contracts: List[ContractInSDC], library_addresses: List[str],
                 state: Dict[str, str], struct_linking_info: Dict[str, str], legacy_struct_linking: Dict[str, str]):
        self.primary_contract = primary_contract
        self.primary_contract_address = primary_contract_address
        self.sdc_origin_file = sdc_origin_file
        self.original_srclist = original_srclist
        self.report_srclist = report_srclist
        self.sdc_name = sdc_name
        self.contracts = contracts
        self.library_addresses = library_addresses
        self.state = state
        self.structLinkingInfo = struct_linking_info
        self.legacyStructLinking = legacy_struct_linking
        self.prototypes = []  # type: List[str]
        self.compiler_collector = compiler_collector
        # The source dir relative to which we resolve srclists
        self.source_dir = "."

    def as_dict(self) -> Dict[str, Any]:
        return {
            "primary_contract": self.primary_contract,
            "primary_contract_address": self.primary_contract_address,
            "srclist": self.report_srclist,
            "sdc_name": self.sdc_name,
            CONTRACTS: list(map(lambda x: x.as_dict(), self.contracts)),
            "library_addresses": self.library_addresses,
            "state": self.state,
            "structLinkingInfo": self.structLinkingInfo,
            "legacyStructLinking": self.legacyStructLinking,
            "prototypeFor": self.prototypes,
            "sourceDir": self.source_dir
        }

    def sources_as_absolute(self) -> Set[Path]:
        return set(map(lambda x: Path(x).absolute(), self.original_srclist.values()))


# this function is Solidity specific.
# todo: create certoraBuildUtilsSol.py file, where such solidity specific functions will be.
def generate_finder_body(f: Func, internal_id: int, sym: int, compiler_collector: CompilerCollectorSol,
                         compressed: bool = False) -> Optional[Tuple[List[int], str]]:
    if compressed:
        return generate_compressed_finder(
            f, internal_id, sym, compiler_collector
        )
    else:
        return generate_full_finder(
            f, internal_id, sym, compiler_collector
        )


def generate_compressed_finder(f: Func, internal_id: int, sym: int,
                               compiler_collector: CompilerCollectorSol) -> Optional[Tuple[List[int], str]]:
    finder_gen = FinderGenerator(internal_id)
    last_loggable_arg = None
    num_symbols = 0
    for i in range(0, len(f.fullArgs)):
        num_symbols += 1
        ty = f.fullArgs[i]
        if f.paramNames[i] != "" and (not finder_gen.is_decomposed(ty) or
                                      compiler_collector.supports_calldata_assembly(f.paramNames[i])):
            last_loggable_arg = i
        if finder_gen.is_decomposed(ty):
            num_symbols += 1

    type_layout = 0
    for ty in f.fullArgs:
        if finder_gen.is_decomposed(ty):
            type_layout = (type_layout << 4 | 0b1110)
        else:
            type_layout = (type_layout << 2) | 0b1
    common_prefix = f"assembly {{ mstore({finder_gen.gen_key(0)}, {sym}) " \
                    f"mstore({finder_gen.gen_key(1)}, {num_symbols}) "

    if last_loggable_arg is None:
        to_return = common_prefix
        to_return += f"mstore({finder_gen.gen_key(2)}, {type_layout}) }}"
        return [], to_return
    else:
        logged_ty = f.fullArgs[last_loggable_arg]
        logged_name = f.paramNames[last_loggable_arg]
        body = ""

        alpha_renamed = finder_gen.normalize_arg(last_loggable_arg, logged_ty, logged_name)
        if alpha_renamed is None:
            instrumentation_logger.debug(f"Failed to alpha rename arg {last_loggable_arg}: "
                                         f"{logged_name} {logged_ty}")
            return None
        body += finder_gen.renaming()

        body += common_prefix
        body += f"mstore({finder_gen.gen_key(3)}, {type_layout}) "
        symbol_offset = 0
        for idx in range(0, last_loggable_arg):
            symbol_offset += 1
            if finder_gen.is_decomposed(f.fullArgs[idx]):
                symbol_offset += 1
        if finder_gen.is_decomposed(logged_ty):
            flag = 0x6100 + symbol_offset
            to_log = alpha_renamed + ".offset"
        else:
            flag = 0x6000 + symbol_offset
            to_log = \
                compiler_collector.normalize_storage(logged_ty.location == CT.TypeLocation.STORAGE, alpha_renamed)
        body += f"mstore({finder_gen.gen_key(flag)}, {to_log}) }}"
        return [last_loggable_arg], body


def generate_full_finder(f: Func, internal_id: int, sym: int,
                         compiler_collector: CompilerCollectorSol) -> Optional[Tuple[List[int], str]]:
    finder_gen = FinderGenerator(internal_id=internal_id)
    to_ret = "assembly { "
    to_ret += f"mstore({finder_gen.gen_key(0)}, {sym}) "
    num_arg_symbols = 0
    for arg_ty in f.fullArgs:
        num_arg_symbols += 1
        if finder_gen.is_decomposed(arg_ty):
            num_arg_symbols += 1
    to_ret += f"mstore({finder_gen.gen_key(1)}, {num_arg_symbols}) "
    used_symbols = []
    for i, ty in enumerate(f.fullArgs):
        arg_name = finder_gen.normalize_arg(i, ty, f.paramNames[i])
        used_symbols.append(i)
        if arg_name is None:
            return None

        if finder_gen.is_decomposed(ty):
            if compiler_collector.supports_calldata_assembly(arg_name):
                len_flag = 0x2000 + i
                offset_flag = 0x3000 + i
                # special encoding
                to_ret += f"mstore({finder_gen.gen_key(len_flag)}, {arg_name}.length) "
                to_ret += f"mstore({finder_gen.gen_key(offset_flag)}, {arg_name}.offset) "
                continue
            else:
                # place holder
                to_ret += f"mstore({finder_gen.gen_key(0x4000 + i)}, 0) "
                continue
        if len(arg_name) == 0:
            to_ret += f"mstore({finder_gen.gen_key(0x5000 + i)}, 0) "
            continue
        flag = 0x1000 + i
        arg = compiler_collector.normalize_storage(getattr(ty, "location", None) == CT.TypeLocation.STORAGE, arg_name)
        to_ret += f"mstore({finder_gen.gen_key(flag)}, {arg}) "
    to_ret += "}"
    return used_symbols, finder_gen.renaming() + to_ret


def generate_modifier_finder(f: Func, internal_id: int, sym: int,
                             compiler_collector: CompilerCollectorSol) -> Optional[Tuple[str, str]]:
    compressed = generate_compressed_finder(f, internal_id, sym, compiler_collector)
    if compressed is None:
        return None
    modifier_name = f"logInternal{internal_id}"
    if len(compressed[0]) == 0:
        return f"{modifier_name}()", f"modifier {modifier_name}() {{ {compressed[1]} _; }}"
    else:
        last_loggable_arg = compressed[0][0]
        logged_ty = f.fullArgs[last_loggable_arg]
        logged_name = f.paramNames[last_loggable_arg]
        modifier_body = f"modifier {modifier_name}"
        modifier_body += f"({logged_ty.get_source_and_location_str()} {logged_name}) {{ "
        modifier_body += compressed[1]
        modifier_body += " _; }"
        return f"{modifier_name}({logged_name})", modifier_body


def generate_inline_finder(f: Func, internal_id: int, sym: int,
                           compiler_collector: CompilerCollectorSol) -> Optional[str]:
    finder = generate_finder_body(f, internal_id, sym, compiler_collector, compressed=True)
    if finder is None:
        return None
    return finder[1]


def convert_pathname_to_posix(json_dict: Dict[str, Any], entry: str, smart_contract_lang: CompilerLang) -> None:
    """
    assuming the values kept in the entry [entry] inside [json_dict] are path names
    :param json_dict: dict to iterate on
    :param entry: entry in [json_dict] to look at
    """
    if entry in json_dict:
        json_dict_posix_paths = {}
        for file_path in json_dict[entry]:
            path_obj = Path(smart_contract_lang.normalize_file_compiler_path_name(file_path))
            if path_obj.is_file():
                json_dict_posix_paths[path_obj.as_posix()] = json_dict[entry][file_path]
            else:
                fatal_error(compiler_logger, f"The path of the source file {file_path}"
                                             f"in the standard json file {json_dict} does not exist")
        json_dict[entry] = json_dict_posix_paths


class CertoraBuildGenerator:
    # 12,14,04,06,00,04,10 is 0xce4604a aka certora.
    CONSTRUCTOR_STRING = "constructor"
    file_to_sdc_name: Dict[Path, str] = {}
    BASE_ADDRESS = (12 * 2 ** 24 + 14 * 2 ** 20 + 4 * 2 ** 16 + 6 * 2 ** 12 + 0 + 4 * 2 ** 4 + 10 * 2 ** 0)

    """ 6321 - "Unnamed return variable can remain unassigned"
          - emitted by solc versions 7.6 and up """
    SEVERE_COMPILER_WARNINGS = ["6321"]

    def __init__(self, input_config: InputConfig, context: CertoraContext) -> None:
        self.input_config = input_config
        self.context = context
        # SDCs describes the set of all 'Single Deployed Contracts' the solidity file whose contracts comprise a single
        # bytecode of interest. Which one it is - we don't know yet, but we make a guess based on the base filename.
        # An SDC corresponds to a single Solidity file.
        self.SDCs = {}  # type: Dict[str, SDC]

        self.config_path = Path.cwd() / Util.get_certora_config_dir()
        build_logger.debug(f"Creating dir {Util.abs_posix_path(self.config_path)}")
        Util.remove_and_recreate_dir(self.config_path)

        self.library_addresses = []  # type: List[str]

        # ASTs will be lazily loaded
        # original source file -> contract file -> nodeid -> node
        # TODO - make this a proper class
        self.asts = {}  # type: Dict[str, Dict[str, Dict[int, Any]]]
        self.certora_verify_generator: CertoraVerifyGenerator
        self.address_generator_counter = 0
        self.function_finder_generator_counter = 0
        self.function_finder_file_remappings: Dict[str, str] = {}
        self.generated_tmp_files: Set[Path] = set()
        self.all_contract_files: Set[Path] = set()
        self.path_for_compiler_collector_file: str = ""
        self.compiler_coll_factory = CompilerCollectorFactory(self.context, self.input_config.solc_args,
                                                              self.input_config.optimize_map, self.input_config.solc,
                                                              self.input_config.solc_mappings, self.config_path)
        # will be set to True if any autofinder generation failed
        self.auto_finders_failed = False
        self.__compiled_artifacts_to_clean: Set[Tuple[str, CompilerLang]] = set()

    @staticmethod
    def CERTORA_CONTRACT_NAME() -> str:
        return Nf.CERTORA_CONTRACT_NAME()

    def is_library_def_node(self, contract_file: str, node_ref: int, build_arg_contract_file: str) -> bool:
        contract_def_node = self.asts[build_arg_contract_file][contract_file][node_ref]
        return "contractKind" in contract_def_node and contract_def_node["contractKind"] == "library"

    def get_contract_file_of(self, build_arg_contract_file: str, reference: int) -> str:
        """
        Returns the contract file that was created from a given original source file and contains the given node
        :param build_arg_contract_file: name of the original source file
        :param reference: the id of the node we are looking for
        :returns: the name of the contract file that contains this node
        """
        original_file_asts = self.asts[build_arg_contract_file]
        for contract in original_file_asts:
            if reference in original_file_asts[contract]:
                return contract
        # error if got here
        fatal_error(ast_logger, f"Could not find reference AST node {reference}")
        return ""

    def get_contract_file_of_non_autofinder(self, build_arg_contract_file: str, reference: int) -> str:
        """
        For purposes of type canonicalization, an autofinder is an alias of the file it instrumented. Therefore, we
        provide the option to find the file which the autofinder aliases so all canonical type names use the original
        file name (note this is necessary since targets of the function finder mappings--mapping generated key to method
        signature--are all written in terms of the original file).
        :param build_arg_contract_file: name of the original file
        :param reference:
        :return: the name of the non-aliased contract file that contains this node
        """
        file = Util.abs_posix_path(self.get_contract_file_of(build_arg_contract_file, reference))
        if file in self.function_finder_file_remappings.keys():
            ret = Path(self.function_finder_file_remappings[file])
        else:
            ret = Path(file)
        abs_sources_dir = Util.get_certora_sources_dir().resolve()
        if abs_sources_dir in ret.parents:
            # Normalize the file-name to never include the extra `.certora_internal/.../.certora_sources` part
            # of the path.
            ret = ret.relative_to(abs_sources_dir).resolve()

        # things look nicer if they are rooted in .certora_sources
        # note that we only have those fully populated after starting to work on internal function finders
        # but that's okay - we will try to build a non-absolute canonical_id for types anyway
        in_sources = Util.find_in(Util.get_certora_sources_dir(), ret)
        if in_sources is not None:
            return str(in_sources)

        return str(ret)

    def get_original_def_node(self, build_arg_contract_file: str, reference: int) -> Dict[str, Any]:
        return self.asts[build_arg_contract_file][
            self.get_contract_file_of(build_arg_contract_file, reference)
        ][reference]

    """
    Cache size reasoning:
    The arguments for this file are contract files; there will not be too many of them.
    On packingTest, we get 4 misses and 16 hits, and reduce runtime by half a second.
    """

    @lru_cache(maxsize=32)
    def collect_type_descriptions(self, build_arg_contract_file: str, c_file: str) -> List[CT.Type]:
        user_defined_types = []  # type: List[CT.Type]
        flattened_ast = self.asts[build_arg_contract_file][c_file]
        for node_id in flattened_ast:
            node = flattened_ast[node_id]
            if Nf.is_user_defined_type_definition(node):
                _type = CT.UserDefinedType.from_def_node(
                    lambda ref: self.get_original_def_node(build_arg_contract_file, ref),
                    lambda ref: self.get_contract_file_of_non_autofinder(build_arg_contract_file, ref),
                    node
                )  # type: CT.Type
                user_defined_types.append(_type)
        return user_defined_types

    def collect_source_type_descriptions(self, contract_file: str, contract_name: str, build_arg_contract_file: str,
                                         smart_contract_lang: CompilerLang) -> List[CT.Type]:
        """
        Collecting type descriptions for a given contract
        @param source_code_file - A Solidity file containing the contract
        @param contract_name - the name of the contract
        @param build_arg_source_file - A Solidity file ()
        """
        # get base contracts and filter out libraries (it turns out you can define a type with the same name in a
        # contract as in a library)
        # TODO: We never use the is_library returned from self.retrieve_base_contract_list,
        # probably because we are not actually filtering libraries. This needs to be addressed.
        # base_contract_files = [(base_contract_file, base_contract_name) for
        #                        (base_contract_file, base_contract_name, _) in
        #                        self.retrieve_base_contracts_list(
        #                            build_arg_contract_file,
        #                            contract_file,
        #                            contract_name)]  # type: List[Tuple[str, str]]
        # think harder about how to make sure only relevant enums are included, this should include everything we need
        # plus potentially more (for example if there's another contract in the same file
        # for future reference: we separated imported types from base contracts to ensure we do not have
        # duplicated entries
        import_files = self.retrieve_imported_files(build_arg_contract_file, contract_file) \
            if smart_contract_lang.get_supports_imports() else []
        source_type_descriptions = []  # type: List[CT.Type]

        for c_file in set(import_files):
            _types = self.collect_type_descriptions(build_arg_contract_file, c_file)
            source_type_descriptions.extend(_types)

        return source_type_descriptions

    def collect_funcs(self, data: Dict[str, Any], contract_file: str,
                      contract_name: str, build_arg_contract_file: str,
                      types: List[CT.Type]) -> List[Func]:

        constructor_string = "constructor"

        def get_getter_func_node_from_abi(state_var_name: str) -> Dict[str, Any]:
            abi = data["abi"]
            abi_getter_nodes = [g for g in
                                filter(lambda x: x["type"] == "function" and x["name"] == state_var_name, abi)]

            assert len(abi_getter_nodes) != 0, \
                f"Failed to find a getter function of the state variable {state_var_name} in the ABI"
            assert len(abi_getter_nodes) == 1, \
                f"Found multiple candidates for a getter function of the state variable {state_var_name} in the ABI"

            return abi_getter_nodes[0]

        def collect_array_type_from_abi_rec(type_str: str, dims: List[int]) -> str:
            outer_dim = re.findall(r"\[\d*]$", type_str)
            if outer_dim:
                type_rstrip_dim = re.sub(r"\[\d*]$", '', type_str)
                if len(outer_dim[0]) == 2:
                    dims.append(-1)  # dynamic array
                else:
                    assert len(outer_dim[0]) > 2, f"Expected to find a fixed-size array, but found {type_str}"
                    dims.append(int(re.findall(r"\d+", outer_dim[0])[0]))
                return collect_array_type_from_abi_rec(type_rstrip_dim, dims)
            return type_str

        # Returns (list of array dimensions' lengths, the base type of the array)
        def collect_array_type_from_abi(type_str: str) -> Tuple[List[int], str]:
            dims = []  # type: List[int]
            base_type = collect_array_type_from_abi_rec(type_str, dims)
            return dims, base_type

        # Gets the CT.TypeInstance of a function parameter (either input or output) from the ABI
        def get_solidity_type_from_abi(abi_param_entry: Dict[str, Any]) -> CT.TypeInstance:
            assert "type" in abi_param_entry, f"Invalid ABI function parameter entry: {abi_param_entry}"
            array_dims, base_type = collect_array_type_from_abi(abi_param_entry["type"])

            internal_type_exists = "internalType" in abi_param_entry
            if internal_type_exists:
                array_dims_internal, internal_base_type = collect_array_type_from_abi(abi_param_entry["internalType"])
                assert array_dims_internal == array_dims
                user_defined_type_matches = [type for type in types if type.type_string == internal_base_type]
                if len(user_defined_type_matches) == 0:
                    # the "internal" type is often the same as the "external"
                    # TODO: we should probably just stop grabbing stuff from the abi json
                    user_defined_type = CT.TypeInstance(CT.Type.from_primitive_name(base_type))
                else:
                    user_defined_type = CT.TypeInstance(user_defined_type_matches[0])  # TODO: error on multiple matches
            else:
                user_defined_type = CT.TypeInstance(CT.Type.from_primitive_name(base_type))

            return user_defined_type

        def get_func_def_nodes_by_visibility(contract_file_ast: Dict[int, Any],
                                             visibility_modifiers: List[str]) -> List[Dict[str, Any]]:
            fun_defs_in_file = [contract_file_ast[node_id] for node_id in filter(
                lambda node_id: "nodeType" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["nodeType"] == "FunctionDefinition" and
                                (("kind" in contract_file_ast[node_id] and
                                  (contract_file_ast[node_id]["kind"] == "function" or contract_file_ast[node_id][
                                      "kind"] == constructor_string)) or
                                 ("isConstructor" in contract_file_ast[node_id] and
                                  contract_file_ast[node_id]["isConstructor"] is False and
                                  "name" in contract_file_ast[node_id] and
                                  contract_file_ast[node_id]["name"] != "")) and  # Not the fallback function (< solc6)
                                "visibility" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["visibility"] in visibility_modifiers, contract_file_ast)]

            assert all(self.CERTORA_CONTRACT_NAME() in fd for fd in fun_defs_in_file)

            fun_defs_in_given_contract = [fd for fd in fun_defs_in_file if fd[self.CERTORA_CONTRACT_NAME()] == c_name]
            return fun_defs_in_given_contract

        def get_func_def_nodes(contract_file_ast: Dict[int, Any]) -> List[Dict[str, Any]]:
            return get_func_def_nodes_by_visibility(contract_file_ast, ["public", "external", "private", "internal"])

        def get_public_state_var_def_nodes(contract_file_ast: Dict[int, Any]) -> List[Dict[str, Any]]:
            public_var_defs_in_file = [contract_file_ast[node_id] for node_id in filter(
                lambda node_id: "nodeType" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["nodeType"] == "VariableDeclaration" and
                                "visibility" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["visibility"] == "public" and
                                "stateVariable" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["stateVariable"] is True, contract_file_ast)]

            assert all(self.CERTORA_CONTRACT_NAME() in vd for vd in public_var_defs_in_file)

            var_defs_in_given_contract = [vd for vd in public_var_defs_in_file if
                                          vd[self.CERTORA_CONTRACT_NAME()] == c_name]
            return var_defs_in_given_contract

        def get_function_selector(f_entry: Dict[str, Any], f_name: str,
                                  input_types: List[CT.TypeInstance], is_lib: bool,
                                  smart_contract_lang: CompilerLang) -> str:
            if "functionSelector" in f_entry:
                return f_entry["functionSelector"]

            f_base = Func.compute_signature(f_name, input_types, lambda x: x.get_abi_canonical_string(is_lib))

            assert f_base in data["evm"]["methodIdentifiers"], \
                f"Was about to compute the sighash of {f_name} based on the signature {f_base}.\n" \
                f"Expected this signature to appear in \"methodIdentifiers\"."

            f_hash = keccak.new(digest_bits=256)
            f_hash.update(str.encode(f_base))

            result = f_hash.hexdigest()[0:8]
            expected_result = data["evm"]["methodIdentifiers"][f_base]

            assert expected_result == smart_contract_lang.normalize_func_hash(result), \
                f"Computed the sighash {result} of {f_name} based on a (presumably) correct signature ({f_base}), " \
                f"but got an incorrect result. Expected result: {expected_result}"

            return result

        def get_solidity_type_from_ast_param(p: Dict[str, Any]) -> CT.TypeInstance:
            assert "typeName" in p, f"Expected a \"typeName\" key, but got {p}"

            type_description = CT.Type.from_type_name_node(
                lambda ref: self.get_original_def_node(build_arg_contract_file, ref),
                lambda ref: self.get_contract_file_of_non_autofinder(build_arg_contract_file, ref),
                p["typeName"])

            # TODO:
            # I tried these assertions, I'm not sure any of them have passed, eventually I will investigate to make sure
            # we get default locations right
            # assert not is_default_ref or isinstance(type_description, PrimitiveType)\
            #        or isinstance(type_description, EnumType) or isinstance(type_description, StructType)\
            #        or isinstance(type_description, UserDefinedValueType)
            #
            # assert is_default_ref or is_memory_ref or is_calldata_ref or is_storage_ref
            #
            # assert is_default_ref or isinstance(type_description, MappingType)\
            #        or isinstance(type_description, ArrayType)
            return CT.TypeInstance(type_description, p["storageLocation"])

        def is_constructor_func(name: str) -> bool:
            # Turns out constructor is a function with no name
            return name == ""

        funcs = list()
        collected_func_selectors = set()
        base_contract_files = self.retrieve_base_contracts_list(
            build_arg_contract_file,
            contract_file,
            contract_name)  # type: List[Tuple[str, str, bool]]
        ast_logger.debug(
            f"build arg contract file {build_arg_contract_file} and base contract files {base_contract_files}")
        for c_file, c_name, c_is_lib in base_contract_files:
            if c_is_lib:
                ast_logger.debug(f"{c_name} is a library")
            for func_def in get_func_def_nodes(self.asts[build_arg_contract_file][c_file]):
                func_name = func_def["name"]
                func_visibility = func_def["visibility"]
                params = [p for p in func_def["parameters"]["parameters"]]
                solidity_type_args = [get_solidity_type_from_ast_param(p) for p in params]
                is_constructor = is_constructor_func(func_name)

                if not is_constructor and func_visibility in ["public", "external"]:
                    func_selector = get_function_selector(func_def, func_name, solidity_type_args,
                                                          c_is_lib, CompilerLangSol())
                    if func_selector in collected_func_selectors:
                        continue
                    collected_func_selectors.add(func_selector)
                else:
                    # TODO: calculate func_selector for internal functions?
                    func_selector = "0"  # constructor doesn't have calldata (!!) so it doesn't really matter what
                    # we put here

                if is_constructor:
                    func_name = CertoraBuildGenerator.CONSTRUCTOR_STRING

                # Refer to https://github.com/OpenZeppelin/solidity-ast/blob/master/schema.json for more info
                return_params = func_def["returnParameters"]["parameters"]
                solidity_type_outs = [get_solidity_type_from_ast_param(p) for p in return_params]

                body_node = func_def.get("body")
                where_tuple: Optional[Tuple[str, str]] = None
                if body_node is not None and body_node["nodeType"] == "Block":
                    ast_logger.debug(f'Found location of body of {func_name} at {body_node["src"]} in {c_file}')
                    where_tuple = (c_file, body_node["src"])
                elif body_node is None and func_def["implemented"]:
                    ast_logger.debug(f"No body for {func_def} but ast claims it is implemented")

                func = Func(
                    func_name,
                    solidity_type_args,
                    [p["name"] for p in params],
                    solidity_type_outs,
                    func_selector,
                    func_def[STATEMUT] in ["nonpayable", "view", "pure"],
                    c_is_lib,
                    is_constructor,
                    func_def[STATEMUT],
                    func_visibility,
                    func_def["implemented"],
                    func_def.get("overrides", None) is not None,
                    ast_id=func_def.get("id", None),
                    where=where_tuple
                )

                ast_logger.debug(f"Looking at Function {func}")

                # TODO: make some notion of contract equality (it *is* possible that two contracts with the
                #       same name but used separately could exist right?
                # Add to the current contract all public/external functions, and internal/private ones if
                # this is the declaring contract.
                if func_visibility in ("public", "external") or (c_name == contract_name):
                    funcs.append(func)
                    ast_logger.debug(f"Function {func.source_code_signature()} added")

            # Add automatically generated getter functions for public state variables.
            for public_state_var in get_public_state_var_def_nodes(self.asts[build_arg_contract_file][c_file]):
                getter_name = public_state_var["name"]
                ast_logger.debug(f"Getter {getter_name} automatically generated")
                getter_abi_data = get_getter_func_node_from_abi(getter_name)
                var_type = get_solidity_type_from_ast_param(public_state_var)
                solidity_type_args, solidity_type_outs = Func.compute_getter_signature(var_type)
                getter_selector = get_function_selector(public_state_var, getter_name, solidity_type_args,
                                                        c_is_lib, CompilerLangSol())
                if getter_selector in collected_func_selectors:
                    continue
                collected_func_selectors.add(getter_selector)

                if "payable" not in getter_abi_data:
                    is_not_payable = False
                else:  # Only if something is definitely non-payable, we treat it as such
                    is_not_payable = not getter_abi_data["payable"]

                if STATEMUT not in getter_abi_data:
                    state_mutability = "nonpayable"
                else:
                    state_mutability = getter_abi_data[STATEMUT]
                    # in solc6 there is no json field "payable", so we infer that if state_mutability is view
                    # or pure, then we're also non-payable by definition
                    # (state_mutability is also a newer field)
                    if not is_not_payable and state_mutability in ["view", "pure", "nonpayable"]:
                        is_not_payable = True  # definitely not payable

                funcs.append(
                    Func(
                        name=getter_name,
                        fullArgs=solidity_type_args,
                        paramNames=[],
                        returns=solidity_type_outs,
                        sighash=getter_selector,
                        notpayable=is_not_payable,
                        fromLib=c_is_lib,
                        isConstructor=False,
                        stateMutability=state_mutability,
                        implemented=True,
                        overrides=public_state_var.get("overrides", None) is not None,
                        # according to Solidity docs, getter functions have external visibility
                        visibility="external",
                        ast_id=None)
                )
                ast_logger.debug(f"Added an automatically generated getter function for {getter_name}")

        def verify_collected_all_abi_funcs(
            abi_funcs: List[Dict[str, Any]], collected_funcs: List[Func], is_lib: bool
        ) -> None:
            for fabi in abi_funcs:
                # check that we collected at least one function with the same name as the ABI function
                fs = [f for f in collected_funcs if f.name == fabi["name"]]
                assert fs, f"{fabi['name']} is in the ABI but wasn't collected"

                # check that at least one of the functions has the correct number of arguments
                fs = [f for f in fs if len(f.fullArgs) == len(fabi["inputs"])]
                assert fs, \
                    f"no collected func with name {fabi['name']} has the same \
                        amount of arguments as the ABI function of that name"

                # check that there is exactly one collected function with the same argument types as the ABI function
                def compareTypes(ct_type: CT.Type, i: Dict[str, Any]) -> bool:
                    def get_type(i: Dict[str, Any]) -> bool:
                        return i["internalType"] if "internalType" in i else i["type"]

                    solc_type = get_type(i)
                    ret = ct_type.type_string == solc_type
                    if not ret:
                        # The representation in the abi changed at some point, so hack up something that will pass
                        # for both older and newer solc versions
                        if isinstance(ct_type, CT.ContractType):
                            ret = solc_type == "address"
                        elif isinstance(ct_type, CT.StructType):
                            ret = solc_type == "tuple"
                    return ret

                fs = [f for f in fs if all(compareTypes(a.type, i)
                                           for a, i in zip(f.fullArgs, fabi["inputs"]))]
                assert fs, \
                    f"no collected func with name {fabi['name']} has the same \
                        types of arguments as the ABI function of that name"

                if len(fs) > 1:
                    assert is_lib, "Collected too many functions with the same ABI specification (non-library)"
                    # if a function is in a library and its first argument is of storage, then it’s not ABI.
                    fs = [f for f in fs if f.fullArgs[0].location != CT.TypeLocation.STORAGE]
                    assert len(fs) == 1, "Collected too many (library) functions with the same ABI specification"

                # At this point we are certain we have just one candidate. Let's do some sanity checks also
                # on the return values
                f = fs[0]
                assert len(f.returns) == len(fabi["outputs"]), \
                    f"function collected for {fabi['name']} has the wrong number of return values"
                assert all(compareTypes(a.type, i) for a, i in zip(f.returns, fabi["outputs"])), \
                    f"function collected for {fabi['name']} has the wrong types of return values"

        verify_collected_all_abi_funcs(
            [f for f in data["abi"] if f["type"] == "function"],
            [f for f in funcs if f.visibility in ("external", "public") and f.name != "constructor"],
            c_is_lib
        )

        return funcs

    def retrieve_imported_files(self, build_arg_source_code_file: str, contract_file: str) -> Set[str]:
        """
        Gets all files that are imported, directly or indirectly, by the contract's source code
        """
        seen = set()  # type: Set[str]
        worklist = [contract_file]
        while worklist:
            curr = worklist.pop()
            if curr not in seen:
                if build_arg_source_code_file not in self.asts:
                    build_logger.debug(f"Failed to find contract file {build_arg_source_code_file} in"
                                       f" {self.asts.keys()}")
                if curr not in self.asts[build_arg_source_code_file]:
                    build_logger.debug(f"Failed to find curr {curr} in {self.asts[build_arg_source_code_file].keys()}")
                curr_ast = self.asts[build_arg_source_code_file][curr]

                # absolute path as key into self.asts[f][key]?
                imports = [curr_ast[node_id]["absolutePath"] for node_id in curr_ast if
                           Nf.is_import(curr_ast[node_id])]
                # those paths can come with node_modules//somepath instead of node_modules/somepath
                # ...
                imports = [Util.normalize_double_paths(import_node) for import_node in imports]
                worklist.extend(imports)
                seen.add(curr)
        return seen

    def retrieve_base_contracts_list(self, build_arg_contract_file: str, contract_file: str,
                                     contract_name: str) -> List[Tuple[str, str, bool]]:
        """
        For each base contract, returns (base_contract_file, base_contract_name, is_library)
        @param build_arg_contract_file: input arg, contract file we want to work on
        @param contract_file: full path of contract file we want to work on
        @param contract_name: contract name without the extension
        @return: List of (base_contract_file, base_contract_name, is_library)

        NB the only member of the list for which is_library should be true should be [contract_file] (libraries can
           never be base contracts, even of other libraries, but since this list includes [contract_file] then up
           to one member of the "base contracts" may be a library
        """
        if get_compiler_lang(contract_file) == CompilerLangVy():
            return [(contract_file, contract_name, False)]

        def retrieve_base_contracts_list_rec(base_contracts_queue: List[Any],
                                             base_contracts_lst: List[Tuple[str, str, bool]]) -> None:
            (curr_contract_file, curr_contract_def_node_ref) = base_contracts_queue.pop()
            curr_contract_def = self.asts[build_arg_contract_file][curr_contract_file][curr_contract_def_node_ref]
            assert "baseContracts" in curr_contract_def, \
                f'Got a "ContractDefinition" ast node without a "baseContracts" key: {curr_contract_def}'
            for bc in curr_contract_def["baseContracts"]:
                assert "nodeType" in bc and bc["nodeType"] == "InheritanceSpecifier"
                assert "baseName" in bc and "referencedDeclaration" in bc["baseName"]
                next_bc_ref = bc["baseName"]["referencedDeclaration"]
                next_bc = self.get_contract_file_of(build_arg_contract_file, next_bc_ref)
                if next_bc not in base_contracts_lst:
                    base_contracts_lst.append(
                        (next_bc, self.asts[build_arg_contract_file][next_bc][next_bc_ref]["name"],
                         self.is_library_def_node(next_bc, next_bc_ref, build_arg_contract_file)))
                    base_contracts_queue.insert(0, (next_bc, bc["baseName"]["referencedDeclaration"]))

            if base_contracts_queue:
                retrieve_base_contracts_list_rec(base_contracts_queue, base_contracts_lst)

        contract_def_node_ref = self.get_contract_def_node_ref(build_arg_contract_file, contract_file, contract_name)
        base_contracts_queue = [(contract_file, contract_def_node_ref)]
        base_contracts_lst = [
            (contract_file, contract_name,
             self.is_library_def_node(contract_file, contract_def_node_ref, build_arg_contract_file))]
        retrieve_base_contracts_list_rec(base_contracts_queue, base_contracts_lst)

        # note the following assumption (as documented above), we turn it off because asserts in the python script
        # are scary
        # assert all([not is_lib or contract_name == c_name for _, c_name, is_lib in
        #             base_contracts_lst]), f'found a library in base_contracts_list {base_contracts_lst} ' \
        #                                   f'for contract {contract_name}'
        return base_contracts_lst

    # used by Equivalence Check
    def collect_func_source_code_signatures_source(self, contract_file: Path,
                                                   contract_name: str, solc: str) -> List[FunctionSig]:
        """
        returns a list of signatures for external or public functions in a given contract.
        This method is currently only used in the context of certoraEqCheck.
        @param contract_file: relative path to the file containing the targeted contract
        @param contract_name: name of the target contract
        @param solc: name of solc executable used to compile target contract
        @return: List of str containing the function signature (a tuple representing
          function name, inputs, outputs, stateMutability) for each contract
        """
        func_signatures = []
        file_abs_path = Path(self.to_autofinder_file(str(contract_file))).resolve()
        if file_abs_path.suffix == VY:
            smart_contract_lang: CompilerLang = CompilerLangVy()
            sdc_name = self.file_to_sdc_name[Path(contract_file).resolve()]
            standard_json_data = self.get_standard_json_data(sdc_name, smart_contract_lang)
            abi = standard_json_data[CONTRACTS][str(Path(contract_file).resolve())][contract_name]['abi']
            ast_logger.debug(f"abi is: \n{abi}")
            for f in filter(lambda x: self.is_imported_abi_entry(x), abi):
                func_signature = self.get_full_func_signature(f)
                ast_logger.debug(f"Collected function signature {func_signature} from ABI")
                func_signatures.append(func_signature)
            return func_signatures
        elif file_abs_path.suffix == SOL:
            smart_contract_lang = CompilerLangSol()
            sdc_name = self.file_to_sdc_name[file_abs_path]
            compilation_path = self.get_compilation_path(sdc_name)
            standard_json_data = self.get_standard_json_data(sdc_name, smart_contract_lang)
            storage_data = smart_contract_lang.collect_storage_layout_info(str(file_abs_path), compilation_path,
                                                                           solc, None,
                                                                           standard_json_data)
            abi = storage_data[CONTRACTS][str(file_abs_path)][contract_name]["abi"]
            ast_logger.debug(f"abi is: \n{abi}")
            for f in filter(lambda x: self.is_imported_abi_entry(x), abi):
                func_signature = self.get_full_func_signature(f)
                ast_logger.debug(f"Collected function signature {func_signature} from ABI")
                func_signatures.append(func_signature)
            return func_signatures
        else:
            raise Util.CertoraUserInputError(
                f'May only collect functions from Solidity/Vyper files: {file_abs_path} received.')

    @staticmethod
    def get_func_args_output_types(inputs_or_outputs: Any) -> List[str]:
        """
        A Helper to create a list of the types for all inputs/return values of a function.
        So if `get_func_args_output_types` gets this as input:
           `[{'internalType': 'uint256', 'name': 'a', 'type': 'uint256'},
           {'internalType': 'uint256', 'name': 'b', 'type': 'uint256'}]`
        it wil produce:
           `['uint256', 'uint256']`.
        :param inputs_or_outputs: a list of function arguments (or return values) and their types.
        :return: returns a list of the types of the inputs/return values of a function.
        """
        return [input_or_output[INTERNALTYPE] if INTERNALTYPE in input_or_output else input_or_output[TYPE] for
                input_or_output in inputs_or_outputs]

    @staticmethod
    def get_full_func_signature(f: Dict[str, Any]) -> FunctionSig:
        """
        grabs function name, inputs, outputs, stateMutability
        """
        name = CertoraBuildGenerator.get_abi_entry_name(f)
        func_inputs = CertoraBuildGenerator.get_func_args_output_types(f[INPUTS])
        func_outputs = CertoraBuildGenerator.get_func_args_output_types(f[OUTPUTS])
        mutability = f[STATEMUT]
        func_signature = (name, func_inputs, func_outputs, mutability)
        return func_signature

    @staticmethod
    def get_abi_entry_name(x: Dict[str, Any]) -> str:
        if x[TYPE] == FUNCTION:
            return x["name"]
        elif x[TYPE] == CertoraBuildGenerator.CONSTRUCTOR_STRING:
            return CertoraBuildGenerator.CONSTRUCTOR_STRING
        else:
            raise Exception("Abi entry name can either be a function name or a constructor.")  # Should be unreachable

    @staticmethod
    def get_func_signature(f: Dict[str, Any]) -> str:
        name = CertoraBuildGenerator.get_abi_entry_name(f)
        func_inputs = CertoraBuildGenerator.get_func_args_output_types(f[INPUTS])
        func_signature = f"{name}({','.join(func_inputs)})"
        return func_signature

    @staticmethod
    def is_imported_abi_entry(x: Dict[str, Any]) -> bool:
        return x[TYPE] == FUNCTION or x[TYPE] == CertoraBuildGenerator.CONSTRUCTOR_STRING

    @staticmethod
    def collect_srcmap(data: Dict[str, Any]) -> Any:
        # no source map object in vyper
        return (data["evm"]["deployedBytecode"].get("sourceMap", ""),
                data["evm"]["bytecode"].get("sourceMap", ""))

    @staticmethod
    def collect_varmap(contract: str, data: Dict[str, Any]) -> Any:
        return data[CONTRACTS][contract]["local-mappings"]

    @staticmethod
    def collect_storage_layout(data: Dict[str, Any]) -> Any:
        return data.get("storageLayout", None)

    # Cache info - on PackingTest there are 514 hits and 34 misses
    @lru_cache(maxsize=128)
    def get_contract_def_node_ref(self, build_arg_contract_file: str, contract_file: str, contract_name: str) -> int:
        """
        Extracts the proper AST from self, based on the [build_arg_contract_file] and the
        [contract_file] files, than invokes [get_contract_def_node_ref_func] to get the definition
        node's reference.
        """
        compiler_lang = get_compiler_lang(build_arg_contract_file)
        contract_file_ast = self.asts[build_arg_contract_file][contract_file]
        return compiler_lang.get_contract_def_node_ref(contract_file_ast, contract_file, contract_name)

    def collect_contract_bytes(self, contract_file: str, contract_name: str,
                               build_arg_contract_file: str) -> Tuple[int, int]:
        ref = self.get_contract_def_node_ref(build_arg_contract_file, contract_file, contract_name)
        node = self.asts[build_arg_contract_file][contract_file][ref]
        src_info = node["src"]
        start, length = src_info.split(":")[0:2]
        return int(start), int(length)

    def get_standard_json_data(self, sdc_name: str, smart_contract_lang: CompilerLang) -> Dict[str, Any]:
        json_file = smart_contract_lang.compilation_output_path(sdc_name, self.config_path)
        process_logger.debug(f"reading standard json data from {json_file}")
        # jira CER_927 - under windows it happens the solc generate wrong
        # path names, we convert them here to posix format.
        json_dict = Util.read_json_file(json_file)
        entries = [CONTRACTS, "sources"]
        for ent in entries:
            convert_pathname_to_posix(json_dict, ent, smart_contract_lang)
        return json_dict

    def cleanup_compiler_outputs(self, sdc_name: str, smart_contract_lang: CompilerLang) -> None:
        for compilation_artifact in smart_contract_lang.all_compilation_artifacts(sdc_name, self.config_path):
            Util.remove_file(compilation_artifact)

    def backup_compiler_outputs(self, sdc_name: str, smart_contract_lang: CompilerLang, tag: str) -> None:
        for compilation_artifact in smart_contract_lang.all_compilation_artifacts(sdc_name, self.config_path):
            if compilation_artifact.exists():
                shutil.copy(compilation_artifact, f"{str(compilation_artifact)}.{tag}")

    @staticmethod
    def address_as_str(address: int) -> str:
        """
        Returns a 40 digits long hexadecimal string representation of address, filled by leading zeros
        """
        return "%0.40x" % address

    def find_contract_address_str(self, contract_file: str, contract_name: str,
                                  contracts_with_chosen_addresses: List[Tuple[int, Any]]) -> str:
        address_and_contracts = [e for e in contracts_with_chosen_addresses
                                 if e[1] == f"{contract_file}:{contract_name}"]
        if len(address_and_contracts) == 0:
            msg = f"Failed to find a contract named {contract_name} in file {contract_file}. " \
                  f"Please make sure there is a file named like the contract, " \
                  f"or a file containing a contract with this name. Available contracts: " \
                  f"{','.join(map(lambda x: x[1], contracts_with_chosen_addresses))}"
            raise Util.CertoraUserInputError(msg)
        address_and_contract = address_and_contracts[0]
        address = address_and_contract[0]
        contract = address_and_contract[1].split(":")[1]

        ast_logger.debug(f"Custom addresses: {self.input_config.address}, looking for a match of "
                         f"{address_and_contract} from {contract_name} in {self.input_config.address.keys()}")
        if contract_name in self.input_config.address.keys():
            address = self.input_config.address[contract_name]
            address = int(str(address), 0)
        ast_logger.debug(f"Candidate address for {contract} is {address}")
        # Can't have more than one! Otherwise we will have conflicting same address for different contracts
        assert len(set(address_and_contracts)) == 1
        return self.address_as_str(address)

    def collect_and_link_bytecode(self,
                                  contract_name: str,
                                  contracts_with_chosen_addresses: List[Tuple[int, Any]],
                                  bytecode: str,
                                  links: Dict[str, Any]
                                  ) -> str:
        build_logger.debug(f"Working on contract {contract_name}")
        for address, _contract_name in contracts_with_chosen_addresses:
            if _contract_name == contract_name:
                build_logger.debug("Chosen address for %s is 0x%X" % (contract_name, address))
                break

        if links:
            # links are provided by solc as a map file -> contract -> (length, start)
            # flip the links from the "where" to the chosen contract address (based on file:contract).
            linked_bytecode = bytecode
            replacements = {}
            for link_file in links:
                for link_contract in links[link_file]:
                    for where in links[link_file][link_contract]:
                        replacements[where["start"]] = {"length": where["length"],
                                                        "address": self.find_contract_address_str(
                                                            link_file,
                                                            link_contract,
                                                            contracts_with_chosen_addresses)
                                                        }
            build_logger.debug(f"Replacements= {replacements}")
            where_list = list(replacements.keys())
            where_list.sort()
            where_list.reverse()
            for where in where_list:
                offset = where * 2
                length = replacements[where]["length"] * 2
                addr = replacements[where]["address"]
                build_logger.debug(f"replacing in {offset} of len {length} with {addr}")
                # is this *definitely* a push? then use our special "library link" opcode 5c, which is unused
                if linked_bytecode[offset - 2:offset] == "73":
                    linked_bytecode = f"{linked_bytecode[:offset - 2]}5c{addr}{linked_bytecode[(offset + length):]}"
                else:
                    linked_bytecode = f"{linked_bytecode[0:offset]}{addr}{linked_bytecode[(offset + length):]}"
                self.library_addresses.append(addr)
            return linked_bytecode

        return bytecode

    def _handle_optimize(self, contract_file_path: str, settings_dict: Dict[str, Any]) -> None:
        """
        @param contract_file_path: the contract that we are working on
        @param settings_dict: data structure for sending to the solc compiler
        """
        if self.context.solc_optimize_map:
            match = Util.match_path_to_mapping_key(Path(contract_file_path), self.context.solc_optimize_map)
            if match and int(match) > 0:
                settings_dict["optimizer"] = {"enabled": True}
                settings_dict["optimizer"]['runs'] = int(match)
        elif self.context.solc_optimize:
            settings_dict["optimizer"] = {"enabled": True}
            if int(self.context.solc_optimize) > 0:
                settings_dict["optimizer"]['runs'] = int(self.context.solc_optimize)

    def standard_json(self,
                      contract_file_posix_abs: Path,
                      contract_file_as_provided: str,
                      remappings: List[str],
                      compiler_collector_lang: CompilerLang) -> Dict[str, Any]:
        """
        when calling solc with the standard_json api, instead of passing it flags, we pass it json to request what we
        want -- currently we only use this to retrieve storage layout as this is the only way to do that,
        it would probably be good to migrate entirely to this API.
        @param contract_file_posix_abs: the absolute posix path of the file the user provided
        @param contract_file_as_provided: the file we are looking at as provided by the user
        @param remappings: package remappings for import resolution
        @param compiler_collector_lang: Solidity or Vyper
        @return:
        """
        if compiler_collector_lang == CompilerLangSol():
            sources_dict = {str(contract_file_posix_abs): {
                "urls": [str(contract_file_posix_abs)]}}  # type: Dict[str, Dict[str, Any]]
            output_selection = ["storageLayout", "abi", "evm.bytecode", "evm.deployedBytecode", "evm.methodIdentifiers",
                                "evm.assembly"]
            ast_selection = ["id", "ast"]
        elif compiler_collector_lang == CompilerLangVy():
            with open(contract_file_posix_abs) as f:
                contents = f.read()
                sources_dict = {str(contract_file_posix_abs): {"content": contents}}
                output_selection = ["abi", "evm.bytecode", "evm.deployedBytecode", "evm.methodIdentifiers"]
                ast_selection = ["ast"]

        settings_dict: Dict[str, Any] = \
            {
                "remappings": remappings,
                "outputSelection": {
                    "*": {
                        "*": output_selection,
                        "": ast_selection
                    }
                }
            }

        if self.context.solc_via_ir:
            settings_dict["viaIR"] = True
        if self.context.solc_evm_version is not None:
            settings_dict["evmVersion"] = self.context.solc_evm_version
        self._handle_optimize(contract_file_as_provided, settings_dict)

        if self.context.solc_optimize is not None:
            settings_dict["optimizer"] = {"enabled": True}
            if int(self.context.solc_optimize) > 0:
                settings_dict["optimizer"]['runs'] = int(self.context.solc_optimize)

        result_dict = {"language": compiler_collector_lang.name, "sources": sources_dict, "settings": settings_dict}
        # debug_print("Standard json input")
        # debug_print(json.dumps(result_dict, indent=4))
        return result_dict

    def get_compilation_path(self, sdc_name: str) -> Path:
        return self.config_path / sdc_name

    def build_srclist(self,
                      data: Dict[str, Any],
                      sdc_name: str,
                      smart_contract_lang: CompilerLang) -> Dict[str, Any]:
        """
        Generates lists of sources for the given Single Deployed Contract.
        :param data: data from the json produced by the solidity compiler
        :param sdc_name: name of the "Single Deployed Contract" whose sources we are gathering
        :param smart_contract_lang: the smart-contract-language which we decide by how to copy contract's file to
               compilation path directory
        :return: The source list as seen by solc.
        """
        # srclist - important for parsing source maps
        srclist = {data["sources"][k]["id"]: k for k in data["sources"]}
        ast_logger.debug(f"Source list= {srclist}")

        return srclist

    def collect_asts(self, original_file: str, contract_sources: Dict[str, Dict[str, Any]]) -> None:
        """
        This function fetches the AST provided by solc and flattens it so that each node_id is mapped to a dict object,
        representing the node's contents.

        @param original_file: Path to a file
        @param contract_sources: represents the AST. Every sub-object with an "id" key is an AST node.
                                 The ast object is keyed by the original file for which we invoked solc.
        """

        if original_file.endswith(".vy"):
            contract_definition_type = "Module"
            node_id_attrb = "node_id"
            node_type_attrb = "ast_type"
        else:
            contract_definition_type = "ContractDefinition"
            node_id_attrb = "id"
            node_type_attrb = "nodeType"

        def stamp_value_with_contract_name(popped_dict: Dict[str, Any], curr_value: Any) -> None:
            if isinstance(curr_value, dict):
                if popped_dict[node_type_attrb] == contract_definition_type:
                    assert "name" in popped_dict
                    curr_value[self.CERTORA_CONTRACT_NAME()] = popped_dict["name"]
                elif self.CERTORA_CONTRACT_NAME() in popped_dict:
                    curr_value[self.CERTORA_CONTRACT_NAME()] = popped_dict[self.CERTORA_CONTRACT_NAME()]
            elif isinstance(curr_value, list):
                for node in curr_value:
                    stamp_value_with_contract_name(popped_dict, node)

        self.asts[original_file] = {}
        for c in contract_sources:
            ast_logger.debug(f"Adding ast of {original_file} for {c}")
            container = {}  # type: Dict[int, Any]
            self.asts[original_file][c] = container
            if "ast" not in contract_sources[c]:
                fatal_error(
                    ast_logger,
                    f"Invalid AST format for original file {original_file} - "
                    f"got object that does not contain an \"ast\" {contract_sources[c]}")
            queue = [contract_sources[c]["ast"]]
            while queue:
                pop = queue.pop(0)
                if isinstance(pop, dict) and node_id_attrb in pop:
                    container[int(pop[node_id_attrb])] = pop
                    for key, value in pop.items():
                        if node_type_attrb in pop \
                            and pop[node_type_attrb] == "InlineAssembly" \
                                and key == "externalReferences":
                            continue
                        stamp_value_with_contract_name(pop, value)
                        if isinstance(value, dict):
                            queue.append(value)
                        if isinstance(value, list):
                            queue.extend(value)

    @staticmethod
    def get_node_from_asts(asts: Dict[str, Dict[str, Dict[int, Any]]], original_file: str, node_id: int) -> Any:
        ast_logger.debug(f"Available keys in ASTs: {asts.keys()}")
        ast_logger.debug(f"Available keys in AST of original file: {asts[original_file].keys()}")
        for contract_file in asts[original_file]:
            node = asts[original_file].get(contract_file, {}).get(node_id)
            if node is not None:
                ast_logger.debug(f"In original file {original_file} in contract file {contract_file}, found for node "
                                 f"id {node_id}")
                return node  # Found the ast node of the given node_id
        return {}  # an ast node with the given node_id was not found

    def collect_immutables(self,
                           contract_data: Dict[str, Any],
                           build_arg_contract_file: str
                           ) -> List[ImmutableReference]:
        out = []
        immutable_references = contract_data["evm"]["deployedBytecode"].get("immutableReferences", [])
        # Collect and cache the AST(s). We collect the ASTs of ALL contracts' files that appear in
        # contract_sources; the reason is that a key of an item in immutableReferences
        # is an id of an ast node that may belong to any of those contracts.
        ast_logger.debug(f"Got immutable references in {build_arg_contract_file}: {immutable_references}")
        for astnode_id in immutable_references:
            astnode = self.get_node_from_asts(self.asts, build_arg_contract_file, int(astnode_id))
            name = astnode.get("name", None)
            if name is None:
                fatal_error(
                    ast_logger,
                    f"immutable reference does not point to a valid ast node {astnode} in {build_arg_contract_file}, "
                    f"node id {astnode_id}"
                )

            ast_logger.debug(f"Name of immutable reference is {name}")
            for elem in immutable_references[astnode_id]:
                out.append(ImmutableReference(elem["start"], elem["length"], name))
        return out

    def generate_address(self) -> int:
        address = CertoraBuildGenerator.BASE_ADDRESS * 2 ** 100 + self.address_generator_counter
        # Don't forget for addresses there are only 160 bits
        self.address_generator_counter += 1
        return address

    @staticmethod
    def check_for_errors_and_warnings(data: Dict[str, Any]) -> None:
        if "errors" in data:
            errors_list = data["errors"]
            severe_errors = [e for e in errors_list if "errorCode" in e and
                             e["errorCode"] in CertoraBuildGenerator.SEVERE_COMPILER_WARNINGS]
            if len(severe_errors) > 0:
                for i, e in enumerate(severe_errors):
                    raw_msg = e["formattedMessage"]
                    err_msg = f"Severe compiler warning:\n{raw_msg}\n" \
                              f"Please fix this warning before running the Certora Prover"

                    # We log all the error messages, but only the last one will be in the exception
                    if i < len(severe_errors) - 1:
                        compiler_logger.error(err_msg)
                    else:
                        raise Util.CertoraUserInputError(err_msg)

    def collect_for_file(self,
                         build_arg_contract_file: str,
                         file_index: int,
                         smart_contract_lang: CompilerLang,
                         compile_wd: Path,
                         fail_on_compilation_error: bool = True,
                         route_packages_to_certora_sources: bool = False
                         ) -> List[SDC]:
        """
        Collects [ContractInSDC]s for all the contracts in a given file [build_arg_contract_file],
        by traversing the dependency graph of those contracts.
        @param build_arg_contract_file - the file we are looking at.
        @param file_index - unique index for the file [build_arg_contract_file].
        @param smart_contract_lang - an indicator for which high level language and compiler we work with
        @param fail_on_compilation_error - boolean parameter which indicates what exception is raised in case of
            a compilation error.
        @param route_packages_to_certora_sources - boolean parameter indicating if we need to adjust the path
            of the mappings (package dependencies) in the input and of the main allowed-path to the contracts
            to the one in .certora_sources.
        @param compile_wd - sets the working directory for the Solidity compiler
        @returns list of [SDC]s, each corresponds to a primary contract in [build_arg_contract_file].
        """
        # the contracts in the file we compile
        contracts_in_file = self.input_config.fileToContractName[build_arg_contract_file]
        file_abs_path = Util.abs_posix_path(build_arg_contract_file)
        is_vyper = smart_contract_lang == CompilerLangVy()
        sdc_name = f"{Path(build_arg_contract_file).name}_{file_index}"
        compilation_path = self.get_compilation_path(sdc_name)
        self.file_to_sdc_name[Path(build_arg_contract_file).resolve()] = sdc_name
        # update remappings and collect_cmd:
        if not is_vyper:
            Util.safe_create_dir(compilation_path)
            compiler_ver_to_run = get_relevant_compiler(Path(build_arg_contract_file), self.input_config.solc,
                                                        self.input_config.solc_mappings)
            """
            when we compile with autofinders, we compile from .certora_sources.
            to avoid compilation issues due to conflicting-but-not-really-conflicting imports
            in solc, we can re-route the packages to point to node_modules or whatever other packages_path
            they have in .certora_sources. This is the role of route_func.
            Also note that remappings expect a full absolute path.
            This is not applied to provided_remappings at the moment
            re. E731 - we don't care about the linter wanting a def instead of a lambda here.
            """
            if route_packages_to_certora_sources:
                route_func = lambda p: self.abs_path_relative_to_certora_sources(p)  # noqa: E731
            else:
                route_func = lambda p: p  # noqa: E731
            main_path = route_func(self.input_config.path)

            # ABI and bin-runtime cmds preparation
            if self.input_config.packages is not None:
                remappings = self.input_config.packages
                compiler_logger.debug(f"remappings={remappings}")

                remapping_pairs = list(map(lambda remap: remap.split("="), remappings))
                rerouted_remapping_pairs = list(map(lambda remap: (remap[0], route_func(remap[1])), remapping_pairs))
                paths_for_remappings = list(map(lambda remap: f'"{remap[1]}"', rerouted_remapping_pairs))
                # solc is so annoying! if the remapped path ends with '/' we need the path to have it in the path too
                # otherwise, the package/ part will be replaced by solc with the full path without the '/',
                # leading to "File not found error".
                # We do this only for the remappings map, not for allow-paths.
                rerouted_remapping_pairs = list(
                    map(lambda p: (p[0], f"{p[1]}/" if p[0].endswith("/") else p[1]), rerouted_remapping_pairs))
                remappings = list(map(lambda remap: f'{remap[0]}={remap[1]}', rerouted_remapping_pairs))

                compiler_logger.debug(f"paths_for_remappings={paths_for_remappings}\n")

                join_remappings = ','.join(paths_for_remappings)

                compiler_logger.debug(f"Join remappings: {join_remappings}\n")
                collect_cmd = f'{compiler_ver_to_run} -o "{compilation_path}/" --overwrite ' \
                              f'--allow-paths "{main_path}",{join_remappings},. --standard-json'
            else:
                remappings = []
                collect_cmd = f'{compiler_ver_to_run} -o "{compilation_path}/" --overwrite ' \
                              f'--allow-paths "{main_path}",. --standard-json'
        else:
            compiler_ver_to_run = CompilerCollectorFactory.get_vyper_compiler(Path(build_arg_contract_file),
                                                                              self.input_config.solc,
                                                                              self.input_config.solc_mappings)

            remappings = []
            collect_cmd = f'{compiler_ver_to_run} -p "{self.input_config.path}" -o "{compilation_path}" ' \
                          f'--standard-json'

        # Make sure compilation artifacts are always deleted
        # Unless we're in debug mode, we prefer to exclude the stdout file which is potentially huge
        if not self.context.debug:
            self.__compiled_artifacts_to_clean.add((sdc_name, smart_contract_lang))
        else:
            # in debug mode, we want to keep artifacts. If we recompile the same contract (e.g. autofinders),
            # we want to preserve the previous artifacts too for a comprehensive view
            # (we do not try to save a big chain history of changes, just a previous and current)
            self.backup_compiler_outputs(sdc_name, smart_contract_lang, "prev")

        # Standard JSON
        input_for_solc = self.standard_json(Path(file_abs_path), build_arg_contract_file, remappings,
                                            smart_contract_lang)
        standard_json_input = json.dumps(input_for_solc).encode("utf-8")
        compiler_logger.debug(f"about to run in {compile_wd} the command: {collect_cmd}")
        compiler_logger.debug(f"solc input = {json.dumps(input_for_solc, indent=4)}")

        if self.context.test == str(Util.TestValue.CHECK_SOLC_OPTIONS):
            raise Util.TestResultsReady({'standard_json_input': standard_json_input, 'main_path': main_path})
        Util.run_compiler_cmd(collect_cmd, f"{sdc_name}.standard.json", self.config_path, wd=compile_wd,
                              compiler_input=standard_json_input)

        compiler_logger.debug(f"Collecting standard json: {collect_cmd}")
        standard_json_data = self.get_standard_json_data(sdc_name, smart_contract_lang)

        for error in standard_json_data.get("errors", []):
            # is an error not a warning
            if error.get("severity", None) == "error":
                compiler_logger.debug(f"Error: standard-json invocation of solc encountered an error: {error}")
                friendly_message = f"{compiler_ver_to_run} had an error:\n" \
                                   f"{error['formattedMessage']}"
                if fail_on_compilation_error:
                    raise Util.CertoraUserInputError(friendly_message)
                else:
                    # We get here when we fail compilation on the autofinders.
                    # This is not a user input error because we generated this Solidity code
                    raise Util.SolcCompilationException(friendly_message)

        compiler_collector = self.compiler_coll_factory \
            .get_compiler_collector(Path(self.path_for_compiler_collector_file))

        # load data
        data = \
            smart_contract_lang.collect_storage_layout_info(file_abs_path, compilation_path, compiler_ver_to_run,
                                                            compiler_collector.compiler_version,
                                                            standard_json_data)  # Note we collected for just ONE file
        self.check_for_errors_and_warnings(data)
        self.collect_asts(build_arg_contract_file, data["sources"])

        contracts_with_libraries = {}
        file_compiler_path = smart_contract_lang.normalize_file_compiler_path_name(file_abs_path)

        compiler_collector = self.compiler_coll_factory \
            .get_compiler_collector(Path(self.path_for_compiler_collector_file))

        # But apparently this heavily depends on the Solidity AST format anyway

        # Need to add all library dependencies that are in a different file:
        seen_link_refs = {Path(file_compiler_path)}
        contracts_to_add_dependencies_queue = [Path(file_compiler_path)]
        resolved_to_orig: Dict[str, str] = {}
        build_logger.debug(f"collecting worklist for {file_compiler_path}")
        while contracts_to_add_dependencies_queue:
            contract_file_obj = contracts_to_add_dependencies_queue.pop()
            contract_file = str(contract_file_obj)
            build_logger.debug(f"Processing dependencies from file {contract_file}")
            # make sure path name is in posix format.
            contract_file_abs = Path(contract_file).resolve().as_posix()
            # using os.path.relpath because Path.relative_to cannot go up the directory tree (no ..)
            contract_file_rel = os.path.relpath(Path(contract_file_abs), Path.cwd())

            build_logger.debug(f"available keys: {data['contracts'].keys()}")
            if contract_file_rel in data[CONTRACTS]:
                contract_file = contract_file_rel
                unsorted_contract_list = data[CONTRACTS][contract_file]
            elif contract_file_abs in data[CONTRACTS]:
                contract_file = contract_file_abs
                unsorted_contract_list = data[CONTRACTS][contract_file_abs]
            elif contract_file in data[CONTRACTS]:
                # when does this happen? Saw this in TrustToken on a package source file
                unsorted_contract_list = data[CONTRACTS][contract_file]
            elif resolved_to_orig.get(contract_file) in data[CONTRACTS]:
                unsorted_contract_list = data[CONTRACTS][resolved_to_orig[contract_file]]
                contract_file = resolved_to_orig[contract_file]
            else:
                # our file may be a symlink!
                raise Exception(
                    f"Worklist contains {contract_file} (relative {contract_file_rel}, "
                    f"absolute {contract_file_abs}), resolved from {resolved_to_orig.get(contract_file)} "
                    f"that does not exist in contract set {resolved_to_orig.get(contract_file) in data['contracts']}")

            contract_list = sorted([c for c in unsorted_contract_list])
            # every contract file may contain numerous primary contracts, but the dependent contracts
            # are the same for all primary contracts in a file
            contracts_with_libraries[contract_file] = contract_list

            if not is_vyper:
                for contract_name in contract_list:
                    # Collecting relevant Solidity files to work on: base, libraries externally called
                    # and libraries internally called
                    base_contracts = sorted(self.retrieve_base_contracts_list(build_arg_contract_file, contract_file,
                                                                              contract_name), key=lambda x: x[0])
                    for c_file, _, _ in base_contracts:
                        norm_c_file = Path(c_file).resolve()
                        resolved_to_orig[str(norm_c_file)] = c_file
                        if norm_c_file not in seen_link_refs:
                            build_logger.debug(f"Adding a base contract link ref {norm_c_file} to worklist")
                            contracts_to_add_dependencies_queue.append(norm_c_file)
                            seen_link_refs.add(norm_c_file)

                    compiler_logger.debug(f"base contracts {base_contracts}")
                    contract_object = data[CONTRACTS][contract_file][contract_name]
                    lib_link_refs = sorted(contract_object["evm"]["deployedBytecode"]["linkReferences"])
                    for lib_link_ref in lib_link_refs:  # linkReference is a library reference
                        norm_link_ref = Path(lib_link_ref).resolve()
                        resolved_to_orig[str(norm_link_ref)] = lib_link_ref
                        if norm_link_ref not in seen_link_refs:
                            build_logger.debug(f"Adding library link ref {norm_link_ref} to worklist")
                            contracts_to_add_dependencies_queue.append(norm_link_ref)
                            seen_link_refs.add(norm_link_ref)

                    # we're also adding libraries that are referenced by internal functions, not just delegations
                    internal_refs = self.get_libraries_referenced_with_internal_functions(build_arg_contract_file,
                                                                                          contract_file, contract_name)
                    for ref in sorted(set(internal_refs)):
                        # Save absolute paths.
                        # There may be confusion as to whether solidity's json output uses
                        # absolute or relative paths
                        # turns out, it can be neither.
                        # The resolving here can ruin us if the entries we get are symlinks.
                        contract_refs = [c_file for c_file in
                                         data[CONTRACTS].keys() if
                                         ref in data[CONTRACTS][c_file].keys()]
                        contract_files_resolved = sorted([Path(x).resolve() for x in
                                                          contract_refs])

                        # There may be two non unique paths but actually referring to the same absolute path.
                        # Normalizing as absolute
                        if len(set(contract_files_resolved)) != 1:
                            build_logger.debug(f'Unexpectedly there are either 0 or multiple unique paths for the same'
                                               f' contract or library name, skipping adding link references: '
                                               f'{ref}, {contract_files_resolved}')
                        else:
                            # let's take the original ref. we know it's in data[CONTRACTS]
                            internal_link_ref = contract_files_resolved[0]
                            # we keep the original to handle symlinks
                            resolved_to_orig[str(internal_link_ref)] = contract_refs[0]
                            if internal_link_ref not in seen_link_refs:
                                build_logger.debug(f"Adding internal link ref {internal_link_ref} to worklist")
                                contracts_to_add_dependencies_queue.append(internal_link_ref)
                                seen_link_refs.add(internal_link_ref)

        build_logger.debug(
            f"Contracts in {sdc_name} (file {build_arg_contract_file}): "
            f"{contracts_with_libraries.get(file_compiler_path, None)}")
        contracts_with_chosen_addresses = \
            [(self.generate_address(), f"{contract_file}:{contract_name}") for contract_file, contract_list in
             sorted(contracts_with_libraries.items(), key=lambda entry: entry[0]) for contract_name in
             contract_list]  # type: List[Tuple[int, Any]]

        build_logger.debug(f"Contracts with their chosen addresses: {contracts_with_chosen_addresses}")
        sdc_lst_to_return = []
        srclist = self.build_srclist(data, sdc_name, smart_contract_lang)
        # if certora_sources directory exists, we can resolve report_srclist
        # what is report_srclist? It is the list based on which we will resolve srcmaps
        # in the Prover jar. Before the jar is invoked it must be resolved relatively
        # to .certora_sources to make sure it's accessible
        if Util.get_certora_sources_dir().exists():
            # how was this source path mapped to .certora_sources?
            # we used a common path. so we try trimming prefixes until it can be relative to certora_sources
            new_srclist_map = {}
            successful = True
            for idx, orig_file in srclist.items():
                new_path = Util.find_filename_in(Util.get_certora_sources_dir(), orig_file)
                if new_path is None:
                    successful = False
                    break
                new_srclist_map[idx] = str(new_path)
            if successful:
                report_srclist = new_srclist_map
            else:  # we will try again and then after syncing of .certora_sources it will succeed
                report_srclist = srclist
        else:
            report_srclist = srclist

        report_source_file = report_srclist[[idx for idx in srclist if srclist[idx] == file_abs_path][0]]

        # all "contracts in SDC" are the same for every primary contract of the compiled file.
        # we can therefore compute those just once...
        # Solidity provides us with the list of contracts (non primary) that helped in compiling
        # the primary contract(s).
        contracts_in_sdc = []
        for contract_file, contract_list in sorted(list(contracts_with_libraries.items())):
            for contract_name in contract_list:
                contract_in_sdc = self.get_contract_in_sdc(
                    contract_file,
                    contract_name,
                    contracts_with_chosen_addresses,
                    data,
                    report_source_file,
                    contracts_in_file,
                    build_arg_contract_file,
                    compiler_collector
                )
                contracts_in_sdc.append(contract_in_sdc)

        for primary_contract in contracts_in_file:
            # every contract inside the compiled file is a potential primary contract (if we requested it)
            build_logger.debug(f"For contracts of primary {primary_contract}")

            build_logger.debug(f"finding primary contract address of {file_compiler_path}:{primary_contract} in "
                               f"{contracts_with_chosen_addresses}")
            primary_contract_address = \
                self.find_contract_address_str(file_compiler_path,
                                               primary_contract,
                                               contracts_with_chosen_addresses)
            build_logger.debug(f"Contracts in SDC {sdc_name}: {[contract.name for contract in contracts_in_sdc]}")
            # Need to deduplicate the library_addresses list without changing the order
            deduplicated_library_addresses = list(OrderedDict.fromkeys(self.library_addresses))
            sdc = SDC(primary_contract,
                      compiler_collector,
                      primary_contract_address,
                      build_arg_contract_file,
                      srclist,
                      report_srclist,
                      sdc_name,
                      contracts_in_sdc,
                      deduplicated_library_addresses,
                      {},
                      {},
                      {})
            sdc_lst_to_return.append(sdc)

        self.library_addresses.clear()  # Reset library addresses
        return sdc_lst_to_return

    def get_bytecode(self,
                     bytecode_object: Dict[str, Any],
                     contract_name: str,
                     primary_contracts: List[str],
                     contracts_with_chosen_addresses: List[Tuple[int, Any]],
                     fail_if_no_bytecode: bool
                     ) -> str:
        """
        Computes the linked bytecode object from the Solidity compiler output.
        First fetches the bytecode objects and then uses link references to replace library addresses.

        @param bytecode_object - the output from the Solidity compiler
        @param contract_name - the contract that we are working on
        @param primary_contracts - the names of the primary contracts we check to have a bytecode
        @param contracts_with_chosen_addresses - a list of tuples of addresses and the
            associated contract identifier
        @param fail_if_no_bytecode - true if the function should fail if bytecode object is missing,
            false otherwise
        @returns linked bytecode object
        """
        # TODO: Only contract_name should be necessary. This requires a lot more test cases to make sure we're not
        # missing any weird solidity outputs.
        bytecode_ = bytecode_object["object"]
        bytecode = self.collect_and_link_bytecode(contract_name, contracts_with_chosen_addresses,
                                                  bytecode_, bytecode_object.get("linkReferences", {}))
        if contract_name in primary_contracts and len(bytecode) == 0:
            msg = f"Contract {contract_name} has no bytecode. " \
                  f"It may be caused because the contract is abstract, " \
                  f"or is missing constructor code. Please check the output of the Solidity compiler."
            if fail_if_no_bytecode:
                raise Util.CertoraUserInputError(msg)
            else:
                build_logger.warning(msg)

        return bytecode

    def get_contract_in_sdc(self,
                            source_code_file: str,
                            contract_name: str,
                            contracts_with_chosen_addresses: List[Tuple[int, Any]],
                            data: Dict[str, Any],
                            report_source_file: str,
                            primary_contracts: List[str],
                            build_arg_contract_file: str,
                            compiler_collector_for_contract_file: CompilerCollector
                            ) -> ContractInSDC:
        contract_data = data[CONTRACTS][source_code_file][contract_name]
        ast_logger.debug(f"Contract {contract_name} is in file {source_code_file}")
        compiler_lang = compiler_collector_for_contract_file.smart_contract_lang
        if compiler_lang == CompilerLangSol():
            lang = "Solidity"
            types = self.collect_source_type_descriptions(source_code_file, contract_name, build_arg_contract_file,
                                                          compiler_lang)
            funcs = self.collect_funcs(contract_data, source_code_file, contract_name, build_arg_contract_file, types)
        else:
            lang = compiler_lang.name
            (types, clfuncs) = compiler_lang.collect_source_type_descriptions_and_funcs(self.asts, contract_data,
                                                                                        source_code_file, contract_name,
                                                                                        build_arg_contract_file)
            funcs = [Func(
                name=x.name,
                fullArgs=x.fullArgs,
                paramNames=x.paramNames,
                returns=x.returns,
                sighash=x.sighash,
                notpayable=x.notpayable,
                fromLib=x.fromLib,
                isConstructor=x.isConstructor,
                stateMutability=x.stateMutability,
                visibility=x.visibility,
                implemented=x.implemented,
                overrides=x.overrides,
                ast_id=x.ast_id,
                where=x.where) for x in clfuncs]
        external_funcs = {f for f in funcs if f.visibility in ['external', 'public']}
        public_funcs = {f for f in funcs if f.visibility in ['public']}
        internal_funcs = {f for f in funcs if f.visibility in ['private', 'internal']}

        source_size = self.collect_contract_bytes(source_code_file, contract_name, build_arg_contract_file)
        ast_logger.debug(f"Source bytes of {contract_name}: {source_size}")

        ast_logger.debug(f"Internal Functions of {contract_name}: {[fun.name for fun in internal_funcs]}")
        ast_logger.debug(f"Functions of {contract_name}: {[fun.name for fun in funcs]}")
        (srcmap, constructor_srcmap) = self.collect_srcmap(contract_data)

        varmap = ""
        deployed_bytecode = self.get_bytecode(contract_data["evm"]["deployedBytecode"], contract_name,
                                              primary_contracts,
                                              contracts_with_chosen_addresses, True)
        deployed_bytecode = compiler_lang.normalize_deployed_bytecode(
            deployed_bytecode)
        constructor_bytecode = self.get_bytecode(contract_data["evm"]["bytecode"], contract_name, primary_contracts,
                                                 contracts_with_chosen_addresses, False)
        constructor_bytecode = compiler_lang.normalize_deployed_bytecode(
            constructor_bytecode)
        address = self.find_contract_address_str(source_code_file,
                                                 contract_name,
                                                 contracts_with_chosen_addresses)
        storage_layout = \
            self.collect_storage_layout(contract_data)
        if storage_layout is not None and type(storage_layout) is dict and "storage" in storage_layout:
            declarations = storage_layout["storage"]
            if type(declarations) is list:
                for storage_slot in declarations:
                    if type(storage_slot) is dict and type(storage_slot.get("astId", None)) is int:
                        ast_id = storage_slot["astId"]  # type: int
                        node = self.get_node_from_asts(self.asts, build_arg_contract_file, ast_id)
                        if type(node) is dict and "typeName" in node:
                            descriptor = CT.Type.from_type_name_node(
                                lambda ref: self.get_original_def_node(build_arg_contract_file, ref),
                                lambda ref: self.get_contract_file_of_non_autofinder(build_arg_contract_file, ref),
                                node["typeName"]
                            )
                            type_descriptor = descriptor

                            def annotate_type(desc: CT.Type, type_name: str, store_types: Dict[str, Any],
                                              slot: Any = None, offset: Any = None) -> None:
                                number_of_bytes = store_types[type_name]["numberOfBytes"]
                                lower_bound = store_types[type_name].get("lowerBound")
                                upper_bound = store_types[type_name].get("upperBound")
                                annotations = [CT.StorageAnnotation(number_of_bytes, slot, offset, lower_bound,
                                                                    upper_bound)]
                                desc.annotate(annotations)

                                if isinstance(desc, CT.StructType):
                                    for desc_member in desc.members:
                                        for struct_member in store_types[type_name]["members"]:
                                            if desc_member.name == struct_member["label"]:
                                                annotate_type(desc_member.type, struct_member["type"], store_types,
                                                              struct_member["slot"], struct_member["offset"])
                                if isinstance(desc, CT.MappingType):
                                    annotate_type(desc.domain, store_types[type_name]["key"], store_types)
                                    annotate_type(desc.codomain, store_types[type_name]["value"], store_types)
                                if isinstance(desc, CT.ArrayType):
                                    annotate_type(desc.elementType, store_types[type_name]["base"], store_types)

                            annotate_type(descriptor, storage_slot["type"], storage_layout["types"])
                            storage_slot["descriptor"] = type_descriptor.as_dict()
        immutables = self.collect_immutables(contract_data, build_arg_contract_file)

        if self.input_config.function_finders is not None:
            all_internal_functions: Dict[str, Any] = \
                Util.read_json_file(self.input_config.function_finders)
            if contract_name in all_internal_functions:
                function_finders = all_internal_functions[contract_name]
            else:
                function_finders = {}
        else:
            function_finders = {}

        ast_logger.debug(f"Found internal functions for contract {contract_name}: {function_finders}")

        return ContractInSDC(contract_name,
                             # somehow make sure this is an absolute path which obeys the autofinder remappings
                             # (i.e. make sure this file doesn't start with autoFinder_)
                             source_code_file,
                             lang,
                             report_source_file,
                             address,
                             external_funcs,
                             deployed_bytecode,
                             constructor_bytecode,
                             srcmap,
                             varmap,
                             constructor_srcmap,
                             storage_layout,
                             immutables,
                             function_finders,
                             internal_funcs=internal_funcs,
                             public_funcs=public_funcs,
                             all_funcs=list(),
                             types=types,
                             compiler_collector=compiler_collector_for_contract_file,
                             source_bytes=source_size
                             )

    @staticmethod
    def get_sdc_key(contract: str, address: str) -> str:
        return f"{contract}_{address}"

    @staticmethod
    def get_primary_contract_from_sdc(contracts: List[ContractInSDC], primary: str) -> List[ContractInSDC]:
        return [x for x in contracts if x.name == primary]

    @staticmethod
    def generate_library_import(file_absolute_path: str, library_name: str) -> str:
        return f"\nimport {'{'}{library_name}{'}'} from '{file_absolute_path}';"

    def add_auto_finders(self, contract_file: str,
                         sdc: SDC) -> Optional[Tuple[Dict[str, InternalFunc], Dict[str, Dict[int, Instrumentation]]]]:
        function_finder_by_contract: Dict[str, InternalFunc] = dict()
        # contract file -> byte offset -> to insert
        function_finder_instrumentation: Dict[str, Dict[int, Instrumentation]] = dict()
        if not isinstance(sdc.compiler_collector, CompilerCollectorSol):
            raise Exception(f"Encountered a compiler collector that is not solc for file {contract_file}"
                            " when trying to add autofinders")
        instrumentation_logger.debug(f"Using {sdc.compiler_collector} compiler to "
                                     f"add auto-finders to contract {sdc.primary_contract}")
        for c in sdc.contracts:
            for f in c.internal_funcs.union(c.public_funcs):
                if f.isConstructor:
                    continue
                function_parameters = [arg for arg in f.fullArgs if isinstance(arg, CT.FunctionType)]
                """
                we don't support a generation of auto-finders for functions that have
                external function type parameters
                """
                if function_parameters:
                    instrumentation_logger.warning(
                        f"Cannot generate an auto-finder for {f.source_code_signature()} " +
                        f"in {c.name} due to external function type parameters: " +
                        ", ".join(map(lambda function_parameter: function_parameter.type_string,
                                      function_parameters)))
                    continue
                loc = f.where
                if loc is None:
                    if not f.implemented:
                        continue
                    instrumentation_logger.debug(f"Found an (implemented) function {f.name} in"
                                                 f" {c.name} that doesn't have a location")
                    return None
                instrumentation_path = Util.convert_path_for_solc_import(loc[0])
                if instrumentation_path not in function_finder_instrumentation:
                    instrumentation_logger.debug(f"New instrumentation for location {loc[0]}, " +
                                                 f"instrumentation path {instrumentation_path}")
                    function_finder_instrumentation[instrumentation_path] = dict()
                else:
                    instrumentation_logger.debug(f"Using existing instrumentation for location {loc[0]}, " +
                                                 f"instrumentation path {instrumentation_path}")

                if len(f.fullArgs) != len(f.paramNames):
                    instrumentation_logger.debug(f"Do not have argument names for {f.name} in"
                                                 f" {c.name}, giving up auto finders")
                    return None

                per_file_inst = function_finder_instrumentation[instrumentation_path]

                start_byte = int(loc[1].split(":")[0])
                # suuuuch a hack
                if start_byte in per_file_inst:
                    continue

                if f.ast_id is None:
                    instrumentation_logger.debug(f"No ast_id for function {f}, giving up here")
                    return None
                def_node = self.asts[contract_file].get(loc[0], dict()).get(f.ast_id, None)
                if def_node is None or type(def_node) != dict:
                    instrumentation_logger.debug(f"Failed to find def node for {f} {def_node} {f.ast_id}")
                    return None
                mods = def_node.get("modifiers", [])  # type: List[Dict[str, Any]]

                internal_id = self.function_finder_generator_counter
                self.function_finder_generator_counter += 1
                function_symbol = 0xf196e50000 + internal_id
                full_contract_file = self.get_contract_file_of_non_autofinder(contract_file, def_node["id"])
                function_finder_by_contract["0x%x" % function_symbol] = InternalFunc(full_contract_file, c.name, f)

                if len(mods) > 0:
                    # we need to add the instrumentation in a modifer because solidity modifiers will (potentially)
                    # appear before any instrumentation we add to the literal source body, which will tank the detection
                    # process. We cannot instrument the modifiers directly because they can be shared among multiple
                    # implementations.
                    #
                    # Q: Why not always instrument with modifiers?
                    # A: Without modifiers already present, the solidity AST makes it extremely difficult to figure out
                    # where in the source such modifiers will go. In order to insert a modifier, we have to have at
                    # least one modifier already present, and then insert before the first modifier's location in the
                    # source code
                    mod_inst = generate_modifier_finder(f, internal_id, function_symbol, sdc.compiler_collector)
                    if mod_inst is None:
                        instrumentation_logger.debug(f"Modifier generation for {f.name} @ {f.where} failed")
                        return None
                    modifier_invocation, modifier_def = mod_inst
                    func_def_start_str = def_node.get("src", None)
                    if func_def_start_str is None or type(func_def_start_str) != str:
                        instrumentation_logger.debug(f"Could not get source information for function "
                                                     f"{f.name} @ {f.where}")
                        return None
                    func_loc_split = func_def_start_str.split(":")
                    func_end_byte = int(func_loc_split[0]) + int(func_loc_split[1]) - 1
                    per_file_inst[func_end_byte] = Instrumentation(expected=b'}', to_ins=modifier_def,
                                                                   mut=InsertAfter())

                    if any(map(lambda mod: mod.get("nodeType", None) != "ModifierInvocation" or
                               type(mod.get("src", None)) != str, mods)):
                        instrumentation_logger.debug(f"Unrecognized modifier AST node for {f.name} @ {f.where}")
                        return None
                    first_mod = min(mods, key=lambda mod: int(mod["src"].split(":")[0]))
                    modifier_name = first_mod.get("modifierName", dict()).get("name", None)
                    if type(modifier_name) != str:
                        instrumentation_logger.debug(f"Can't infer expected name for modififer "
                                                     f"{modifier_invocation} for {f.name} @ {f.where}")
                        return None
                    first_mod_offset = int(first_mod["src"].split(":")[0])
                    per_file_inst[first_mod_offset] = Instrumentation(expected=bytes(modifier_name[0:1], "utf-8"),
                                                                      to_ins=modifier_invocation, mut=InsertBefore())
                else:
                    finder_res = generate_inline_finder(f, internal_id, function_symbol, sdc.compiler_collector)
                    if finder_res is None:
                        instrumentation_logger.debug(f"Generating auto finder for {f.name} @ {f.where}"
                                                     f" failed, giving up generation")
                        return None
                    finder_string = finder_res
                    per_file_inst[start_byte] = Instrumentation(expected=b'{', to_ins=finder_string,
                                                                mut=InsertAfter())
        return function_finder_by_contract, function_finder_instrumentation

    def cleanup(self) -> None:
        for f in self.generated_tmp_files:
            if f.is_file():
                Util.remove_file(f)
        for sdc_name, smart_contract_lang in self.__compiled_artifacts_to_clean:
            self.cleanup_compiler_outputs(sdc_name, smart_contract_lang)

    def get_all_function_call_refs(self, contract_file_ast: Dict[int, Any], contract_name: str) -> List[int]:
        """
        We assume that AST nodes that do not have self.CERTORA_CONTRACT_NAME() as a key, are not part of
        the contract; in particular, file level variable declarations cannot include contract functions' calls.
        For example, in solc8.12 one gets the following TypeError (note that only constant declarations are allowed):
        '
        TypeError: Initial value for constant variable has to be compile-time constant.
        | uint constant bla = cd.stakedBalance();
        |                     ^^^^^^^^^^^^^^^^^^
        '
        """
        return [int(contract_file_ast[node_id]["expression"]["referencedDeclaration"]) for node_id in
                contract_file_ast if
                "nodeType" in contract_file_ast[node_id] and contract_file_ast[node_id][
                    "nodeType"] == "FunctionCall" and "expression" in contract_file_ast[
                    node_id] and "referencedDeclaration" in contract_file_ast[node_id]["expression"].keys() and
                # a referencedDeclaration could be None
                contract_file_ast[node_id]["expression"]["referencedDeclaration"] is not None and \
                self.CERTORA_CONTRACT_NAME() in contract_file_ast[node_id] and
                contract_file_ast[node_id][self.CERTORA_CONTRACT_NAME()] == contract_name]

    def get_libraries_referenced_with_internal_functions(self, build_arg_contract_file: str, contract_file: str,
                                                         contract_name: str) -> List[str]:
        ast = self.asts[build_arg_contract_file][contract_file]
        referenced_functions = self.get_all_function_call_refs(ast, contract_name)
        referenced_nodes = [self.get_node_from_asts(self.asts, build_arg_contract_file, node_id) for
                            node_id in referenced_functions]
        # some referenced function calls could be builtins like require, whose declarations we do not see
        return [node[self.CERTORA_CONTRACT_NAME()] for node in referenced_nodes if self.CERTORA_CONTRACT_NAME() in node]

    @staticmethod
    def __find_closest_methods(method_name: str, methods: List[Func]) -> List[str]:
        """
        Gets a name of a method and a list of existing methods. Returns a list of closest matching method signatures.
        The match is performed on the name only, ignoring the parameters in the function.
        :param method_name: Name of a method
        :param methods: A list of possible methods.
        :return: An list of best suggested method signatures as replacement. Ordered by descending relevance.
        """
        # Step 1: find the closest method names
        all_method_names = [method.name for method in methods]
        all_method_names = list(set(all_method_names))  # remove duplicate names
        possible_method_names = Util.get_closest_strings(method_name, all_method_names)

        # Step 2: fetch the parameters of the closest matching method names
        possible_methods = list()
        for name in possible_method_names:
            for method in methods:
                if method.name == name:
                    possible_methods.append(method.signature())
        return possible_methods

    @staticmethod
    def __suggest_methods(wrong_sig: str, suggested_replacements: List[str]) -> None:
        """
        Raises an error suggesting replacement methods for an erroneous signature.
        :param wrong_sig: A method signature as inserted by the user. Had no exact matches in the code.
        :param suggested_replacements: A list of suggested method signatures, ordered by descending relevance
        :raises: AttributeError always
        """
        if len(suggested_replacements) == 0:
            raise Util.CertoraUserInputError(f"Method {wrong_sig} was not found.")

        if len(suggested_replacements) == 1:
            options_str = suggested_replacements[0]
        elif len(suggested_replacements) == 2:
            options_str = " or ".join(suggested_replacements)
        elif len(suggested_replacements) > 2:
            # Code below adds or after the last comma if there are multiple options
            options_str = ", ".join(suggested_replacements)
            last_commas_location_regex = r"(?<=,)(?=[^,]*$)"
            options_str = re.sub(last_commas_location_regex, r" or", options_str)

        raise Util.CertoraUserInputError(f"Method {wrong_sig} was not found. Maybe you meant {options_str}?")

    def __verify_method(self, method_input: str, sdc_pre_finder: SDC) -> None:
        input_method_name = method_input.split('(')[0]
        input_method_sig = method_input.replace(' ', '')

        """
        A list of suggested methods, in case the user inserted a wrong method signature. Only public/external methods
        are suggested to the user. The suggestions are ordered by closest match - index zero is the best match, and
        descending.
        """
        possible_methods = list()

        # Step #1 - check if an exact match exists. If not, check if only the parameters were wrong in the signature

        public_method_sets = [contract.methods for contract in sdc_pre_finder.contracts]
        public_methods = Util.flatten_set_list(public_method_sets)

        for method in public_methods:
            if method.name == input_method_name:  # Correct name, now we check parameter types
                if method.signature() == input_method_sig:  # An exact match was found
                    return

                # A method with the same name but different parameters exists
                possible_methods.append(method.signature())

        # Now we check if the method exists, but is private or external
        private_method_sets = [contract.internal_funcs for contract in sdc_pre_finder.contracts]
        private_methods = Util.flatten_set_list(private_method_sets)

        for method in private_methods:
            if method.name == input_method_name:  # Correct name, now we check parameter types
                if method.signature() == input_method_sig:  # An exact match was found
                    raise Util.CertoraUserInputError(
                        f"Method {input_method_sig} is {method.visibility}. Please change it to external or public")

        # We suggest a different method name, if we have a good enough suggestion

        # A method with correct name but wrong argument types takes precedence over a method with a different name
        if len(possible_methods) == 0:
            possible_methods = self.__find_closest_methods(input_method_name, public_methods)

        if len(possible_methods) > 0:  # We have suggestions
            self.__suggest_methods(method_input, possible_methods)

        raise Util.CertoraUserInputError(f"Method {method_input} was not found")

    @staticmethod
    def get_fresh_backupdir(backupdir: Path) -> Path:
        """
        returns a non-existing directory for backing-up of sources pre/post-autofinder generation.
        Every compiled contract should backup the sources before trying to overwrite with new autofinders,
        in case the autofinder compilation fails and we need to restore the previous ones.
        We should also keep post-autofinders, because otherwise our kotlin-parsed sourcemaps are wrong.
        Note that this should *not* be called in a concurrent setting and assumes sequential compilation of contracts.
        """
        folder_id = 0
        base = Util.get_certora_sources_dir() / backupdir
        while True:
            candidate = Path(f"{str(base)}.{folder_id}")
            if not candidate.exists():
                break  # it's a do-while really

            folder_id += 1
        return candidate

    def build(self) -> None:
        context = self.context
        for i, build_arg_contract_file in enumerate(sorted(self.input_config.files)):
            build_logger.debug(f"\nbuilding file {build_arg_contract_file}")
            compiler_lang = get_compiler_lang(build_arg_contract_file)
            self.path_for_compiler_collector_file = Util.abs_posix_path(build_arg_contract_file)
            orig_file_name = Path(build_arg_contract_file)
            Util.print_progress_message(f"Compiling {orig_file_name}...")
            sdc_pre_finders = self.collect_for_file(build_arg_contract_file, i, compiler_lang, Path(os.getcwd()))
            self.all_contract_files.update(reduce(lambda paths, sdc: add_contract_files(set(paths), sdc),
                                                  sdc_pre_finders, set()))
            if context.method and (build_arg_contract_file in context.verified_contract_files):
                # we check the --method flag's argument on compile time only for those modes
                # notice: when the backend will support multiple contracts to be verified/asserted,
                # we will have to be more careful here, since we assume there is only one contract
                # which is verified/asserted. For now, only the CLI support such multiple contracts.
                if context.verify:
                    verified_contract_name = context.verify.split(":")[0]
                elif context.assert_contracts:
                    verified_contract_name = context.assert_contracts[0]
                else:
                    verified_contract_name = None

                if verified_contract_name:
                    sdc_with_verified_contract_name = next(
                        curr_sdc for index, curr_sdc in enumerate(sdc_pre_finders) if
                        curr_sdc.primary_contract == verified_contract_name)
                    self.__verify_method(context.method, sdc_with_verified_contract_name)

            # Build sources tree
            build_logger.debug("Building source tree")
            sources = self.collect_sources(context)
            try:
                self.build_source_tree(sources, context)
            except Exception as e:
                build_logger.debug(f"build_source_tree failed. Sources: {sources}", exc_info=e)
                raise

            # .certora_sources, when zipped and sent to cloud, should be a pristine copy of the original files.
            # However, we need to keep both intermediate backups of pre-autofinder versions before compilation
            # (in order to restore previous state), and backups of post-autofinders, for srcmap resolution in Prover.
            # Having .certora_sources be pristine means we can get a clean zipInput file,
            # on which we can run certoraRun for idempotent results.
            # The complications start with multliple contracts. If we compile contract A, B, C, and we successfully
            # got autofinders for A and B, but failed for C. What happens? We roll back _everything_ including
            # A and B. But sources maps for A and B refer to the instrumented versions. Oops!
            # We therefore need new backup dirs to checkpoint every successful autofinder generation.
            # It also tells us we cannot have full parallel compilation of all contracts.
            pre_backup_dir = self.get_fresh_backupdir(Util.PRE_AUTOFINDER_BACKUP_DIR)
            ignore_patterns = shutil.ignore_patterns(f"{Util.PRE_AUTOFINDER_BACKUP_DIR}.*",
                                                     f"{Util.POST_AUTOFINDER_BACKUP_DIR}.*")
            build_logger.debug(f"Backing up current .certora_sources to {pre_backup_dir}")
            sources_dir = Util.get_certora_sources_dir()
            Util.safe_copy_folder(sources_dir, pre_backup_dir, ignore_patterns)

            # Instrument autofinders
            if compiler_lang == CompilerLangSol():
                added_finders_to_sdc, success = \
                    self.instrument_auto_finders(build_arg_contract_file, i,
                                                 sdc_pre_finders)  # type: Tuple[List[Tuple[Dict, SDC]],bool]
                # successful or not, we backup current .certora_sources for either debuggability, or for availability
                # of sources.
                post_backup_dir = self.get_fresh_backupdir(Util.POST_AUTOFINDER_BACKUP_DIR)
                build_logger.debug(f"Backing up instrumented .certora_sources to {post_backup_dir}")
                Util.safe_copy_folder(Util.get_certora_sources_dir(), post_backup_dir, ignore_patterns)

                # we're rolling back anyway to make extra sure we won't get dirty files in the next compilation
                # (although this is guaranteed by the other call to build_source_tree),
                # and to keep .certora_sources pristine.
                # roll back .certora_sources by copying from backup directory
                build_logger.debug(f"Rolling back .certora_sources to {pre_backup_dir} version")
                shutil.copytree(pre_backup_dir, Util.get_certora_sources_dir(), dirs_exist_ok=True,
                                ignore=ignore_patterns)
                if not success:
                    self.auto_finders_failed = True
                else:
                    # setup source_dir
                    for _, sdc in added_finders_to_sdc:
                        sdc.source_dir = str(post_backup_dir.relative_to(Util.get_certora_sources_dir()))
            else:
                # no point in running autofinders in vyper right now
                added_finders_to_sdc = [({}, sdc_pre_finder) for sdc_pre_finder
                                        in sdc_pre_finders]

            for added_finders, sdc in added_finders_to_sdc:
                for contract in sdc.contracts:
                    all_functions: List[Func] = list()
                    for k, v in added_finders.items():
                        # we also get the auto finders of the other contracts in the same file.
                        contract.function_finders[k] = v
                    all_functions.extend(contract.methods)
                    all_functions.extend(contract.internal_funcs)
                    functions_unique_by_internal_rep = list()  # type: List[Func]
                    for f in all_functions:
                        if not any([f.same_internal_signature_as(in_list) for in_list in
                                    functions_unique_by_internal_rep]):
                            functions_unique_by_internal_rep.append(f)
                    # sorted to ease comparison between sdcs
                    contract.all_funcs = sorted(functions_unique_by_internal_rep)

                if sdc.primary_contract in self.input_config.prototypes:
                    sdc.prototypes += self.input_config.prototypes[sdc.primary_contract]

                # First, add library addresses as SDCs too (they should be processed first)
                build_logger.debug(f"Libraries to add = {sdc.library_addresses}")
                for library_address in sdc.library_addresses:
                    library_contract_candidates = [contract for contract in sdc.contracts
                                                   if contract.address == library_address]
                    if len(library_contract_candidates) != 1:
                        fatal_error(
                            build_logger,
                            f"Error: Expected to have exactly one library address for {library_address}, "
                            f"got {library_contract_candidates}"
                        )

                    library_contract = library_contract_candidates[0]
                    build_logger.debug(f"Found library contract {library_contract}")
                    # TODO: What will happen to libraries with libraries?
                    sdc_lib = SDC(library_contract.name,
                                  sdc.compiler_collector,
                                  library_address,
                                  library_contract.original_file,
                                  sdc.original_srclist,
                                  sdc.report_srclist,
                                  f"{sdc.sdc_name}_{library_contract.name}",
                                  self.get_primary_contract_from_sdc(sdc.contracts, library_contract.name),
                                  [],
                                  {},
                                  {},
                                  {})
                    sdc_lib.source_dir = sdc.source_dir
                    self.SDCs[self.get_sdc_key(sdc_lib.primary_contract, sdc_lib.primary_contract_address)] = sdc_lib

                # Filter out irrelevant contracts, now that we extracted the libraries, leave just the primary
                sdc.contracts = self.get_primary_contract_from_sdc(sdc.contracts, sdc.primary_contract)
                assert len(
                    sdc.contracts) == 1, f"Found multiple primary contracts ({sdc.contracts}) in SDC {sdc.sdc_name}"

                self.SDCs[self.get_sdc_key(sdc.primary_contract, sdc.primary_contract_address)] = sdc

        self.handle_links()
        self.handle_struct_links()

    def build_source_tree(self, sources: Set[Path], context: CertoraContext, overwrite: bool = False) -> None:
        sources = sources_to_abs(sources)
        context = self.context
        # The common path is the directory that is a common ancestor of all source files used by the certoraRun script.
        # By getting the relative paths of all the sources the original directory structure can be copied to a new
        # location. In order to be able to rerun the certoraRun, also the current working directory should be mapped
        # that is why CWD is added to the list of sources

        cwd = Path(os.getcwd())
        common_path = Path(os.path.commonpath(list(sources.union({cwd}))))
        self.cwd_rel_in_sources = cwd.relative_to(common_path)

        for source_path in sources:
            is_dir = source_path.is_dir()
            # copy file to the path of the file from the common root under the sources directory

            # make sure directory exists
            target_path = Util.get_certora_sources_dir() / source_path.relative_to(common_path)
            target_directory = target_path if is_dir else target_path.parent
            try:
                target_directory.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                build_logger.debug(f"Failed to create directory {target_directory}", exc_info=e)
                raise

            # copy files. if we got a directory, nothing to do
            if is_dir:
                build_logger.debug(f"Skipping directory {source_path}")
                continue

            try:
                if overwrite:
                    # expecting target path to exist.
                    if target_path.exists():
                        build_logger.debug(f"Overwriting {target_path} by copying from {source_path}")
                    else:
                        build_logger.warning(f"Supposed to overwrite {target_path} by copying from {source_path}" +
                                             " but it does not exist... this may indicate bad things happen")
                if overwrite or not target_path.exists():
                    build_logger.debug(f"Copying {source_path} to {target_path}")
                    shutil.copyfile(source_path, target_path)
            except OSError as e:
                build_logger.debug(f"Couldn't copy {source_path} to {target_path}", exc_info=e)
                raise

        """
        Once the resource files are copied to the source tree, the paths in the value of the 'prover_resource_files'
        attribute are replaced with the relative path of the resource file from the source tree root.
        This way The server can easily find the resource files in the source tree. The path from the source tree is the
        relative path of cwd from source tree root (most cases '.') concatenated with the relative path of the resource
        file from cwd
        """
        if context.prover_resource_files:
            new_value = []
            len_orig = len(context.prover_resource_files)
            for value in context.prover_resource_files:
                label, file_path = value.split(':')
                rel_path = Path(os.path.relpath(file_path, '.'))
                new_value.append(':'.join([label, os.path.normpath(self.cwd_rel_in_sources / rel_path)]))
            if len_orig != len(new_value):
                raise RuntimeError(f"fail to process prover_resource_files {len_orig} out of {len(new_value)}")
            setattr(context, Attr.ContextAttribute.PROVER_RESOURCE_FILES.get_conf_key(), new_value)

    @staticmethod
    def normalize_path(path: str) -> str:
        """
        get wrekt solidity:
        When you write `import "yeet.sol" the solidity compiler in its ast output claims that the
        absolute path of the import is... "yeet.sol" despite that clearly being a relative path.
        according to the official solidity documentation, the *actual* conversion to a relative path
        is handled by the virtual file system, which prepends base paths or the other include paths to
        the name, and then tries to find a file at that absolute address.
        so we do the same thing: we know we don't pass a different base path (or other include paths)
        so we use solidity's documented default: the working directory of the compiler, which is the
        working directory of this script
        :param path: the string of the path to normalize
        :return: the original path if it was absolute, or the path placed relative to the CWD and the resolved
        """
        p = Path(path)
        if p.is_absolute():
            return path
        return str(Path.cwd() / p.resolve())

    def instrument_auto_finders(self, build_arg_contract_file: str, i: int,
                                sdc_pre_finders: List[SDC]) -> Tuple[List[Tuple[Dict[str, InternalFunc], SDC]], bool]:

        # initialization
        ret = []  # type: List[Tuple[Dict[str, InternalFunc], SDC]]
        instrumentation_logger.debug(f"Instrumenting auto finders in {build_arg_contract_file}")
        # all of the [SDC]s inside [sdc_pre_finders] have the same list of [ContractInSDC]s
        # (generated in the [collect_from_file] function).
        sdc_pre_finder = sdc_pre_finders[0]
        added_finders_tuple = self.add_auto_finders(build_arg_contract_file, sdc_pre_finder)
        if added_finders_tuple is None:
            instrumentation_logger.warning(f"Computing finder instrumentation failed for {build_arg_contract_file}")
            return [({}, old_sdc) for old_sdc in sdc_pre_finders], False
        (added_finders, instr) = added_finders_tuple
        abs_build_arg_contract_file = Util.abs_posix_path(build_arg_contract_file)
        if abs_build_arg_contract_file not in instr:
            instrumentation_logger.debug(
                f"Adding {build_arg_contract_file} as {abs_build_arg_contract_file} to instrumentation")
            instr[abs_build_arg_contract_file] = dict()

        autofinder_remappings = {}  # type: Dict[str, str]

        for contract_file, instr_loc in instr.items():
            new_name = self.to_autofinder_file(contract_file)
            old_abs_path = Path(contract_file)
            new_abs_path = Path(new_name)

            if new_name in autofinder_remappings:
                # instrumentation should be keyed only using absolute paths
                instrumentation_logger.warning(f"Already generated autofinder for {new_name}, "
                                               f"cannot instrument again for {contract_file}")
                return [({}, old_sdc) for old_sdc in sdc_pre_finders], False

            autofinder_remappings[new_name] = contract_file

            instr_rewrites: List[Tuple[int, Instrumentation]] = list(instr_loc.items())
            instrumentation_logger.debug(
                f"Generating autofinder file for {new_name} based on {contract_file}, "
                f"has {len(instr_rewrites)} rewrites")
            ordered_rewrite = sorted(instr_rewrites, key=lambda it: it[0])

            with old_abs_path.open('rb') as in_file:
                with new_abs_path.open("wb+") as output:
                    read_so_far = 0
                    for byte_offs, to_insert in ordered_rewrite:
                        instrumentation_logger.debug(f"Next chunk: {byte_offs}, inserting {to_insert.to_ins}")
                        amt = byte_offs - read_so_far
                        next_chunk = in_file.read(amt)
                        old_pos = in_file.tell()
                        output.write(next_chunk)
                        next_byte = in_file.read(1)
                        if next_byte != to_insert.expected:
                            instrumentation_logger.debug(f"Failed to find {repr(to_insert.expected)} at offset"
                                                         f" {byte_offs} in {old_abs_path} (got {repr(next_byte)})")
                            instrumentation_logger.debug(f"Underlying file reports {in_file.tell()}"
                                                         f" (before read: {old_pos})")
                            return [({}, old_sdc) for old_sdc in sdc_pre_finders], False
                        to_skip = to_insert.mut.insert(to_insert.to_ins, to_insert.expected, output)
                        if to_skip != 0:
                            in_file.read(to_skip)
                        read_so_far += amt + 1 + to_skip
                    output.write(in_file.read(-1))

        new_file = self.to_autofinder_file(build_arg_contract_file)
        self.input_config.fileToContractName[new_file] = self.input_config.fileToContractName[
            build_arg_contract_file]
        if build_arg_contract_file in self.input_config.solc_mappings:
            self.input_config.solc_mappings[new_file] = self.input_config.solc_mappings[build_arg_contract_file]
        autofinder_remappings[new_file] = build_arg_contract_file
        # TODO: I think this file name gets passed on to kotlin?? Not sure if it'll ever want to open the
        #       file, or if it'll only get the .certora_config one??
        try:
            orig_file_name = Path(build_arg_contract_file)
            Util.print_progress_message(f"Compiling {orig_file_name} to expose internal function information...")
            # record what aliases we have created (for the purposes of type canonicalization, the generated autofinder
            # is an alias of the original file)
            for k, v in autofinder_remappings.items():
                self.function_finder_file_remappings[Util.abs_posix_path(k)] = Util.abs_posix_path(v)
            new_sdcs = self.collect_for_file(new_file, i, get_compiler_lang(build_arg_contract_file),
                                             Util.get_certora_sources_dir(),
                                             fail_on_compilation_error=False,
                                             route_packages_to_certora_sources=True)
            for new_sdc in new_sdcs:
                ret.append((added_finders, new_sdc))

        except Util.SolcCompilationException as e:
            print(f"Encountered an exception generating autofinder {new_file} ({e}), falling back to original "
                  f"file {Path(build_arg_contract_file).name}")
            ast_logger.debug(f"Encountered an exception generating autofinder {new_file}, "
                             f"falling back to the original file {Path(build_arg_contract_file).name}", exc_info=e)
            # clean up mutation
            self.function_finder_file_remappings = {}
            return [({}, sdc_pre_finder) for sdc_pre_finder in sdc_pre_finders], False
        return ret, True

    def to_autofinder_file(self, contract_file: str) -> str:
        """
        Autofinder files are generated in the same directory of the contract under .certora_sources.
        In times past, they had a different name. Not anymore! If autofinder generation failed, we just
        copy back the sources to the .certora_sources and overwrite the failed attempt.
        """
        # we do normalizations towards re-rooting the file in .certora_sources
        contract_path = Util.abs_posix_path_obj(contract_file)
        rel_directory = Path(os.path.relpath(contract_file, '.')).parent
        contract_filename = contract_path.name
        new_path = Util.get_certora_sources_dir() / self.cwd_rel_in_sources / rel_directory / contract_filename
        new_path.parent.mkdir(parents=True, exist_ok=True)
        return str(new_path)

    def abs_path_relative_to_certora_sources(self, path: str) -> str:
        """
        Used to remap allowed paths and package paths to their new location under .certora_sources.
        This assumes those paths can be related to cwd.
        """
        rel_to_cwd_path = Path(os.path.relpath(path, '.'))
        new_path = Util.get_certora_sources_dir() / self.cwd_rel_in_sources / rel_to_cwd_path
        return str(new_path.resolve())

    def handle_links(self) -> None:
        # Link processing
        if self.input_config.link is not None:
            links = self.input_config.link
            for link in links:
                src, dst = link.split("=", 2)
                src_contract, reference_to_replace_with_link = src.split(":", 2)
                sources_to_update = self.get_matching_sdc_names_from_SDCs(src_contract)
                if len(sources_to_update) > 1:
                    build_logger.fatal(
                        f"Not expecting to find multiple SDC matches {sources_to_update} for {src_contract}")
                if len(sources_to_update) == 0:
                    build_logger.fatal(f"No contract to link to with the name {src_contract}")
                source_to_update = sources_to_update[0]
                # Primary contract name should match here
                if self.has_sdc_name_from_SDCs_starting_with(dst):
                    example_dst = self.get_one_sdc_name_from_SDCs(dst)  # Enough to pick one
                    dst_address = self.SDCs[example_dst].primary_contract_address
                else:
                    if Util.is_hex(dst):
                        dst = Util.hex_str_to_cvt_compatible(dst)
                        # The jar doesn't accept numbers with 0x prefix
                    dst_address = dst  # Actually, just a number

                # Decide how to link
                matching_immutable = list({(c, x.varname) for c in self.SDCs[source_to_update].contracts for x in
                                           c.immutables
                                           if
                                           x.varname == reference_to_replace_with_link and c.name == src_contract})
                if len(matching_immutable) > 1:
                    fatal_error(
                        ast_logger,
                        f"Not expecting to find multiple immutables with the name {reference_to_replace_with_link}, "
                        f"got matches {matching_immutable}")
                """
                Three kinds of links, resolved in the following order:
                1. Immutables. We expect at most one pair of (src_contract, immutableVarName) that matches
                2. Field names. Allocated in the storage - we fetch their slot number. (TODO: OFFSET)
                3. Slot numbers in EVM. Requires knowledge about the Solidity compilation. (TODO: OFFSET)
                """
                build_logger.debug(f"Reference to replace with link: {reference_to_replace_with_link}")
                if len(matching_immutable) == 1 and reference_to_replace_with_link == matching_immutable[0][1]:
                    contract_match = matching_immutable[0][0]

                    def map_immut(immutable_reference: ImmutableReference) -> ImmutableReference:
                        if immutable_reference.varname == reference_to_replace_with_link:
                            return PresetImmutableReference(immutable_reference.offset, immutable_reference.length,
                                                            immutable_reference.varname, dst_address)
                        else:
                            return immutable_reference

                    contract_match.immutables = [map_immut(immutable_reference) for immutable_reference in
                                                 contract_match.immutables]

                    continue
                elif not reference_to_replace_with_link.isnumeric() and not Util.is_hex(reference_to_replace_with_link):
                    # We need to convert the string to a slot number
                    resolved_src_slot = self.resolve_slot(src_contract, reference_to_replace_with_link)
                else:
                    # numeric case
                    if Util.is_hex(reference_to_replace_with_link):
                        # if hex, need to remove the 0x
                        reference_to_replace_with_link = Util.hex_str_to_cvt_compatible(reference_to_replace_with_link)
                    else:
                        # need to convert the dec to hex
                        reference_to_replace_with_link = \
                            Util.decimal_str_to_cvt_compatible(reference_to_replace_with_link)
                    resolved_src_slot = reference_to_replace_with_link
                build_logger.debug(f"Linking slot {resolved_src_slot} of {src_contract} to {dst}")
                build_logger.debug(' '.join(k for k in self.SDCs.keys()))

                build_logger.debug(f"Linking {src_contract} ({source_to_update}) to {dst_address} "
                                   f"in slot {resolved_src_slot}")
                self.SDCs[source_to_update].state[resolved_src_slot] = dst_address

    def handle_struct_links(self) -> None:
        # struct link processing
        if self.input_config.struct_link is not None:
            build_logger.debug('handling struct linking')
            links = self.input_config.struct_link
            for link in links:
                src, dst = link.split("=", 2)
                src_contract, reference_to_replace_with_link = src.split(":", 2)
                sources_to_update = self.get_matching_sdc_names_from_SDCs(src_contract)
                if len(sources_to_update) > 1:
                    fatal_error(build_logger,
                                f"Not expecting to find multiple SDC matches {sources_to_update} for {src_contract}")
                source_to_update = sources_to_update[0]
                # Primary contract name should match here
                if self.has_sdc_name_from_SDCs_starting_with(dst):
                    example_dst = self.get_one_sdc_name_from_SDCs(dst)  # Enough to pick one
                    dst_address = self.SDCs[example_dst].primary_contract_address
                else:
                    dst_address = dst  # Actually, just a number

                build_logger.debug(f"STRUCT Reference to replace with link: {reference_to_replace_with_link}")

                if not reference_to_replace_with_link.isnumeric() and not Util.is_hex(reference_to_replace_with_link):
                    self.SDCs[source_to_update].structLinkingInfo[reference_to_replace_with_link] = dst_address
                else:
                    if Util.is_hex(reference_to_replace_with_link):
                        resolved_src_slot = Util.hex_str_to_cvt_compatible(reference_to_replace_with_link)
                    else:
                        resolved_src_slot = Util.decimal_str_to_cvt_compatible(reference_to_replace_with_link)
                    build_logger.debug(f"STRUCT Linking slot {resolved_src_slot} of {src_contract} to {dst}")
                    build_logger.debug(' '.join(k for k in self.SDCs.keys()))

                    build_logger.debug(f"STRUCT Linking {src_contract} ({source_to_update}) to {dst_address} in slot "
                                       f"{resolved_src_slot}")
                    self.SDCs[source_to_update].legacyStructLinking[resolved_src_slot] = dst_address

    def has_sdc_name_from_SDCs_starting_with(self, potential_contract_name: str) -> bool:
        candidates = self.get_matching_sdc_names_from_SDCs(potential_contract_name)
        return len(candidates) > 0

    def __get_matching_sdc_names_for_SDCs_iterator(self, contract: str) -> Iterator[str]:
        return (k for k, v in self.SDCs.items() if k.startswith(f"{contract}_"))

    def get_one_sdc_name_from_SDCs(self, contract: str) -> str:
        return next(self.__get_matching_sdc_names_for_SDCs_iterator(contract))

    def get_matching_sdc_names_from_SDCs(self, contract: str) -> List[str]:
        return list(self.__get_matching_sdc_names_for_SDCs_iterator(contract))

    class SlotResolution(Enum):
        SLOT_NO_STORAGE_LAYOUT = enum.auto()
        SLOT_INVALID_STORAGE_LAYOUT = enum.auto()
        SLOT_NOT_FOUND = enum.auto()
        SLOT_FOUND_MULTIPLE = enum.auto()
        SLOT_RESOLVED = enum.auto()

    @staticmethod
    def resolve_slot_from_storage_layout(primary_contract: str, slot_name: str,
                                         sdc: SDC) -> Tuple[SlotResolution, Optional[str], Optional[str]]:
        """
        @param primary_contract: Name of the contract
        @param slot_name: Name of the field we wish to associate with a slot number
        @param sdc: The object representing an invocation of solc where we hope to find storageLayout
        @return: A tuple: SlotResolution - enum depicting If there is a valid storage layout and a valid slot number
                          string - returns the slot number associated with slot_name as hex without preceding 0x (or 0X)
                          string - relevant slots found, in case more than 1 slot found.
        """
        storage_layouts = [c.storageLayout for c in sdc.contracts if
                           c.name == primary_contract and c.storageLayout is not None]
        if len(storage_layouts) != 1:
            build_logger.debug(f"Expected exactly one storage layout matching {primary_contract}, "
                               f"got {len(storage_layouts)}")
            return CertoraBuildGenerator.SlotResolution.SLOT_NO_STORAGE_LAYOUT, None, None

        storage_layout = storage_layouts[0]
        if storage_layout is None or "storage" not in storage_layout:
            build_logger.debug(f"Storage layout should be an object containing a 'storage'"
                               f" field, but got {storage_layout}")
            return CertoraBuildGenerator.SlotResolution.SLOT_INVALID_STORAGE_LAYOUT, None, None

        relevant_slots = [slot for slot in storage_layout["storage"] if "label" in slot and slot["label"] == slot_name]
        relevant_slots_set = {slot['slot'] for slot in relevant_slots}
        build_logger.debug(f"Found relevant slots in storage layout of {primary_contract}: {relevant_slots}")
        if not relevant_slots:
            return CertoraBuildGenerator.SlotResolution.SLOT_NOT_FOUND, None, None
        elif len(relevant_slots_set) == 1:
            slot_number = relevant_slots_set.pop()
            cvt_compatible = Util.decimal_str_to_cvt_compatible(slot_number)
            # slot_number from storage layout is already in decimal.
            return \
                CertoraBuildGenerator.SlotResolution.SLOT_RESOLVED, cvt_compatible, None
        else:
            return CertoraBuildGenerator.SlotResolution.SLOT_FOUND_MULTIPLE, None, str(relevant_slots)

    def resolve_slot(self, primary_contract: str, slot_name: str) -> str:
        """
        @param primary_contract: Name of the contract
        @param slot_name: Name of the field we wish to associate with a slot number
        @return: The resolved slot number as hex without preceding 0x (or 0X)
        """
        build_logger.debug(f"Resolving slots for {primary_contract} out of {self.SDCs.keys()}")
        sdc = self.SDCs[self.get_one_sdc_name_from_SDCs(primary_contract)]  # Enough to pick one

        slot_result, slot_number_from_storage_layout, relevant_slots = \
            self.resolve_slot_from_storage_layout(primary_contract, slot_name, sdc)

        if slot_result == CertoraBuildGenerator.SlotResolution.SLOT_RESOLVED:
            return typing.cast(str, slot_number_from_storage_layout)
        elif slot_result == CertoraBuildGenerator.SlotResolution.SLOT_NOT_FOUND:
            msg = f"Link to a variable {slot_name} that doesn't exist in the contract {primary_contract}," \
                  f" neither as a state variable nor as an immutable."
            raise Util.CertoraUserInputError(msg)
        elif slot_result == CertoraBuildGenerator.SlotResolution.SLOT_FOUND_MULTIPLE:
            raise RuntimeError(f"Cannot link, found multiple matches for {slot_name} "
                               f"in storage layout of contract {primary_contract}: {relevant_slots}")

        build_logger.debug(
            f"Storage layout not available for contract {primary_contract}. "
            "Matching slots from ASM output instead"
        )

        file = sdc.sdc_origin_file
        file_of_primary_contract = self.input_config.contract_to_file[
            primary_contract]  # maybe its the same as [file]
        solc_ver_to_run = get_relevant_compiler(Path(file_of_primary_contract), self.input_config.solc,
                                                self.input_config.solc_mappings)

        asm_collect_cmd = f'{solc_ver_to_run} -o {self.config_path}/ --overwrite --asm ' \
                          f'--allow-paths "{self.input_config.path}" "{Util.abs_posix_path(file)}"'
        if self.input_config.packages is not None:
            asm_collect_cmd = f"{asm_collect_cmd} {' '.join(self.input_config.packages)}"

        Util.run_compiler_cmd(asm_collect_cmd, f"{primary_contract}.asm", self.config_path, Path(os.getcwd()))

        evm_file_path = self.config_path / f'{primary_contract}.evm'
        with evm_file_path.open() as asm_file:
            build_logger.debug(f"Got asm {asm_file}")
            saw_match = False
            candidate_slots = []
            for line in asm_file:
                if saw_match:
                    candidate_slots.append(line)
                    saw_match = False
                else:
                    regex = r'/\* "[a-zA-Z0-9./_\-:]+":[0-9]+:[0-9]+\s* %s \*/' % (slot_name,)
                    saw_match = re.search(regex, line) is not None
                    if saw_match:
                        build_logger.debug(f"Saw match for {regex} on line {line}")
            build_logger.debug(f"Candidate slots: {candidate_slots}")
            normalized_candidate_slots = [x.strip() for x in candidate_slots]
            build_logger.debug(f"Candidate slots: {normalized_candidate_slots}")
            filtered_candidate_slots = [x for x in normalized_candidate_slots if re.search('^0[xX]', x)]
            set_candidate_slots = set(filtered_candidate_slots)
            build_logger.debug(f"Set of candidate slots: {set_candidate_slots}")
            if len(set_candidate_slots) == 1:
                # Auto detect base (should be 16 though thanks to 0x)
                slot_number = hex(int(list(set_candidate_slots)[0], 0))[2:]
                build_logger.debug(f"Got slot number {slot_number}")
            else:
                if len(set_candidate_slots) > 1:
                    msg = f"Cannot link, Found multiple matches for {slot_name}" \
                          f" in {primary_contract}, valid candidates: {set_candidate_slots}"
                    raise RuntimeError(msg)
                else:
                    msg = f"Link to a var that doesnt exist on the contract. Failed to resolve slot for {slot_name}" \
                          f" in {primary_contract}, valid candidates: {set_candidate_slots}"
                    raise Util.CertoraUserInputError(msg)

        return slot_number

    # The sources that are collected for the .certora_sources directory are all the files that are provided as input
    # (i.e. they are not generated during the certora build process) that are needed for precise rerunning certoraRun.
    #
    # Including:
    #
    #   1) All contract files, including those in packages
    #   2) The package.json file for parsing dependencies
    #   3) All spec files, including imported specs
    #   4) bytecode files (spec and json)

    def collect_sources(self, context: CertoraContext) -> Set[Path]:
        def add_to_sources(path_to_file: Path) -> None:
            if path_to_file.exists():
                sources.add(Path(os.path.normpath(Path.cwd() / path_to_file)))
            else:
                raise Util.CertoraUserInputError(f"collect_sources: {path_to_file} does not exist cwd - {Path.cwd()}."
                                                 f"abs - {os.path.normpath(Path.cwd() / path_to_file)}")

        sources = self.all_contract_files
        sources |= self.certora_verify_generator.get_spec_files()
        if Util.PACKAGE_FILE.exists():
            add_to_sources(Util.PACKAGE_FILE)
        if Util.REMAPPINGS_FILE.exists():
            add_to_sources(Util.REMAPPINGS_FILE)
        if context.bytecode_jsons:
            for file in context.bytecode_jsons:
                add_to_sources(Path(file))
        if context.bytecode_spec:
            sources.add(Path(context.bytecode_spec))
        if "package_name_to_path" in vars(context):
            for path_str in context.package_name_to_path.values():
                path = Path(path_str)
                if path.exists():
                    add_to_sources(path)
        if hasattr(context,
                   Attr.ContextAttribute.PROVER_RESOURCE_FILES.get_conf_key()) and context.prover_resource_files:
            for value in context.prover_resource_files:
                _, file_path = value.split(':')
                add_to_sources(Path(file_path))

        # if certoraRun runs from conf file the sources in the conf file
        # will replace the conf file in context.files so we add the conf file separately
        if hasattr(context, CONF_FILE_ATTR):
            add_to_sources(Path(getattr(context, CONF_FILE_ATTR)))
        return sources

    def __del__(self) -> None:
        self.cleanup()


def add_contract_files(paths: Set[Path], contract: SDC) -> Set[Path]:
    paths.update(contract.sources_as_absolute())
    return paths


class SpecImportLexer(Lexer):
    """
        A lexer that creates designated tokens for 'import' keywords and strings literals in the given spec file.
    """

    def __init__(self, spec_file: Path, spec_content: str):
        self.spec_file = spec_file
        self.spec_content = spec_content

    tokens = {ANY, IMPORT, STRING}  # type: ignore # noqa: F821

    ignore = ' \t'  # Ignore whitespace and tab characters

    # Ignore comments; in particular, ignore commented out imports;
    ignore_comments_a = r'[/][/][^\n\r]*'

    @_(r'[/][*][\s\S]*?[*][/]')  # type: ignore # noqa: F821
    def ignore_comments_b(self, t: Token) -> None:
        self.lineno += t.value.count("\n")

    IMPORT = r'\bimport\b'  # First, match against 'import' keywords and string literals

    @_(r'\"[^"]*\"')  # type: ignore # noqa: F821
    def STRING(self, t: Token) -> Token:  # Extract the characters of the string literal, e.g., '"abc"' --> 'abc'
        result = re.search(r'[^"]+', t.value)
        if result:
            t.value = result.group(0)
        else:  # An empty string literal (i.e., '""')
            t.value = ''
        return t

    ANY = r'.'  # Default: Characters that have nothing to do with import declarations

    @_(r'\n+')  # type: ignore # noqa: F821
    def ignore_newline(self, t: Token) -> None:  # Ignore new line characters; use those to compute the line number
        self.lineno += len(t.value)

    # Error handling
    def error(self, t: Token) -> None:
        raise Util.CertoraUserInputError(f'{self.spec_file}:{self.lineno}:{self.find_column(t.index)}: '
                                         f'Encountered the illegal symbol {repr(t.value[0])}')

    # Computes the column number from the given token's index
    def find_column(self, token_index: int) -> int:
        last_cr = self.spec_content.rfind('\n', 0, token_index)
        if last_cr < 0:
            last_cr = 0
        column = (token_index - last_cr) + 1
        return column


class SpecImportParser(Parser):
    """
           A parser for import declarations of specification files, namely strings that have the form
           'IMPORT STRING'.
           NOTE: The parser should guarantee that if the spec file has a valid syntax, then all of its imports
           are parsed. In particular, no actual imports are omitted, and no
           non-existing or commented out imports are erroneously added.
           If the spec has an invalid syntax, we may over-approximate the actual set of imports,
           but we expect that the CVL parser would fail later.

    """

    def __init__(self, _lexer: SpecImportLexer):
        self.lexer = _lexer
        self.parse_error_msgs = []  # type: List[str]

    # Get the token list from the lexer (required)
    tokens = SpecImportLexer.tokens

    # Grammar rules and actions
    @_('imports maybe_import_decl')  # type: ignore # noqa: F821,F811
    def imports(self, p: YaccProduction) -> List[Tuple[str, str]]:
        return p.imports if not p.maybe_import_decl else p.imports + p.maybe_import_decl

    @_('')  # type: ignore # noqa: F821,F811
    def imports(self, p: YaccProduction) -> List[Tuple[str, str]]:  # noqa: F821,F811
        return []

    @_('ANY', 'STRING')  # type: ignore # noqa: F821,F811
    def maybe_import_decl(self, p: YaccProduction) -> None:  # Surely NOT an import declaration
        return None

    @_('IMPORT STRING')  # type: ignore # noqa: F821,F811
    def maybe_import_decl(self, p: YaccProduction) -> List[Tuple[str, str]]:  # noqa: F821,F811
        # Surely an import declaration
        # Also log the location of the import declaration
        return [(p.STRING, f'{p.lineno}:{self.lexer.find_column(p.index)}')]

    def error(self, p: Token) -> Token:
        self.parse_error_msgs.append(fr'{self.lexer.spec_file}:{p.lineno}:{self.lexer.find_column(p.index)}: '
                                     fr'Did not expect the symbol {repr(p.value)}')  # log the error
        # Read ahead looking for an 'import' keyword.
        # If such a keyword is found, restart the parser in its initial state
        while True:
            p = next(self.tokens.__iter__(), None)
            if not p or p.type == 'IMPORT':
                break
            self.restart()
        return p  # Return IMPORT as the next lookahead token


class SpecWithImports:
    """
        .spec file together with the import declarations of .spec files that were collected transitively from it.
    """

    def __init__(self, _spec_file: str, _spec_idx: int, _abspath_imports_to_locs: Dict[str, Set[str]],
                 _spec_files_to_orig_imports: Dict[str, Set[str]]):

        self.spec_file = _spec_file  # The path of the main .spec file

        self.spec_idx = _spec_idx  # The index that will be prepended to the names of the main and imported .spec files

        #  The path where the main .spec file will eventually be copied to
        self.eventual_path_to_spec = self.__get_eventual_path_to_spec(Path(self.spec_file))

        # Maps absolute .spec import paths to locations of corresponding import declarations in the .spec files
        self.abspath_imports_to_locs = _abspath_imports_to_locs

        # Maps each .spec file to the import paths that appear in the import declarations that this file contains.
        # Each key is the absolute path of the .spec file
        self.spec_files_to_orig_imports = _spec_files_to_orig_imports

        # Maps each "eventual" path of a .spec file to the import paths that appear in this file.
        # The "eventual" path is where the .spec file will eventually be copied to;
        # e.g., "./someFolder/s.spec" -> .certora_config/{self.spec_idx}_s.spec
        self.eventual_path_to_orig_imports = {self.__get_eventual_path_to_spec(Path(abspath)): list(orig_imports) for
                                              abspath, orig_imports in self.spec_files_to_orig_imports.items()}

        #  Maps each absolute .spec import path to the one where the imported .spec file will eventually be copied to
        self.abspath_to_eventual_import_paths = {abspath: self.__get_eventual_path_to_spec(Path(abspath)) for abspath in
                                                 self.abspath_imports_to_locs.keys()}

        # Maps each "eventual" .spec import path to a (canonicalized) relative form of the original import declaration
        self.eventual_import_paths_to_relpaths = {
            self.__get_eventual_path_to_spec(Path(abspath)): str(Path(abspath).relative_to(Path().resolve()))
            for abspath in self.abspath_imports_to_locs.keys()
        }

        self.__assert_distinct_filenames()

    def __get_eventual_path_to_spec(self, path: Path) -> str:
        return f"{Util.get_certora_sources_dir()}/.{self.spec_idx}_{path.name}.spec"

    #  Checks that we don't have distinct import paths that share the same file names, e.g.,
    #  './folder/a.spec' and './otherFolder/a.spec'
    #  Also checks that there is no import path whose file name is the same as that of the main .spec file.
    #  Note: This is required because we copy all of the imported .spec files, together with the main .spec file,
    #  into the same directory.
    def __assert_distinct_filenames(self) -> None:

        def invalid_imports_str(invalid_imports: List[str]) -> str:
            return '\n'.join(
                [f'\"{abspath}\" @ {"; ".join(self.abspath_imports_to_locs[abspath])}' for abspath in
                 invalid_imports])

        distinct_imports_filenames = list(
            map((lambda path: os.path.basename(path)), self.abspath_imports_to_locs.keys()))

        distinct_imports_with_shared_filenames = \
            [path for path in self.abspath_imports_to_locs.keys() if
             distinct_imports_filenames.count(os.path.basename(path)) > 1]

        if distinct_imports_with_shared_filenames:
            raise Util.CertoraUserInputError(
                f'Expected all distinct .spec file imports to also have distinct file names, but got:\n'
                f'{invalid_imports_str(distinct_imports_with_shared_filenames)}')

        spec_file_basename = os.path.basename(self.spec_file)
        imports_with_spec_file_basename = [path for path in self.abspath_imports_to_locs.keys() if
                                           os.path.basename(path) == spec_file_basename]
        if imports_with_spec_file_basename:
            raise Util.CertoraUserInputError(
                f'Expected all .spec file imports to have file names different from \'{spec_file_basename}\', but got:'
                f'\n{invalid_imports_str(imports_with_spec_file_basename)}')


class CertoraVerifyGenerator:
    def __init__(self, build_generator: CertoraBuildGenerator):
        self.build_generator = build_generator
        self.input_config = build_generator.input_config
        self.certora_verify_struct = {}  # type: Dict[str, Any]
        self.verify_spec = None
        self.verify_contract = None
        # cannot have both --verify and --assert so we try each one
        if self.input_config.verify is not None:
            verification_query = self.input_config.verify

            vq_contract, vq_spec = verification_query.split(":", 2)
            vq_spec = Util.abs_posix_path(vq_spec)  # get full abs path, will need to update later to .certora_sources

            vq_spec_with_imports = self.get_spec_with_imports(vq_spec)  # type: SpecWithImports
            self.verify_contract = vq_contract
            self.verify_spec = vq_spec_with_imports
            self.copy_specs()
            # we need to build once because of the early typechecking...
            self.update_certora_verify_struct(False)

        elif self.input_config.assert_contracts is not None:
            contractToCheckAssertsFor = self.input_config.assert_contracts
            self.certora_verify_struct = {"type": "assertion",
                                          "primaryContracts": contractToCheckAssertsFor}

    def update_certora_verify_struct(self, in_certora_sources: bool) -> None:
        """
        Updates the struct that .certora_verify.json is based on.
        @param in_certora_sources - whether all paths should be rooted relatively to
                                    .certora_sources.
                                    This is set to true before we actually call the Prover,
                                    and before that - local typechecking - we don't care.
        """
        if self.input_config.verify is not None:
            assert self.verify_contract is not None and self.verify_spec is not None

            vq_contract, vq_spec_with_imports = self.verify_contract, self.verify_spec

            def path_updater(path: str) -> str:
                if in_certora_sources:
                    res = Util.find_filename_in(Util.get_certora_sources_dir(), path)
                    assert res is not None
                    return res
                else:
                    return path

            vq_spec = path_updater(vq_spec_with_imports.spec_file)
            self.certora_verify_struct = {"type": "spec",
                                          "primary_contract": vq_contract,
                                          "specfile": vq_spec,
                                          "specfileOrigRelpath": Util.as_posix(os.path.relpath(vq_spec)),
                                          "specfilesToImportDecls": {path_updater(k): list(v) for k, v in
                                                                     vq_spec_with_imports.spec_files_to_orig_imports
                                                                     .items()},
                                          "importFilesToOrigRelpaths":
                                              {path_updater(k): str(Path(k).relative_to(Path().resolve())) for k in
                                               vq_spec_with_imports.abspath_imports_to_locs
                                               .keys()}
                                          }

    def get_spec_with_imports(self, spec_file: str) -> SpecWithImports:
        seen_abspath_imports_to_locs = dict()  # type: Dict[str, Set[str]]
        spec_file_to_orig_imports = dict()  # type: Dict[str, Set[str]]
        self.check_and_collect_imported_spec_files(Path(spec_file), seen_abspath_imports_to_locs, [spec_file],
                                                   spec_file_to_orig_imports)
        # will start with spec_idx == 0 to give the imports the unique names starting with 1
        return SpecWithImports(spec_file, 0, seen_abspath_imports_to_locs, spec_file_to_orig_imports)

    def check_and_collect_imported_spec_files(self, spec_file: Path, seen_abspath_imports_to_locs: Dict[str, Set[str]],
                                              dfs_stack: List[str],
                                              spec_file_to_orig_imports: Dict[str, Set[str]]) -> None:
        with spec_file.open() as f:
            spec_content = f.read()
            spec_import_lexer = SpecImportLexer(spec_file, spec_content)
            spec_import_parser = SpecImportParser(spec_import_lexer)
            imports_with_locs = spec_import_parser.parse(spec_import_lexer.tokenize(spec_content))

            if imports_with_locs:
                spec_file_to_orig_imports[str(spec_file)] = set()
                for orig_import_to_loc in imports_with_locs:
                    spec_file_to_orig_imports[str(spec_file)].add(orig_import_to_loc[0])

            build_logger.debug(fr'In {spec_file}, found the imports: {imports_with_locs}')
            if spec_import_parser.parse_error_msgs:  # We have parsing errors
                errors_str = '\n'.join(spec_import_parser.parse_error_msgs)
                raise Util.CertoraUserInputError(f'Could not parse {spec_file} '
                                                 f'due to the following errors:\n{errors_str}')

            abspath_imports_with_locs = list(map(
                lambda path_to_loc: (Util.abs_posix_path_relative_to_root_file(Path(path_to_loc[0]), spec_file),
                                     path_to_loc[1]),
                imports_with_locs))

            invalid_imports_with_locs = [p for p in abspath_imports_with_locs if not os.path.isfile(p[0]) or
                                         os.path.splitext(p[0])[1] != '.spec']

            def path_to_loc_str(path_to_loc: Tuple[Path, str]) -> str:
                return f'{path_to_loc[1]}:\"{path_to_loc[0]}\"'

            if invalid_imports_with_locs:
                invalid_paths_str = '\n'.join(map(path_to_loc_str, invalid_imports_with_locs))
                raise Util.CertoraUserInputError(
                    f'In {spec_file}, the following import declarations do not import existing .spec files:'
                    f'\n{invalid_paths_str}\n'
                )

            for import_path_to_loc in abspath_imports_with_locs:  # Visit each import declaration in a DFS fashion
                if import_path_to_loc[0] in dfs_stack:  # We have cyclic imports :(((
                    imports_cycle = ' -->\n'.join(
                        dfs_stack[dfs_stack.index(str(import_path_to_loc[0])):] + [str(import_path_to_loc[0])])
                    raise Util.CertoraUserInputError(
                        f'In {spec_file}, the import declaration {path_to_loc_str(import_path_to_loc)} '
                        f'leads to an imports\' cycle:\n{imports_cycle}')

                import_loc_with_spec_file = f'{spec_file}:{import_path_to_loc[1]}'

                if import_path_to_loc[0] in seen_abspath_imports_to_locs:  # Visit each import declaration only once
                    seen_abspath_imports_to_locs[str(import_path_to_loc[0])].add(import_loc_with_spec_file)
                    continue

                seen_abspath_imports_to_locs[str(import_path_to_loc[0])] = {import_loc_with_spec_file}
                dfs_stack.append(str(import_path_to_loc[0]))
                self.check_and_collect_imported_spec_files(Path(import_path_to_loc[0]), seen_abspath_imports_to_locs,
                                                           dfs_stack, spec_file_to_orig_imports)
                dfs_stack.pop()

    def copy_specs(self) -> None:
        spec = self.verify_spec
        assert spec is not None
        Path(spec.eventual_path_to_spec).parent.mkdir(parents=True, exist_ok=True)
        build_logger.debug(f"copying spec file {spec.spec_file} to "
                           f"{Util.abs_posix_path(spec.eventual_path_to_spec)}")
        shutil.copy2(spec.spec_file, spec.eventual_path_to_spec)
        #  copy .spec imports
        for import_srcpath, import_dstpath in spec.abspath_to_eventual_import_paths.items():
            shutil.copy2(import_srcpath, import_dstpath)

    def get_spec_files(self) -> Set[Path]:
        specs = set()  # type: Set[Path]
        if self.verify_spec is not None:
            spec = self.verify_spec
            path = Path(spec.spec_file).resolve()
            if path.exists():
                specs.add(path)
            for import_srcpath, import_dstpath in spec.abspath_to_eventual_import_paths.items():
                path = Path(import_srcpath).resolve()
                if path.exists():
                    specs.add(path)
        return specs

    def check_primary_contact_is_in_build(self) -> None:
        contract = self.verify_contract
        if contract is not None:
            if len(self.build_generator.get_matching_sdc_names_from_SDCs(contract)) == 0:
                fatal_error(
                    build_logger,
                    f"Error: Could not find contract {contract} in contracts "
                    f"[{','.join(map(lambda x: x[1].primary_contract, self.build_generator.SDCs.items()))}]")

    def dump(self) -> None:
        build_logger.debug(f"writing {Util.abs_posix_path(Util.get_certora_verify_file())}")
        with Util.get_certora_verify_file().open("w+") as output_file:
            json.dump(self.certora_verify_struct, output_file, indent=4, sort_keys=True)


# make sure each source file exists and its path is in absolute format
def sources_to_abs(sources: Set[Path]) -> Set[Path]:
    result = set()  # Set[Path]
    for p in sources:
        if p.exists():
            result.add(Path(os.path.normpath(p.absolute())))
    return result


def build(context: CertoraContext, ignore_spec_syntax_check: bool = False) -> None:
    """
    This is the main function of certoraBuild
    @param context: A namespace including command line arguments. We expect the namespace to include validated arguments
    @param ignore_spec_syntax_check: If true, we skip checking the spec file for syntax errors.
           Otherwise, if syntax errors are found, we quit immediately
    @returns True if succeeded, False otherwise
    """

    try:
        input_config = InputConfig(context)

        # Create generators
        certora_build_generator = CertoraBuildGenerator(input_config, context)

        # Build .certora_verify.json
        certora_build_generator.certora_verify_generator = CertoraVerifyGenerator(certora_build_generator)
        certora_build_generator.certora_verify_generator.dump()  # first dump

        # Start by syntax checking, if we're in the right mode
        if Util.mode_has_spec_file(context.mode) and not context.build_only and not ignore_spec_syntax_check:
            attr = context.disable_local_typechecking
            if attr:
                build_logger.warning(
                    "Local checks of CVL specification files disabled. It is recommended to enable the checks.")
            else:
                spec_check_exit_code = Util.run_local_spec_check(with_typechecking=False, rules_to_check=context.rule)
                if spec_check_exit_code != 0:
                    raise Util.CertoraUserInputError("CVL specification syntax check failed")

        # Start to collect information from solc
        certora_build_generator.build()

        # Build sources tree
        sources = certora_build_generator.collect_sources(context)
        try:
            certora_build_generator.build_source_tree(sources, context)
        except Exception as e:
            build_logger.debug("build_source_tree failed", exc_info=e)

        certora_build_generator.certora_verify_generator.check_primary_contact_is_in_build()
        certora_build_generator.certora_verify_generator.update_certora_verify_struct(True)
        certora_build_generator.certora_verify_generator.dump()  # second dump with properly rooted specs

        # Output
        build_logger.debug(f"writing file {Util.abs_posix_path(Util.get_certora_build_file())}")
        with Util.get_certora_build_file().open("w+") as output_file:
            json.dump({k: v.as_dict() for k, v in certora_build_generator.SDCs.items()},
                      output_file,
                      indent=4,
                      sort_keys=True)

        # in autofinder assertion mode, we want to hard-fail.
        if certora_build_generator.auto_finders_failed and context.assert_autofinder_success:
            raise Exception("Failed to create autofinders, failing")

    except Exception as e:
        build_logger.debug("build failed")
        raise e
