def get_answer(prof_name):
    import copy
    import json
    import requests

    def get_dict_komp_weight_clear(d):
        t = copy.deepcopy(d)
        for i in t:
            for j in t[i]:
                t[i][j] = 0
            t[i]['weight'] = 0
        return t

    def connection(a_from, d_to):
        i_weight = 1
        j_weight = 1
        all_weight = 0
        for header_komp in d_komp:
            for komp in d_komp[header_komp]:
                for tool in d_komp[header_komp][komp]:
                    if tool in a_from:
                        d_to[header_komp][komp] += j_weight
                        d_to[header_komp]['weight'] += i_weight
                        all_weight += i_weight

        if all_weight != 0:
            for header_komp in d_to:
                d_to[header_komp]['weight'] /= all_weight

    def get_dict_komp(url):
        d = {}
        i = 0
        while True:
            re = requests.get(f'{url}/{i}')
            if str(re) != '<Response [200]>':
                break
            ans = json.loads(re.text)
            if ans['competencyMainTechnology'] not in d:
                d[ans['competencyMainTechnology']] = {}
            d[ans['competencyMainTechnology']][ans['competencyTitle']] = ans['competencyKnowledge']
            i += 1
        return d

    def get_list_proff(prof_name, url):
        i = 0
        re = requests.get(f'{url}/{i}')
        d = json.loads(re.text)
        if d['professionTitle'] == prof_name:
            return d['professionCompetencies']

    kurs_mark = dict()
    index_ = 0
    d_komp = get_dict_komp('http://127.0.0.1:8000/comp')
    array_proff = get_list_proff(prof_name, 'http://127.0.0.1:8000/profession')
    url_course = 'http://127.0.0.1:8000/course'
    while True:
        re = requests.get(f'{url_course}/{index_}')
        index_ += 1
        if str(re) != '<Response [200]>':
            break
        ans = json.loads(re.text)
        kurs_text = ans['courseTitle']
        array_kurs = set(ans['courseCompetencies'])

        weight_prof = get_dict_komp_weight_clear(d_komp)
        weight_kurs = get_dict_komp_weight_clear(d_komp)
        connection(array_proff, weight_prof)
        connection(array_kurs, weight_kurs)

        # for i in weight_prof:
        #     print(i)
        #     for j in weight_prof[i]:
        #         if weight_prof[i][j] != 0:
        #             print(j, weight_prof[i][j])
        #     print()

        # print('_' * 50)
        # print(kurs_key)
        # for i in weight_kurs:
        #     print(i)
        #     for j in weight_kurs[i]:
        #         if weight_kurs[i][j] != 0:
        #             print(j, weight_kurs[i][j])
        #     print()
        #
        # print('_' * 50)

        Plus = 0
        k_del = 5
        Loss = 0

        for header_komp in weight_prof:
            k_dot = weight_prof[header_komp]['weight']
            t = (weight_kurs[header_komp]['weight'] - weight_prof[header_komp]['weight']) * (1 - k_dot)
            if t > 0:
                if k_dot > 0.2:
                    Loss += t / k_del
                else:
                    Loss += t
            else:
                Loss += abs(t)
            for komp in weight_prof[header_komp]:
                if komp == 'weight':
                    continue
                if weight_prof[header_komp][komp] >= weight_kurs[header_komp][komp]:
                    Plus += weight_kurs[header_komp][komp] * k_dot
                else:
                    Plus += weight_prof[header_komp][komp] * k_dot

        answer = [Plus, -Loss]
        kurs_mark[ans['courseId']] = answer
        # print(answer)
        # print()
        # print('*' * 50)
        # print()

    # print(kurs_mark)
    ans = []

    for i in kurs_mark:
        ans.append([i, kurs_mark[i]])

    ans.sort(key=lambda x: x[-1], reverse=True)
    global_ans = []
    for i in ans:
        global_ans.append(i[0])
    # print(f'№: Курс | [Plus, -Loss]')
    # for i, j in enumerate(ans):
    #     for t in range(2):
    #         j[1][t] = round(j[1][t], 2)
    #     print(f'{i + 1}: {j[0]} | {j[1]}')

    return global_ans


print(get_answer('Web-разбраотчик'))
