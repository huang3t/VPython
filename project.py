#https://youtu.be/KRUxdIO6CG0
from vpython import*

m_He=6.67E-27                                                  # the mass of a Helium atom = 4.002(g)*10^(-3)(kg/g)/(6*10^23) = 6.67*10^(-27)kg
N = 50                                                         # 50 molecules
k= 1.38E-23                                                    # Boltzmann constant
temperature= [ 273, 323, 373]                        # 0, 50, 100 degree Celsius
length = [] 
size = 5E-10                                                   

scene = canvas(width = 400, height =400, align = 'left', background = vec(1, 1, 1)) 

ideal_gas  = graph(width = 600, align = 'left', xmin=0, ymin=0, xtitle='1/V', ytitle='P') 
P_V1 = gcurve(color=color.blue, graph=ideal_gas)
P_V2 = gcurve(color=color.green, graph=ideal_gas)
P_V3 = gcurve(color=color.red, graph=ideal_gas)


for i in range(100):                                            # 各體積邊長設定
    EachLength = (N*(i+1))**(1/3) * 1E-9
    length.append ( EachLength )


containers = []

for T in temperature:
    for L in length:
        containers.append(box(length = 2*L, height = 2*L, width = 2*L, opacity=0.4, color = color.yellow ))
        molecules=[]

        for i in range(N):
            theta = 2*pi*random() # the angle between velocity and x-y plane
            phi = 2*pi*random() # the angle between the projected velocity on the x-y plane and x-axis
            molecule = sphere(radius=size, color=vec(random(), random(), random() ) )
            molecule.pos = (L - size)* vec(2*random()-1, 2*random()-1, 2*random()-1)
            molecule.v = (3 * k * T / m_He)**0.5 * vec( cos(theta) *cos(phi), cos(theta) *sin(phi), sin(theta))
            molecules.append ( molecule )

        t=0
        dt = 5E-14
        times = 0                                               # 下面迴圈跑的次數
        J = 0                                                   # 衝量加總
        while True:
            rate(300000)
            for i in range(N):
                molecules[i].pos += molecules[i].v * dt
                        
            for i in range(N):
                if abs(molecules[i].pos.x) >= L - size and molecules[i].pos.x * molecules[i].v.x > 0:               # to check if any molecule collides any of the six walls
                    J += 2*m_He*abs(molecules[i].v.x)           # add the total impulse molecules do on walls in x direction
                    molecules[i].v.x *= -1

                if abs(molecules[i].pos.y) >= L - size and molecules[i].pos.y * molecules[i].v.y > 0:
                    J += 2*m_He*abs(molecules[i].v.y)           # add the total impulse molecules do on walls in y direction
                    molecules[i].v.y *= -1

                if abs(molecules[i].pos.z) >= L - size and molecules[i].pos.z * molecules[i].v.z > 0:
                    J += 2*m_He*abs(molecules[i].v.z)           # add the total impulse molecules do on walls in z direction
                    molecules[i].v.z *= -1
                
            t += dt
            times += 1
            
            if times >= 3000:
                P = J/(t*6*((2*L)**2))                          # P=F/A=(J/t)/A=J/(t*A), A=6*(2L^2)  # 乘了一個T，因為時間尺度的關係
                
                if T == 273:
                    P_V1.plot(pos = ((2*L)**(-3),P))
                    for i in range(N):
                        molecules[i].visible = False
                    containers[-1].visible = False
                    break
                if T == 323:
                    P_V2.plot(pos = ((2*L)**(-3),P))
                    for i in range(N):
                        molecules[i].visible = False
                    containers[-1].visible = False
                    break
                if T == 373:
                    P_V3.plot(pos = ((2*L)**(-3),P))
                    for i in range(N):
                        molecules[i].visible = False
                    containers[-1].visible = False
                    break
