import numpy as np
import math
#Numero de particiones

M=15

#Valores de r y a

r=3.99
a1=0.5
N=4500

#valores de las condiciones iniciales

i=np.random.random_sample()
j=np.random.random_sample()

#Acople 1

x=np.zeros((N+1,))
x[0]=i
y=np.zeros((N+1,))
y[0]=j
#Acople 2

s=np.zeros((N+1,))
s[0]=i
print(i)
t=np.zeros((N+1,))
t[0]=j
#Parametros de acople (utilizaremos los mismos para ambos acoples)
m=0.4
e=0.2

#n es el numero de particiones que se desean hacer y x es una lista   

def particion(x,n):
    b=[]
    for i in range(500,len(x)):
        contador=0
        for j in range(n):
            a=0
            if contador*(1/n)<x[i]<=(contador+1)*(1/n):
                a=contador
                b.append(a)
            contador+=1
    return np.array(b)

#Mapa logístico con parametro r

def f(x, r):
    return r*x*(1-x)

#Mapa triangular con parametro a

def g(x,a):
    if 0<=x and x<=a:
        return (x/a)
    elif a<x and x<=1:
        return ((1-x)/(1-a))


#Funcion para calcular las probabilidades marginales se ingresa el arreglo
# y  n es el numero de particiones devolvera un arreglo con las probabilidades marginales
#para n particiones
def Mar(X,n):
    X_p=np.zeros((n,))
    for i in range(n):
        a=0
        X_p[i]=np.count_nonzero(X == i)
        
    return X_p/len(x)


def Conj(X,Y,n):
    XY_p=np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            contador=0
            for k in range(len(X)):
                u=X[k]
                v=Y[k]
                if u==i and v==j:
                    contador +=1
            XY_p[i,j]=contador
    return XY_p/len(X)

def Inf(X,Y,n):
    b=Mar(X,n)
    c=Conj(X,Y,n)
    e=Mar(Y,n)
    
    H1=0
    for i in range(len(c)):
       for j in range(len(b)):
           p=c[i,j]
           q=b[i]*e[j]
           if p>0:
               H1=p*math.log2(p/q)+H1
   
    return H1


for k in range(N):
    #acople 1
    """u=x[k]+m*(y[k]-x[k])
    v=y[k]+e*(x[k]-y[k])
    x[k+1]=f(u,r)
    y[k+1]=g(v,a1)"""
    #acople 2
    w=f(s[k],r)*(1-m)+m*f(t[k],r)
    z=g(t[k],a1)*(1-e)+e*g(s[k],a1)
    s[k+1]=w
    t[k+1]=z
#Vamos a guardar todos los datos en archivos de la siguiente manera: Z    informacion mutua  ac1    informacion mutua  ac2

file2=open('Inf_MutA.txt','w') 
file2.write('particiones  '+'       Informacion Mutua Ac1'+'       Informacion Mutua Ac2'+'\n')

for l in range(2,M):
    k=2**l
    print(l,k)
    X=particion(x,k)
    Y=particion(y,k)
    S=particion(s,k)
    T=particion(t,k)
    K=str(k)
    #acople 1
    A=Inf(X,Y,k)
    K=str(k)
    InfMut_XY=str(A)
    #acople 2
    B=Inf(S,T,k)
    InfMut_ST=str(B)
    file2.write('     '+K+'          '+InfMut_XY+'          '+InfMut_ST+'\n')
file2.close()
