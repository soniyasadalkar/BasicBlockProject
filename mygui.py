from Tkinter import *
import tkMessageBox
from main import *
import ScrolledText

root = Tk()
root.wm_title("BASIC BLOCK")
top = Frame(root)

top.pack()
text = ScrolledText.ScrolledText(root)
fn = None
root1 = None
top1 = None
text1 = None

root2 = None
top2 = None
text2 = None
curr_block = None

def load():
	global fn
	fn = e.get()
	
	list1 = create_fr()
	
	f = open(fn,"r")
	instrn = f.readline()
	
	while instrn :
		list1[2].insert(INSERT, instrn)
		instrn  = f.readline()
	f.close()
	
	B = Button(list1[1],text="Create Basic Blocks",command=create_bb)
	B.pack(side = BOTTOM)
	
def create_bb():
	global text
	global top
	create_fr()
	list_of_bb = create(text,fn)
	create_buttons(top,list_of_bb)
	
def create_buttons(top,list_of_bb):
	for i in range(1,len(list_of_bb)+1):
		bb_button(i,list_of_bb[i-1])


def bb_button(i,bb):
	global top
	B = Button(top,text="BASIC"+str(i),command = lambda:create_bbfr(bb))
	B.pack(side = LEFT)


def create_bbfr(b_obj):
	global root1
	global top1
	global text1
	
	root1 = Tk()
	
	top1 = Frame(root1)
	top1.pack()
	text1 = ScrolledText.ScrolledText(root1)
	text1.pack()
	
	b_obj.display(text1)

	list_optimize(b_obj)

def list_optimize(bb):
	global top1
	global curr_block 
	B = Button(top1,text="Algebraic Simplification",command = lambda: wrapper(bb,bb.algebraic_simplification))
	B.pack(side = LEFT)
	B1 = Button(top1,text="Constant Folding",command =lambda:wrapper(bb,bb.const_folding ))
	B1.pack(side = LEFT)
	B2 = Button(top1,text="Const|Var Propagation",command =lambda:wrapper(bb,bb.const_propagation))
	B2.pack(side = LEFT)
	B3 = Button(top1,text="Common Subexpression",command =lambda:wrapper(bb,bb.subexpression))
	B3.pack(side = LEFT)

def clear():
	global text1
	text1.delete(1.0,END)

def wrapper(bb,func_nm):
	global text2
	global root2
	global top2

	func_nm()
	
	root2 = Tk()
	top2 = Frame(root2)
	top2.pack()
	text2 = ScrolledText.ScrolledText(root2)
	text2.pack()
	bb.display(text2)

def create_fr():
	global root
	global top
	global text
	global sbar
	root.destroy()
	root = Tk()
	top = Frame(root)
	top.pack()
	text = ScrolledText.ScrolledText(root)
	text.pack()
	
	return root,top,text

	


inpfile = Label(top,text = 'Input FileName ')
inpfile.pack(side=TOP)
e = Entry(top)
e.pack(side = TOP)

B = Button(top,text="SUBMIT",command=load)
B.pack(side = TOP)

root.mainloop()
