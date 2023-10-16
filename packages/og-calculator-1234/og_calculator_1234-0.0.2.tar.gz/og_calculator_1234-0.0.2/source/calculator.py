class Calculator:
    '''Calculator can add, subtract, multiply, divide, & do nth root

    ...

    Attributes
    ----------
    memory : int
        calculator memory, starts at and resets to 0

    Methods
    -------
    add
        Adds new number to number stored in memory
    subtract
        Subtracts new number from number stored in memory
    multiply
        Multiplies number stored in memory by new number
    divide
        Divides number stored in memory by new number
        returns error if new number is 0
    nth root
        Calculates new number as nth root of number in memory
        returns error if either number is negative
    reset_memory
        Resets calculator memory to 0
    get_memory
        Shows what is currently stored in calculator memory
    '''

    def __init__(self):
        self.memory = 0

    def add(self, x):
        self.memory += x
        return self.memory

    def subtract(self, x):
        self.memory -= x
        return self.memory

    def multiply(self, x):
        self.memory *= x
        return self.memory

    def divide(self, x):
        if x != 0:
            self.memory /= x
            return self.memory
        else:
            return "Error! Division by zero."

    def nth_root(self, x):
        if self.memory >= 0 and x >= 0:
            return self.memory ** (1 / x)
        else:
            raise ValueError("Cannot calculate nth root of a negative number.")

    def reset_memory(self):
        self.memory = 0
        return "Memory reset to 0."

    def get_memory(self):
        return self.memory

def main():
    '''Contains user input statements and returns based on user input
    User inputs number (1-8) to select operation from menu
    User inputs number for calculation
    Calculation is performed with number stored in memory
    '''
    calc = Calculator()
    print("Welcome to the Calculator!")
    while True:
        print("Current Memory:", calc.get_memory())
        print("Select operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. nth root")
        print("6. Get Memory")
        print("7. Store to Memory")
        print("8. Reset Memory")
        print("9. Exit")

        choice = input("Enter choice(1/2/3/4/5/6/7/8/9): ")

        if choice == '1':
            num = float(input("Enter number to add: "))
            print("Result:", calc.add(num))

        elif choice == '2':
            num = float(input("Enter number to subtract: "))
            print("Result:", calc.subtract(num))

        elif choice == '3':
            num = float(input("Enter number to multiply: "))
            print("Result:", calc.multiply(num))

        elif choice == '4':
            num = float(input("Enter number to divide: "))
            print("Result:", calc.divide(num))

        elif choice == '5':
            num = float(input("Enter number for nth root: "))
            print("Result:", calc.nth_root(num))

        elif choice == '6':
            print("Memory currently stores:", calc.memory)

        elif choice == '7':
            num = float(input("Enter number to store in memory: "))
            calc.memory = num
            print("Memory set to:", calc.memory)

        elif choice == '8':
            print(calc.reset_memory())

        elif choice == '9':
            print("Exiting calculator.")
            break

        else:
            print("Invalid Input")

if __name__ == "__main__":
    main()
