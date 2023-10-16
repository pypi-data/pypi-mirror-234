def Figonacci(n):
    if n < 0:
        return None

    elif n == 0:
        return 0

    elif n == 0:
        return 1

    else:
        dict = [0, 1, 1]
        for i in range(2, n):
            dict[0] = dict[1]
            dict[1] = dict[2]
            dict[2] = dict[1] + dict[0]
        return dict[2]
