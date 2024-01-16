# f = open("demo.txt",mode='w')
# f.write("Hello I am Python!")
# f.close()


# f=open("demo.txt",mode="r")
# file_content=f.read()
# print(file_content)

# f=open("demo.txt",mode="a")
# f.write("I will start Data science!\n")
# f.close()


# f=open("demo.txt",mode="r")
# file_content=f.read()
# print(file_content)

# f=open("demo.txt",mode="r")
# file_content=f.readlines()
# print(file_content[0][:5])


f=open("demo.txt",mode="r")
file_content=f.readline()
while file_content:
    print(file_content)
    file_content=f.readline()
f.close()