"""
@author Michał Łopaciuch
@date 14.11.2020
"""


import time


class Timer:
    def __init__(self, label=''):
        self.label = label
        self.start = time.time()

    def stop(self):
        self.end = time.time()

    def get_interval(self, precision=2):
        return f'{self.label}: {str(round(self.end - self.start, precision))}'
