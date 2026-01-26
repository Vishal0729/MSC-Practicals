def overlapping(list1,list2):
    for item in list1:
        if item in list2:
            return True
        return False

list1=[1,2,3,4,5]
list2=[5,6,7,8,9]
if overlapping(list1,list2):
    print("Overlapping (common elements found)")
else:
    print("Not overlapping (no common elements)")
