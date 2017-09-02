"""Lists defines simple list related operations"""

def get_first_item(li):
    return li[0]

def get_last_item(li):
    size = len(li)
    return li[size-1]

def get_second_and_third_items(li):
    return [li[1], li[2]]

def get_sum(li):
    sum = 0
    for num in li:
        sum += num
    return sum

def get_avg(li):
    size = len(li)
    sum = float(get_sum(li))
    return sum / size
