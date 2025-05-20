import glob
import os
import subprocess
import json
import importlib.util
from google.protobuf import descriptor_pb2, message_factory
from google.protobuf.json_format import MessageToDict


def delete_files(*folder_path):
    extensions = [".py", ".db", ".json"]
    for folder in folder_path:
        for extension in extensions:
            # 获取指定文件夹下的所有符合扩展名的文件路径
            files = glob.glob(os.path.join(folder, f"*{extension}"))

            # 遍历所有文件并删除
            for file in files:
                if "__init__.py" == os.path.basename(file):
                    continue
                else:
                    try:
                        os.remove(file)
                        print(f"Deleted: {file}")
                    except Exception as e:
                        print(f"Failed to delete {file}: {e}")


def compile_proto_files():
    """编译proto文件并生成Python文件和描述符文件"""
    output_folder = r"{}\protobuf_py".format(os.path.dirname(os.path.abspath(__file__)))

    proto_folder = r"{}\protobuf_file".format(
        os.path.dirname(os.path.abspath(__file__))
    )

    json_folder = os.path.join(
        r"{}\protobuf_json".format(os.path.dirname(os.path.abspath(__file__)))
    )
    # 清空编译的文件
    delete_files(output_folder, json_folder)

    # 创建输出目录如果它不存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        with open(os.path.join(output_folder, "__init__.py"), "w") as f:
            f.write(
                "# This file is required for Python to recognize the folder as a module"
            )
            print(f"Created: {os.path.join(output_folder, '__init__.py')}")

    # 遍历proto_folder中的所有文件
    for filename in os.listdir(proto_folder):
        if filename.endswith(".proto"):
            proto_file = os.path.join(proto_folder, filename)
            # 调用protoc命令来生成Python文件和描述符文件
            command = [
                "protoc",
                f"--python_out={output_folder}",
                f"--proto_path={proto_folder}",
                f"--descriptor_set_out={os.path.join(output_folder, filename + '.pb')}",
                proto_file,
            ]
            subprocess.run(command, check=True)

            print(f"Compiled {filename} to {output_folder}")


def parse_descriptor(descriptor_path):
    """解析生成的描述符文件"""
    with open(descriptor_path, "rb") as f:
        file_desc_set = descriptor_pb2.FileDescriptorSet()
        file_desc_set.MergeFromString(f.read())
    return file_desc_set


def set_default_values(message):
    """递归地为所有字段设置默认值"""
    for field in message.DESCRIPTOR.fields:
        if field.label == field.LABEL_REPEATED:
            continue
        if field.type == field.TYPE_MESSAGE:
            nested_message = getattr(message, field.name)
            set_default_values(nested_message)
        elif field.type == field.TYPE_STRING:
            setattr(message, field.name, f"default_{field.name}")
        elif field.type in {
            field.TYPE_INT32,
            field.TYPE_INT64,
            field.TYPE_UINT32,
            field.TYPE_UINT64,
        }:
            setattr(message, field.name, 0)
        elif field.type == field.TYPE_DOUBLE:
            setattr(message, field.name, 0.0)
        elif field.type == field.TYPE_BOOL:
            setattr(message, field.name, False)


def proto_to_json(output_folder):
    """将描述符文件中的所有Protobuf消息转换为带有默认值的JSON文件"""
    for filename in os.listdir(output_folder):
        if filename.endswith(".pb"):
            descriptor_path = os.path.join(output_folder, filename)
            descriptor_set = parse_descriptor(descriptor_path)

            json_data_all_messages = {}  # 存储所有消息类型的 JSON 数据

            for file_descriptor in descriptor_set.file:
                module_name = (
                    os.path.splitext(os.path.basename(file_descriptor.name))[0] + "_pb2"
                )
                spec = importlib.util.spec_from_file_location(
                    module_name, os.path.join(output_folder, module_name + ".py")
                )
                proto_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(proto_module)

                for message_type in file_descriptor.message_type:
                    message_name = message_type.name
                    message_class = getattr(proto_module, message_name)
                    message_instance = message_class()
                    set_default_values(message_instance)
                    json_data = MessageToDict(
                        message_instance,
                        # including_default_value_fields=True,
                        preserving_proto_field_name=True,
                    )
                    json_data_all_messages[message_name] = json_data

            json_output_path = os.path.join(
                r"{}\protobuf_json".format(os.path.dirname(os.path.abspath(__file__))),
                f"default_{os.path.splitext(filename)[0].lower()}.json",
            )
            with open(json_output_path, "w") as json_file:
                json.dump(json_data_all_messages, json_file, indent=2)
            print(f"Generated JSON file: {json_output_path}")


if __name__ == "__main__":

    # 编译proto文件
    compile_proto_files()
    output_folder = r"{}\protobuf_py".format(os.path.dirname(os.path.abspath(__file__)))

    import sys

    sys.path.append(
        r"{}\protobuf_py".format(os.path.dirname(os.path.abspath(__file__)))
    )
    # 将proto消息转换为带默认值的JSON文件
    proto_to_json(output_folder)
