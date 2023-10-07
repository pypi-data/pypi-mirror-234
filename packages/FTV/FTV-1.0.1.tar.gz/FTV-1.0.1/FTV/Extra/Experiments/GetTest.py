

def test(func):
    def wrapper(*args):
        print("->")
        func(*args)
        print("<-")

    return wrapper

@test
def run(value):
    print(value)


run("lahav")
