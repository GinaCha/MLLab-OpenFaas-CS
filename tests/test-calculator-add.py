"""Author: Gina Chatzimarkaki"""

#test-calculator-add.py
def handle(s):
    """
        Add two numbers and return the result. If there are more
        just take the first two

        Parameters
        ----------
        s : String
            the provided input

        Returns
        -------
        int
            the 2 numbers add
    """
    try:
        numbers = s.strip().split()
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



def main():
    print("Hello World!")
    arg = '25.0 67.0'
    print(arg)
    handle(arg)

if __name__ == "__main__":
    main()
