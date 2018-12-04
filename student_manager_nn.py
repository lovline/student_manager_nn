__author__ = 'lovline'
'''
	this is the system main function.
'''
"""
    this is a employee-manager system
    its function is used by Python by lovline
    begin day : 2018-11-21
    update day: 2018-12-04
"""
import os
import re
from datetime import datetime
import time
import MySQLdb

curr_admin = 'admin'  #default admin#
stu_index = 0   #studend database index#
stu_info = []   #tempory record one line student infomation#
stu_sys_info = []   #total student infomations in system#
login_users = {
    'admin': '******',
    'user': '******'
}

conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='Nqwer123', db='student_info', charset='utf8')
cursor = conn.cursor()


def record_operation_or_security_log(who, content, eResult, iType):
    global conn, cursor
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into optseclog(who, contents, whenT, eResult, iType) values('%s', '%s', '%s', '%s', '%s')" \
          % (who, content, curr_time, eResult, iType)
    cursor.execute(sql)
    conn.commit()


def invalid_current_db_data():
    sql = "select * from student_info"
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(sql)
    conn.commit()
    for row in cursor.fetchall():
        if row is not ():
            change_t = int(list(row)[13]) + 1
            sql_del = "update student_info set data_status=0,update_time='%s',change_times=%d" \
                      % (update_time, change_t)
            cursor.execute(sql_del)
            conn.commit()


def initial_system():
    print '*** system initialing ***'
    #time.sleep(1.5)
    print '*** system initial succeed ***'
    #time.sleep(0.8)
    global conn, cursor, stu_index, stu_sys_info, curr_admin
    select_th, ret_msg = '', ''
    if 'admin' == curr_admin:
        select_th = raw_input('management is loading, '
                              'you can use original database by input other words or input [C] to create yours : ')
    if ('admin' == curr_admin) and ('c' == select_th or 'C' == select_th):
        # create a new management system#
        # sql = 'truncate table student'
        invalid_current_db_data()
        # time.sleep(1.5)
        print '*** congratulations! a new database has created succeed! ***'
        ret_msg = 'user [%s] create a new database.' % curr_admin
    else:
        #use original database#
        print '*** original database is loading ***'
        #time.sleep(1)
        print '*** congratulations! original database has loaded succeed! ***'
        ret_msg = 'user [%s] load the original database.' % curr_admin
    record_operation_or_security_log(curr_admin, ret_msg, 'succeed', 'opt_log')
    stu_index, stu_sys_info = query_current_data_from_db()


def is_valid_number(num):
    if len(num) > 1:
        return False
    elif re.search(r'[1|2|3|4|5|6]', num):
        return 1 <= int(num) <= 7
    return False


def have_record_data(username):
    global conn
    global cursor
    sql = "select * from student_info where user_name='%s'" % username
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    if result is not None:
        if 0 == list(result)[14]:
            return False
        #print type(cursor.fetchone()) #the cursor is step by step
        return list(result)[0]  #return primary key ID#
    else:
        return False


def query_current_data_from_db():
    global conn, cursor, stu_index, stu_sys_info
    stu_index = 0
    stu_sys_info = []
    sql = "select * from student_info"
    cursor.execute(sql)
    conn.commit()
    for row in cursor.fetchall():
        if 1 == list(row)[14]:
            stu_index += 1
            stu_sys_info.append(list(row))
    if 0 == stu_index:
        return 0, []
    return stu_index, stu_sys_info


