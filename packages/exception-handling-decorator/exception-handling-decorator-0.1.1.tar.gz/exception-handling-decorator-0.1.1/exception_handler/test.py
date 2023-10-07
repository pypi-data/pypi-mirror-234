import random
from exception_handler import ExceptionHandler


class SomeException(Exception):

    def __str__(self) -> str:
        return "SomeException message"

class SomeOtherException(Exception):
    def __str__(self) -> str:
        return "SomeOtherException message"

def get_rand_bool():
    """
    Returns ranfom boolean value
    """
    rand_int = random.getrandbits(1)
    return bool(rand_int)

def handle_exception1(ex):
    print(f"Exception message handling_func1: {ex}")

def handle_exception2(ex):
    print(f"Exception message handling_func2: {ex}")

@ExceptionHandler(handling_func=handle_exception1, reraise=False)
def divide_by_zero():
        x = 0
        x = 1 / 0
        print(x)


def do_something():
    if get_rand_bool():
        try:
            raise SomeException
        except SomeException as e:
            handle_exception1(e)
            raise
    try:
        raise SomeOtherException
    except SomeOtherException as e:
        handle_exception2(e)

def run_functions():
    divide_by_zero()
    #do_something()

run_functions()