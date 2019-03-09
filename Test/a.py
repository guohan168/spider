class a():
    num = 0


if __name__ == "__main__":
    obj1 = a()
    obj2 = a()
    print(obj1.num, obj2.num, a.num)

    obj2.num += 1
    print(obj1.num, obj2.num, a.num)

    a.num += 2
    print(obj1.num, obj2.num, a.num)

    obj1.num += 1
    print(obj1.num, obj2.num, a.num)