def random_decomposition(total, max_cnt):
    import random
    cnt = max_cnt
    assert cnt >= 1
    while total > 0:
        if cnt == 1:
            n = total
        else:
            n = random.randint(1, total)
            cnt -= 1
        yield n
        total -= n


if __name__ == "__main__":
    # will divide total 1000 randomly, and get a list with length <= 10
    print(list(random_decomposition(1000, 10)))
