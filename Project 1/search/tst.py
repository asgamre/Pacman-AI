import util

class A():
	def __init__(self,a,b):
		print a
	
a = A(1,2)	
s = util.Stack()
s.push(a)

s.push(['1'])

t = s.pop()
print t