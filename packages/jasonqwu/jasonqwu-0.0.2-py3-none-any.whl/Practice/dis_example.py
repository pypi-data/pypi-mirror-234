import dis

def g():
    import math as m
    def f():
        d['a'] = 1
    b = a.attr
    b = a.method()
    return f

code = g.__code__
dis.dis(g)
print(f"code.co_code: {code.co_code}")
print(f"code.co_name: {code.co_name}")
print(f"code.co_filename: {code.co_filename}")
print(f"code.co_lnotab: {code.co_lnotab}")
print(f"code.co_flags: {code.co_flags}")
print(f"code.co_stacksize: {code.co_stacksize}")
print(f"code.co_argcount: {code.co_argcount}")
print(f"code.co_posonlyargcount: {code.co_posonlyargcount}")
print(f"code.co_kwonlyargcount: {code.co_kwonlyargcount}")
print(f"code.co_nlocals: {code.co_nlocals}")
print(f"code.co_varnames: {code.co_varnames}")
print(f"code.co_names: {code.co_names}")
print(f"code.co_cellvars: {code.co_cellvars}")
print(f"code.co_freevars: {code.co_freevars}")
print(f"code.co_consts: {code.co_consts}")
