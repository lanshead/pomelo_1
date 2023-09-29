lst1 = list(map(int, input().split(':')))
lst2 = list(map(int, input().split(':')))
sec = lst2[2] - lst1[2]
m = 0
if sec < 0:
    sec = 60 + sec
    m = -1

mn = lst2[1] - lst1[1] + m
if mn < 0:
    mn = 60 + mn
    lst2[0] -= 1

print(lst2[0] - lst1[0], mn, sec)
