# -*- coding: utf-8 -*-
"""
Created on Thu Sep 04 17:23:12 2014

@author: danie_000
"""
#Primeiro passo, transfomar tudo em verde
#Criar bolas como a expressao = X**2 + Y**2 = R**2 // sendo R um numero de principio fixo, mas depois colocar um numero randomico limitado.
#Colocar as bolas em cores diferentes
import pylab as p
import math as mt
import random
import matplotlib.pyplot as plt

fx=400 #(tamanho da matriz)
fy=400
x1=100 #(comessar alterar valor)
x2=200 #(terminar alterar valor)
cut=0.99
r_max=50*(x2-x1)*0.01
a=1
grad=p.ones((fx,fy))
for i in range(x1,x2):
	for j in range(fy):
	    if p.rand()<cut:
                   grad[j][i]=2
        else:
                   grad[j][i]=3
grid=grad.copy()

for i in range(x1,x2):
    for j in range(fy):
        if grad[j][i]==3:
            rad=int(r_max*p.rand())
            for ii in range(i-rad,i+rad+1):
                for jj in range (j-rad,j+rad+1):
                    if (ii*ii+jj*jj)<(rad*rad):
                        grid[j][i]=3

p.contour(grid)

