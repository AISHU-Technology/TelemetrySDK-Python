def add(x: int, y: int) -> int:
    return x + y


def multiply(x: int, y: int) -> int:
    return x * y


if __name__ == "__main__":
    # 业务代码
    num = add(1, 2)
    num = multiply(num, 2)
    num = add(num, 3)
    num = multiply(num, 4)
    print(num)
