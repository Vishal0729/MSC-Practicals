def non_overlapping(list1,list2):
    unique_items=[]
    for item in list1:
        if item not in list2:
            unique_items.append(item)
    return unique_items

list1=[1,2,3,4,5]
list2=[3,4,6,7,8]
result=non_overlapping(list1,list2)
print("Elements from list1 not in list2:",result)
