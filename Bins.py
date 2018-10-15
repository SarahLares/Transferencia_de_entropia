
import numpy as np
import math
#Numero de particiones

M=4

#Valores de r y a

r=3.99
a1=0.5
N=2500


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
t=np.zeros((N+1,))
t[0]=j
#Parametros de acople (utilizaremos los mismos para ambos acoples)
m=0.00
e=0.6

#n es el numero de particiones que se desean hacer y x es una lista   

def particion(x,n):
    b=[]
    for i in x:
        contador=0
        for j in range(n):
            a=0
            if contador*(1/n)< i <=(contador+1)*(1/n):
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

def num(x,n):
    num=[]
    for i in range(0,len(x)-int(len(x)/n),n):
        nu=0
        p=[]
        if i<len(x)-n:
            for j in range(n):
                p.append(x[i+j])

            for j in range(len(p)):
                nu=p[j]*2**((n-1)-j)+nu
        num.append(nu)   
    return np.array(num)



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

#Funcion para calcula las probabilidades conjuntas de x_n+1,x_n y y_n
#n es el numero de particiones 

def Conj1(X,Y,n):
    X_P=np.zeros((n,n,n))
    for k in range(n):
        for i in range(n):
            for j in range(n):
                contador=0
                for l in range(len(X)):
                    if l+1<len(X):
                        t=X[l+1]
                        u=X[l]
                        v=Y[l]
                        if t==k and u==i and v==j:
                            contador+=1
                X_P[k,i,j]=contador
    return X_P/(len(X)-1)

#Ahora calculamos las probabilidades conjuntas en x_n y x_n+1
#n es el numero de particiones 
def ConjX(X,n):
    XY_p=np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            contador=0
            for k in range(len(X)):
                if k+1<len(X):
                    t=X[k+1]
                    u=X[k]
                    if t==i and u==j:
                        contador+=1
            XY_p[i,j]=contador
    return XY_p/(len(X)-1)

def Inf(X,Y,n):
    a=Conj1(X,Y,n)
    b=Mar(X,n)
    c=Conj(X,Y,n)
    d=ConjX(X,n)
    e=Mar(Y,n)
    f=Conj1(Y,X,n)
    g=ConjX(Y,n)
    
    T=0
    for i in range(len(a)):
        for j in range(n):
            for k in range(n):
                t=a[i,j,k]*b[j]
                u=c[j,k]*d[i,j]
                if t>0 and u>0:
                    T=a[i,j,k]*math.log2(t/u)+T
    U=0
    for i in range(len(a)):
        for j in range(n):
            for k in range(n):
                v=f[i,j,k]*e[j]
                w=c[j,k]*g[i,j]
                if v>0 and w>0:
                    U=f[i,j,k]*math.log2(v/w)+U

    return T,U

for k in range(N):
    #acople 1
    u=x[k]+m*(y[k]-x[k])
    v=y[k]+e*(x[k]-y[k])
    x[k+1]=f(u,r)
    y[k+1]=g(v,a1)
    #acople 2
    w=f(s[k],r)*(1-m)+m*f(t[k],r)
    z=g(t[k],a1)*(1-e)+e*g(s[k],a1)
    s[k+1]=w
    t[k+1]=z

#Acople 1
X=particion(x,2)
Y=particion(y,2)
#Acople 2
S=particion(s,2)
T=particion(t,2)

#Vamos a guardar todos los datos en archivos de la siguiente manera:   Z    informacion mutua    tras entr x-->y   tras entr y-->x
file3=open('datos3.txt','w') #Archivo para el acople 1 
file4=open('datos4.txt','w') #Archivo para el acople 2

for l in range(2,M):
    A=0
    B=0
    k=2**l
    print(l,k)
    X_1=num(X,l)
    Y_1=num(Y,l)
    S_1=num(S,l)
    T_1=num(T,l)
    L=str(l)
    #acople 1
    A=Inf(X_1,Y_1,k)
    TranfEnt_XY=str(A[0])
    TranfEnt_YX=str(A[1])
    file3.write('     '+L+'          '+TranfEnt_XY+'     '+TranfEnt_YX+'\n')

    
    #acople 2
    B=Inf(S_1,T_1,k)
    TranfEnt_ST=str(B[0])
    TranfEnt_TS=str(B[1])
    file4.write('     '+L+'           '+TranfEnt_ST+'     '+TranfEnt_TS+'\n')
file3.close()
file4.close()
