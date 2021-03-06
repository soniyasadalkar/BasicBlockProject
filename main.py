from new_basic_block import *
from Tkinter import *
from collections import OrderedDict


def create(text,fn):
	f = open(fn,"r")
	jumps = ['jmp','jge','jgt','jlt','jle']
	list_blocks = []
	instrn = f.readline()
	pat = "[a-z|A-Z][a-z|A-Z|0-9]*[\s]*:"
	count = 1

	b = block()
	b.start = count
	end_file=False
	
	block_d = {}	

	while instrn :
		instrn = instrn.strip() 
		temp = instrn
		first_word = instrn.split(' ')[0]
		instrn  = f.readline()

		if(first_word in jumps):
			b.end = count
			list_blocks.append(b)
			b.instrn_list[count] = temp
			b.instrn_numbs.append(count)

			if(instrn):
				b = block()
				b.start = count + 1
				end_file=False
			else:
				end_file = True

		elif(re.match(pat,first_word)):
			second_word = temp.split(' ')[1]
		
			if(count is not 1):
				b.end = count - 1
				list_blocks.append(b)
		
			b = block()
			b.start = count

			if(second_word in jumps):
				b.end = b.start
				b.instrn_list[count] = temp
				b.instrn_numbs.append(count)
				list_blocks.append(b)
				b=block()
				b.start = count + 1
			
			b.instrn_list[count] = temp		
			b.instrn_numbs.append(count)
		else:
			b.instrn_list[count] = temp
			b.instrn_numbs.append(count)
	
		count = count + 1
	
	if(not end_file):
		b.end = count - 1
		list_blocks.append(b)
	

	i = 1
	for b in list_blocks:
		block_d["BASIC"+str(i)] = b.display
		i = i + 1
		b.display(text)	

	
	return list_blocks

