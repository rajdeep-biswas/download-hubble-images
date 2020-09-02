monthdates = []

with open('C:\\Users\Rajdeep\Documents\Python Code\selenium\hubbleimages\leftouts.txt', 'r') as f:
    for item in f:
        monthdates.append(item)

for md in monthdates:
    month = md.split()[0].upper().strip()
    date = md.split()[1]
    print(month, date)
