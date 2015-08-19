import pylab as p

#TROCAR X POR Y NA MATRIZ!

class FD_Solver:
    def __init__(self,M=50,N=50,iter_total=300,edge_type="edge_dirichlet_firstorder"):
        self.edge_type=edge_type
        self.x=M
        self.y=N
        self.x2=self.x/2
        self.y2=self.y/2
        self.edge_size=5
        if self.edge_type=="edge_dirichlet_firstorder":
            self.edge_size=1
        self.edge_fall=2./self.edge_size
        self.iter_total=iter_total
        self.matrix_0=p.zeros((N,M))
        self.matrix_1=p.zeros((N,M))
        self.matrix_2=p.zeros((N,M))
        if self.edge_type=="edge_dirichlet_fourthorder":
            self.matrix_n2=p.zeros((N,M))
            self.matrix_n1=p.zeros((N,M))
        self.vel=p.zeros((N,M))
        self.vel_set()
        self.wave_type="pulse"
        #Courant- Friedrichs-Lewy or CFL condition: dt<(dx/vel)
        freq=40e3
        self.dx=self.vel.max()/(freq*10.)
        self.dt=1/(freq*20.)
        print "dt:",self.dt,"s, dx:",self.dx, "m"
        self.vel1=(self.vel*self.dt/self.dx)
        self.vel2=self.vel1**2

    def vel_set(self):
        for i in range(self.x):
            for j in range(self.y):
                if i<self.x2:
                    self.vel[j][i]=1
                else:
                    self.vel[j][i]=1

    def wave_gen(self,ploti=1):
        if self.wave_type=="pulse":
            self.wave_origin=p.exp(-5e-2*(p.arange(self.iter_total)-20)**2)
        elif self.wave_type=="sine":
            self.wave_origin=(1-p.exp(-1e-7*(p.arange(self.iter_total))))*p.sin(2*p.pi*p.arange(self.iter_total)/(20))
        
        if ploti==1:
            p.figure(3)
            p.plot(self.wave_origin)

    def run(self,it):
        for i in range(self.edge_size,self.x-self.edge_size):
            for j in range(self.edge_size,self.y-self.edge_size):
                self.matrix_2[j][i]=-self.matrix_0[j][i]+2*self.matrix_1[j][i]+self.vel2[j][i]*(self.matrix_1[j+1][i]+self.matrix_1[j-1][i]+self.matrix_1[j][i+1]+self.matrix_1[j][i-1]-4*self.matrix_1[j][i])
        # border condition
        eval("self.%s(0)" % self.edge_type)

        if self.edge_type=="edge_dirichlet_fourthorder":
            self.matrix_n2=self.matrix_n1.copy()
            self.matrix_n1=self.matrix_0.copy()

        self.matrix_0=self.matrix_1.copy()
        self.matrix_1=self.matrix_2.copy()

    def edge_closed(self,it):
        # Zero field at border, total reflection
        pass
    def edge_endless(self,it):
        for i in range(self.x-self.edge_size,self.x):
            i_1=i+1
            if i_1==self.x:
                i_1=0
            for j in range(0,self.y):
                j_1=j+1
                if j_1==self.y:
                    j_1=0
                self.matrix_2[j][i]=-self.matrix_0[j][i]+2*self.matrix_1[j][i]+self.vel2[j][i]*(self.matrix_1[j_1][i]+self.matrix_1[j-1][i]+self.matrix_1[j][i_1]+self.matrix_1[j][i-1]-4*self.matrix_1[j][i])
        for i in range(0,self.x):
            i_1=i+1
            if i_1==self.x:
                i_1=0
            for j in range(self.y-self.edge_size,self.y):
                j_1=j+1
                if j_1==self.y:
                    j_1=0
                self.matrix_2[j][i]=-self.matrix_0[j][i]+2*self.matrix_1[j][i]+self.vel2[j][i]*(self.matrix_1[j_1][i]+self.matrix_1[j-1][i]+self.matrix_1[j][i_1]+self.matrix_1[j][i-1]-4*self.matrix_1[j][i])

    def edge_dirichlet_firstorder(self,it):
        #(x-y)/a-(v/b)*(z-y)=0, solve for x
        #chegano: x = (a v (z-y)+b y)/b and b!=0 and a!=0
        #saino: x = (a v (y-z)+b y)/b
        for j in range(0,self.y):
            self.matrix_2[j][0] = self.vel1[j][0]*(self.matrix_1[j][1]-self.matrix_1[j][0]) + self.matrix_1[j][0]
            self.matrix_2[j][-1] = self.vel1[j][-1]*(self.matrix_1[j][-2]-self.matrix_1[j][-1]) + self.matrix_1[j][-1]
        for i in range(0,self.x):
            self.matrix_2[0][i] = self.vel1[0][i]*(self.matrix_1[1][i]-self.matrix_1[0][i]) + self.matrix_1[0][i]
            self.matrix_2[-1][i] = self.vel1[-1][i]*(self.matrix_1[-2][i]-self.matrix_1[-1][i]) + self.matrix_1[-1][i]

        self.matrix_2[0][0] = self.vel1[0][0]*(self.matrix_1[1][1]-self.matrix_1[0][0]) + self.matrix_1[0][0]
        #self.matrix_2[-1][-1] = self.vel1[-1][-1]*(self.matrix_1[-2][-2]-self.matrix_1[-1][-1]) + self.matrix_1[-1][-1]
        #self.matrix_2[-1][0] = self.vel1[-1][0]*(self.matrix_1[-2][0]-self.matrix_1[-1][0]) + self.matrix_1[-1][0]
        #self.matrix_2[0][-1] = self.vel1[0][-1]*(self.matrix_1[0][-2]-self.matrix_1[0][-1]) + self.matrix_1[0][-1]

    def edge_dirichlet_fourthorder(self,it):
        # como descrito em 
        #DIVERGE PRA BURRO, provavelmente por causa de usar matrix_2!!!
        c=(1/self.dt**4)+(2*(self.vel)/((self.dt**3)*(self.dx)))+(6*(self.vel**2)/((self.dt**2)*(self.dx**2)))+(2*(self.vel**3)/((self.dx**3)*(self.dt)))
        for j in range(self.y):
            Y1=(-4*self.matrix_1[j][1]+6*self.matrix_0[j][1]-4*self.matrix_n1[j][1]+self.matrix_n2[j][1])/(self.dt**4)
            Y2=(self.matrix_2[j][3]-3*self.matrix_1[j][3]+3*self.matrix_0[j][3]-self.matrix_n1[j][3]+3*self.matrix_1[j][1]-3*self.matrix_0[j][1]+self.matrix_n1[j][1])/(2*self.dx*(self.dt**3))
            Y3=(self.matrix_2[j][3]-2*self.matrix_1[j][3]+self.matrix_0[j][3]-2*self.matrix_2[j][2]+4*self.matrix_1[j][2]-2*self.matrix_0[j][2]-2*self.matrix_1[j][1]+self.matrix_0[j][1])/((self.dx**2)*(self.dt**4))
            Y4=(self.matrix_2[j][4]-3*self.matrix_2[j][3]+3*self.matrix_2[j][2]-self.matrix_0[j][4]+3*self.matrix_0[j][3]-3*self.matrix_0[j][2]+self.matrix_0[j][1])/(2*self.dt*(self.dx**3))
            Y5=(self.matrix_1[j][5]-4*self.matrix_1[j][4]+6*self.matrix_1[j][3]-4*self.matrix_1[j][2]+self.matrix_1[j][1])/(self.dx**4)
            self.matrix_2[j][1]=(-Y1+4*self.vel[j][1]*Y2-6*(self.vel[j][1]**2)*Y3+4*(self.vel[j][1]**3)*Y4-(self.vel[j][1]**4)*Y5)/c[j][1]
    
    def run_to_the_hills(self,plot_wave=0):
        self.wave_gen(plot_wave)
        self.wave_probe=p.zeros(self.iter_total)
        for it in range(self.iter_total):
            if plot_wave>=1:
                print "iter:", it#, self.wave_probe[it-1]
            self.run(it)
            #self.matrix_1[self.y2*0.5][self.x2*0.5]=self.wave_origin[it]
            self.matrix_1[self.y2][self.x2*0.5]=self.wave_origin[it]
            self.wave_probe[it]=self.matrix_1[self.y2*0.8][self.x2*0.5]
            #self.wave_probe[it]=self.matrix_1[self.y-2][self.x-2]
            if it%10==0:
                self.plot(it)
                p.draw()
                #raw_input()
            #print self.matrix_1[10][50]
    def plot(self,it=0):
        p.figure(1)
        #5.437 s
        #p.contourf(self.matrix_1)
        #10.215 s
        #p.imshow(self.matrix_1)
        #7.069 s
        p.pcolormesh(self.matrix_1)
        #8.254 s
        #ax = p.subplot(1, 1, 1)
        #ax.pcolorfast(self.matrix_1)
        p.title("iter: %s" % it)
        #p.figure(2)
        #p.plot(self.matrix_1[self.y2])
        #p.plot(abs(self.wave_probe))
        #p.yscale("log")

if __name__ == '__main__':
    p.ion()
    solver=FD_Solver()
    solver.run_to_the_hills(0)
    solver.plot()
    print "total time (ms):", solver.iter_total*solver.dt*1e6
    #p.ioff()
    #p.figure()
    #p.plot(solver.fall)
    #p.show()
