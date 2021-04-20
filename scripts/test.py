import sys

result = sys.argv

with open(f'test.txt', 'a+') as f:
    f.write(f"{result}")