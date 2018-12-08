"""
    this is a student manager system
    its function is used by Python by lovline
    there are two user permission and some sql function
    begin day : 2018-11-21
    update day:2018-11-30
"""

# import used modules#
import os
import re
from datetime import datetime
import time
import MySQLdb

# some global variables#
curr_admin = 'admin'  # default user:admin#
stu_index = 0  # studend database valid count#
stu_sys_info = []  # total student infomations in system#
login_users = {
    'admin': '***',
    'user': '***'
}  # login users#

# mysql connect sql comments#
conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='Nqwer123', db='student_info', charset='utf8')
cursor = conn.cursor()


def record_operation_or_security_log(who, content, eResult, iType):
    """
    record operation adnd security log to database
    :param who:
    :param content:
    :param eResult:
    :param iType:
    :return:
    """
    global conn, cursor
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into optseclog(who, contents, whenT, eResult, iType) values('%s', '%s', '%s', '%s', '%s')" \
          % (who, content, curr_time, eResult, iType)
    cursor.execute(sql)
    conn.commit()


def invalid_current_db_data():
    """
    set istatus of users to 0 in database
    :return:
    """
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
    """
    initial student manager system
    :return:
    """
    print '*** system initialing ***'
    # time.sleep(1.5)
    print '*** system initial succeed ***'
    # time.sleep(0.8)
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
        # use original database#
        print '*** original database is loading ***'
        # time.sleep(1)
        print '*** congratulations! original database has loaded succeed! ***'
        ret_msg = 'user [%s] load the original database.' % curr_admin
    record_operation_or_security_log(curr_admin, ret_msg, 'succeed', 'opt_log')
    stu_index, stu_sys_info = query_current_data_from_db()


def is_valid_number(num):
    """
    check the num between 1 and 6
    :param num:
    :return:
    """
    if len(num) > 1:
        return False
    elif re.search(r'[1|2|3|4|5|6]', num):
        return 1 <= int(num) <= 7
    return False


def have_record_data(username):
    """
    check if username exists in database
    :param username:
    :return:curr_user ID or False
    """
    global conn
    global cursor
    sql = "select * from student_info where user_name='%s'" % username
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    if result is not None:
        if 0 == list(result)[14]:
            return False
        # print type(cursor.fetchone()) #the cursor is step by step
        return list(result)[0]  # return primary key ID#
    else:
        return False


def get_user_original_old_info(user_id):
    """
    throught user_id query the list result row
    :param user_id:
    :return:
    """
    global conn, cursor
    sql = "select * from setudent_info where id=%d" % user_id
    cursor.execute(sql)
    conn.commit()
    row = cursor.fetchone()
    # return user_name, password, salary and change times#
    return list(row)


def query_current_data_from_db():
    """
    query and record current valid datas from DB
    :return:
    """
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


def have_lover_exits_then_merge(cur_user, lover_name, update_time):
    """
    merge address and salary of two - latest_user's lovers and itself
    :param latest_user:
    :param lover_name
    :param update_time
    :return:
    """
    global stu_index, stu_sys_info, conn, cursor
    merge_address, merge_salary = '', 0
    cur_uid = have_record_data(cur_user)
    lover_uid = have_record_data(lover_name)
    if lover_uid is not False:
        #get total address and salary#
        sql = "select * from student_info where id=%d or id=%d" % (lover_uid, cur_uid)
        cursor.execute(sql)
        conn.commit()
        for row in cursor.fetchall():
            merge_address += (list(row)[6] + ' ')
            merge_salary += int(list(row)[9])
        #update total address, salary and change times#
        sql = "select * from student_info where id=%d or id=%d" % (lover_uid, cur_uid)
        cursor.execute(sql)
        conn.commit()
        for row in cursor.fetchall():
            #get individual change time#
            change_t = int(list(row)[13]) + 1
            sql_new = "update student_info set address='%s',salary=%d,update_time='%s',change_times=%d where id=%d" \
                      % (merge_address, merge_salary, update_time, change_t, list(row)[0])
            cursor.execute(sql_new)
            conn.commit()
        ret_msg = 'update user=[%s] and user=[%s] succeed.' % (lover_name, cur_user)
        print ret_msg
        record_operation_or_security_log('admin', ret_msg, 'succeed', 'opt_log')


