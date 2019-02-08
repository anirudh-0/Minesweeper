import time
start_time=time.time()
from sys import exit
import numpy as np
from tkinter import *
root = Tk()
root.title("Minesweeper")
root.geometry("350x300")
displayframe=Frame(root)
displayframe.pack()
im3 = PhotoImage(file="bomb.png")
im2 = PhotoImage(file="flag.png")
im  = PhotoImage(file="start.png")
imone = PhotoImage(file="1.png")
imtwo = PhotoImage(file="2.png")
imthree = PhotoImage(file="3.png")
imfour = PhotoImage(file="4.png")
imfive = PhotoImage(file="5.png")

#click counter to determine win
cc=np.zeros(1,dtype=int)

#Mine config
mine_loc=np.zeros(100,dtype=int)
mine_loc[0:10]=10
np.random.shuffle(mine_loc)
mine_loc=mine_loc.reshape(10,10)

#Mine count
mine_count=np.copy(mine_loc)
p,q=mine_count.shape
for i in range(p):
	for j in range(q):
		if mine_loc[i,j]==0:
			count=0
			for l in range(-1,2):
				for m in range(-1,2):
					if (i+l) in range(10) and (j+m) in range(10) and mine_loc[i+l,j+m]!=0:
						count+=1
			mine_count[i,j]=count
		else:
			pass

def click_count():
	cc[0]=cc[0]+1
	if cc[0]==90:
		win()
		sys.exit()
	else:
		pass

def win():
	root2=Tk()
	root2.geometry("150x100")
	lab=Label(root2,text="YOU WIN!")
	lab.pack()
	root2.mainloop()

def gameover():
	root2=Tk()
	root2.geometry("150x100")
	lab=Label(root2,text="GAME OVER :(")
	lab.pack()
	root2.mainloop()

class cfrm:
	def __init__(self,root):
		self.frm=Frame(root,width=250,height=25,background="gray30")
		self.frm.pack_propagate(0)
		self.frm.pack()


class butt:
	def __init__(self,frm,im,i,j):
		self.i=i
		self.j=j
		self.status=1			# to avoid recursion while clearing blanks
		self.frm=frm.frm
		self.im=im
		self.b=Button(self.frm,image=self.im,width=23,bd=1,height=23,highlightthickness=0,background="gray62")
		self.b.bind("<Button-1>",self.action)
		self.b.bind("<Button-3>",self.flaggg)
		self.b.grid(row=self.i,column=self.j)

	def action(self,event=None):
		# if cc[0]==0:
		# 	mine_config()
		self.b.destroy()
		self.status=0
		self.frm=Frame(self.frm,width=25,height=25,background="gray30")
		self.frm.grid_propagate(0)
		self.frm.grid(row=self.i,column=self.j,sticky=E)
		if mine_loc[self.i,self.j]!=0:
			gameover()
			sys.exit()
		else:
			self.im=self.countdisp()
		self.b=Label(self.frm,image=self.im,width=23,bd=1,height=23,background="gray62")
		# self.b=Label(self.frm,textvariable=bombs,bd=2,background="gray62")	#Have to define TextVar
		self.b.grid_propagate(0)
		self.b.grid(row=0,column=0,padx=1,pady=1)
		click_count()

	def flaggg(self,event):
		if self.im==im:
			self.im=im2
		elif self.im==im2:
			self.im=im
		self.b=Button(self.frm,image=self.im,width=23,bd=1,height=23,highlightthickness=0,background="gray62")
		self.b.bind("<Button-3>",self.flaggg)
		if self.im==im:
			self.b.bind("<Button-1>",self.action)
		self.b.grid(row=self.i,column=self.j)

	def countdisp(self):
		self.count=mine_count[self.i,self.j]
		for l in range(-1,2):
			for m in range(-1,2):
				condition=(self.i+l) in range(10) and (self.j+m) in range(10) and buttonslist[self.i+l,self.j+m].status==1
				condition1= condition and self.count!=10 and self.count!=0 and mine_count[self.i+l,self.j+m]==0
				condition2= condition and self.count==0
				if condition1 or condition2:
					buttonslist[self.i+l,self.j+m].status=0
					buttonslist[self.i+l,self.j+m].action()

		switch={
		1:imone,
		2:imtwo,
		3:imthree,
		4:imfour,
		5:imfive
		}
		return switch.get(self.count,im)


buttonslist=np.empty((10,10),dtype=butt)
for i in range(10):
	c=cfrm(root)
	for j in range(10):
		b=butt(c,im,i,j)
		buttonslist[i,j]=b


elapsed=round(time.time()-start_time,2)
print("[Time elapsed : {}s]".format(elapsed))
root.mainloop()
