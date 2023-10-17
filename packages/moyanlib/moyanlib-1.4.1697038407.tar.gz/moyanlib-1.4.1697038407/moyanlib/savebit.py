import struct
import base64

FORMAT_STR = "<22s25s"

def dumps(data):
    global FORMAT_STR
    new_dict = []
    format_list = []
    
    for key, value in data.items():
        if isinstance(value, dict):
            # 如果值是字典，则进行递归调用dumps()函数
            packed_value = dumps(value)
        elif isinstance(value, bytes):
            packed_value = value
        else:
            packed_value = str(value)
        
        dbs = str(key) + ":;::;:" + str(packed_value)
        new_dict.append(dbs.encode())
        format_list.append(f"{len(dbs)}s")
    
    FORMAT_STR = " ".join(format_list)
    
    # 使用 struct.pack() 打包数据
    packed_data = struct.pack("".join(format_list), *new_dict)
    b64_packed_data = base64.b64encode(packed_data)
    print("打包完毕")
    return b64_packed_data

def load(packed_data:bytes):
    print("开始解包")
    print(type(packed_data).__name__)
    global FORMAT_STR
    packed_data = base64.b64decode(packed_data)
    # 使用 struct.unpack() 解包数据
    unpacked_data = struct.unpack(FORMAT_STR, packed_data)
    
    ok_data = [item.rstrip(b'\x00').decode('utf-8') for item in unpacked_data]
    ok_dict = {}

    for i in ok_data:
        i_kv = i.split(":;::;:")
        key = i_kv[0]
        value = i_kv[1]
        if ":" in value or "b'"in value:
            print(value.rstrip("'").strip("'"))
            # 如果值中包含 ":", 则进行递归调用load()函数
            value = load(value)
        
        ok_dict[key] = value
    
    return ok_dict

def test():
    data = {
        "name": "xiaoming",
        "age": 18,
        "hobby": {
            "sport": True,
            "game": False,
            "movie": True
        },
        "skill": [
            "python",
            "java",
            "c"
        ]
    }

    packed_data = dumps(data)
    #print(packed_data)
    unpacked_data = load(packed_data)
    print(unpacked_data)
if __name__ == "__main__":
    test()
