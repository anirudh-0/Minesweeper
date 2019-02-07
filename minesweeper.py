import time
start_time=time.time()
from tkinter import *
root = Tk()
root.title("Minesweeper")
root.geometry("350x300")
displayframe=Frame(root)
displayframe.pack()
im2 =PhotoImage(file="flag.png")
im = PhotoImage(file="start.png")


class cfrm:
	def __init__(self,root):
		self.frm=Frame(root,width=250,height=25,background="gray30")
		self.frm.pack_propagate(0)
		self.frm.pack()


class butt:
	def __init__(self,frm,im,i,j):
		self.i=i
		self.j=j
		self.frm=frm.frm
		self.im=im
		self.b=Button(self.frm,image=self.im,width=23,bd=1,height=23,highlightthickness=0,background="gray62")
		self.b.bind("<Button-1>",self.action)
		self.b.bind("<Button-3>",self.flaggg)
		self.b.grid(row=self.j,column=self.i)

	def action(self,event):
		self.b.destroy()
		self.frm=Frame(self.frm,width=25,height=25,background="gray62")
		self.frm.grid_propagate(0)
		self.frm.grid(row=self.j,column=self.i,sticky=E)
		self.b=Label(self.frm,bd=2,background="gray62")
		# self.b=Label(self.frm,textvariable=bombs,bd=2,background="gray62")	#Have to define TextVar
		self.b.grid_propagate(0)
		self.b.grid(row=0,column=0,padx=1,pady=1)

	def flaggg(self,event):
		if self.im==im:
			self.im=im2
		elif self.im==im2:
			self.im=im
		self.b=Button(self.frm,image=self.im,width=23,bd=1,height=23,highlightthickness=0,background="gray62")
		self.b.bind("<Button-3>",self.flaggg)
		if self.im==im:
			self.b.bind("<Button-1>",self.action)
		self.b.grid(row=self.j,column=self.i)


for j in range(10):
	c=cfrm(root)
	for i in range(10):
		b=butt(c,im,i,j)
elapsed=round(time.time()-start_time,2)
print("[Time elapsed : {}s]".format(elapsed))
root.mainloop()