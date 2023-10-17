# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Specker JSON Specification Validator,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import json
import logging
import argparse
import typing
from pathlib import Path
from sys import exit

from .loader import SpecLoader

def get_defaults() -> None:
    """_summary_
    """
    parser:argparse.ArgumentParser = argparse.ArgumentParser(description="Validate a Spec File")
    parser.add_argument("-s","--spec",help="Directory to load Specs from",required=True)
    parser.add_argument("-v","--verbose",help="Turn on Debugging",action="store_true")
    args:argparse.Namespace = parser.parse_args()

    loglevel:int = logging.INFO
    if args.verbose:
        loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel)

    spec_path:Path = Path(args.spec).resolve()
    full_path:str = spec_path.as_posix()
    if not spec_path.exists():
        logging.error(f"Cannot locate {full_path}")
        exit(1)
    spec_name:str = ""
    single:bool = False
    if spec_path.is_file():
        spec_name = spec_path.stem
        spec_path = spec_path.parent
        single = True
    spec_loader:SpecLoader = SpecLoader(spec_path,debug=True)
    if single:
        print(json.dumps(spec_loader.defaults(spec_name),indent=4))
    else:
        for spec_name in spec_loader.spec_names:
            spec_defaults:typing.Any = spec_loader.defaults(spec_name)
            print(json.dumps(spec_defaults,indent=4))
    exit(1)

def validate_spec_file() -> None:
    """Validate Spec File is a valid Spec File
    """
    parser:argparse.ArgumentParser = argparse.ArgumentParser(description="Validate a Spec File")
    parser.add_argument("-s","--spec",help="Spec file to validate",required=True)
    parser.add_argument("-v","--verbose",help="Turn on Debugging",action="store_true")
    args:argparse.Namespace = parser.parse_args()

    loglevel:int = logging.INFO
    if args.verbose:
        loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel)

    spec_path:Path = Path(args.spec).resolve()
    full_path:str = spec_path.as_posix()
    if not spec_path.exists():
        logging.error(f"Cannot locate {full_path}")
        exit(1)

    try:
        with open(spec_path, "r", encoding="utf-8") as f:
            content:dict[str,typing.Any] = json.loads(f.read())
    except BaseException as e:
        logging.error(f"Unable to load {full_path}, {e}")
        logging.debug(e,exc_info=True)
        exit(1)

    spec_loader:SpecLoader = SpecLoader(Path(__file__).resolve().parent.joinpath("specs"))
    total_result:bool = True
    for k,spec_content in content.items():
        spec_result:bool = spec_loader.compare("specker",spec_content)
        if not spec_result:
            total_result = False
            logging.error(f"Spec Validation Failed for option: {k}")
    if total_result:
        logging.info("Valid Spec")
        exit(0)
    exit(1)

def generate_spec_docs() -> None:
    """Generate Documentation from Spec Files
    @retval None Nothing
    """
    parser:argparse.ArgumentParser = argparse.ArgumentParser(description="Generate Documentation from Spec files")
    parser.add_argument("-p","--path",help="Path to search for Spec files",required=True)
    parser.add_argument("-o","--outfile",help="Output File",required=True)
    parser.add_argument("-v","--verbose",help="Turn on Debugging",action="store_true")
    args:argparse.Namespace = parser.parse_args()

    loglevel:int = logging.INFO
    if args.verbose:
        loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel)

    full_path:str = ""
    search_path:Path = Path(args.path).resolve()
    if not search_path.exists():
        full_path = search_path.as_posix()
        logging.error(f"Cannot locate {full_path}")
        exit(1)

    output_file:Path = Path(args.outfile).resolve()
    outdir:Path = output_file.parent
    if not outdir.exists():
        try:
            outdir.mkdir(parents=True)
        except BaseException as e:
            full_path = outdir.as_posix()
            logging.error(f"Unable to create output dir {full_path}, {e}")
            logging.debug(e,exc_info=True)
            exit(1)

    spec_loader:SpecLoader = SpecLoader(search_path)
    spec_loader.write(output_file)
