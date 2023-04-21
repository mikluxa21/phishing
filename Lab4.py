from atexit import register
import sqlite3
import requests
from bs4 import BeautifulSoup
import ast
from colorama import Fore
from datetime import datetime

count_spam = 149250

conn = sqlite3.connect('world.db')
cur = conn.cursor()
#cur.execute("CREATE TABLE IF NOT EXISTS table_world(world TEXT, ncount INT);")

def SiteName(str_of_words):
    result = None
    for i in str_of_words.split(' '):
        if i[0:4] == "http":
            result = i
    return result

def GetDomain(str_email):
    return str_email.split('@')[1].split('.')[0]

def ToLowRegister(str_up_register):
    return str_up_register.lower().split(' ')[0]

def FindServer(str_http):
    return str_http.split('.')[-3]


def SenderProblem(str_text, str_from_email, str_from_name):
    print(Fore.RED)

    str_http = None
    site_name = SiteName(str_text)
    if site_name != None:
        str_http = FindServer(site_name)

    domain = GetDomain(str_from_email)
    company = ToLowRegister(str_from_name)
    result_summ = 0

    if  str_http != None and domain != None and str_http != domain:
        print('>> The link does not match the sender!')
        result_summ += 1

    if str_http != company and str_http != None:
        print('>> The link does not match the company!')
        result_summ += 1

    if domain != company and domain != None:
        print('>> The sender does not the company!')
        result_summ += 1

    return result_summ


def DetectedText(str_text):
    sql_querty_select_ncount = """SELECT ncount FROM table_world WHERE world = ?"""
    summ = 0
    for i in str_text.split(' '):
        cur.execute(sql_querty_select_ncount, (i, ))
        ncount = cur.fetchone()[0]
        if ncount > 0:
            summ += ncount

    if summ/count_spam > 0.7:
        print(Fore.RED + ">> The resulting word summ: ", int(100*summ/count_spam), " > 70")
        return 1
    else:
        print(Fore.GREEN + ">> The resulting word summ: ", int(100*summ/count_spam), " < 70")
        return 0

def TakeDateFromText(text):
    return text.split(' ')[2]

def CheckData(str_mes_data, str_text):
    str_text_data = TakeDateFromText(str_text)

    text_data = datetime.strptime(str_text_data, '%d.%m.%Y')
    mes_data = datetime.strptime(str_mes_data, '%Y-%m-%d')

    if text_data.year > mes_data.year:
        print('>> Error in tne date! (Year)')
        return 1
    elif text_data.year == mes_data.year and text_data.month > mes_data.month:
        print('>> Error in tne date! (Month)')
        return 1
    elif text_data.year == mes_data.year and text_data.month == mes_data.month and text_data.day > mes_data.day:
        print('>> Error in tne date! (Day)')
        return 1

    return 0


def AttachmentInMess(attachment):
    if attachment != None:
        last_simv = attachment[-3:]
        if last_simv == 'exe' or last_simv == 'zip' or last_simv == 'enc':
            print(Fore.YELLOW + '>> Dangerous attachment!', last_simv, Fore.RED)
            return 1
    return 0

if __name__ == '__main__':
    for z in range(0, 25):
        r = requests.get('https://vir-lab.ru')
        soup = BeautifulSoup(r.text, 'lxml')
        string = str(soup)[15:-18]

        result = ast.literal_eval(string)
        text = result['text']
        for t in result:
            print(t, ': ', result[t])

        sender_problemm = SenderProblem(result['text'], result['from_email'], result['from_name'])
        check_data = CheckData(result['date'], result['text'])
        attachment_in_mess = AttachmentInMess(result['attachment'])
        detected_text = DetectedText(result['text'])

        print('\n')

        result_count = sender_problemm + detected_text + check_data + attachment_in_mess
        if result_count == 0:
            print(Fore.GREEN + '>> NOT fishing')
        elif result_count > 0 and result_count < 3:
            print(Fore.YELLOW + '>> MAYBE fishing')
        elif result_count >= 3:
            print(Fore.RED + '>> FISHING')

        print(Fore.WHITE + '\n\n====================================================================================\n\n\n\n')
    conn.commit()




    '''
    print('\n\n>>  W - word;\n>>  P - the probability that the word spam;\n\n')
    print('W              P')

    for i in text_list:
        cur.execute(sql_querty_select_ncount, (i, ))
        ncount = cur.fetchone()[0]
        if ncount > 0:
            print(i, 100*ncount/count_spam, '%')
            summ += ncount

    print("\n\n>>  The resulting probability: ", 100*summ/count_spam)
    if summ/count_spam > 0.5:
        print(">>  Result: SPAM")
    else:
        print(">>  Result: NOT SPAM")
    '''



    '''
    sql_querty_select_all = """SELECT * FROM table_world ORDER BY ncount"""
    cur.execute(sql_querty_select_all)
    result = cur.fetchall()
    '''


    '''
    for i in result:
        if i[1] < 100 :
            sql_querty_update = """UPDATE table_world SET ncount = 0 WHERE world = ?"""
            cur.execute(sql_querty_update, (i[0], ))
        else:
            print(i[0], i[1], ' :')
            num = int(input())
            if num == 0:
                sql_querty_update = """UPDATE table_world SET ncount = 0 WHERE world = ?"""
                cur.execute(sql_querty_update, (i[0], ))
    '''

    '''
    def Insert_Id(str_world):
    sql_querty_count = """SELECT EXISTS (SELECT * FROM table_world WHERE world = ?);"""
    sql_querty_insert = """INSERT INTO table_world VALUES(?, ?)"""
    sql_querty_update = """UPDATE table_world SET ncount = ncount + 1 WHERE world = ?"""
    #sql_querty_select_all = """SELECT * FROM table_world"""

    cur.execute(sql_querty_count, (str_world, ))
    if cur.fetchone()[0] == 0:
        cur.execute(sql_querty_insert, (str_world, 1, ))
    else:
        cur.execute(sql_querty_update, (str_world, ))
    '''







