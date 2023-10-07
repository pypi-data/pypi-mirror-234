#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import time
import traceback
import copy
import multiprocessing
from cryptography.fernet import Fernet

class KOT_Run:
    def __init__(self, cloud, encryption_key, interval=5, try_number = 0) -> None:
        self.encryption_key = encryption_key
        self.connection = cloud
        self.interval = interval
        self.threads = {}
        self.uniq = (((Fernet.generate_key()).decode()).replace("-", "").replace("_", ""))[
                :10
            ]
        self.try_number = try_number
    



    def add_task(self, name, endless=False, thread=False, args_for_func=(), kwargs_for_func={}):
        try_number = 0
        while try_number <= self.try_number or self.try_number == 0:
            all_records = self.connection.get_all(encryption_key=self.encryption_key)
            runners = [runner for runner in all_records if runner.startswith("RUNNER-") and (time.time() - all_records[runner]) <= self.interval*2]
            if len(runners) == 0:
                try_number += 1
                time.sleep(self.interval)
            else:
                self.connection.set(f"TASK-{name}", [name, args_for_func, kwargs_for_func, endless, thread, random.choice(runners)], encryption_key=self.encryption_key)


    def delete_task(self, name):

        self.connection.delete(f"TASK-{name}")

    

    def result(self, name,):
        return self.connection.get(f"RESULT-{name}",encryption_key=self.encryption_key)


    def run(self,name, args_for_func=(), kwargs_for_func={}):
        self.add_task(name, args_for_func=args_for_func, kwargs_for_func=kwargs_for_func)
        time.sleep(self.interval*2)
        while True:
            the_result = self.result(name)
            if the_result is not None:
                return the_result
            time.sleep(self.interval)
 

    def runner(self,):
        while True:
            all_elements = self.connection.get_all(encryption_key=self.encryption_key)
            tasks = [all_elements[a] for a in all_elements if a.startswith("TASK-")]
            new_thread_list = {}
            for thread in self.threads:
                is_in = False
                for i in tasks:
                    if thread == i[0]:
                        is_in = True
                if not is_in:
                    self.threads[thread].terminate()
                else:
                    new_thread_list[thread] = self.threads[thread]
            self.threads = new_thread_list
            for i in tasks:
                if i[5] == f"RUNNER-{self.uniq}":
                    try:
                        if not i[4]:
                            self.connection.delete(f"RUNNER-{self.uniq}")
                            result = self.connection.get(i[0], encryption_key=self.encryption_key)(*i[1], **i[2])
                        else:
                            if i[0] not in self.threads:
                                the_thread = multiprocessing.Process(target=self.connection.get(i[0], encryption_key=self.encryption_key), args=i[1], kwargs=i[2])
                                self.threads[i[0]] = the_thread
                                self.threads[i[0]].start()
                                result = True
                    except Exception as e:
                        result = e
                        traceback.print_exc()
                    self.connection.set(f"RESULT-{i[0]}", result, encryption_key=self.encryption_key)
                    if not i[3]:
                        self.connection.delete(f"TASK-{i[0]}")
            self.connection.set(f"RUNNER-{self.uniq}", time.time(), encryption_key=self.encryption_key)
            time.sleep(self.interval)
