import threading
import random
from tkinter import *
from queue import Queue
import time
import os
fl=False
guiEventQueue=Queue()
gridOfEnviornment=[]
ashtarg=(-1,-1)

class agent:
  @staticmethod
  def sensor(pos):
    px,py=pos
    curD=enviornment.distance(pos)
    ret=[]
    if enviornment.distance((px+1,py))<curD:
      if enviornment.distance((px+1,py))!=0:
        ret.append((px+1,py,False))
      else:
        ret.append((px+1,py,True))
    if enviornment.distance((px-1,py))<curD:
      if enviornment.distance((px-1,py))!=0:
        ret.append((px-1,py,False))
      else:
        ret.append((px-1,py,True)) 
    if enviornment.distance((px,py+1))<curD:
      if enviornment.distance((px,py+1))!=0:
        ret.append((px,py+1,False))
      else:
        ret.append((px,py+1,True))
    if enviornment.distance((px,py-1))<curD:
      if enviornment.distance((px,py-1))!=0:
        ret.append((px,py-1,False))
      else:
        ret.append((px,py-1,True))
    return ret
  @staticmethod
  def actuator(pos,newpos,name):
    global gridOfEnviornment
    x,y=pos
    nx,ny=newpos
    l=[]
    l.append(int(name))
    l.append(False)
    l.append((x,y))
    #to_delete the name from previos position
    guiEventQueue.put(l)
    l1=[]
    l1.append(int(name))
    l1.append(True)
    l1.append((nx,ny))
    pos=nx,ny
    if pos!=ashtarg:
      #to_add the name on current position
      guiEventQueue.put(l1)
    #unlock the previos position 
    gridOfEnviornment[x][y].release()
    return True
  @staticmethod
  def executive(pos,event):
    global gridOfEnviornment
    while True:
      li=agent.sensor(pos)
      if len(li)==0:
        break
      x,y=pos
      for i,j,k in li:
        temp=True
        if not k:
            temp=gridOfEnviornment[i][j].acquire(False)
        if temp:
          name=threading.current_thread().name
          state=agent.actuator((x,y),(i,j),name)
          if state:
            pos=i,j
          event.wait(5)
          break
    return True
#updating GUI
def func(m,n,targ):
  tk=Tk()
  tk.geometry("1350x725")
  h=(float(1)/m)
  w=(float(1)/n)
  h=int(h)
  w=int(w)
  btn=[]
  for i in range(m):
      l=[]
      for j in range(n):
        pixel=PhotoImage(width=w,height=h)
        asp=Button(tk,text = '           '+os.linesep+'           ')
        #asp.configure(height = w,width = h)
        l.append(asp)
      btn.append(l) 
  for i in range(m):
      for j in range(n):
          btn[i][j].grid(row = i, column = j, sticky = W, pady = 2)
          #btn[i][j]['height']=h
          #btn[i][j]['width']=w
  x1,y1=targ
  btn[x1][y1].config(text='G')
  tk.update()
  while True:
    
    while not guiEventQueue.empty():
      l=guiEventQueue.get()
      x,y=l[2]
      ind=l[0]
      if l[1]:
        btn[x][y].config(text=str(ind)+os.linesep+'           ')
        tk.update()
      else:
        btn[x][y].config(text='           '+os.linesep+'   ')
        tk.update()
    if fl:
      break

    

      


      
class enviornment:

  def __init__(self, m,n,l):
    self.m=m
    self.n=n
    self.initia_pos=l
  @staticmethod
  def distance(pos):
    x,y=ashtarg
    x1,y1=pos
    return abs(x-x1)+abs(y-y1)

  
  def main(self):
    global fl
    global gridOfEnviornment
    m=self.m
    n=self.n
    #m=50
    #n=50
    targ=ashtarg
    self.target=targ
    gridOfEnviornment.clear()
    for _ in range(m):
      l=[]
      for _ in range(n):
        l.append(threading.Lock())
      gridOfEnviornment.append(l)
    thr=[]
    count=0
    gui=threading.Thread(target=func,name=str('gui'),args=(m,n,targ))
    gui.start()
    for x,y in self.initia_pos:
        count+=1
        event=threading.Event()
        temp=threading.Thread(target=agent.executive,name=str(count),args=((x,y),event))
        gridOfEnviornment[x][y].acquire()
        thr.append(temp)
    count1=0
    for i in thr:
      count1+=1
      i.start()
      if count1%4==0:
        now=time.time()
        future=now+0.9
        while time.time()<future:
            pass
     
    for i in thr:
      i.join()
    fl=True
    gui.join()

if __name__=="__main__":
  m=int(input("enter number of rows\n"))
  n=int(input("enter  number of column\n"))
  st=[]
  count=0
  x1=int(input("x coordinate of target\n"))
  y1=int(input("y coordinate of target\n"))
  ashtarg=(x1,y1)
  while count<10:
      x=random.randint(0, m)%m
      y=random.randint(0, n)%m
      if not (x,y) in st and (x,y)!=ashtarg:
        st.append((x,y))
        count+=1
  
  c=enviornment(m,n,st)
  c.main()
