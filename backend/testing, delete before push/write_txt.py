# Open a file named 'hello_world.txt' in write mode
with open('hello_world.txt', 'w') as file:
    # Write the string 'Hello World' to the file
    file.write('Hello World')

# Open the file in read mode and print its contents
with open('hello_world.txt', 'r') as file:
    contents = file.read()
    print(contents)
