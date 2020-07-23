class foo(object):
    def decorate(self):
        print("STARTING DECOR")
        @func
        def magic():
            print("THIS IS MAGIC")
            print("ENDING MAGIC")
        return magic
        
    
    def f(self):
        print("INSIDE MAGIC")

def func(fo):
    print("FUNC")
    fo()
    print("END FUNC")


m = foo()
m.decorate()
