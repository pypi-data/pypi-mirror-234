import os
import sys


def write_text_to_file(filename: str, content: str, encoding="utf-8") -> bool:
    """
    把文本写入文件
    :author wjh
    :date 2023-05-18
    :param filename: 要写入的文件名。
    :param encoding: 文件编码，默认为utf-8
    :param content: 文本内容
    :return: 是否写入成功。
    """
    try:
        with open(filename, "w", encoding=encoding) as f:
            f.write(content)
    except Exception as e:
        return False

    return True


def read_text_from_file(filename, encoding="utf-8") -> str:
    """
    从指定文件中读取文本内容并返回。
    :author wjh
    :date 2023-05-18
    :param filename：要读取的文件名。
    :param encoding：文件的编码方式，默认为utf-8。
    :return: 从文件中读取到的文本内容。
    """
    with open(filename, "r", encoding=encoding) as file:
        text = file.read()
    return text


def read_text_by_line(filename, encoding="utf-8"):
    """
    逐行读取文本文件，返回一个数组。
    :author wjh
    :date 2023-09-05
    :param filename：要读取的文件名。
    :param encoding：文件的编码方式，默认为utf-8。
    :return: 从文件中读取到的文本内容。
    """
    with open(filename, 'r', encoding=encoding) as file:
        lines = [line.strip() for line in file]
    return lines


def get_parent_directory(current_directory, levels: int) -> str:
    """
    获取当前目录的上级目录路径
    :author wjh
    :date 2023-05-23
    :param current_directory: 当前目录的路径
    :param levels: 要获取的上级目录级数
    :return:
    """
    parent_directory = current_directory
    for _ in range(levels):
        parent_directory = os.path.dirname(parent_directory)

    return parent_directory
