import tkinter as tk, os, subprocess, datetime

root_path = r'N:\loveNN\2019下半年主要工作'
nation_question = r'N:\loveNN\2019下半年主要工作\National_Questions国内问题'
overseas_question = r'N:\loveNN\2019下半年主要工作\Overseas_Question海外问题'
patch_task = r'N:\loveNN\2019下半年主要工作\paths补丁&需求处理'
other_common = r'N:\loveNN\2019下半年主要工作\otherThing其他公共事务'

record_question = '问题录入，格式如：【陕西电信】【SR 1137689】入局呼叫甄别失败问题'

questions_description, select_path = '', ''

directory_choice = [
        # (root_path, 0),
        (nation_question, 0),
        (overseas_question, 1),
        (patch_task, 2),
        (other_common, 3),
    ]

legend_skills = {
    '01': '淘气打击',
    '02': '爱卡西亚的暴雨',
    '03': '故技重施',
    '04': '诸神黄昏',
    '05': '羊灵生息',
    '06': '星河急涌',
    '07': '厄运钟摆',
    '08': '唤潮之佑',
    '09': '苍白之瀑',
    '10': '月之降临',
    '11': '精准弹幕',
    '12': '终极时刻'
}

def get_questions_description():
    global questions_description
    questions_description = view_string_question.get()

def get_directory_choice():
    global select_path
    for index in range(4):
        if view_int_choice.get() == index:
            select_path = directory_choice[index][0]


def start_create_and_open():
    global select_path, questions_description, nation_question
    get_directory_choice()
    get_questions_description()
    now_time = datetime.datetime.now().strftime('%Y-%m')
    month = now_time[5:]
    month_str = now_time.replace('-', '年')
    curr_month_skill = legend_skills[month]
    month_str = month_str + '月' + ' ' + curr_month_skill
    if select_path is nation_question:
        result_path = select_path + '\\' + month_str + '\\' + questions_description
    else:
        result_path = select_path + '\\' + questions_description
    # print(result_path)
    # create the directory #
    os.makedirs(result_path)
    # open the directory #
    os.startfile(result_path)


window = tk.Tk()
window.title('create directory')
window.geometry('800x600')


view_int_choice, view_string_question = tk.IntVar() ,tk.StringVar()

tk.Label(window, textvariable='', width='27').pack()
tk.Label(window, text='-- 选择其中一个路径添加目录 --', bg='gray', font=('blue', 15), fg='black').pack(anchor='w')
for lan, num in directory_choice:
    tk.Radiobutton(window, text=lan, value=num, command=get_questions_description, variable=view_int_choice).pack(anchor='w')

tk.Label(window, textvariable='', width='27').pack()
label = tk.Label(window,
    text=record_question,       # 标签的文字
    bg='gray',                 # 背景颜色
    font=('Arial', 10),         # 字体和字体大小
    width=100, height=2          # 标签长宽
    )
label.pack()    # 固定窗口位置
tk.Label(window, textvariable='', width='27').pack()
tk.Entry(window, textvariable=view_string_question, width=100).pack()
tk.Label(window, textvariable='', width='27').pack()

tk.Button(window, text="create and open", height='2', width='20', font=('black', 12), command=start_create_and_open,
           bg='#FFFAFA', fg='#4F4F4F', activebackground='white', relief='raised').pack()


window.mainloop()
