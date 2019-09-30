import matplotlib.pyplot as plt
import random as rd
import math as mh
global lcrom
global tam_pob
global x1
global x2
global prob_c
global prob_m
global max_iter
lcrom =32
tam_pob = 10
x1 = 0
x2 = 2*mh.pi
prob_c = 0.4
prob_m = 0.1
max_iter = 100

#--------------------------------------------------------------
"funcion a minimizar"
def Fun(x):
    y = mh.sin(x)
    #y = (mh.pow(x,2)*abs(mh.sin(0.1*x)))*mh.exp(-0.03*x)
    return y
#--------------------------------------------------------------

"Estructura de datos"
class IND:
    def __init__(self):
        self.gen = [0]*lcrom
        self.fen = 0
        self.adt = 0
        self.score = 0
        self.sum_score = 0

"Función Generar individuo"
def Gind():
    ind = IND()
    #Definición del genotipo
    for i in range(lcrom):
        ind.gen[i] = rd.randint(0,1)
    #Fenotipo
    fen(ind)
    return(ind)

"función que traduce el genotipo a fenotipo"
def fen(ind):
    b = str(ind.gen)
    b = b.replace("[","")
    b = b.replace("]","")
    b = b.replace(",","")
    b = b.replace(" ","")
    ind.fen = x1 + (x2-x1)/(mh.pow(2,lcrom)-1)*int(b,2)

#--------------------------------------------------------------
"Función que mide la adaptación "
def adt(ind):
    ind.adt = Fun(ind.fen)
#--------------------------------------------------------------

"Función generadora de población"
def Gpob():
    pob = []
    for i in range(tam_pob):
        pob.append(Gind())
    return pob

"Evaluación de la población"
def Eval(pob):
    sum_adt = 0
    sum_score = 0
    for i in range(tam_pob):
        adt(pob[i])
        sum_adt = sum_adt+pob[i].adt
    for i in range(tam_pob):
        pob[i].score = pob[i].adt/sum_adt
        sum_score = sum_score+pob[i].score
        pob[i].sum_score = sum_score

"Función selección, Metodo de la ruleta"
def select(pob):
    l_s = []
    for i in range(tam_pob):
        p = rd.random()
        for j in range(tam_pob):
            if(pob[j].sum_score>p):
                #Creando lista con clones 
                ind = IND()
                ind.gen = pob[j].gen
                ind.fen = pob[j].fen
                ind.adt = pob[j].adt
                l_s.append(ind)
                break
    return l_s
        
"función Cruce por parejas"
def cruce(P1,P2,p):
    H1 = IND()
    H2 = IND()
    H1.gen = P1.gen[:p]+P2.gen[p:]
    H2.gen = P2.gen[:p]+P1.gen[p:]
    fen(H1)
    fen(H2)
    return(H1,H2)
    
"Función para cruzar la población"
def cruce_pob(pob):
    #Seleccionados para cruce
    l_c = []
    for i in range(tam_pob):
        p = rd.random()
        if (p<prob_c):
            l_c.append(pob[i])

    if (len(l_c)%2!=0):
        l_c.remove(l_c[-1])
    
    #Cruzando los seleccionados
    punto_cruce = rd.randint(1,lcrom-1) 
    for i in range(0,len(l_c),2):
        H1,H2 = cruce(pob[i],pob[i+1],punto_cruce)
        pob[i] = H1
        pob[i+1] = H2
    
"Función para mutar individuo"
def Mutacion_ind(ind):
    for i in range(lcrom):
        p = rd.random()
        if(p<prob_m):
            ind.gen[i] = int(ind.gen[i]!=1)
    fen(ind)

"Función que muta la población"
def Mutacion_pob(pob):
    for i in range(tam_pob):
        Mutacion_ind(pob[i])

"función que busca el mas adaptado en una generación"
def mejor_adt(pob):
    adt_mejor = 0
    pos_mejor = 0
    for i in range(tam_pob):
        if(pob[i].adt>adt_mejor):
            adt_mejor = pob[i].adt
            pos_mejor = i
    ind = IND()
    ind.gen = pob[pos_mejor].gen
    ind.fen = pob[pos_mejor].fen
    ind.adt = pob[pos_mejor].adt
    return(ind)
  
"Función Evolucion"
def Evolucion():
    L_mgen =[]
    pob = Gpob()
    Eval(pob)
    Elite = mejor_adt(pob)
    print(Elite.adt)

    for i in range(max_iter):
        pob = select(pob)
        cruce_pob(pob)
        Mutacion_pob(pob)
        Eval(pob)
        Elite_gen = mejor_adt(pob)
        
        print(Elite_gen.adt)
        if(Elite_gen.adt>Elite.adt):

            L_mgen.append(Elite_gen.adt)
            
            Elite = Elite_gen
            print("El mejor = ",Elite.adt)
    plt.plot(range(len(L_mgen)),L_mgen)
    plt.show()
    return(Elite)

"funcion que imprime adaptacion de poblacion"
def disp_adt(pob):
    print("######")
    for i in range(tam_pob):
        print(pob[i].adt)
def disp_fen(pob):
    for i in range(tam_pob):
        print(pob[i].fen)

"Prueba del Algoritmo"

Elite = Evolucion()
y = []
x = list(range(500))
for i in x:
    y.append(Fun(i))
plt.plot(x,y)
plt.show()



