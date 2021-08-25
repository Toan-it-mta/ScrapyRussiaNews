import json
import pandas as pd
import re
import jsonlines
import requests

def split_msk_links(path_to_file_json_links='./result/msk_all_links.jl'):
    # Chia các link thành 3 phần:
    regexs = ['^https:\/\/www\.msk\.kp\.ru\/online\/news\/[0-9]{0,}\/',
              '^https:\/\/www\.kp\.ru\/daily\/[0-9\.]{0,}\/[0-9\.]{0,}\/', '^\/daily\/[0-9.]{0,}\/[0-9.]{0,}\/',
              '^\/online\/news\/[0-9.]{0,}\/']
    jsonObj = pd.read_json(path_or_buf=path_to_file_json_links, lines=True)
    group1 = []
    group2 = []
    group3 = []
    group4 = []
    # print(jsonObj)
    for obj in jsonObj['href']:
        if re.match(regexs[0], obj):
            group1.append(obj)
        elif re.match((regexs[1]), obj):
            group2.append(obj)
        elif re.match((regexs[2]), obj) or re.match(regexs[3], obj):
            group3.append('https://www.kp.ru{}'.format(obj))
        else:
            group4.append(obj)

    result = set(group1 + group2 + group3)
    sorted(result)


    df = pd.DataFrame(result, columns=['href'])
    df.to_json('last_msk_links.jl', orient='records', lines=True)


if __name__ == '__main__':
    split_msk_links()
