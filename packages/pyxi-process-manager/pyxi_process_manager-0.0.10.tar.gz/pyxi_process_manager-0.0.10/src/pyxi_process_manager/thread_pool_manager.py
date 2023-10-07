import concurrent.futures

def core_fn():
    pass


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(core_fn, range(5))