def nn_add_student():
    global stu_index, stu_sys_info, conn, cursor
    print 'please input fellowing message and sperate as [space]'
    while True:
        student = raw_input('^username password[six numbers] sex[M|F] age[7-100] single[Y|N] address graduate_school'
                            ' company salay and whose_lover$ or q\Q to return back \n')
        if 'q' == student or 'Q' == student:
            break
        len_student = len(re.split('\s+', student))
        if 10 != len_student:
            ret_msg = 'input have too few or much parameters -- parameters len is need 10 yours are %d.\n' % len_student
            print ret_msg
            record_operation_or_security_log('admin', ret_msg, 'failure', 'opt_log')
            return 1  # parameters len is wrong#
        user_name, password, sex, age, single, address, graduate_school, company, salary, whose_lover \
            = re.split('\s+', student)
        # print user_name, password, sex, single, address, graduate_school, company, salary, whose_lover#
        if 0 == re.match(r'^[_A-Za-z1-9]+$', user_name):
            ret_msg = 'user name=[%s] is invalid.\n' % user_name
            print ret_msg
            record_operation_or_security_log('admin', ret_msg, 'failure', 'opt_log')
            continue  # invalid user name#
        if have_record_data(user_name):
            ret_msg = 'database have already own this record '
            print ret_msg
            record_operation_or_security_log('admin', ret_msg, 'failure', 'opt_log')
            continue
        if 0 == re.match('\d{6}', password):
            ret_msg = 'your input password is invalid.\n'
            print ret_msg
            record_operation_or_security_log('admin', ret_msg, 'failure', 'opt_log')
            continue
        if 'F' != sex and 'M' != sex:
            ret_msg = 'your input sex=[%s] is invalid.\n' % sex
            print ret_msg
            record_operation_or_security_log('admin', ret_msg, 'failure', 'opt_log')
            continue  # invalide sex#
        if int(age) < 7 or int(age) > 100:
            ret_msg = 'your input age=[%s] is invalid.\n' % age
            print ret_msg
            record_operation_or_security_log('admin', ret_msg, 'failure', 'opt_log')
            continue  # invalide age#
        if 'Y' != single and 'N' != single:
            ret_msg = 'your input singele=[%s] is invalid.\n' % single
            print ret_msg
            record_operation_or_security_log('admin', ret_msg, 'failure', 'opt_log')
            continue  # invalide sex#
        if 0 == re.match(r'^[_A-Za-z]+$', address):
            ret_msg = 'your input address=[%s] is invalid.\n' % address
            print ret_msg
            record_operation_or_security_log('admin', ret_msg, 'failure', 'opt_log')
            continue  # invalide address#
        if int(salary) < 0 or int(salary) > 100000:
            ret_msg = 'your input salary=[%s] is invalid.\n' % salary
            print ret_msg
            record_operation_or_security_log('admin', ret_msg, 'failure', 'opt_log')
            continue  # invalide salary#
        if 0 == re.match(r'^[_A-Za-z1-9]+$', whose_lover):
            ret_msg = 'your input whose_lover=[%s] is invalid.\n' % whose_lover
            print ret_msg
            record_operation_or_security_log('admin', ret_msg, 'failure', 'opt_log')
            continue  # invalid whose_lover#
        create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_time = create_time
        sql = "insert into student_info(user_name, password, sex, age, single, address, graduate_school, \
              company, salary, whose_lover, create_time, update_time, change_times, data_status)  \
              values('%s', '%s', '%s', %d, '%s', '%s', '%s', '%s', %d, '%s', '%s', '%s', %d, %d)" % \
              (user_name, password, sex, int(age), single, address, graduate_school, company, int(salary),
               whose_lover, create_time, update_time, 0, 1)
        cursor.execute(sql)
        conn.commit()
        stu_index, stu_sys_info = query_current_data_from_db()
        ret_msg = 'add student info succeed.\n'
        print ret_msg
        record_operation_or_security_log('admin', ret_msg, 'succeed', 'opt_log')
        #if lovers merge address and salary#
        #TODO#


def display_current_db_data(index, sys_info):
    global stu_index, stu_sys_info
    if stu_index != index or stu_sys_info != sys_info:
        tmp_index, tmp_sys_info = index, sys_info
    else:
        tmp_index, tmp_sys_info = stu_index, stu_sys_info
    print 'there are %d student-info in system, and they are : ' % tmp_index
    for index, info in enumerate(tmp_sys_info):
        if 0 == info[14]:
            #iStatus is False#
            continue
        info = [str(ele) for ele in info]  #convert non-str to str#
        info_no_pwd = info[1:2] + info[3:11]
        dsp_info = '  '.join(info_no_pwd)
        print '  No.%d --- %s' % (index + 1, dsp_info)


