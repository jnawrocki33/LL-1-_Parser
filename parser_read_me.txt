Jason Nawrocki Lab 3 Instructions--

To run this, open idle and type in the command window:
	main("inputFileName.txt")

The program will then run, first printing the token and lexeme lists.
Then it will print any expressions which were to be printed from the input code.

**If there is a return statement, the program will exit(), simulating the way in C
	a function ends at a return statement. This does NOT mean my program detected
	an error in the input code.

In my implementation, I allow widening type conversion, meaning float variables can be
	assigned integer values. But integer variabls cannot be assigned float values.

Also, bool data cannot be added/multiplied with integer or float data in any way.

My program implements while loops containing a single statement

