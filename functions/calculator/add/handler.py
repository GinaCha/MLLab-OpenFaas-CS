"""Author: Gina Chatzimarkaki"""

#test-calculator-add.py
def handle(str):
    """
        Add two numbers and return the result. Seperate the 
        numbers via space If there are more just take the 
        first two.

        Parameters
        ----------
        str : String
            the provided input

        Returns
        -------
        int
            the 2 numbers add
    """
    try:
        numbers = str.strip().split()
        accumulator = 0
        count = 0
        for n in numbers:
            accumulator += float(n)
            count += 1
            if count == 2:
                break
        print(accumulator)

    except ValueError as v:
        print("*** Value Error: ",v)
    except Exception as x:
        print("*** Error: ",x)