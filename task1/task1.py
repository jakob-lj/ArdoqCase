

def get_max(list_of_numbers):
    if (len(list_of_numbers) < 1): return 1, False
    return max(list_of_numbers), True


def highest_product(list_of_numbers):
    # result = 1
    # for i in range(3):
    #     m, has_more_elements = get_max(list_of_numbers)
    #     if not has_more_elements:
    #         break
    #     result *= m
    #     list_of_numbers.remove(m)

    # return result


    sortedList = sorted(list_of_numbers, reverse=True)
    
    positive = sortedList[0]*sortedList[1]*sortedList[2]
    negative = sortedList[0]*sortedList[-1]*sortedList[-2]
    return max(positive, negative)

print(highest_product([1, -5, -2, -1, -76]))
print(highest_product([-4, -5, -2, -1, -76]))
print(highest_product([1, 6, 3, 10, 5, 2]))