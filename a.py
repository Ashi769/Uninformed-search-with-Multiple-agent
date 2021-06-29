import threading
import numpy as np
import random
from tkinter import *
from queue import Queue
import time
import os
fl=False
ash=[]
for i in range(10):
  ash.append(Queue())
shubh=Queue()
mat=[]
def valid(target,pos):
  px,py=pos
  tx,ty=target
  ret=[]
  if tx>px:
    ret.append((px+1,py))
  if tx<px:
    ret.append((px-1,py))
  if ty>py:
    ret.append((px,py+1))
  if ty<py:
    ret.append((px,py-1))
  return ret


def agent(target,pos,event):
  global mat

  while(pos!=target):
    #print(threading.current_thread().name)
    li=valid(target,pos)
    x,y=pos
    for i,j in li:
      temp=True
      if (i,j)!=target:
          temp=mat[i][j].acquire(False)
      if temp:
        #print(threading.active_count())
        #print(threading.current_thread().name)
   
        st=threading.current_thread().name
        ind=int(st)
        l=[]
        l.append(int(st))
        l.append(False)
        l.append((x,y))
        #ash[ind].put(l)
        shubh.put(l)
        l1=[]
        l1.append(int(st))
        l1.append(True)
        l1.append((i,j))
        pos=i,j
        if pos!=target:
          #ash[ind].put(l1)
          shubh.put(l1)
        mat[x][y].release()
        now=time.time()
        future=now+2
        while time.time()<future:
          pass
        #event.wait(20)
        break
  x1,y1=target
  return True
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
   
    while not shubh.empty():
      l=shubh.get()
      x,y=l[2]
      ind=l[0]
      if l[1]:
        btn[x][y].config(text=str(ind)+os.linesep+'           ')
        tk.update()
      else:
        btn[x][y].config(text='           '+os.linesep+'   ')
        tk.update()

    #print(threading.active_count())
    '''
    for i in ash:
      if not i.empty():
        l=i.get()
        x,y=l[2]
        ind=l[0]
        if l[1]:
          btn[x][y].config(text=str(ind)+os.linesep+'           ')
          tk.update()
        else:
          btn[x][y].config(text='           '+os.linesep+'   ')
          tk.update()
    '''
    if fl:
      break

   

     


     

def main():
  global fl
  global mat
  m=int(input("enter number of rows\n"))
  n=int(input("enter  number of column\n"))
  #m=50
  #n=50
  rx=int(input("enter x of  target\n"))
  ry=int(input("enter y  of target\n"))
  targ=(rx,ry)
  mat.clear()
  for _ in range(m):
    l=[]
    for _ in range(n):
      l.append(threading.Lock())
    mat.append(l)
  thr=[]
  st=[]
  count=0
  gui=threading.Thread(target=func,name=str('gui'),args=(m,n,targ))
  gui.start()
  while count<1:
    x=int(input("enter x of  agent\n"))
    y=int(input("enter y  of agent\n"))
    if not (x,y) in st:
      event=threading.Event()
      temp=threading.Thread(target=agent,name=str(count),args=(targ,(x,y),event))
      mat[x][y].acquire()
      thr.append(temp)
      st.append((x,y))
      count+=1

  for i in thr:
    i.start()
    now=time.time()
    future=now+0.9
    while time.time()<future:
        pass
  for i in thr:
    i.join()
  fl=True
  gui.join()

if __name__=="__main__":
  main()
