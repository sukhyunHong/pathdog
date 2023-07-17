# -*- coding: utf-8 -*-

import os
import time
import math
from collections import Counter
from collections import namedtuple
import psutil
#from watchdog.events import FileSystemEventHandler
#from watchdog.observers import Observer
# 프로세스에 대한 자식 프로세스 구분을 위한 structure
ProcInfo = namedtuple("ProcInfo", "pname pid path childpid connection")
#target Main process 프로세스네임은 pid 프로세스 모니터나 system informer를 참고해서 확인함
Proc_id = namedtuple("ProcId", "pname pid path")


#  프로세스 이름으로 PID 가져오기
def get_process_pid(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            print(proc)
            return proc.pid
    return None
# get_process_pid('ZZeroSrvc.exe')

def process_info(process_name):
    for proc in psutil.process_iter([]):
        if proc.info['name'] == process_name:
            # print(proc.info['connections'][1].raddr)
            target = ProcInfo(proc.name(), proc.pid, psutil.Process(proc.pid).exe(), psutil.Process(proc.pid).children(recursive=True), proc.info['connections'])
            print(target)
            break
            # print(proc.info)
    return target

# 프로세스.exe의 PID로 db 가져오기
def get_process_db(db_list, pid):
    try:
        target_pid = pid
        if target_pid:
            # 프로세스.exe의 PID로 열려있는 핸들 가져오기
            handles = psutil.Process(target_pid).open_files() + psutil.Process(target_pid).connections()
            # target_list = []
            for handle in handles:
                # 각 핸들의 정보 확인
                if hasattr(handle, 'path') and handle.path and 'db' in handle.path:
                    if handle.path not in db_list:
                        db_list.append(handle.path)
                        print(handle.path)
            return db_list
        else:
            print("Process not found.")
            return db_list
    except psutil.AccessDenied:
        #print(f"Access denied to process {target_pid}")
        return db_list
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return db_list



#엔트로피 계산 함수
def calculate_entropy(file_path):
    # 파일을 바이너리 모드로 열기
    with open(file_path, 'rb') as file:
        # 파일의 모든 데이터를 읽어오기
        data = file.read()
    
    # 각 바이트의 빈도 계산
    byte_count = Counter(data)
    
    # 엔트로피 계산
    entropy = 0.0
    total_bytes = len(data)
    
    for count in byte_count.values():
        probability = count / total_bytes
        entropy -= probability * math.log2(probability)
    
    return entropy

#db, log 엔트로피 파일 제거
def remove_entropy_list(db_list):
    for i in db_list:
        entropy = calculate_entropy(i)
        if entropy > 6:
            db_list.remove(i)

    return db_list

#폴더의 전체 db, log 파일 가져오기
def get_file_paths(directory_path, db_list):
    file_paths = []  # 파일 경로를 저장할 리스트

    # os.walk를 사용하여 모든 디렉토리, 하위 디렉토리, 파일을 순회
    for root, directories, files in os.walk(directory_path):
        for filename in files:
            # os.path.join을 사용하여 파일 경로를 생성
            filepath = os.path.join(root, filename)
            # db, log sdb 파일 조건문 
            if '.db' in filepath or 'log' in filepath or '.sdb' in filepath:
                #기존 경로 중복 체크
                if filepath not in db_list:
                    db_list.append(filepath)  # 파일 경로를 리스트에 추가
    return db_list


                

#프로세스 이름을 pid 가져오기
process_name = 'node'
target_pid = get_process_pid(process_name)
print(target_pid)
#temp = process_info(process_name)
#procId= Proc_id(temp.pname, temp.pid, temp.path)
#process_list = []
#부모 process 리스트에 추가
#process_list.append(procId)

#child process 리스트에 추가
#for i in temp.childpid:
#    child = Proc_id(i.name(), i.pid, psutil.Process(i.pid).exe())
#    process_list.append(child)

#db_list = []

#for i in process_list:
    
 #   db_list = get_process_db(db_list, i.pid)

#print(db_list)


