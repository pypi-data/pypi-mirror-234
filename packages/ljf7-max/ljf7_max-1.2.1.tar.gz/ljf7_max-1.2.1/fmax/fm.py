# calculate max frequency

def max_frequency(s):
 max_frequency = {}

 for i in s:
    if i in max_frequency:
        max_frequency[i] += 1
    else:
        max_frequency[i] = 1

 my_result = max(max_frequency, key=lambda x: x[0])

 print("The max frequency of a letter in an essay: " + my_result)


# max_frequency()