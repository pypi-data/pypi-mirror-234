#!/usr/bin/env python

import sys
import os
import argparse
import yaml

from npu_compiler import VERSION
from npu_compiler.v100.config import Config as Config_1_0
import npu_compiler.v100.compiler as compiler_1_0
from npu_compiler.v120.config import Config as Config_1_2
import npu_compiler.v120.compiler as compiler_1_2
from npu_compiler.v150.config import Config as Config_1_5
import npu_compiler.v150.compiler as compiler_1_5
from npu_compiler.v160.config import Config as Config_1_6
import npu_compiler.v160.compiler as compiler_1_6

def get_config_from_file(config_file, quant):
    if isinstance(config_file, str):
        # input from yaml file
        try:
            with open(config_file) as f:
                config_dict = yaml.safe_load(f)
                config_dict["IS_QUANT"] = quant
                config_dir = os.path.dirname(config_file)
        except IOError:
            print("[ERROR] can't open config file: \"%s\"" % config_file)
            sys.exit(1)
    else:
        # input from stdin, e.g. `cat xxx.yaml|gxnpuc`
        config_dict = yaml.safe_load(sys.stdin)
        config_dict["IS_QUANT"] = quant
        config_dir = ""
    return config_dir, config_dict


def load_1_0(config_dict, config_para):
    Config_1_0.load_config(config_dict, config_para)

def load_1_2(config_dict, config_para):
    Config_1_2.load_config(config_dict, config_para)

def load_1_5(config_dict, config_para):
    Config_1_5.load_config(config_dict, config_para)

def load_1_6(config_dict, config_para):
    Config_1_6.load_config(config_dict, config_para)

def run_1_0():
    compiler_1_0.run()

def run_1_2():
    compiler_1_2.run()

def run_1_5():
    compiler_1_5.run()

def run_1_6():
    compiler_1_6.run()

def quant_1_2():
    compiler_1_2.quant()

COREMAP = {
    "LEO": {"load": load_1_0, "run":run_1_0},
    "APUS": {"load": load_1_2, "run":run_1_2, "quant":quant_1_2},
    "GRUS": {"load": load_1_5, "run":run_1_5},
    "AQUILA": {"load": load_1_6, "run":run_1_6},
    "V100": {"load": load_1_0, "run":run_1_0},
    "V120": {"load": load_1_2, "run":run_1_2, "quant":quant_1_2},
    "V150": {"load": load_1_5, "run":run_1_5},
    "V160": {"load": load_1_6, "run":run_1_6},
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="gxnpuc", description="NPU Compiler")
    parser.add_argument("-V", "--version", action="version", version="gxnpuc %s" % VERSION)
    parser.add_argument("-L", "--list", action="store_true", help="list supported ops")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbosely list the processed ops")
    parser.add_argument("-m", "--meminfo", action="store_true", help="verbosely list memory info of ops")
    parser.add_argument("-w", "--weights", action="store_true", help="print compressed weights (GRUS only)")
    parser.add_argument("-s", "--save_hist", action="store_true", help="save histograms of weights value to 'npu_jpgs' directory (GRUS only)")
    parser.add_argument("-q", "--quant", action="store_true", help="inference and generate quant file")
    parser.add_argument("config_filename", nargs="?", default=sys.stdin, help="config file")
    args = parser.parse_args()
    if args.list:
        from npu_compiler.v100.ops import OpsFactory as OpsFactory_1_0
        from npu_compiler.v120.ops import OpsFactory as OpsFactory_1_2
        from npu_compiler.v150.ops import OpsFactory as OpsFactory_1_5
        print(OpsFactory_1_0.get_tf_ops_note())
        print(OpsFactory_1_2.get_tf_ops_note())
        print(OpsFactory_1_5.get_tf_ops_note())
        sys.exit(0)
    elif args.config_filename:
        config_dir, config_dict = get_config_from_file(args.config_filename, args.quant)
    else:
        parser.print_help()
        sys.exit(0)

    config_para = {"VERBOSE": args.verbose, "MEMINFO": args.meminfo, "PRINT_WEIGHTS": args.weights,\
            "SAVE_HIST": args.save_hist, "CONFIG_DIR": config_dir}
    corename = config_dict.get("CORENAME", "")
    core_funcs = COREMAP.get(corename, {})
    if not core_funcs:
        print("CORENAME not supported!")
        sys.exit(1)

    core_funcs.get("load")(config_dict, config_para)
    if args.quant:
        if not core_funcs.get("quant"):
            print("CORENAME '%s' doesn't need to run quantized inference" % corename)
            sys.exit(1)
        core_funcs.get("quant")()
    else:
        core_funcs.get("run")()