def nn_add_student():
    """
    add a new student to DB
    :return:
    """
    global stu_index, stu_sys_info, conn, cursor
    print 'please input username'
    while True:
        user_name = raw_input('username:')
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
        print 'username is valid, please input following message and sperate as [space] '
        student = raw_input('^password[six numbers] sex[M|F] age[7-100] single[Y|N] address graduate_school'
                            ' company salay and whose_lover$ or q\Q to return back \n')
        if 'q' == student or 'Q' == student:
            break
        len_student = len(re.split('\s+', student))
        if 9 != len_student:
            ret_msg = 'input have too few or much parameters -- parameters len is need 10 yours are %d.\n' % len_student
            print ret_msg
            record_operation_or_security_log('admin', ret_msg, 'failure', 'opt_log')
            return 1  # parameters len is wrong#
        password, sex, age, single, address, graduate_school, company, salary, whose_lover \
            = re.split('\s+', student)
        # print user_name, password, sex, single, address, graduate_school, company, salary, whose_lover#
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
        # each commit needs to get latest DB data#
        stu_index, stu_sys_info = query_current_data_from_db()
        ret_msg = 'admin adds a new student info succeed.\n'
        print ret_msg
        record_operation_or_security_log('admin', ret_msg, 'succeed', 'opt_log')
        # if lovers exits in DB the merge them address and salary#
        if whose_lover is not 'NA':
            have_lover_exits_then_merge(user_name, whose_lover, create_time)
        return


def display_current_db_data(index, sys_info):
    """
    according to param to display current DB data or query result data
    :param index:
    :param sys_info:
    :return:
    """
    global stu_index, stu_sys_info
    if stu_index != index or stu_sys_info != sys_info:
        tmp_index, tmp_sys_info = index, sys_info
    else:
        tmp_index, tmp_sys_info = stu_index, stu_sys_info
    print 'there are %d student-info in system, and they are : ' % tmp_index
    for index, info in enumerate(tmp_sys_info):
        if 0 == info[14]:
            # iStatus is False#
            continue
        info = [str(ele) for ele in info]  # convert non-str to str#
        info_no_pwd = info[1:2] + info[3:11]
        dsp_info = '  '.join(info_no_pwd)
        print '  No.%d --- %s' % (index + 1, dsp_info)


def nn_delete_student():
    """
    delete one student from DB
    :return:
    """
    global stu_index, stu_sys_info
    display_current_db_data(stu_index, stu_sys_info)
    del_user = raw_input('please choose one user you want to delete by user_name: ')
    del_id = have_record_data(del_user)
    if del_id:
        list_row = get_user_original_old_info(del_id)
        change_times = int(list_row[13]) + 1
        sql = "update student_info set change_times='%s',data_status=0 where id=%s" % (change_times, del_id)
        cursor.execute(sql)
        conn.commit()
        ret_msg = 'admin delete user=[%s] succeed.' % del_user
        result = 'succeed'
        print ret_msg
    else:
        ret_msg = 'delete user fail, user_name=[%s] is not in system.' % del_user
        result = 'failure'
        print ret_msg
    # time.sleep(1)
    record_operation_or_security_log('admin', ret_msg, result, 'opt_log')


def update_student_personal_info(up_id, target_column, up_data):
    """
    user up_data to update personal information by his or her column
    :param up_id:
    :param target_column:
    :param up_data:
    :return:
    """
    global stu_index, stu_sys_info, conn, cursor
    # must match old password then update datas#
    confirm_pwd = raw_input('please input user password to check:')
    list_row = get_user_original_old_info(up_id)
    up_name, old_password, old_salary, up_change_time = list_row[1], list_row[2], int(list_row[9]), int(list_row[13]) + 1
    if confirm_pwd != old_password:
        ret_msg = 'old password checked wrong! update user=[%s] data failure!' % up_name
        print ret_msg
        record_operation_or_security_log('admin', ret_msg, 'failure', 'sec_log')
        return
    up_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if 'salary' == target_column:
        sql = "update student_info set '%s'=%d,update_time='%s',change_times=%d where id=%d" \
                % (target_column, int(up_data), up_time, up_change_time, up_id)
    else:
        sql = "update student_info set '%s'='%s',update_time='%s',change_times=%d where id=%d" \
                % (target_column, up_data, up_time, up_change_time, up_id)
    cursor.execute(sql)
    conn.commit()
    # if address or salary change then update lover's#
    if 'whose_lover' == target_column:
        # up_lover or original lover#
        have_lover_exits_then_merge(up_name, up_data, up_time)
    # time.sleep(1)
    ret_msg = 'admin update user=[%s] succeed' % up_name
    print ret_msg
    record_operation_or_security_log('admin', ret_msg, 'succeed', 'opt_log')


def nn_update_student():
    global stu_index, stu_sys_info
    display_current_db_data(stu_index, stu_sys_info)
    update_user = raw_input('please choose one user you want to delete by user_name: ')
    update_id = have_record_data(update_user)
    if update_id:
        variables = raw_input('which attributes you want to update from [password or single or address or '
                              'graduate_school or company or salary or whose_lover]? input like this [address:xian]')
        variables_info = variables.split(' ')
        # variables_info looks like ['salary:10000', 'address:xian']#
        up_dic = {}
        for up_data in variables_info:
            # sep_data looks like this ['address', 'xian']#
            sep_data = re.split(':', up_data)
            up_dic[sep_data[0]] = sep_data[1]
        # up_dic {'salary': '10000', 'address': 'xian'}
        for target_column, up_data in up_dic.items():
            update_student_personal_info(update_id, target_column, up_data)


