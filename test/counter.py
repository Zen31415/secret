# Our goal is to take a predefined list, count how many times each element occurs in the list, and print the results as a dictionary.
def counter(input):
# Define a function named 'counter', with one var.
# This var will be the list 'src', and will be referred to as 'input' as a local var for the rest of this function.
	result = {}
	# Define an empty dictionary named 'result'. We do this outside of the loop so that we don't overwrite the data we're putting into this dictionary.
	# This indentation is important as our baseline inside the function. Everything needs to be indented exactly this much unless it is nested deeper.
	for x in input:
	# define a new var 'x', which means each element inside 'input'.
	# We will perform the following loop until we run out of elements inside 'input'.
		if x not in result:
		# If element 'x' exists in the list but not in the dictionary, we want to write a new index:key pair to the dictionary.
		# So, this line will check if 'x' is not in the 'result' dictionary.
		# This indentation is the baseline for everything we want affected by line 8.
			result[x] = 0
			# If element 'x' is not in 'result', this means it's the first time we are seeing 'x' in the list, and it's not yet defined in the dictionary.
			# This line defines a new key : index pair in 'result', where the index is 'x', and the key is our new count of how many times the index is found in the list.
			# This indentation is only for what happens when our 'if' is true.
		result[x] = result[x] +1
		# This indentation means that we've moved to defining behavior for when index 'x' is already present in the dictionary.
		# For every time after we define the index : key pair, this will update the key count by 1.
		# At this point our loop ends, looks for another element in the list, and repeats if one is found.
	return result
	# After we have reached the end of the elements in 'input', we return the final 'result' value outside of the function.
	# This indentation ends the 'for' loop from line 8.

# This blank line is the end of the 'counter' function and its indentation refers to the fact that we are finishing the definition we started on line 2. 
src = ['apple', 'peach', 'banana', 'banana', 'apple']
# This line defines a new list titled 'src' and what its contents will be. This is the input that we start the problem with.
# This needs to be a list because it needs the ability for elements to occur more than once.
# Dictionaries cannot track when elements happen more than once unless the dictionary's key is a counter value, removing our ability to use any other key.
# A dictionary where the keys are a counter value is not useful for any purpose besides counting.
lmao = counter(src)
# This line defines a new value named 'lmao', which will be used to call the 'counter' function.
# It passes the variable that 'counter' will be looking for, which in this case is our 'src' list.
print(lmao)
# This line prints the value for 'lmao', and when we try to do that, line 31 makes it so that we call a function in order to decide what 'lmao' will mean. 
# if lmao prints as {'apple': 2, 'peach': 1, 'banana': 2} , then we have achieved our goal.