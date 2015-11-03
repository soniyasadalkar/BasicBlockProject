#a = a * 32

import re
from collections import OrderedDict
from Tkinter import *

class block(object):

	__slots__ = ['start','end','instrn_numbs','instrn_list']

	def __init__(self):
		self.instrn_list = OrderedDict()
		self.instrn_numbs = []
	
	def display(self,text):
		for i in self.instrn_numbs:
			text.insert(INSERT,self.instrn_list[i])
			text.insert(INSERT,"\n")
						
		text.insert(INSERT,"\n")


	def check_label(self,string):
		first_word = string.split(' ')[0]
		pat = "[a-z|A-Z][\w]*[\s]*:"
		m = re.match(pat,first_word)
		
		if(m):
			return True
		else:
			return False
	
	def is_power2(self,num):
		for i in range(num/2 + 1):
			if(num == pow(2,i)):
				return i
		return 0
		
	def fun1234(self,i,string):
		if(self.check_label(self.instrn_list[i])):
			first_word = string.split(' ')[0]
			self.instrn_list[i] = first_word
		else:
			del self.instrn_list[i]
			self.instrn_numbs.remove(i)

	def fun5(self,i,m5,string):
		res_instrn = m5.group(1) + ' = ' + m5.group(5) + ' * ' + m5.group(5)
					 
		if(self.check_label(self.instrn_list[i])):
				first_word = string.split(' ')[0]
				self.instrn_list[i] = first_word + ' ' + res_instrn
		else:
				self.instrn_list[i] = res_instrn
				
		
	def fun6(self,i,m6,string):
		
		p = self.is_power2(int(m6.group(9)))
				
		if(p):
	
			res_instrn = m6.group(1) + ' = ' + m6.group(5) + ' << ' + str(p)
			 
			if(self.check_label(self.instrn_list[i])):
					first_word = string.split(' ')[0]
					self.instrn_list[i] = first_word + ' ' + res_instrn
			else:
					self.instrn_list[i] = res_instrn
	
	def add(self,i,m7):
		result = int(m7.group(5)) + int(m7.group(9))
		res_instrn = m7.group(1) + ' = ' + str(result)
		return res_instrn
		
	def sub(self,i,m7):
		result = int(m7.group(5)) - int(m7.group(9))
		res_instrn = m7.group(1) + ' = ' + str(result)
		return res_instrn

	def mul(self,i,m7):
		result = int(m7.group(5)) * int(m7.group(9))
		res_instrn = m7.group(1) + ' = ' + str(result)
		return res_instrn

	def div(self,i,m7):
		result = int(m7.group(5)) / int(m7.group(9))
		res_instrn = m7.group(1) + ' = ' + str(result)
		return res_instrn

	def fun7(self,i,res_instrn,string):
		 
		if(self.check_label(self.instrn_list[i])):
				first_word = string.split(' ')[0]
				self.instrn_list[i] = first_word + ' ' + res_instrn
		else:
				self.instrn_list[i] = res_instrn
	
	def fun8(self,i,string):
		if(self.check_label(self.instrn_list[i])):
			first_word = string.split(' ')[0]
			self.instrn_list[i] = first_word
		else:
			del self.instrn_list[i]
			self.instrn_numbs.remove(i)


	def algebraic_simplification(self):
		#remove identities
		pat1 = "([a-zA-Z][\w]*)(\s)*([=])(\s)*([a-zA-Z][\w]*)(\s)*([+])(\s)*([0])" #a = a + 0
		pat2 = "([a-zA-Z][\w]*)(\s)*([=])(\s)*([0])(\s)*([+])(\s)*([a-zA-Z][\w]*)" #a = 0 + a
		pat3 = "([a-zA-Z][\w]*)(\s)*([=])(\s)*([a-zA-Z][\w]*)(\s)*([*])(\s)*([1])(\s)" #a = a * 1
		pat4 = "([a-zA-Z][\w]*)(\s)*([=])(\s)*([1])(\s)*([*])(\s)*([a-zA-Z][\w]*)" #a = 1 * a
		
		#exponentiation operator to multiplication		
		pat5 = "([a-zA-Z][\w]*)(\s)*([=])(\s)*([a-zA-Z][\w]*)(\s)*([*][*])(\s)*([2])"
				
		# x = x * 8 ==> x = x << 3
		pat6 = "([a-zA-Z][\w]*)(\s)*([=])(\s)*([a-zA-Z][\w]*)(\s)*([*])(\s)*([\d][\d]*)"

		
		#rem_list = []
		
		temp = list(self.instrn_numbs)	
		for i in temp:
			
			string = self.instrn_list[i]	
			m1 = re.search(pat1,string)
			m2 = re.search(pat2,string)
			m3 = re.search(pat3,string)
			m4 = re.search(pat4,string)
			m5 = re.search(pat5,string)
			m6 = re.search(pat6,string)
			
			if(m5):
				self.fun5(i,m5,string)
						
			elif(m6):
				self.fun6(i,m6,string)
			
			elif(m1):
				if(m1.group(1) == m1.group(5)):
					self.fun1234(i,string)
			elif(m2):
				if(m2.group(1) == m2.group(9)):
					self.fun1234(i,string)
			elif(m3):
				if(m3.group(1) == m3.group(5)):
					self.fun1234(i,string)
			elif(m4):
				if(m4.group(1) == m4.group(9)):
					self.fun1234(i,string)
	
			
					
	def const_propagation(self):
		for i in self.instrn_numbs:
			stmt = self.instrn_list[i]	
				
			asgn_pattern = "([a-zA-Z][\w]*)(\s)*([=])(\s)*([\w]+)(?!.)"
			
			m = re.search(asgn_pattern,stmt)
			count = len(self.instrn_numbs)
			k = self.instrn_numbs.index(i) + 1
			flag=True
			
			if(m):
				
				var = m.group(1)
				num = m.group(5)			
				while(k < count and flag):
					j = self.instrn_numbs[k] 
					pat1 = "([a-zA-Z][\w]*)([\s]*[=][\s]*)(?P<op1>[\w])((?P<opr>[\s]*[\-+*/][\s]*)(?P<op2>[\w]))?"
					nxt_instrn = self.instrn_list[j]	
						
					m1 = re.search(pat1,nxt_instrn)
					if(m1):
						lhs = m1.group(1)
						equal = m1.group(2)
						op1 = m1.group("op1")
				
						op2 = m1.group("op2")
						opr = m1.group("opr")
						res_instrn = nxt_instrn
						if(op1 == var):
							if(op2):
								res_instrn = lhs + equal + num + opr + op2

							else:
								res_instrn = lhs + equal + num 
					
							op1 = num

						if(op2 == var):
								res_instrn = lhs + equal + op1 + opr + num

						self.replace_instrn(j,res_instrn,nxt_instrn) 
						if(m1.group(1) == var):
							flag = False
							
					k = k + 1
					
	def subexpression(self):
		for i in self.instrn_numbs:
			stmt = self.instrn_list[i]
			
			asgn_pat = "([a-zA-Z][\w]*)(\s)*([=])(\s)*([\w\-+*/\s]+)"

			m = re.search(asgn_pat,stmt)
			
			count = len(self.instrn_numbs)
			k = self.instrn_numbs.index(i) + 1
			flag=True

			if(m):
				var = m.group(1)
				while(k < count and flag):
									
					j = self.instrn_numbs[k] 
					pat1 = "([a-zA-Z][\w]*)([\s]*[=][\s]*)([\w\-+*/\s]+)"
					nxt_instrn = self.instrn_list[j]	
					m1 = re.search(pat1,nxt_instrn)
					
					if(m1):
						if(m1.group(3) == m.group(5)):
							res_instrn = m1.group(1) + m1.group(2) + var
							self.replace_instrn(j,res_instrn,nxt_instrn)
					k = k + 1
	
 
	def replace_instrn(self,i,res_instrn,string):

		if(self.check_label(self.instrn_list[i])):
				first_word = string.split(' ')[0]
				self.instrn_list[i] = first_word + ' ' + res_instrn
		else:
				self.instrn_list[i] = res_instrn
					
	def const_folding(self):
		pat7 = "([a-zA-Z][\w]*)(\s)*([=])(\s)*([-]?[\d][\d]*)(\s)*([-|+|*|/])(\s)*([-]?[\d][\d]*)"
		op_fun = {'+':self.add,'-':self.sub,'*':self.mul,'/':self.div}	
		for i in self.instrn_numbs:
		
			string = self.instrn_list[i]
		
			m7 = re.search(pat7,string)
			if(m7):
				res_instrn = op_fun[m7.group(7)](i,m7)
			
				self.fun7(i,res_instrn,string)		

