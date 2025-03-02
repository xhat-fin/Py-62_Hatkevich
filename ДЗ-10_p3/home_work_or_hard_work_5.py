with open('student.txt', 'r') as f:
    text = f.readlines()

for t in text:
    t_l = t.split(' ')
    if int(t_l[2][0]) < 3:
        print(t)
