import argparse
import json

def get_data():
    try:
        f = open('storage.data', 'r+', encoding='utf-8')
        data = json.load(f)
        f.close()
    except:
        data = {}
    return data

def safe_data(data):
    f = open('storage.data', 'w+', encoding='utf-8')
    json.dump(data, f)
    f.close()


def get_value(key):
    data = get_data()
    return data[key]

def set_value(key, value):
    data = get_data()
    if key in data:
        data[key].append(value)
    else:
        data[key] = [value]
    safe_data(data)

def main():
    parser = argparse.ArgumentParser(description="CLI утилита для добавление записей")
    parser.add_argument('--key', type=str, help='Ключ')
    parser.add_argument('--val', help='значение')
    args = parser.parse_args()
    if args.key and args.val:
        set_value(args.key, args.val)
    elif args.key:
        val = get_value(args.key)
        print(', '.join(val))
    else:
        print("ВВеди правильно, балда")


if __name__ == '__main__':
    main()