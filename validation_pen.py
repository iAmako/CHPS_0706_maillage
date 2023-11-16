#validation.py
from maillage import Maillage, lit_fichier_msh,pas_et_qualite_maillage
from sympy import solve
from math import pi,cos,sin,dist,sqrt
import numpy as np

#note : un "Tri" est un array 3*2 (x,y)(x,y)(x,y)

def tri_coords_from_refs(tri_refs,coords):
    res = np.zeros((len(tri_refs),3,2))
    for i in range(len(tri_refs)):
        
        for j in range(0,3):
            #print(tri_refs[i][j])
            
            res[i][j][0] = coords[int(tri_refs[i][j])-1][0]
            res[i][j][1] = coords[int(tri_refs[i][j])-1][1]
    return res

def area(Tri): 
    a = dist(Tri[1], Tri[0])
    b = dist(Tri[2], Tri[1])
    c = dist(Tri[0], Tri[2])
    s = (a+b+c) / 2
    return sqrt(s * (s - a) * (s - b) * (s - c))

#la solution exacte u(x, y) = 1 + sin((π/2)*x) + x(x − 4) cos((π/2)*y) (ici connue)
def fct_u(x,y):
    return  1 + sin((pi/2)*x) + x*(x - 4) * cos((pi/2)*y)

#la température extérieure uE(x, y) = 1 ici (au bord de Dirichlet/Fourier-Robin)
def fct_uE():#x,y
    return  1

#la fonction source de chaleur f(x, y) = (π**2/4)*sin((π/2)*x) + (π**2/4)*x**2 - (π**2)*x - 2) cos(π/2)*y)
def fct_f(x,y):
    return ((pi**2)/4) * sin((pi/2) * x) + (((pi**2/4)*(x**2) - (pi**2)*x) - 2) * cos((pi/2)*y)

#la fonction de conductivité κ(x, y) = 1 (ici)
def fct_kappa():#x,y
    return 1

#le facteur de transfert α(x, y) = 10**8 ici (au bord Fourier-Robin)
def fct_alpha():#x,y
    return 10**8

