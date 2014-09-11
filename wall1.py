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
grad=p.ones((fx,fy))
for i in range(x1,x2):
	for j in range(fy):
		grad[j][i]*=p.rand()
for i in range (400):
    a= random.randint(100,200)
    b= random.randint(0,400)
    r= random.randint(10,20)
    
##    circle1=plt.Circle((a,b),r,color='white')
##fig = plt.gcf()
##fig.gca().add_artist(circle1)
##fig.savefig('plotcircles.png')
p.contour(grad)
