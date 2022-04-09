def counter(input):
#defines 'counter' function
	result = {}
    #defines empty dictionary named 'result'
	for x in input:
    #for everything in 'input' until end of results
		y = input.count(x)
        # defines 'y' variable as the number of times that 'input' is found in 'result' dictionary
		z = x
        # defines 'z' variable as a copy of 'x', because we cannot write {x: y} in the following line
		result.update({z: y})
        # updates 'result' dictionary with new index:key pair defined as 'z': 'y' each time the loop found another entry to run through
	return(result)
    # passes 'result' dictionary outside of function

src = ['apple', 'peach', 'banana', 'banana', 'apple']
# defines input, in this case a hardcoded list

lmao = counter(src)
# defines new variable 'lmao' as the result of running 'counter' function on input

print(lmao)
# print results