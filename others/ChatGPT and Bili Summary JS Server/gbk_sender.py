
import requests
import json
import binascii


# encode 接口
bytess = b'\xc4\xe3\xba\xc3nodejs\xb0\xa1'
print(str(bytess)[2:-1])
r = requests.get('http://localhost:3000?api=encode&data=' + str(bytess)[2:-1])

data = json.loads(str(r.text))['data']
the_bytes = binascii.unhexlify(data) # bytes 对象
gbk_str = the_bytes.decode('gbk') # by chatgpt.将形如bbd8d3a6c4e3bac36e6f64656a73b0a1的16进制字符串，转码为gbk编码的字符串，可直接用于支持gbk编码的显示设备

print(r.text, data, the_bytes,gbk_str)

# chatGPT 接口
# question = '地球含量最高的元素是?我指的是内部'.encode('gbk')
# print(question)
# r = requests.get('http://localhost:3000?api=chatgpt&data=' + str(question)[2:-1])
# data = json.loads(str(r.text))['data']
# gbk_str = binascii.unhexlify(data).decode('gbk')
# print(gbk_str)

# bilisumup 接口
# bvid = 'BV1d24y1F7HH'
# bvid = 'BV1rv4y1G7rD'
bvid = 'BV1Uv4y1h7Gb'
r = requests.get('http://localhost:3000?api=bilisumup&data=' + bvid)
data = json.loads(str(r.text))['data']
gbk_str = binascii.unhexlify(data).decode('gbk')
print(gbk_str)