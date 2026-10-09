import sys


def main():
    line = list(map(int, input().split()))
    size = line[0]
    columns = line[1:]
    i = 0
    max_square = min(columns)
    bigger_rectangle = [columns[0]]
    for i in range(len(columns) - 1):
        if columns[i] <= columns[i + 1]:
            bigger_rectangle.append(columns[i + 1])
        else:
            while len(bigger_rectangle) > 0:
                rec = bigger_rectangle.pop(0)
                max_square = max(rec * (len(bigger_rectangle) + 1), max_square)
            bigger_rectangle.append(columns[i + 1])
    
    print(max_square)



if __name__ == '__main__':
    main()
