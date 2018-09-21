# -*- coding: utf-8 -*-


import sqlite3
import os 
import time

def create_load_info_table(cursor):
    create_sql = '''
        CREATE TABLE IF NOT EXISTS load_info(
        min1_load               REAL,
        min5_load               REAL,
        min15_load              REAL,
        record_time             TEXT,
        time_stamp              TEXT
        )
    '''
    cursor.execute(create_sql)

def create_task_info_table(cursor):
    create_sql = '''
        CREATE TABLE IF NOT EXISTS task_info(
        total                  INTEGER,
        running                INTEGER,
        sleeping               INTEGER,
        stopped                INTEGER,
        zombie                 INTEGER,
        record_time             TEXT,
        time_stamp              TEXT
        )
    '''
    cursor.execute(create_sql)

def create_cpu_info_table(cursor):
    create_sql = '''
        CREATE TABLE IF NOT EXISTS cpu_info(
        cpu_name               TEXT,
        us                     REAL,
        sy                     REAL,
        ni                     REAL,
        id                     REAL,
        wa                     REAL,
        hi                     REAL,
        si                     REAL,
        st                     REAL,
        record_time            TEXT,
        time_stamp             TEXT
        )
    '''
    cursor.execute(create_sql)

def create_mem_info_table(cursor):
    create_sql = '''
        CREATE TABLE IF NOT EXISTS mem_info(
        total                  REAL,
        used                   REAL,
        free                   REAL,
        buffers                REAL,
        record_time            TEXT,
        time_stamp             TEXT
        )
    '''
    cursor.execute(create_sql)

def create_swap_info_table(cursor):
    create_sql = '''
        CREATE TABLE IF NOT EXISTS swap_info(
        total                  REAL,
        used                   REAL,
        free                   REAL,
        cached                 REAL,
        record_time            TEXT,
        time_stamp             TEXT
        )
    '''
    cursor.execute(create_sql)

def create_process_info_table(cursor):
    create_sql = '''
        CREATE TABLE IF NOT EXISTS process_info(
        PID                    INTEGER,
        VIRT                   REAL,
        RES                    REAL,
        SHR                    REAL,
        S                      TEXT,
        CPU                    REAL,
        MEM                    REAL,
        COMMAND                TEXT,
        record_time            TEXT,
        time_stamp             TEXT
        )
    '''
    cursor.execute(create_sql)

static_record_time = ''

def set_record_time(time):
    global static_record_time
    static_record_time = time

def get_record_time():
    global static_record_time
    return static_record_time


#top - 11:48:50 up 285 days, 23:40,  1 user,  load average: 0.10, 0.08, 0.08
def get_load_info(cursor, line):
    load_list = line.split(',')
    cur_time_list = load_list[0].split()
    cur_time = cur_time_list[2]
    cur_record_time = cur_time
    set_record_time(cur_time)

    min_load_list = load_list[3].strip().split(':')
    min1_load = float(min_load_list[1])
    min5_load = float(load_list[4])
    min15_load = float(load_list[5])

    cur_time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    insert_sql = "INSERT INTO load_info VALUES (%0.2f, %0.2f, %0.2f, '%s', '%s')" % (min1_load, min5_load, min15_load, cur_record_time, cur_time_stamp)
    cursor.execute(insert_sql)

#Threads:  49 total,   0 running,  49 sleeping,   0 stopped,   0 zombie
def get_task_info(cursor, line):
    task_list = line.split(',')
    sum_task_count = int(task_list[0].strip().split(':')[1].split()[0])
    running_task_count = int(task_list[1].strip().split()[0])
    sleeping_task_count = int(task_list[2].strip().split()[0])
    stopped_task_count = int(task_list[3].strip().split()[0])
    zombie_task_count = int(task_list[4].strip().split()[0])

    cur_time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    cur_record_time = get_record_time()

    insert_sql = "INSERT INTO task_info VALUES (%d, %d, %d, %d, %d, '%s', '%s')" % (sum_task_count, running_task_count, sleeping_task_count, stopped_task_count, zombie_task_count, cur_record_time, cur_time_stamp)
    cursor.execute(insert_sql)

