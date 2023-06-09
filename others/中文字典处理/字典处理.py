import struct
dict_file_1 = 'simplifiedChineseCharacter.yaml'  # 中文字典
dict_file_2 = 'simp.dict.yaml'  # 中文字词典
out_put_dir = './out/'
# 输出目标文件名：
out_dict_file = 'zhCN.dict'
out_put_file_cn_char_to_gbk = 'cn_char_to_gbk.json'  # 字到GBK的映射
out_put_file_pinyin_to_cn_char = 'pinyin_to_cn_char.json'  # 拼音到字的映射
out_put_file_pinyin_to_cn_char_word = 'pinyin_to_cn_char_word.json'  # 拼音到字和词的映射
out_put_file_pinyin_to_gbk = 'pinyin_to_gbk.json'  # 拼音到字GBK的映射
out_put_file_pinyin_to_gbk_all = 'pinyin_to_gbk_all.json'  # 拼音到字和词GBK的映射

_COMMON_DEGRESS = 400  # 常见度阈值，低于阈值的字直接排除
_WORD_COMMON_DEGRESS = 500  # 常见度阈值，低于阈值的词直接排除
_WORD_GROUP_COMMON_DEGRESS = 500  # 常见度阈值，低于阈值的词组直接排除

DEGREES = [0, _COMMON_DEGRESS, _WORD_COMMON_DEGRESS,
           _WORD_GROUP_COMMON_DEGRESS, _WORD_GROUP_COMMON_DEGRESS]


def parse_line(line):
    e = line.split(' ')
    cn_word = e[0]
    pinyin = ''.join(e[1:-1])
    usage = e[-1]  # 常见度
    return {'words_count': len(cn_word), 'cn_word': cn_word, 'pinyin': pinyin, 'usage': usage}


def get_lines_of_file(filename):  # 筛选原始字典文件中有用的行并格式化为对象列表
    f = open(filename, "r", encoding='utf-8')
    lines = []
    for line in f:
        line_info = parse_line(line)
        if int(line_info['usage']) > DEGREES[line_info['words_count']]:
            lines.append(line_info)
    return lines


def get_pinyin_dict_of_file(filename):  # By ChatGPT
    lines = get_lines_of_file(filename)
    print(filename + '  过滤后字词数 ' + str(len(lines)))
    dct = {}
    for item in lines:
        key = item['pinyin']
        if key in dct:
            dct[key].append(item)
        else:
            dct[key] = [item]

    for key in dct:  # 将值排序
        # print(dct[key])
        dct[key] = sorted(dct[key], key=lambda x: int(x['usage']), reverse=True)
        # print(dct[key])
    return dct


def get_gbk_list(same_pinyin_words_list):
    gbk_list = []
    for e in same_pinyin_words_list:
        bytedata = e['cn_word'].encode("gbk")
        gbk = []
        for byte in bytedata:
            int_data = struct.unpack('<B', bytes([byte]))[0]  # 使用struct模块转换
            gbk.append(int_data)
        gbk_list.append(gbk)
    return gbk_list


def get_word_list(same_pinyin_words_list):
    words = []
    for e in same_pinyin_words_list:
        words.append(e['cn_word'])
    return words


def make_pinyin_dict_file(dict_type, in_file, out_file,  out_file_type='json'):
    dct = get_pinyin_dict_of_file(in_file)
    func = {
        'pinyin_to_gbk': get_gbk_list,
        'pinyin_to_word': get_word_list
    }[dict_type]
    lines = []
    sorted_keys = sorted(dct.keys())
    if out_file_type == 'json':
        for key in sorted_keys:
            lines.append('"'+key + '":' + str(func(dct[key])))
        with open(out_file, "w", encoding="utf-8") as file:
            file.write("{")
            for l in lines:
                file.write(l + ',' + "\n")
            file.write("}")
    else:
        for key in sorted_keys:
            lines.append(key + ':' + str(func(dct[key])))
        with open(out_file, "w", encoding="utf-8") as file:
            file.write("")
            for l in lines:
                file.write(l + "\n")


make_pinyin_dict_file('pinyin_to_gbk', dict_file_1,
                      out_put_dir + out_put_file_pinyin_to_gbk)
make_pinyin_dict_file('pinyin_to_gbk', dict_file_2,
                      out_put_dir + out_put_file_pinyin_to_gbk_all)
make_pinyin_dict_file('pinyin_to_word', dict_file_1,
                      out_put_dir + out_put_file_pinyin_to_cn_char)
make_pinyin_dict_file('pinyin_to_word', dict_file_2,
                      out_put_dir + out_put_file_pinyin_to_cn_char_word)
make_pinyin_dict_file('pinyin_to_gbk', dict_file_1,
                      out_put_dir + out_dict_file, 'dict')
