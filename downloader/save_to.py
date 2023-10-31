import json

'''
把每一条entry的结果存到JSON文件里,或许还可以直接存成sql形式，
或先全部存为json，然后再在mySQL中进行数据库的构建
'''


def save_to(filename, entry):
    try:
        # utf-8将一个汉字编码为3个字节,gbk将一个汉字编码为2个字节,
        with open(filename, 'r',encoding='utf-8') as f:
            existing_data = json.load(f)
            existing_data.append(entry)  # 增加条目
        with open(filename, 'w',encoding='utf-8') as new_f:  # 重新写入
            json.dump(existing_data, new_f,ensure_ascii=False,indent=4) # 最后一个参数会保证dump之后的结果所有的字符都能被ascii表示
            # if entry.get('篇名',[]): # 输出文献的标题
            #     print(f"{entry['篇名']}saved")
    except json.decoder.JSONDecodeError:
        print('Make sure the json file is in valid format,[{},{}...]')


if __name__ == '__main__':
    my_filename = 'TCM_journal.json'
    entry_instance = {'name': 'Bob',
                      'age': 35, }

    save_to(my_filename, entry_instance)
