import requests
from urllib.parse import quote
import _thread
import time
import threading

threadLock = threading.Lock()


def thread_send_log(url, content, name):
    threadLock.acquire()
    content = quote(content, 'utf-8')
    name = quote(name, 'utf-8')
    url = url + '&name=' + name + '&content=' + content
    # print('sendLog:' + url)
    try:
        # print("----------------sendLog...----------------")
        requests.get(url, timeout=5)
        # print('\nsendLog finish', r.status_code, r.content)
        # print('sendLog finish')
    except Exception as e:
        print('\nsendLog network error!')
    finally:
        # print("----------------sendLog...----------------")
        threadLock.release()


class LogClass:
    def __init__(self, on=False):
        self.on = on

    def send_log(self, content, name):
        if self.on:
            try:
                _thread.start_new_thread(thread_send_log, (content, name))
            except Exception as e:
                print("cloud log error")


if __name__ == '__main__':
    log_class = LogClass()
    log_class.send_log('35.8', 'PSNR')
    log_class.send_log('35.8', 'PSNR')
    while True:
        pass
