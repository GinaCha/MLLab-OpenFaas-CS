"""Author: Gina Chatzimarkaki"""
import sys

def fib(n):
    """
        Generate the first N fibonacci numbers

        Parameters
        ----------
        str : String
            the provided input

        Returns
        -------
        int
            the 2 numbers divided
    """
    
    if n <= 1: return n
    else: return fib(n-1) + fib(n-2)


def handle(req):
    """
        Divide two numbers and return the result. If there are more
        just take the first two

        Parameters
        ----------
        str : String
            the provided input

        Returns
        -------
        int
            the fibonacci sequence with str length
    """
    

    try:
        numbers = int(req)
        if len(req) >= 1:
            output = []
            for i in range(numbers):
                output.append(str(fib(i)))

            print(', '.join(output))
        else:
            print("*** Need to provide one value", len(numbers))
       
    except ValueError as v:
        print("*** Value Error: ", v)
    except Exception as x:
        print("*** Error: ", x)