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
        return lists.get_avg(self.numbers[line_number])

    def get_max(self, line_number):
        list = self.numbers[line_number]
        max = list[0]
        for num in list:
          if num > max:
            max = num
        return max

    def get_min(self, line_number):
        list = self.numbers[line_number]
        min = list[0]
        for num in list:
          if num < min:
            min = num
        return min

    def get_sum(self, line_number):
        list = self.numbers[line_number]
        sum = 0
        for num in list:
          sum += num
        return sum
