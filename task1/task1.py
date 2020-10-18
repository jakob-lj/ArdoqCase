

def get_max(list_of_numbers):
    if (len(list_of_numbers) < 1): return 1, False
    return max(list_of_numbers), True


def highest_product(list_of_numbers):
    result = 1
    for i in range(3):
        m, has_more_elements = get_max(list_of_numbers)
        if not has_more_elements:
            break
        result *= m
        list_of_numbers.remove(m)

    return result

print(highest_product([1, -5, -2, -1, -76]))