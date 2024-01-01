import sys
num1 = 4
num2 = 5
num3 = 6

for i in range(1, 4):
    print(eval(f"num{i}")) 

for i in range(3):
    exec(f'num{i} = {i}')

# Check the values
print(num1, num2)

print(sys.path)