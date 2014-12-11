"""
Created on Wed Dec 9 19:51:00 2014

@author: danie_000
"""

import pylab as p
import numpy as np
import scipy.ndimage.filters as ft
import matplotlib.pyplot as pp
import matplotlib.colors as cl
import matplotlib.animation as anim

# Dimensionality of the system
d = 2
# Array size
M = 400
# Run-time
t = 1000000
# How often to update the plot
every = 5
#position of wave source
source_x = 50
source_y = M/2.

#wall creation

fx=M 
fy=M
x1=100 #(comessar alterar valor)
x2=200 #(terminar alterar valor)
cut=0.99
r_max=2.5*(x2-x1)*0.01 #porcentagem
a=1
wall_v=2 
hole_v=3
#generating matrix with number 1, iterating (x1,x2) (definindo a parede), abaixo, definindo a semente de buracos
grad=p.ones((fx,fy))
for i in range(x1,x2):
    for j in range(fy):#iteragig in hight
        if p.rand()<cut:#numero de corte, os numeros randomicos de 0 ate 1... ou seja 99% por causa do cut
            grad[j][i]=wall_v
        else:#otherway is a hole
            grad[j][i]=hole_v

grid=np.copy(grad)#copiando a matrix, pq soh queremos os valores nao queremos trocar o nome

#print grid

for i in range(x1+int(r_max),x2-int(r_max)):#iterating on the wall
    for j in range(int(r_max),fy-int(r_max)):#iterating in the hight of the wall
        if grad[j][i]==hole_v:#testing o ponto que ta iterando, se eh buraco ou nao, tem que ser grad, pois se for o grid vai gerar semente onde ja tem buraco
        	rad=int(r_max*np.random.rand())#criar um raio nesse buraco, randomico o valor max eh r_max
	    	for ii in range((i-rad),(i+rad+1)):#criando um circulo em volta do fy, no i e no j, testar esse circulo
        	    for jj in range ((j-rad),(j+rad+1)):#64/65 iterar sobre os valores do quadrado em volta da semente original
                	if ((ii-i)*(ii-i)+(jj-j)*(jj-j))<(rad*rad):
                            grid[jj][ii]=hole_v

fig = pp.figure()#soh pra gravar e fazer o desenho da parede
ax = fig.gca()
ax.imshow(grid)
grid.tofile("wall.dat")
fig.savefig('wall.png')

#wave simulation

# Wave propagation speed
l = 0.08*grid#desse jeito converto o valores , wallv e holev, e serao vel relativos ao ar

# Set up a figure window with an array color plot 'im', using a logarithmic color scale
fig = pp.figure()#criando outra figura com escala logaritimica, msm se a amplitude onda for menor, ainda voce ve no graf
ax = fig.gca()
ax.set_xticks([])
ax.set_yticks([])
im = ax.imshow([[1]], norm=cl.LogNorm())

# Set up a 3xMxM array to hold the state of the system at the current, last and last-but-one timesteps // pq quando vc usa o fdtd vc vai ter o estado novo da celula da grade e voce precisa do estado anterior. pq a equacao de onda precisa de dois estados anteriores pq a onda eh derivada segunda.
a = np.ones([3] + d * [M])#fazendo uma matrix mxm. e por 3, uma matrix 3d na vdd.

for i in range(t):
    # Iterate the system according the finite-difference algorithm
    a[0] = 2.0 * a[1] - a[2] + l * ft.laplace(a[1])#pegando duas vezes o valor da onda anterior - a onda mais velha ( a[2])+  a transformada de laplace  pra derivar ou a taxa da onda que ta variando, vezes a velocidade que ela ta

    # wave source, the ideal was a gaussian wave but this is what i got.
    if i == 0:
        #a[0][tuple(np.random.randint(0, M, size=d))] += 1.0
        a[0][source_y][source_x] += 1.0#pegando o numero na posicao atual, pega na altura y, e distancia x,(as distancias da paredes) no ponto e somado +1.
        # Subtract a bit from all of the array to keep the overall sum constant
        a[0] -= 1.0 / a[0].size

    # Every 'every' iterations, update the plot and save an image
    if i % every == 0:
        im.set_data(a[0])
        fig.savefig('%08i.png' % i)
        print('%.2f%%' % (100.0 * float(i) / t))
        # Hack to make the colormap scaling work correctly
        if i == 0:
            im.autoscale()

    # Shift the last array into last-but-one, and current into last // fez a iteracao e troca as matrizes.
    a[2] = a[1]
    a[1] = a[0]
