#validation.py
from maillage import lit_fichier_msh
from sympy import solve
from math import pi,cos,sin
import numpy as np

#note : un "Tri" est un array 3*2 (x,y)(x,y)(x,y)

def area(base,hauteur):
    return base*hauteur 

#la solution exacte u(x, y) = 1 + sin((π/2)*x) + x(x − 4) cos((π/2)*y) (ici connue)
def fct_u(x,y):
    return  1 + sin((pi/2)*x) + x(x - 4) * cos((pi/2)*y)

#la température extérieure uE(x, y) = 1 ici (au bord de Dirichlet/Fourier-Robin)
def fct_uE():#x,y
    return  1

#la fonction source de chaleur f(x, y) = (π**2/4)*sin((π/2)*x) + (π**2/4)*x**2 - (π**2)*x - 2) cos(π/2)*y)
def fct_f(x,y):
    return (pi**2/4)*sin((pi/2)*x) + (pi**2/4)*x**2 - (pi**2)*x - 2 * cos((pi/2)*y)

#la fonction de conductivité κ(x, y) = 1 (ici)
def fct_kappa():#x,y
    return 1

#le facteur de transfert α(x, y) = 10**8 ici (au bord Fourier-Robin)
def fct_alpha():#x,y
    return 10**8

#mes(truc) = aire du triangle 
def coeffelem_P1_rigid(Tri):
    k = np.array(3,3)
    
    k[1,1] = ( (fct_kappa()) / 4 * area(Tri) ) * ((Tri[1][0]-Tri[2][0])**2 +  (Tri[1][1]-Tri[2][1])**2)  
    k[2,2] = ( (fct_kappa()) / 4 * area(Tri) ) * ((Tri[2][0]-Tri[0][0])**2 + (Tri[2][1]-Tri[0][1])**2)  
    k[3,3] = ( (fct_kappa()) / 4 * area(Tri) ) * ((Tri[0][0]-Tri[1][0])**2 + (Tri[0][1]-Tri[1][1])**2)  
    
    '''
    res[1,1] = ( (fct_kappa()) / 4 * area(Tri) ) * ((x2-x3)**2 + (y2-y3)**2)  
    res[2,2] = ( (fct_kappa()) / 4 * area(Tri) ) * ((x3-x1)**2 + (y3-y1)**2)  
    res[3,3] = ( (fct_kappa()) / 4 * area(Tri) ) * ((x1-x2)**2 + (y1-y2)**2)  
    '''
    
    k[1,2] = k[2,1] = ( (fct_kappa()) / 4 * area(Tri) ) * ()  #TODO PAGE 3/5
    k[1,3] = k[3,1] = ( (fct_kappa()) / 4 * area(Tri) ) * ()  
    k[2,3] = k[3,2] = ( (fct_kappa()) / 4 * area(Tri) ) * ()  
    
    return


def coeffelem_P1_source(Tri):
    matrix = np.array(((1),(1),(1)))
    return np.matmul(area(Tri)/3 * fct_f((Tri[0]+Tri[1]+Tri[2])/3),matrix)
0
def coeffelem_P1_transf(Tri):
    matrix = np.array((1),(1))
    return np.matmul(((area(Tri) / 2 ) * fct_alpha() * fct_uE() * ( (Tri[0] + Tri[1]) / 2 ) ), matrix)

def coeffelem_P1_poids(Tri):
    matrix = np.array((2,1),(1,2))
    return np.matmul(((area(Tri) / 6 ) * fct_alpha()), matrix)


#affectation de la matrice EF−P1 A et du second membre F
def assemblage_EF_P1(nbn,nbe,nba,coord,tri,ar,refn,reft,refa):
    #initialisations (matrice et vecteur nuls)
    A = np.zeros(shape=(nbn,nbn))
    F = np.zeros(shape=(1,nbn))
    
    kl = np.zeros(shape=(3,3))
    fl = np.zeros(shape=(3))
    
    pa = np.zeros(shape=(3,3))
    ea = np.zeros(shape=(3))
    
    
    
    for l in range(1,nbe):
        #Calcul des coefficients élémentaires 
        for i in range(3):
            for j in range(3):
                kl[i][j] = 
            fl[i] = 
        
        
        I1 = tri(l,0)
        I2 = tri(l,1)
        I3 = tri(l,2)
        
        
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
        
    K = A #conservation de la matrice de Rigidité 
    
    for a in GammaF
        #calcul des coefficients d'arêtes 
        for i in range(2):
            for j in range(2):           
                pa[i][j] =
            ea[i] =
            
        I1 = ar(a,1)
        I2 = ar(a,2)
        
        
        
        A[I1,I1] += pa[1][1]
        A[I1,I2] += pa[1][2]
        F[I1]    += ea[1]
        
        A[I2,I1] += pa[2][1]
        A[I2,I2] += pa[2][2]
        F[I2]    += ea[2]
        
    return A,F


if __name__ == '__main__':
    path_maillage = "Maillage/m00.msh"
    [nbn,nbe,nba,coord,tri,ar,refn,reft,refa] = lit_fichier_msh(path_maillage)
    assemblage_EF_P1(nbn,nbe,nba,coord,tri,ar,refn,reft,refa)