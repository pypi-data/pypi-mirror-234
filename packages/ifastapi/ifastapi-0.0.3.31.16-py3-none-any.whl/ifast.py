import os
import shutil
import sys
import zipfile


def main():
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case 'init':
                copy_file()


def copy_file():
    # 拷贝文件到运行目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    zip_directory = os.path.dirname(current_directory)
    zip_directory = os.path.dirname(zip_directory)
    # 要复制的目录名称
    zip_file_name = 'init_builder.zip'
    destination_dir = os.getcwd()

    # 压缩包文件路径
    zip_file_path = os.path.join(zip_directory, zip_file_name)

    # 打开压缩包
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # 解压所有文件到目标目录
        zip_ref.extractall(destination_dir)
