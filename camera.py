import requests
from concurrent.futures import ThreadPoolExecutor
import time
import json
import random

STATES = [
    'recording',
    'updating',
    'unhealthy',
]

thread_pool = ThreadPoolExecutor()

class Camera():

    def __init__(self, identifier):
        self._identifier = identifier
        self._logs = []
        self._current_state = STATES[0]

    def start(self):
        thread_pool.submit(self.update_logs)
        thread_pool.submit(self.update_state)
        thread_pool.submit(self.wait_for_request)


    def update_logs(self):
        while True:
            new_log = random.choice(['tampering detected', 'occlusion detected'])
            self._logs.append({'time': time.time(), 'message': new_log})
            time.sleep(3)

    def update_state(self):
        while True:
            current_state = random.choice(STATES)
            time.sleep(3)


    def wait_for_request(self):
        while True:
            try:
                camera_request = requests.post('http://127.0.0.1:5000/getRequest', 
                        data=self._identifier, timeout=30)
                print('got camera request', camera_request.text)
                if camera_request.text == 'get_logs':
                    requests.post('http://127.0.0.1:5000/submitLogs', json=self._logs)
            except:
                pass


def main():
    cam1 = Camera(identifier='1')
    cam1.start()

    # # uncomment for final section
    # cam2 = Camera(identifier='2')
    # cam2.start()

    thread_pool.shutdown(wait=True)

if __name__ == '__main__':
    main()
