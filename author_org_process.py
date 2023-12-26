import json
import re
from json_file_process import *


def author_afl_process(filename): # 构建字典，{name:作者名，affiliations：单位列表，papers：作品列表}
    with open(filename, 'r', encoding='utf-8') as f:
        existing_entries = json.load(f)

    certain_author_count = 0
    author_dics=[]
    for entry in existing_entries[1:]:
        # UID = f"{year}{index(entry)+1}"这个UID的生成应该写到预处理里，给每一篇文章一个
        author_list = entry.get('authors')  # 一定存在的列表
        afl_list = entry.get('affiliations')
        tag_list = entry.get('tags')
        uid=entry.get('uid')

        if "incomplete" in tag_list:
            continue

        if ("with nums" in tag_list) or len(author_list) == 1 or len(afl_list) == 1:  # 作者和单位能够唯一确定
            try:
                for author_name in author_list:
                    author_dic = dict()
                    numbers_at_end = re.findall(r'\d', author_name)  # 可能不止一个数字，以,分隔
                    if numbers_at_end:  # 如果找到数字
                        author_name_without_num = re.sub(r'\d', '', author_name)  # 去除作者名字末尾的数字
                        author_name_without_num = re.sub(r',', '', author_name_without_num)  # 去除,
                        author_dic['name']=author_name_without_num
                        author_dic['affiliations']=[]
                        for number_at_end in numbers_at_end:
                            author_dic['affiliations'].append(afl_list[int(number_at_end) - 1])
                    else:  # 如果没找到数字
                        author_dic['name']=author_name
                        author_dic['affiliations'] = []
                        for afl in afl_list:
                            author_dic['affiliations'].append(afl)
                    author_dic["papers"]=[]# 创建作品列表并添加uid
                    author_dic["papers"].append(uid)
                    author_dics.append(author_dic)
                certain_author_count += 1  # 执行完没问题才计数
            except IndexError:
                entry['tags'].append("with problems")
                print(f"{entry['title']}with problems")
    print(f'{filename}中条目完整且作者和单位能够准确对应的比例{certain_author_count/(len(existing_entries)-1)}')
    overwrite_to(filename,existing_entries)
    return author_dics


if __name__=='__main__':
    province = "北京"
    for year in range(2010, 2023):
        filename = '%s/%sresult%d.json' % (province, province, year)
        result_filename='%s/%sauthor%d.json' % (province, province, year)
        new_json_file(result_filename,author_afl_process(filename))
    # filename = '%s/%sresult%d.json' % (province, province, 2012)
    # result_filename = '%s/%sauthor%d.json' % (province, province, 2012)
    # new_json_file(result_filename, author_afl_process(filename))







