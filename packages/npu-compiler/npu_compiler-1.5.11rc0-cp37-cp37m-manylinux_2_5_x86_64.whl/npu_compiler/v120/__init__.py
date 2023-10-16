#coding: utf-8
import os

import tensorflow as tf
from tensorflow.python.framework import graph_util
from tensorflow.python.framework import ops

from npu_compiler.v120.config import Config
from npu_compiler.v120.compiler import run

from . import __file__

def compile_model(config_file):
    Config.parse_config(config_file, {"QUIET":True})
    Config.parse_para()
    Config.check_config()
    run()

def update_npu_model(sess, output_nodes, pb_path, config_path):
    constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph_def, output_nodes)
    with tf.gfile.FastGFile(pb_path, mode='wb') as f:
        f.write(constant_graph.SerializeToString())
    compile_model(config_path)

