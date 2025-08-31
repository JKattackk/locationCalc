while True:
        print("Waiting for input: ")
        userInput = input()
        if userInput == "r":
            print("starts a new search")
        elif userInput == "p":
            print("shows a plot")
        elif userInput == "u":
            print("removes a sphere")
        else:
            inputNumbers = []
            userInput = userInput.split()
            for string in userInput:
                try:
                    inputNumbers.append(float(string))
                except:
                    print(string, " not a valid number, ignoring")
            if len(inputNumbers) == 0:
                print("grabs coordinates from clipboard and makes a spbere with default radius")
            elif len(inputNumbers) == 1:
                rad1 = inputNumbers[0]
                print("makes a sphere with coordinates from clipboard and radius: ", rad1)
            elif len(inputNumbers) == 2:
                [rad1, rad2] = [inputNumbers[0], inputNumbers[1]]
                print("makes a sphere with coordinates from clipboard, inner radius: ", rad2, " and outer radius: ", rad1)
            elif len(inputNumbers) == 4:
                sphere = inputNumbers
                print("creates sphere", sphere)
            elif len(inputNumbers) == 5:
                sphere = inputNumbers
                print("creates sphere", sphere)
            else:
                print("not valid input")
                      