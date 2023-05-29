import os
class FS:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.files = self._resort_files(os.listdir())
    
    def _resort_files(self, filenames):
        # By ChatGPT
        # 创建两个空数组，用于存放含有 . 字符和不含有 . 字符的字符串
        contains_dot_arr = []
        not_contains_dot_arr = []

        # 遍历字符串数组，将含有 . 字符和不含有 . 字符的字符串分别添加到对应的数组中
        for s in filenames:
            if s == 'System Volume Information':
                pass
            elif s.find(".") != -1: # 或者 s.index(".") != -1
                contains_dot_arr.append(s)
            else:
                not_contains_dot_arr.append(s)
        
        filenames_list = sorted(not_contains_dot_arr, key=str.lower) + sorted(contains_dot_arr, key=str.lower)
        files = []
        for f in filenames_list:
            files.append({
                'name': f,
                'type': ['FOLDER', 'FILE'][f.find(".") != -1],
                'show_name':['[' + f +']', ' ' + f][f.find(".") != -1]
            })
        
        return files
    
    def goto_dir(self,dir):
        os.chdir(dir)
        self.current_dir = os.getcwd()
        self.files = self._resort_files(os.listdir())
    
    def get_files(self):
        return self.files
    
    def get_current_folder_show_name(self):
        current_folder = 'FileSystem'
        if self.current_dir != '/flash':
            current_folder =  '.' + self.current_dir[self.current_dir.rfind('/') :]
        return current_folder
    
    def open(self, filename):
        for tail in ('.txt', '.reg', '.dict', '.bin', '.inf', '.py'):
            if filename.endswith(tail):
                f = open(filename, 'r', encoding='UTF-8')
                lines = []
                for line in f:
                    lines.append(line.strip())
                return lines
        
    def save(self, filename, lines): # By ChatGPT
        with open(filename, 'w') as file:
            file.write('\n'.join(lines))
            
