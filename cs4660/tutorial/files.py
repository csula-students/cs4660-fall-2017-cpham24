"""Files tests simple file read related operations"""
from io import open
from tutorial import lists

class SimpleFile(object):
    """SimpleFile tests using file read api to do some simple math"""
    def __init__(self, file_path):
        f = open(file_path, encoding='utf-8')
        content = f.readlines()
        self.numbers = []
        index = 0
        for line in content:
          entries = line.split(' ')
          li = []
          for entry in entries:
            try:
              x = int(entry)
              li.append(x)
            except ValueError:
              """TODO: handle error"""
          self.numbers.append(li)
          index += 1

    def get_mean(self, line_number):
        list = self.numbers[line_number]
        return lists.get_avg(list)

    def get_max(self, line_number):
        list = self.numbers[line_number]
        return max(list)

    def get_min(self, line_number):
        list = self.numbers[line_number]
        return min(list)

    def get_sum(self, line_number):
        list = self.numbers[line_number]
        return sum(list)
