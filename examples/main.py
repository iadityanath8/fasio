

def hellp():
    print("Hello")
    yield

    print("Bye")



a = hellp()
next(a)
next(a)
