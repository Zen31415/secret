"""Program to sum every whole number below 1000 divisible by 3 or 5."""
def euler1(toprange):
    """Finds every number that is divisible by either 3 or 5,
    with an upper range of input number given.
    """
    result = {}
    for i in (range(1, toprange)):
        if i%3==0 and i not in result or i%5==0 and i not in result:
            result[i] = 1
        continue
    return result

dictionary = euler1(1000)
final = list(dictionary)
print(sum(final))
