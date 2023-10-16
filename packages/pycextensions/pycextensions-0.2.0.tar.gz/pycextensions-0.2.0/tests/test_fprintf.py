from conf import TestConfig

import pycextensions.fprintf as fpt


def test_fprintf():
    """测试 c 扩展中 fprintf 的方法"""
    save_str = "Hello ayuge"
    save_file = f"{TestConfig.test_data_dir}/save_file.txt"
    saved_str_len = fpt.fprintf(save_str, save_file)
    with open(save_file, "r") as f:
        read_str = f.read()

    assert all([read_str == save_str, len(save_str) == saved_str_len])