def nn_delete_student():
    global stu_index, stu_sys_info
    display_current_db_data(stu_index, stu_sys_info)
    del_user = raw_input('please choose one user you want to delete by user_name: ')
    del_id = have_record_data(del_user)
    if del_id:
        sql = "update student_info set data_status=0 where id=%s" % del_id
        cursor.execute(sql)
        conn.commit()
        print 'delete user [%s] succeed.' % del_user
        #time.sleep(1)
    else:
        print 'delete user fail, user_name [%s] is not in system.' % del_user


def nn_update_student():
    pass


def according_to_query_type_display(q_type, little=0, larger=0):
    global stu_sys_info
    query_count = 0
    tmp_stu_info = []
    if 0 == little == larger:
        for info in stu_sys_info:
            tmp_stu_info.append(info)
            query_count += 1
        tmp_stu_info.sort(key=lambda ele: int(ele[q_type]), reverse=False)
    else:
        if larger > 100:
            q_type = 9
        for info in stu_sys_info:
            if little <= int(info[q_type]) <= larger:
                tmp_stu_info.append(info)
                query_count += 1
    display_current_db_data(query_count, tmp_stu_info)


def according_to_query_key_word_display(key_words):
    global stu_sys_info
    query_count = 0
    tmp_stu_info = []
    for q_type in range(6, 11):
        for index, info in enumerate(stu_sys_info):
            if key_words == info[q_type]:
                tmp_stu_info.append(info)
                query_count += 1
        else:
            if 0 != query_count:
                break
    display_current_db_data(query_count, tmp_stu_info)


def according_to_query_directory_display():
    global stu_sys_info
    cunt_name, cunt_address, cunt_school, cunt_company = 0, 0, 0, 0
    name, address, school, company = [], [], [], []
    for ind, info in enumerate(stu_sys_info):
        if info[1] not in name:
            cunt_name += 1
            name.append(info[1])
        if info[6] not in address:
            cunt_address += 1
            address.append(info[6])
        if info[7] not in school:
            cunt_school += 1
            school.append(info[7])
        if info[8] not in company:
            cunt_company += 1
            company.append(info[8])
    lst_key = [cunt_name, cunt_address, cunt_school, cunt_company]
    lst_value = [name, address, school, company]
    result_lst = [lst_key, lst_value]
    return result_lst


def nn_display_student():
    global stu_index, stu_sys_info
    if 0 == stu_index:
        print 'there are no student info in system please choose 1 to add.\n'
        return
    #query type to judge which method query#
    request_msg = 'we offer three types to query messages : \n' \
                     '  [1] display all informations\n' \
                     '  [2] according to [age] display informations\n' \
                     '  [3] according to [salary] display informations\n' \
                     '  [4] display the infor between ages eg:24-68 or salary 5000-7000 \n' \
                     '  [5] acording to key-word display informationsn\n' \
                     '  [6] display how many different types in system'
    print request_msg
    while True:
        q_type = raw_input('please input query condition [1-6] or q/Q to quit : ')
        if 'q' == q_type or 'Q' == q_type:
            print 'have an amazing day, good bye.'
            break
        if is_valid_number(q_type):
            q_type = int(q_type)
            if 1 == q_type:
                #according to no conditions to query#
                display_current_db_data(stu_index, stu_sys_info)
            elif 2 == q_type:
                #according to age conditions to query#
                print 'information according to age literally...'
                according_to_query_type_display(q_type=4)
            elif 3 == q_type:
                # according to salary conditions to query#
                print 'information according to salary literally...'
                according_to_query_type_display(q_type=9)
            elif 4 == q_type:
                #accroding to age border to query#
                age_border = raw_input('please given border between ages eg:24-68 or salary 3000-5000 : ')
                if re.search('-\w+', age_border):
                    little_age, large_age = age_border.split('-')
                    little_age, large_age = int(little_age), int(large_age)
                    if little_age > large_age:
                        little_age, large_age = large_age, little_age
                    according_to_query_type_display(4, little_age, large_age)
                else:
                    print 'please input valid border ages eg:24-68 or salary 3000-5000'
            elif 5 == q_type:
                # according to key-words conditions to query#
                key_words = raw_input('which key-word will you like to input, please write it down : ')
                according_to_query_key_word_display(key_words)
            elif 6 == q_type:
                #display how many different types in system#
                stuff = ['name', 'address', 'school', 'company']
                result_lst = according_to_query_directory_display()
                for idx in xrange(len(result_lst[0])):
                    print '[%s] are %d matches and they are : ' % (stuff[idx], result_lst[0][idx])
                    for match in result_lst[1][idx]:
                        print '   ***    ' + match


