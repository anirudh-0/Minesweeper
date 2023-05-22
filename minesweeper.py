import time
import gc
import sys
import math
import numpy as np
from tkinter import *
from tkinter import messagebox as msg



root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.title("Minesweeper")
w1=w/2-270/2
h1=h/2-350/2
root.geometry("%dx%d+%d+%d" % (270,350,w1,h1))
root.configure(background="gray30")
try:
	im3 = PhotoImage(file="bomb.png")
	im2 = PhotoImage(file="flag.png")
	im  = PhotoImage(file="Start.png")
	imone = PhotoImage(file="1.png")
	imtwo = PhotoImage(file="2.png")
	imthree = PhotoImage(file="3.png")
	imfour = PhotoImage(file="4.png")
	imfive = PhotoImage(file="5.png")
except Exception as e:
	print(e)
	sys.exit()
 
highscore=1000
cheatlist="abcdefghij"

def cheat(event):
	global cheatlist, buttonslist, mine_loc
	cheatlist=cheatlist+event.char
	cheatlist=cheatlist[1:]
	if event.char=="t" and cheatlist[5:]=="cheat":
		for i in range(10):
			for j in range(10):
				if mine_loc[i,j]==10:
					buttonslist[i,j].b.config(background="red")


root.bind("<Key>",cheat)


def main():
	global mine_loc, buttonslist, flagc
	flagc=0
	displayframe=Frame(root,background="gray30")
	displayframe.pack()
	frm001=Frame(displayframe,width=250,height=45,background="gray30")
	frm001.pack_propagate(0)
	frm001.pack()
	#click counter to determine win
	cc=np.zeros(1,dtype=int)

	#Mine config
	mine_loc=np.zeros(100,dtype=int)
	mine_loc[0:10]=10
	np.random.shuffle(mine_loc)
	mine_loc=mine_loc.reshape(10,10)
	#Mine count
	def minecount():
		global mine_count
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

	minecount()

	def click_count():
		global time1
		cc[0]=cc[0]+1
		if cc[0]==90:
			win()
		elif cc[0]==1:
			time1=time.time()
			tick()
		else:
			pass


	class cfrm:
		def __init__(self,displayframe):
			self.frm=Frame(displayframe,width=250,height=25,background="gray30")
			self.frm.pack_propagate(0)
			self.frm.pack()

		def destroy(self):
			self.frm.destroy()


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

		def destroy(self):
			self.b.destroy()
			self.frm.destroy()

		def action(self,event=None):
			global mine_loc
			if cc[0]!=0 or mine_loc[self.i,self.j]==0:
				
				self.b.destroy()
				self.status=0
				self.frm=Frame(self.frm,width=25,height=25,background="gray30")
				self.frm.grid_propagate(0)
				self.frm.grid(row=self.i,column=self.j,sticky=E)
				if mine_loc[self.i,self.j]!=0:
					gameover()
					self.im=im3
					sys.exit()
				else:
					self.im=self.countdisp()
				self.b=Label(self.frm,image=self.im,width=23,bd=1,height=23,background="gray62")
				self.b.grid_propagate(0)
				self.b.grid(row=0,column=0,padx=1,pady=1)
				click_count()
			else:
				np.random.shuffle(mine_loc)
				minecount()
				self.action()

		def flaggg(self,event):
			global flagc
			if self.im == im:
				flagc = flagc + 1
				self.im=im2
			elif self.im == im2:
				flagc = flagc - 1
				self.im = im
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
			5:imfive,
			6:im,
			7:im,
			8:im
			}
			return switch.get(self.count,im)


	buttonslist=np.empty((10,10),dtype=butt)
	for i in range(10):
		c=cfrm(displayframe)
		for j in range(10):
			b=butt(c,im,i,j)
			buttonslist[i,j]=b

	def reset():
		global id
		clock.after_cancel(id)
		displayframe.destroy()
		gc.collect()
		main()

	bfrm=Button(frm001,text="Reset",command=reset,background="gray62",highlightthickness=0,font=[11],width=6)
	clock=Label(frm001,bg="gray62",highlightthickness=0,bd=1,relief=RIDGE,font=[11],width=7,anchor=E)
	mine=Label(frm001,bg="gray62",highlightthickness=0,bd=1,relief=RIDGE,font=[11],width=7,anchor=E)
	bfrm.pack(expand=0,fill=BOTH,anchor=S,side=LEFT,padx=(0,2),pady=(15,3))
	clock.pack(expand=0,fill=BOTH,anchor=S,side=RIGHT,padx=(2,1),pady=(15,3))
	mine.pack(expand=0,fill=BOTH,anchor=S,side=RIGHT,padx=(2,1),pady=(15,3))
	clock.config(text="0 ")
	mine.config(text="10 ** ")
	frm002=Frame(displayframe,width=250,height=45,background="gray30")
	frm002.pack_propagate(0)
	frm002.pack()
	quitb=Button(frm002,text="QUIT !",command=root.destroy,background="gray62",highlightthickness=0,font=[11])
	quitb.pack(expand=True,fill=BOTH,pady=(3,15))

	def win():
		global id,time1,highscore
		score=round(time.time()-time1,1)
		clock.after_cancel(id)
		if score<highscore:
			highscore=score
			msg.showinfo(" ","YOU WIN!\nNEW HIGHSCORE!!")
		else:
			msg.showinfo(" ","YOU WIN!")

	def gameover():
		global id
		clock.after_cancel(id)
		msg.showinfo(" ","You lose :(!")
		reset()

	def tick():
		global time1,id,flagc
		time2=math.floor(time.time()-time1)
		clock.config(text=time2)
		mine.config(text="{} ** ".format(10-flagc))
		id=clock.after(100,tick)

	root.mainloop()


if __name__=="__main__":
	main()
