def main():
    while True:
        command = input("Enter the command: ")
        if command in ["good bye", "close", "exit"]:
            exit()

if __name__ == "__main__":
    main()