#%Cpu0  :  0.3 us,  0.3 sy,  0.0 ni, 99.3 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
def get_cpu_info(cursor,line):
    cpu_name = line[:line.index(':')].strip()
    cpu_list = line.split(':')[1].strip().split(',')

    us = float(cpu_list[0].strip().split()[0])
    sy = float(cpu_list[1].strip().split()[0])
    ni = float(cpu_list[2].strip().split()[0])
    id = float(cpu_list[3].strip().split()[0])
    wa = float(cpu_list[4].strip().split()[0])
    hi = float(cpu_list[5].strip().split()[0])
    si = float(cpu_list[6].strip().split()[0])
    st = float(cpu_list[7].strip().split()[0])

    cur_time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    cur_record_time = get_record_time()

    insert_sql = "INSERT INTO cpu_info VALUES ('%s', %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, '%s', '%s')" % (cpu_name, us, sy, ni, id, wa, hi, si, st, cur_record_time, cur_time_stamp)
    cursor.execute(insert_sql)

#  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
# 6387 root     -81   0 3399928 291316   3780 S  1.0  0.9   8:26.01 eMP1
# 6405 root     -81   0 3399928 291316   3780 S  1.0  0.9   8:03.11 eMP7
def get_process_info(cursor,line):
    process_list = line.split()
    PID = int(process_list[0])

    VIRT = 0.0
    if 'm' in process_list[4]:
        VIRT = float(process_list[4][:-1])
    elif 'g' in process_list[4]:
        VIRT = float(process_list[4][:-1]) * 1024
    else:
        VIRT = float(process_list[4])/1024

    RES = 0.0
    if 'm' in process_list[5]:
        RES = float(process_list[5][:-1])
    elif 'g' in process_list[5]:
        RES = float(process_list[5][:-1]) * 1024
    else:
        RES = float(process_list[5])/1024    

    SHR = 0.0
    if 'm' in process_list[6]:
        SHR = float(process_list[6][:-1])
    elif 'g' in process_list[6]:
        SHR = float(process_list[6][:-1]) * 1024
    else:
        SHR = float(process_list[6])/1024

    process_status = process_list[7]

    cpu = float(process_list[8])
    mem = float(process_list[9])
    command_name = process_list[11]

    cur_time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    cur_record_time = get_record_time()

    insert_sql = "INSERT INTO process_info VALUES (%d, %0.2f, %0.2f, %0.2f, '%s', '%0.2f', '%0.2f','%s','%s','%s')" % (PID, VIRT, RES, SHR, process_status, cpu, mem, command_name, cur_record_time, cur_time_stamp)
    cursor.execute(insert_sql)


if __name__ == '__main__':
    cur_dir = os.getcwd()
    db_name = 'top_info.db'
    top_log_name = 'top_cpu.log'

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    get_all_table = "SELECT tbl_name FROM sqlite_master Where type = 'table'"
    cursor.execute(get_all_table)
    all_table_list = cursor.fetchall()
    all_table_name_list = []

    for table_name in all_table_list:
        all_table_name_list.append(table_name[0])
        delete_sql = "DELETE FROM %s" % (table_name[0])
        cursor.execute(delete_sql)

    cursor.execute("VACUUM")
    conn.commit()

    topfile = open(top_log_name,'r')

    try:
        lines = topfile.readlines()
        for line in lines:
            line = line.strip()
            
            if len(line) == 0:
                continue
            elif line[:3] == 'top':
                if 'load_info' not in all_table_name_list:
                    create_load_info_table(cursor)
                get_load_info(cursor, line)
            elif line[:7] == 'Threads':
                if 'task_info' not in all_table_name_list:
                    create_task_info_table(cursor)
                get_task_info(cursor,line)
            elif line[:4] == '%Cpu':
                if 'cpu_info' not in all_table_name_list:
                    create_cpu_info_table(cursor)
                get_cpu_info(cursor,line)
            elif line[:3] == "KiB":
                continue
            elif line[:3] == "PID":
                continue
            else:
                if 'process_info' not in all_table_name_list:
                    create_process_info_table(cursor)
                get_process_info(cursor,line)
        
    finally:
        topfile.close()
        cursor.close()
        conn.commit()
        conn.close()


