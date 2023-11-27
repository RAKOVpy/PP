# Первая сырая тестовая версия
# По двум текстам находит совпадения только по названиям определенных инструментов

kurs_text = """

"1. Написание безопасного и устойчивого к изменениям кода на TypeScript
2. Проектирование архитектуры веб-приложений
3. Использование TypeScript при разработке компонентов в Angular и React.js"

"1. TypeScript
2. Основы веб-разработки
3. Архитектура веб-приложений"




"""

gpt_test_now = """
1. **Языки программирования:**
   - *JavaScript*: Аналоги - TypeScript, CoffeeScript.
   - *Python:* Аналоги - Ruby, Java, C++, JavaScript.
   - *Ruby:* Аналоги - Python, JavaScript, PHP.

2. **HTML/CSS:**
   - *HTML:* Аналоги - XML, XHTML.
   - *CSS:* Аналоги - SASS, LESS.

3. **Фреймворки и библиотеки:**
   - *React (JavaScript):* Аналоги - Angular, Vue.js.
   - *Angular (JavaScript):* Аналоги - React, Vue.js.
   - *Vue.js (JavaScript):* Аналоги - React, Angular.
   - *Django (Python):* Аналоги - Flask, Pyramid.
   - *Flask (Python):* Аналоги - Django, Pyramid.

4. **Базы данных:**
   - *SQL:* Аналоги - MySQL, PostgreSQL, SQLite.
   - *NoSQL:* Аналоги - MongoDB, CouchDB, Cassandra.

5. **Протоколы HTTP и HTTPS:**
   - *HTTP:* Аналоги - FTP, SMTP.
   - *HTTPS:* Аналоги - HTTP/2, SPDY.

6. **Безопасность веб-приложений:**
   - *Защита от инъекций:* Аналоги - Предотвращение SQL-инъекций, XSS-инъекций.
   - *Контроль доступа:* Аналоги - RBAC (ролевой доступ), ABAC (атрибутивный доступ).
   - *Шифрование данных:* Аналоги - TLS, SSL.
"""

alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alph += alph.lower()


def get_raw_words(gpt_ans):
    def is_word_is_eng(word):
        for symbol in word:
            if symbol in alph:
                return True
        return False

    gpt_ans_lines = gpt_ans.split('\n')
    raw_wards = [[]]
    chesk_new_word = False
    new_word_symbols = ':,;.-()*'
    for line in gpt_ans_lines:
        # print(line)
        line_split = line.split(' ')
        # print(line_split)

        for word in line_split:
            # print(word)
            if len(word) > 0 and not chesk_new_word:
                chesk_new_word = '(' in word.strip()
            if len(word) > 0 and word[0] not in alph:
                chesk_new_word = True
            if is_word_is_eng(word):
                if chesk_new_word:
                    raw_wards.append([word])
                    chesk_new_word = False
                else:
                    raw_wards[-1].append(word)
            if len(word) > 0 and not chesk_new_word:
                chesk_new_word = word.strip()[-1] in new_word_symbols

        chesk_new_word = True
        # print('_' * 50)
    # print(raw_wards)
    return raw_wards


def get_norm_word(word):
    ans = ''
    for i in word:
        if i not in '*,()\"':
            ans += i.lower()
    if ans[-1] in '.:':
        return ans[:-1]
    return ans


def get_norm_list(array_raw_words):
    array_ans = []
    for word in array_raw_words:
        ans = ''
        for word_i in word:
            ans += get_norm_word(word_i) + ' '
        if len(ans) > 0:
            array_ans.append(ans[:-1])

    return set(array_ans)


def get_dict_komp():
    d = dict()

    with open('komp.txt', 'r', encoding='utf-8') as f:
        all = f.readlines()
        for i in all:
            temp = i[:-1].split('	')
            temp[-1] = temp[-1][:-1] if temp[-1][-1] == '.' else temp[-1]
            add = []
            for j in temp[1].split(','):
                add.append(j.lower().strip())
            add += get_norm_list(get_raw_words(temp[0]))
            d[temp[0]] = add

    return d


array_proff = get_norm_list(get_raw_words(gpt_test_now))
array_kurs = get_norm_list(get_raw_words(kurs_text))
# for i in array_kurs:
#     print(i)

d_komp = get_dict_komp()


def alg_curr(a):
    komp_val_sort = []
    for komp_i in d_komp:
        cnt = 0
        for nav in d_komp[komp_i]:
            cnt += nav in a
        komp_val_sort.append([komp_i, cnt])

    komp_val_sort.sort(key=lambda x: x[-1], reverse=True)
    return komp_val_sort


def get_dict_curr(a):
    d = dict()
    for i in a:
        if i[-1] > 0:
            d[i[0]] = i[-1]
    return d


proff_curr = alg_curr(array_proff)
kurs_curr = alg_curr(array_kurs)
d_ans_proff = get_dict_curr(proff_curr)
d_ans_kurs = get_dict_curr(kurs_curr)

# for i in d_ans_proff:
#     print(i, d_ans_proff[i])
# print()
# for i in d_ans_kurs:
#     print(i, d_ans_kurs[i])
counter = 0
for i in d_ans_proff:
    if i in d_ans_kurs:
        counter += d_ans_kurs[i]
# print()
print(counter)
