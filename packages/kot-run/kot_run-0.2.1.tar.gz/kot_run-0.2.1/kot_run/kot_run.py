#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import traceback
import copy


class KOT_Run:
    def __init__(self, cloud, encryption_key, interval=5) -> None:
        self.encryption_key = encryption_key
        self.connection = cloud
        self.interval = interval
    



    def add_task(self, name, endless=False, args_for_func=(), kwargs_for_func={}):
        self.connection.set(f"TASK-{name}", [name, args_for_func, kwargs_for_func, endless], encryption_key=self.encryption_key)


    def delete_task(self, name):

        self.connection.delete(f"TASK-{name}", encryption_key=self.encryption_key)

    

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
            for i in tasks:
                try:
                    result = self.connection.get(i[0], encryption_key=self.encryption_key)(*i[1], **i[2])
                except Exception as e:
                    result = e
                    traceback.print_exc()
                self.connection.set(f"RESULT-{i[0]}", result, encryption_key=self.encryption_key)
                if not i[3]:
                    self.connection.delete(f"TASK-{i[0]}")
            time.sleep(self.interval)
