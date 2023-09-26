import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri
import math

class FichierMaillage():
    def __init__(self,path_to_file):
        self.path = path_to_file
        


def lit_fichier_msh(fichier_msh, verbose=False) -> []:
    if(verbose):
        print("lecture du fichier :",fichier_msh)
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
       
    if(verbose): 
        print("nbn :",nbn,"\n","nbe :", nbe,"nba :","\n", nba,"coord :", coord,"\n","tri :", tri,"\n","ar :", ar,"\n","refn :", refn,"\n","reft :", reft,"\n","refa :", refa,"\n")
    
    return [nbn,nbe,nba,coord,tri,ar,refn,reft,refa]

def trace_maillage_ind(nbn,nbe,nba,coord,tri,ar, verbose=False):
    
    if(verbose):
        print("traçage du maillage\n")
    
    fig,ax = plt.subplots()
    ax.set_aspect('equal')
    ax.triplot(coord[:,0],coord[:,1],(tri[:])-1,'go-',lw=1.0)
    #pour le test
    #plt.show(block=False))
    return [fig,ax]

def trace_maillage_ref(nbn,nbe,nba,coord,tri,ar,refn,reft,refa, verbose=False):
    fig,ax = trace_maillage_ind(nbn,nbe,nba,coord,tri,ar)
    return [fig,ax]
    #changer les indices par les refs 
    
    #pour le test
    #plt.show(block=False)
    
def charge_et_affiche_maillage(FichierMaillage, verbose=False):
    #si ce n'est pas un FichierMaillage (donc surememnt un string) --> créer un fichiermaillage à partir de celui-là

    [nbn,nbe,nba,coord,tri,ar,refn,reft,refa] = lit_fichier_msh(FichierMaillage.path)
    fig,ax = trace_maillage_ref(nbn,nbe,nba,coord,tri,ar,refn,reft,refa)
    plt.show()
    
    if(verbose):
        print("lecture du fichier :",FichierMaillage.path)
        print("nbn :",nbn,"\n","nbe :", nbe,"nba :","\n", nba,"coord :", coord,"\n","tri :", tri,"\n","ar :", ar,"\n","refn :", refn,"\n","reft :", reft,"\n","refa :", refa,"\n")
     
    return [[nbn,nbe,nba,coord,tri,ar,refn,reft,refa],[fig,ax]]

def pas_et_qualite_maillage(tri,coord, verbose=False):
    #pour chaque triangle, calculer leur pas & leur qualité, on récupère le max de chaque   
    if(verbose):
        print("calcul du pas et de la qualité du maillage")
    pas_max = 0
    qualite_max = 0
    pas = 0
    qualite = 0
    current_triangle = [0,0,0]
    
    for triangle in tri:
        #for i in range(3):
        #    current_triangle[i] = coord[(triangle[i])]
        #print(coord[int(triangle[0])]) # TODO, c'est pas les bonnes coords, il faut avoir un input de ce format : [[i,j],[i,j],[i,j]]
        for i in range(3):
            current_triangle[i] = coord[int(triangle[i])-1]
            
        pas = pas_triangle(current_triangle)
        qualite = qualite_triangle(current_triangle)
        
        if(qualite > qualite_max):
            qualite_max = qualite
        if(pas > pas_max):
            pas_max = pas
    return [pas_max,qualite_max]

# en parametre les coordonnes des points du triangle dans la forme suivante : 
# [[i,j],[i,j],[i,j]]
def rayon_cercle_inscrit(triangle, verbose=False):
    longueurs_cotes = [0,0,0]
    
    # calculer la longueur de chaque cote 
    for i in range(3):
        longueurs_cotes[i] = math.dist(triangle[i%3],triangle[(i+1)%3])
    
    # calcul du demi-perimetre 
    demi_perimetre = (longueurs_cotes[0]+longueurs_cotes[1]+longueurs_cotes[2]) / 2
    # 2 * aire / perimetre 
    aire = math.sqrt(demi_perimetre * (demi_perimetre - longueurs_cotes[0]) * (demi_perimetre - longueurs_cotes[1]) * (demi_perimetre - longueurs_cotes[2]))
    return  (aire/demi_perimetre)

# en parametre les coordonnes des points du triangle dans la forme suivante : 
# [[i,j],[i,j],[i,j]]
def pas_triangle(triangle, verbose=False):
    longueur_max = 0
    longueur_cur = 0
    
    # calculer la longueur de chaque cote 
    for i in range(3):
        #print(triangle[i%3])
        
        longueur_cur = math.dist(triangle[i%3],triangle[(i+1)%3])
        if(longueur_cur > longueur_max):
            longueur_max = longueur_cur
    return longueur_max

# en parametre les coordonnes des points du triangle dans la forme suivante : 
# [[i,j],[i,j],[i,j]]
def qualite_triangle(triangle, verbose=False):
    return math.sqrt(3) / 6 * (pas_triangle(triangle) / rayon_cercle_inscrit(triangle))
if __name__ == '__main__':
    print("Demo:\n")
    #[nbn,nbe,nba,coord,tri,ar,refn,reft,refa] = lit_fichier_msh("D:\\Users\\omkil\\Documents\\CHPS0706\\TP\\Maillages\\m00.msh")
    #trace_maillage_ind(nbn,nbe,nba,coord,tri,ar)
    [[nbn,nbe,nba,coord,tri,ar,refn,reft,refa],[fig,ax]] = charge_et_affiche_maillage(FichierMaillage("./Maillages\\m1.msh"),verbose=True)
    pas,qualite = pas_et_qualite_maillage(tri,coord)
    print("pas du maillage : ", pas,"\nqualite du maillage: ", qualite)
    charge_et_affiche_maillage(FichierMaillage("rectangle_4x2_struct.msh"))