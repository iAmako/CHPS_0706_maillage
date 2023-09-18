import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri
import math

class FichierMaillage():
    def __init__(self,path_to_file):
        self.path = path_to_file
        


def lit_fichier_msh(fichier_msh) -> []:
    #plt.text()
    #plt.triplot()
    file = open(fichier_msh, 'r')

    #lecture du format
    [nbn,nbe,nba] = [int(i) for i in (file.readline().split())]
    
    coord = np.zeros((nbn,2))
    refn = np.zeros(nbn)
    tri = np.zeros((nbe,3))
    reft = np.zeros(nbe)
    ar = np.zeros((nba,2))
    refa = np.zeros(nba)
    
    
    
    for i in range(nbn):
        [coord[i,0],coord[i,1],refn[i]] = (file.readline().split())
    
    for i in range(nbe):
       [tri[i,0],tri[i,1],tri[i,2],reft[i]] = file.readline().split()
    
    for i in range(nba):
       [ar[i,0],ar[i,1],refa[i]] = file.readline().split()
       
    print("nbn :",nbn,"\n","nbe :", nbe,"nba :","\n", nba,"coord :", coord,"\n","tri :", tri,"\n","ar :", ar,"\n","refn :", refn,"\n","reft :", reft,"\n","refa :", refa,"\n")
    
    return [nbn,nbe,nba,coord,tri,ar,refn,reft,refa]

def trace_maillage_ind(nbn,nbe,nba,coord,tri,ar):
    fig,ax = plt.subplots()
    ax.set_aspect('equal')
    ax.triplot(coord[:,0],coord[:,1],(tri[:])-1,'go-',lw=1.0)
    return [fig,ax]
    #pour le test
    #plt.show()
    
def trace_maillage_ref(nbn,nbe,nba,coord,tri,ar,refn,reft,refa):
    fig,ax = trace_maillage_ind(nbn,nbe,nba,coord,tri,ar)
    return [fig,ax]
    #changer les indices par les refs 
    
    #pour le test
    #plt.show()
    
def charge_et_affiche_maillage(FichierMaillage):
    #si ce n'est pas un FichierMaillage (donc surememnt un string) --> créer un fichiermaillage à partir de celui-là
    
    [nbn,nbe,nba,coord,tri,ar,refn,reft,refa] = lit_fichier_msh(FichierMaillage.path)
    fig,ax = trace_maillage_ref(nbn,nbe,nba,coord,tri,ar,refn,reft,refa)
    plt.show()
    
def pas_et_qualite_maillage():
    #pour chaque triangle, calculer leur pas & leur qualité, on récupère le max de chaque   
    pas = max
    qualite = max
    return pas,qualite

def rayon_cercle_inscrit(triangle):
    return
def pas_triangle(triangle):
    return 
def qualite_triangle(triangle):
    return math.sqrt(3) / 6 * (pas_triangle(triangle) / rayon_cercle_inscrit(triangle))
if __name__ == '__main__':
    print("test:\n")
    #[nbn,nbe,nba,coord,tri,ar,refn,reft,refa] = lit_fichier_msh("D:\\Users\\omkil\\Documents\\CHPS0706\\TP\\Maillages\\m00.msh")
    #trace_maillage_ind(nbn,nbe,nba,coord,tri,ar)
    charge_et_affiche_maillage(FichierMaillage("D:\\Users\\omkil\\Documents\\CHPS0706\\TP\\Maillages\\m00.msh"))