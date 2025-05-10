def str_len(s):
    count = 0
    try:
        while True:
            _ = s[count]
            count += 1
    except:
        return count

def str_get(s, i):
    return s[i]

def list_len(lst):
    count = 0
    try:
        while True:
            _ = lst[count]
            count += 1
    except:
        return count

def list_append(lst, val):
    new_lst = []
    i = 0
    while i < list_len(lst):
        new_lst += [lst[i]]
        i += 1
    new_lst += [val]
    return new_lst

def list_contains(lst, val):
    i = 0
    while i < list_len(lst):
        if lst[i] == val:
            return True
        i += 1
    return False

def list_sort(lst):
    n = list_len(lst)
    i = 0
    while i < n:
        j = 0
        while j < n - 1:
            if lst[j] > lst[j + 1]:
                temp = lst[j]
                lst[j] = lst[j + 1]
                lst[j + 1] = temp
            j += 1
        i += 1
    return lst

def list_copy(lst):
    new_lst = []
    i = 0
    while i < list_len(lst):
        new_lst = list_append(new_lst, lst[i])
        i += 1
    return new_lst