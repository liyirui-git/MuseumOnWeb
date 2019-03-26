# 利用THULAC的用户词典功能，重新封装了一个可以按照自己的词典路径自行决定
import thulac
import io


class myLA:
    def __init__(self, addr):
        self.thu = thulac.thulac(user_dict=addr)

    def normal(self, s):
        text = self.thu.cut(s, text=True)  # 进行一句话分词
        return text

    def get_word(self, s):
        text = self.normal(s)
        text_return = []
        for element in text.split(' '):
            text_return.append(element.split('_')[0])
        return text_return
        # for s in text.split():
        #     if s.find('_uw') != -1:
        #         return s.split('_uw')[0]


# 加载带编号的列表
def load_dict_from_file(filepath):
    _list = []
    try:
        with io.open(filepath, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                (key, value) = line.strip().split('$')  # 将原本用$分开的键和值用冒号分开来，存放在列表中。
                element = []
                element.append(key)
                element.append(value)
                _list.append(element)

    except IOError as ioerr:
        print("文件 %s 不存在" % (filepath))

    return _list
