import random

def list_like(data):
    return isinstance(data, tuple) or isinstance(data, list)

def randint(minn, maxn):
    return random.randint(minn, maxn)

def randfloat(minn, maxn):
    return random.uniform(minn, maxn)