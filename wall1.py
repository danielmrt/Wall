# -*- coding: utf-8 -*-
"""
Created on Thu Sep 04 17:23:12 2014

@author: danie_000
"""

import pylab as p
fx=400 #(tamanho da matriz)
fy=400
x1=100 #(comessar alterar valor)
x2=200 #(terminar alterar valor)
grad=p.ones((fx,fy))
for i in range(x1,x2):
	for j in range(fy):
		grad[j][i]*=p.rand()
p.contour(grad)
p.show()

#Testar metodo de circulos - atribuir valor 1 de ar, 2 pra numeros <0.9 e 3 pra > 0.9
#Criar uma ooutra matriz pra encontrar o numeros >3 e criar o raio

#Criar uma matriz parar suavizar os numeros fazendo as medias
# E transformar uma faixa em ar.