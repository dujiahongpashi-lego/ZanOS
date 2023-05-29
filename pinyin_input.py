import json


class Pinyin_Input:
    def __init__(self) -> None:
        self.input_char = ''
        self.page = 0
        self.result = []
        self.f = open('zhCN.dict', 'r', encoding='UTF-8')
        self.dict_lines = []
        for line in self.f:
            self.dict_lines.append(line)

    def _update_result(self):
        for line in self.dict_lines:
            pinyin_line = line.split(':')
            if pinyin_line[0] == self.input_char:
                self.result = json.loads(pinyin_line[1])
                break

    def _get_line_encode_str(self, result, page):
        str = bytearray()
        no = 0x30
        for words in result[page*4:]:
            no += 1
            str.append(no)  # 序号
            str.append(0x2E)  # 分隔符
            for one_byte in words:
                str.append(int(one_byte))
        return bytes(str)

    def reset(self):
        self.input_char = ''
        self.page = 0
        self.result = []

    def input(self, input):
        if input == '=':  # 翻页
            self.page += 1
        elif input == '-' and self.page > 0:  # 翻页
            self.page -= 1
        elif input == '[BACKSPACE]':
            self.input_char = self.input_char[:-1]
        elif len(input) == 1 and input.isalpha() and input.islower():
            self.input_char += input

        self._update_result()
        return self._get_line_encode_str(self.result, self.page)

    def get_pinyin(self):
        return self.input_char

    def get_result(self):
        return self.result

    def get_selected_word(self, no):
        b = bytearray()
        for one_byte in self.result[no + self.page * 4]:
            b.append(int(one_byte))  # 2字节是一个汉字
        return b

    def next_page(self):
        pass

    def pre_page(self):
        pass
