#validation.py
import maillage 
import math
import scipy.linalg as sla



def u (x,n,y):
    return 1.0+math.sin(0.5*math.pi*x) + n * (x - 4.0) * math.cos (0.5 * math.pi * y)

def f():
    return

if __name__ == '__main__':
    path_maillage = "Maillage/m4.msh"

    [nbn,nbe,nba,coord,tri,ar,refn,reft,refa] = maillage.lit_fichier_msh(path_maillage)

    codeDir = 1
    uE = 1.0

    fespace Vh(Th,P1) #Espace EF-P1
    Vh uh, vh #inconnue & Fct test
    
    
    #uh,vh = sla.cho_solve(Th,Uh,Vh,CodeDir,uh=uE)
    
    #problem PBLAPLACE(uh, vh, solver=Cholesky) = 
    #    int2d(Th)(dx(Uh)*dx(Vh)+dy(Uh)*dy(Vh)) 
    #    - int2d(Th)(f*vh) 
    #    + on (CodeDir, uh=uE);//décla = FV
    #PBLAPLACE//Appel au solver EF => calcul de uh

    #Calcul d'Erreurs : 
    varf b(uh,vh) = int2d(Th)
                    (dx(uh)*dx(vh)
                    +dy(uh)*dy(vh)) #forme bilinéaire
    matrix K = b(Vh,Vh) #matrice de rigidité 
    Vh KEh, Eh = h-uh
    KEh[] = K * Eh[]
    real eh = sqrt(Eh[]'*KEh[]); // ' == transposé 
    cout << "eh = |u - uh|_H1 = " << eh << endl

    plot(Th,uh,cmm = "Solution EF-P1 uh");