def according_to_query_type_display(q_type, little=0, larger=0):
    """
    according to type of age, salary, age_border, salary_border to
    display query result DB data
    :param q_type:
    :param little:
    :param larger:
    :return:
    """
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
    record_operation_or_security_log('admin', 'according_to_query_type_display', 'succeed', 'opt_log')


def according_to_query_key_word_display(key_words):
    """
    according to key word by user to display DB data
    :param key_words:
    :return:
    """
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
    record_operation_or_security_log('admin', 'according_to_query_key_word_display', 'succeed', 'opt_log')


def according_to_query_directory_display():
    """
    display current DB data including:
        user name, address, graduate_school, company.
    :return:
    """
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
    record_operation_or_security_log('admin', 'according_to_query_directory_display', 'succeed', 'opt_log')
    return result_lst


def nn_display_student():
    """
    according different type to display data
    :return:
    """
    global stu_index, stu_sys_info
    if 0 == stu_index:
        print 'there are no student info in system please choose 1 to add.\n'
        return
    # query type to judge which method query#
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
                # according to no conditions to query#
                display_current_db_data(stu_index, stu_sys_info)
            elif 2 == q_type:
                # according to age conditions to query#
                print 'information according to age literally...'
                according_to_query_type_display(q_type=4)
            elif 3 == q_type:
                # according to salary conditions to query#
                print 'information according to salary literally...'
                according_to_query_type_display(q_type=9)
            elif 4 == q_type:
                # accroding to age border to query#
                age_border = raw_input('please given border between ages eg:24-68 or salary 3000-5000 : ')
                if re.search('-\w+', age_border):
                    little_age, large_age = age_border.split('-')
                    little_age, large_age = int(little_age), int(large_age)
                    if little_age > large_age:
                        little_age, large_age = large_age, little_age
                    according_to_query_type_display(4, little_age, large_age)
                else:
                    print 'please input valid border ages eg:24-68 or salary 3000-5000'
                    record_operation_or_security_log('admin', 'age or salary border is fault', 'failure', 'opt_log')
            elif 5 == q_type:
                # according to key-words conditions to query#
                key_words = raw_input('which key-word will you like to input, please write it down : ')
                according_to_query_key_word_display(key_words)
            elif 6 == q_type:
                # display how many different types in system#
                stuff = ['name', 'address', 'school', 'company']
                result_lst = according_to_query_directory_display()
                for idx in xrange(len(result_lst[0])):
                    print '[%s] are %d matches and they are : ' % (stuff[idx], result_lst[0][idx])
                    for match in result_lst[1][idx]:
                        print '   ***    ' + match


def personal_transfer_to_someone(cur_uname, transfer_name, transfer_money):
    """
    transfer money to someone
    :param cur_name:
    :param transfer_name:
    :param transfer_money:
    :return:
    """
    global conn, cursor, stu_index, stu_sys_info
    #get current user's deposit#
    cur_uid = have_record_data(cur_uname)
    list_row = get_user_original_old_info(cur_uid)
    cur_user_deposit = int(list_row[9])
    if transfer_money > cur_user_deposit:
        ret_msg = 'your deposit is insufficient. please recharge first'
        print ret_msg
        record_operation_or_security_log('user', ret_msg, 'failure', 'opt_log')
        return False
    up_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transfer_uid = have_record_data(transfer_name)
    list_row = get_user_original_old_info(transfer_uid)
    transfer_deposit = int(list_row[9])
    cur_user_deposit -= transfer_money
    transfer_deposit += transfer_money
    dic_tmp = dict(zip([cur_uid, transfer_uid], [cur_user_deposit, transfer_deposit]))
    for id, deposit in dic_tmp.items():
        list_row = get_user_original_old_info(id)
        change_time = int(list_row[13]) + 1
        sql = "update student_info set salary=%d,update_time='%s',change_times='%s where id=%d" \
                % (int(deposit), up_time, change_time, id)
        cursor.execute(sql)
        conn.commit()
    ret_msg = 'user=[%s] transfered money=[%d] to user=[%s] succeed.' % (cur_uname, transfer_money, transfer_name)
    print ret_msg
    record_operation_or_security_log(cur_uname, ret_msg, 'succeed', 'opt_log')
    return True


def leave_messages_to_lover(u_name, whisper_info):
    global conn, cursor
    u_id = have_record_data(u_name)
    row_list_user = get_user_original_old_info(u_id)
    lover_name = row_list_user[10]
    lover_id = have_record_data(lover_name)
    up_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #TODO#
    sql = "insert into student_info () values() where id=%d" % (lover_id)
    cursor.execute(sql)
    conn.commit()
    ret_msg = 'user=[%s] leaves a message to user=[%s].' %(u_name, lover_name)
    print ret_msg


