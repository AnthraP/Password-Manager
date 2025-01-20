"""
Name: merge_sort_ac
Parameters: myList: List
Returns: List
Purpose: Divides the list into halves using recursion
"""
def merge_sort_ac(myList):
    list_length = len(myList)
    if list_length == 1:
        return myList
    mid_point = list_length // 2
    left = merge_sort_ac(myList[:mid_point])
    right = merge_sort_ac(myList[mid_point:])
    return merge_ac(left, right)

"""
Name: merge_ac
Parameters: left: List, right: List
Returns: output: List
Purpose: Merges the pieces of the list in ascending  order
"""
def merge_ac(left, right):
    output = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            output.append(left[i])
            i += 1
        else:
            output.append(right[j])
            j += 1
    output.extend(left[i:])
    output.extend(right[j:])
    return output



"""
Name: merge_sort_de
Parameters: myList: List
Returns: List
Purpose: Divides the list into halves using recursion
"""
def merge_sort_de(myList):
    list_length = len(myList)
    if list_length == 1:
        return myList
    mid_point = list_length // 2
    left = merge_sort_de(myList[:mid_point])
    right = merge_sort_de(myList[mid_point:])
    return merge_de(left, right)

"""
Name: merge_de
Parameters: left: List, right: List
Returns: output: List
Purpose: Merges the pieces of the list in decending order
"""

def merge_de(left, right):
    output = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] > right[j]:
            output.append(left[i])
            i += 1
        else:
            output.append(right[j])
            j += 1
    output.extend(left[i:])
    output.extend(right[j:])
    return output
