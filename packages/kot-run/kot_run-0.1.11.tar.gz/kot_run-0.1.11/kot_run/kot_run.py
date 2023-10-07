#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import traceback
import copy

class KOT_Run:
    def __init__(self, cloud, encryption_key, interval=5) -> None:
        self.encryption_key = encryption_key
        self.connection = cloud
        task_record = self.connection.get("KOT_Run_tasks", encryption_key=self.encryption_key)
        if task_record is None:
            self.connection.set("KOT_Run_tasks", [], encryption_key=self.encryption_key)
            self.tasks = []
        else:
            self.tasks = task_record
        if self.connection.get("KOT_Run_results", encryption_key=self.encryption_key) is None:
            self.connection.set("KOT_Run_results", {}, encryption_key=encryption_key)
        self.interval = interval
    
    def tasks_sync(self):
        self.tasks = self.connection.get("KOT_Run_tasks", encryption_key=self.encryption_key)
    def add_task(self, name, args_for_func=(), kwargs_for_func={}):
        self.tasks_sync()
        self.tasks.append([name, args_for_func, kwargs_for_func])
        self.connection.set("KOT_Run_tasks", self.tasks, encryption_key=self.encryption_key)
    def delete_task(self, name):
        self.tasks_sync()
        self.tasks.remove(name)  

    

    def result(self, name,):
        records = self.connection.get("KOT_Run_results", encryption_key=self.encryption_key)
        if name in records:
            result = copy.copy(records[name])
            records.pop(name)
            return result
        else:
            return None


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
            self.tasks_sync()
            result_list = self.connection.get("KOT_Run_results", encryption_key=self.encryption_key)
            original_result = copy.copy(original_result)
            for i in self.tasks:
                try:
                    result = self.connection.get(i[0], encryption_key=self.encryption_key)(*i[1], **i[2])
                except Exception as e:
                    result = e
                    traceback.print_exc()
                result_list[i[0]] = result
            self.connection.set("KOT_Run_tasks", [], encryption_key=self.encryption_key)
            if original_result != result:
                self.connection.set("KOT_Run_results", result_list, encryption_key=self.encryption_key)
            time.sleep(self.interval)
