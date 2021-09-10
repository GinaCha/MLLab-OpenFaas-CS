"""Author: Gina Chatzimarkaki"""

#test-calculator-multiply.py
def handle(str):
    """
        Multiple two numbers and return the result. If there are more
        just take the first two

        Parameters
        ----------
        str : String
            the provided input

        Returns
        -------
        int
            the 2 numbers multiplied
    """
    try:
        numbers = str.strip().split()

        if len(numbers) == 2:
            print( float(numbers[0]) * float(numbers[1]) )
        else:
            print("*** Need two values got", len(numbers))

    except ValueError as v:
        print("*** Value Error: ", v)
    except Exception as x:
        print("*** Error: ", x)