def login_personal_info_features():
    global conn, cursor
    per_info = raw_input('please personal user_name and password : ')
    u_name, u_pwd = per_info.split('\s+')
    u_id = have_record_data(u_name)
    if False == u_id:
        ret_msg = 'the user=[%s] is not exits, please add first.' % u_name
        print ret_msg
        record_operation_or_security_log(u_name, ret_msg, 'failure', 'sec_log')
        return False
    list_row = get_user_original_old_info(id)
    old_pwd = list_row[2]
    if old_pwd is not u_pwd:
        ret_msg = 'old password checked wrong! login user=[%s] failure!' % u_name
        print ret_msg
        record_operation_or_security_log(u_name, ret_msg, 'failure', 'sec_log')
        return False
    ret_msg = 'correct password checked' % u_name
    print ret_msg
    record_operation_or_security_log(u_name, ret_msg, 'succeed', 'sec_log')
    print 'Hello [%s], welcome to your personal manager system!' % u_name
    sql = "select * from student_info where id=%d" % u_id
    cursor.execute(sql)
    conn.commit()
    personal_info = list(cursor.fetchone())
    print personal_info[0:2] + personal_info[2:14]
    return u_name


def taobao_shopping_feature(u_name):
    global conn, cursor
    shop_stuff = ['books', 'computer', 'snacks']
    cost = 5700
    u_id = have_record_data(u_name)
    row_list = get_user_original_old_info(u_id)
    u_deposit = int(row_list[9])
    if u_deposit < cost:
        ret_msg = 'you dont have enough money to buy these thins, it costs [%d] and you have [%d]' % (cost, u_deposit)
        print ret_msg
        return
    ret_msg = 'user=[%s] bought stuff [%s] cost=[%d] and now deposit is [%d]' % (u_name, shop_stuff, cost, u_deposit)
    #TODO#
    sql = "update record_history set () valuse()"
    cursor.execute(sql)
    conn.commit()


def start_manager_system():
    """
    start student manager system
    :return:
    """
    global curr_admin
    while True:
        if 'admin' == curr_admin:
            welcome_title = '-------------------------------------------\n' \
                            'welcome to my student manager systeme\n' \
                            'now you gonna start the xiao_L Robot\n' \
                            ' (1) add one new student to the system\n' \
                            ' (2) delete one student info from system\n' \
                            ' (3) update one student record into system\n' \
                            ' (4) show existence students through system\n'
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
            # login in personal info system#
            u_name = login_personal_info_features()
            if u_name is not False:
                transfer_info = raw_input('please give a name to transfer and money like Tony:1000 ')
                transfer_name, transfer_money = transfer_info.split(':')
                if have_record_data(transfer_name) is False:
                    ret_msg = 'user=[%s] is not exits in system' % transfer_name
                    print ret_msg
                    record_operation_or_security_log(u_name, ret_msg, 'failure', 'opt_log')
                    return
                # transfer to other people#
                transfer_flag = personal_transfer_to_someone(u_name, transfer_name, int(transfer_money))
                if transfer_flag and transfer_name is not u_name:
                    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    have_lover_exits_then_merge(u_name, transfer_name, update_time)
                # leave a message to lovers#
                whisper_info = raw_input('please leave a messag to your lover ')
                leave_messages_to_lover(u_name, whisper_info)
                # shooping features#
                taobao_shopping_feature(u_name)


def clear_system():
    """
    exit student manager system
    :return:
    """
    global curr_admin
    exit_title = '*** welcome to you next time ***'
    print exit_title
    select_th, ret_msg = 'y', ''
    if 'admin' == curr_admin:
        select_th = raw_input('you want to save your records or not [Y/N] : ')
    if select_th is not 'n' or select_th is not 'N':
        # create a new management system#
        print '*** records are being saving ***'
        # time.sleep(2)
        print '*** records have been saved successfully ***'
        print '*** good bye ***'
        ret_msg = 'user=[%s] exit student system.' % curr_admin
    elif 'admin' == curr_admin:
        print '*** your records are deleting ***'
        # time.sleep(1)
        invalid_current_db_data()
        print '*** your records have been deleted ***'
        print '*** good bye ***'
        ret_msg = 'user=[admin] truncate data and exit student system.'
    record_operation_or_security_log(curr_admin, ret_msg, 'succeed', 'sec_log')
    conn.close()


def is_allowed_user_login(login_name, login_pwd):
    """
    check the allowed user for logging in
    :param login_name:
    :param login_pwd:
    :return: True or False
    """
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
    """
    main function of the student manager system
    :return:
    """
    while True:
        # increase system permissions admin&user#
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


# gonna begin#
student_manger_system()

