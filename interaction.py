#! /bin/python3

from queue import Queue
import threading
from random import uniform

q = Queue()

class Sender:
    def __init__(self, number):
        q.put("start")

        self.number = number

    def __call__ (self):
        for i in range(self.number):
            q.put(uniform(0, 1))

        q.put("end")

class Reciever:
    def  __init__(self):
        self.sender_num = 0

    def recieve(self):
        i = 1

        while True:

            messege = q.get()

            match messege:
                case "start":
                    self.sender_num += 1
                case "end":
                    self.sender_num -= 1
                case _:
                    print(f"messege #{i}: {messege**2}")
                    i += 1


            if (self.sender_num == 0):
                break
            


senders = []

for _ in range(10):
    senders.append(Sender(2))

print(len(senders))

for sender in senders:
    threading.Thread(target = sender).start()


r = Reciever()
threading.Thread(target = r.recieve).start()
