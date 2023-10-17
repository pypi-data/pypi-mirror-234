import string
import random
import psutil
import platform as pf
import hashlib as h
def generate_verifi_code(wei:int = 4):
    """_summary_

    Keyword Arguments:
        wei -- 位数 (default: {4})

    Returns:
        生成的验证码
    """    
    # 生成所有可能出现在验证码中的字符
    characters = string.ascii_letters + string.digits

    # 生成8位随机验证码
    verification_code = "".join(random.choice(characters) for _ in range(wei))

    return verification_code

def getDeviceID():
    system_name = pf.platform()
    computer_name = pf.node()
    computer_system = pf.system()
    computer_bit = pf.architecture()[0]
    cpu_count = psutil.cpu_count()
    mem = psutil.virtual_memory()
    mem_total = format(float(mem.total) / 1024 / 1024 / 1024)
    id = system_name + "_"+computer_name + "_"+computer_system + \
        "_"+computer_bit+"_"+str(cpu_count)+"_"+mem_total
    # 对id进行sha1
    hash_id = h.sha1(id.encode("utf-16be")).hexdigest()
    big_hash_id = str(hash_id).upper()
    return big_hash_id
