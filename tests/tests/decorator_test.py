class A(object):

    @property
    def b(self):
        return 'sobaka'

s = A.b
pass


#from random import choice
#from tests.pages import HomePage
#
#print {x * x for x in range(10)}
#print [x * x for x in range(10)]
#print (x * x for x in range(10))
#print dict((x, x * x) for x in range(10))
#
#list1 = [7, 2, 3, 10, 12]
#list2 = [-1, 1, -5, 4, 6]
#print map(lambda x, y: x*y, list1, list2)
#
#d = {'a': 'sobaka', 'b': 'kote', 'c': 'kote2', 'd': 'kote3', 'e': 'kote4'}
#print d
#print choice([';\r\n', ',\r\n']).join(["%s=%s" % (k, v) for k, v in d.items()])
#d['a'] = 'lol'
#print d
#a = 'asdfasd'
#print [arg for arg in dir(HomePage) if callable(getattr(HomePage, arg))]
#print 'a' ^ 'b'