#mes(truc) = aire du triangle 
def coeffelem_P1_rigid(Tri):
    k = np.array([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
    c = (fct_kappa()) / (4 * area(Tri))
    k[0,0] = c * ((Tri[1][0]-Tri[2][0])**2 +  (Tri[1][1]-Tri[2][1])**2)  
    k[1,1] = c * ((Tri[2][0]-Tri[0][0])**2 + (Tri[2][1]-Tri[0][1])**2)  
    k[2,2] = c * ((Tri[0][0]-Tri[1][0])**2 + (Tri[0][1]-Tri[1][1])**2)  

    k[0,1] = k[1,0] = c * ( - (Tri[0][0]-Tri[2][0]) * (Tri[1][0]-Tri[2][0]) - (Tri[0][1] - Tri[2][1]) * (Tri[1][1] - Tri[2][1])) 
    k[0,2] = k[2,0] = c * ( - (Tri[2][0]-Tri[1][0]) * (Tri[0][0]-Tri[1][0]) - (Tri[2][1] - Tri[1][1]) * (Tri[0][1] - Tri[1][1])) 
    k[1,2] = k[2,1] = c * ( - (Tri[1][0]-Tri[0][0]) * (Tri[2][0]-Tri[0][0]) - (Tri[1][1] - Tri[0][1]) * (Tri[2][1] - Tri[0][1])) 
    
    return k


def coeffelem_P1_source(Tri):
    matrix = np.ones(3,float)
    x,y = (Tri[0][0] + Tri[1][0] + Tri[2][0])/3,(Tri[0][1] + Tri[1][1] + Tri[2][1])/3
    return (area(Tri)/3)*fct_f(x,y)*matrix
0
def coeffelem_P1_transf(a,b):
    matrix = np.ones(2,float)
    mid_ab = dist(a, b) / 2
    return mid_ab  * fct_alpha() * fct_uE()  * matrix#pansement 

def coeffelem_P1_poids(a,b):
    matrix = np.array([[2.,1.],[1.,2.]])
    return ((dist(a,b) / 6 ) * fct_alpha()) * matrix


#affectation de la matrice EF−P1 A et du second membre F
def assemblage_EF_P1(nbn,nbe,nba,coord,tri,ar,refn,reft,refa,trirefs):
    #initialisations (matrice et vecteur nuls)
    A = np.zeros(shape=(nbn,nbn))
    F = np.zeros(shape=(nbn))
    
    kl = np.zeros(shape=(3,3))
    fl = np.zeros(shape=(3))
    
    pa = np.zeros(shape=(3,3))
    ea = np.zeros(shape=(3))
    
    
    for l in range(0,nbe):
        
        #Calcul des coefficients élémentaires 
        kl = coeffelem_P1_rigid(trirefs[l])
        fl = coeffelem_P1_source(trirefs[l])
        
        
        I1 = int(tri[l][0])-1
        I2 = int(tri[l][1])-1
        I3 = int(tri[l][2])-1
        
        
        A[I1,I1] += kl[0][0]
        A[I1,I2] += kl[0][1] 
        A[I1,I3] += kl[0][2]
        F[I1] += fl[0]
        
        A[I2,I1] += kl[1][0]
        A[I2,I2] += kl[1][1] 
        A[I2,I3] += kl[1][2]
        F[I2] += fl[1]
        
        A[I3,I1] += kl[2][0]
        A[I3,I2] += kl[2][1] 
        A[I3,I3] += kl[2][2]
        F[I3] += fl[2]
        
    K = np.copy(A) #conservation de la matrice de Rigidité 
    
    for a in range(0,2):
        #calcul des coefficients d'arêtes 

            
        I1 = int(ar[a][0]-1)
        I2 = int(ar[a][1]-1)
        
        pa = coeffelem_P1_poids(coord[I1], coord[I2])
        ea = coeffelem_P1_transf(coord[I1], coord[I2])
        
        A[I1,I1] += pa[0][0]
        A[I1,I2] += pa[0][1]
        F[I1]    += ea[0]
        
        A[I2,I1] += pa[1][0]
        A[I2,I2] += pa[1][1]
        F[I2]    += ea[1]
        
        print("Arete n°",a,"A = ",A,"F = ",F)
        
    return A,F,K


def validation(path):
    print("================= validation_pas_a_pas =================")
    print(" * Resultats de calculs elementaires ...")
    print(" * element triangle: xl = [0,1,0] (abscisses), yl = [0,0,1] (ordonnees)")
    kl = coeffelem_P1_rigid([[0,0],[1,0],[0,1]])
    print("kl = ")
    print(kl)
    #ml = coeffelem_P1_masse([[0,0],[1,0],[0,1]])
    #print("ml = ")
    #print(ml)
    fl = coeffelem_P1_source([[0,0],[1,0],[0,1]])
    print("fl = ")
    print(fl)

    print(" * element arete: xa = [0,0] (abscisses), ya = [0,1] (ordonnees)")
    pa = coeffelem_P1_poids([0,0], [0,1])
    print("pa = ")
    print(pa)
    ea = coeffelem_P1_transf([0,0], [0,1])
    print("ea =")
    print(ea)
    maillage = Maillage(path)
    print("================= validation_pas_a_pas =================")
    print(" * Resultats sur le mini_maillage "+path+" ...")
    print("nbn = " + str(maillage.nbn))
    print("nbe = " + str(maillage.nbe))
    print("nba = " + str(maillage.nba))

    #ça fonctionne jusque là :p
    A,F,K = assemblage_EF_P1(maillage.nbn,maillage.nbe,maillage.nba,maillage.coord,maillage.tri,maillage.ar,maillage.refn,maillage.reft,maillage.refa,tri_coords_from_refs(maillage.tri,maillage.coord))
    print("A = ",A)
    #affichage de A
    print("F = ",F)
    #affichage de F
    Uh = np.linalg.solve(A,F)
    
    print("Uh = ",Uh)
    #affichage de Uh
    
    h,Q = pas_et_qualite_maillage(maillage.tri,maillage.coord,False)

    print(" ___---===***   RESULTATS:   ***===---___")
    print(" ________________________________________")
    print(" {            min(Uh) : ",Uh.min())#minUh
    print(" {            max(Uh) : ",Uh.max())#maxUh
    print(" {           mean(Uh) : ",Uh.mean())#moyenneUh
    print(" {            h       : ",h)#h, le pas
    print(" {            Q       : ",Q)#Q, la qualité 
    
    U = np.array([0. for x in range(len(maillage.coord))])
    for i in range(len(maillage.coord)):
        U[i] = fct_u(maillage.coord[i][0], maillage.coord[i][1])
    
    print(" {erreur |uh-rh(u)|_H1: ",sqrt(np.matmul(np.matmul(np.transpose(U-Uh),K),(U-Uh))))#1ère erreur
    print(" {erreur |Uh-U|_inf   : ",max(Uh-U))#2ème erreur
    print(" ________________________________________")
    
    print("================= validation_pas_a_pas =================")


if __name__ == '__main__':
    validation("./Maillages/m00.msh")