def start_manager_system():
    global curr_admin
    while True:
        if 'admin' == curr_admin:
            welcome_title = '-------------------------------------------\n' \
                            'welcome to my student manager systeme\n' \
                            'now you gonna start the xiao_L Robot\n' \
                            ' (1) add one new student to the system\n' \
                            ' (2) delete one student info from system\n' \
                            ' (3) update one student record into system\n' \
                            ' (4) show existence students through system\n' \
                            ' (5) new feature to do...'
            print welcome_title
            choice = raw_input('please input valid number between [1-5] or q/Q to quit: ')
            if 'q' == choice or 'Q' == choice:
                print 'have an amazing day, good bye.'
                break
            if is_valid_number(choice):
                choice = int(choice)
                if 1 == choice:
                    nn_add_student()
                elif 2 == choice:
                    nn_delete_student()
                elif 3 == choice:
                    nn_update_student()
                elif 4 == choice:
                    nn_display_student()
                else:
                    print 'to be or not to be'
        else:
            #login in personal info system#
            #TODO#
            return


def clear_system():
    global conn, cursor, curr_admin
    exit_title = '*** welcome to you next time ***'
    print exit_title
    select_th, ret_msg = 'y', ''
    if 'admin' == curr_admin:
        select_th = raw_input('you want to save your records or not [Y/N] : ')
    if select_th is not 'n' or select_th is not 'N':
        #create a new management system#
        print '*** records are being saving ***'
        #time.sleep(2)
        print '*** records have been saved successfully ***'
        print '*** good bye ***'
        ret_msg = 'user=[%s] exit student system.' % curr_admin
    elif 'admin' == curr_admin:
        print '*** your records are deleting ***'
        #time.sleep(1)
        invalid_current_db_data()
        print '*** your records have been deleted ***'
        print '*** good bye ***'
        ret_msg = 'user=[admin] truncate data and exit student system.'
    record_operation_or_security_log(curr_admin, ret_msg, 'succeed', 'sec_log')
    conn.close()


def is_allowed_user_login(login_name, login_pwd):
    global login_users, curr_admin
    for key, value in login_users.items():
        if login_name == key and login_pwd == value:
            content = 'user=[%s] login succeed.' % login_name
            curr_admin = login_name
            print content
            record_operation_or_security_log(login_name, content, 'succeed', 'sec_log')
            return True
    else:
        return False


def student_manger_system():
    while True:
        #increase system permissions admin&user#
        login_name = raw_input('username:')
        login_pwd = raw_input('password:')
        if is_allowed_user_login(login_name, login_pwd):
            initial_system()
            start_manager_system()
            clear_system()
            break
        else:
            ret_msg = 'user=[%s] login fail.' % login_name
            print ret_msg
            record_operation_or_security_log(login_name, ret_msg, 'failure', 'sec_log')


#main begin#
student_manger_system()



