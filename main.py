# -*- coding: utf-8 -*-
"""
Projet Algo 1
OOMS Aur��lien
BA1 INFO
"""

from os import system


class Patient:

    def __init__(self,ticket,name,language):
        self.__ticket = ticket                                  #ordre dans la file d'attente
        self.__name = name                                      #nom du patient
        self.__language = language                              #langue du patient

    def getTicket(self):                                        
        return self.__ticket

    def getName(self):
        return self.__name

    def getLanguage(self):
        return self.__language

    def setTicket(self,newTicket):
        self.__ticket = newTicket

    def setName(self,newName):
        self.__name = newName

    def setLanguage(self,newLanguage):
        self.__language = newLanguage


class Docteur:

    def __init__(self,ticket,name,language,disposable = True):
    
        self.__ticket = ticket                                  #ordre dans la file d'attente
        self.__name = name                                      #nom du patient
        self.__language = language                              #langue du patient
        self.__disposable = disposable
        
    def getTicket(self):                                        
        return self.__ticket

    def getName(self):
        return self.__name

    def getLanguage(self):
        return self.__language

    def getDisposable(self):
        return self.__disposable

    def setTicket(self,newTicket):
        self.__ticket = newTicket

    def setName(self,newName):
        self.__name = newName

    def setLanguage(self,newLanguage):
        self.__language = newLanguage

    def setDisposable(self,newDisposable):
        self.__disposable = newDisposable


class FileLangues:
    
    """
    File selon le principe FIFO
    Le patient "factice" sert �� r��cup��rer certaines erreurs lorsque la liste est vide, lors d'une insertion, on ins��re donc ��
    l'indice 1 et non 0. On utilise un dictionnaire pour limiter la recherche d'��l��ment lors d'un remove. L'attribut nbrPatients
    permet d'enregistrer la taille de la file et donc de ne pas compter les ��l��ments lors d'un appel �� size()
    NB: 'f' est > que n'importe quel entier et certains noms d'attributs font penser qu'il s'agit uniquement de la file d'attente
    alors que cette classe est ��galement utilis��e afin de donner un ordre aux diff��rents m��decins.
    """
    
    
    def __init__(self):
    
        self.__file = {}
        self.__indicesA = ['f']                        #indice des objets parlant la langue A
        self.__indicesB = ['f']                        #indice des objets parlant la langue B
        self.__indicesAB = ['f']                       #indice des objets parlant la langue AB
        self.__nbrPatients = 0                         #nombre d'objets dans la file


    def getFile(self):
        return self.__file
    
    
    def isEmpty(self):
        return self.__nbrPatients == 0
        
        
    def insert(self,patient):
        
        if patient.getLanguage() not in 'AB':

            raise   #n'arrive jamais lors de l'utilisation de l'interface, car on teste si la langue est correcte

        else:

            self.__nbrPatients += 1
            
            #ins��re dans la liste d'indice appropri��e et dans la file
            
            if patient.getLanguage() == 'A':
                self.__file[patient.getTicket()] = patient
                self.__indicesA.insert(1,patient.getTicket())   #insert est ici l'op��rateur sur les listes Python

            elif patient.getLanguage() == 'B':
                self.__file[patient.getTicket()] = patient
                self.__indicesB.insert(1,patient.getTicket())   #insert est ici l'op��rateur sur les listes Python
                
            elif patient.getLanguage() == 'AB':
                self.__file[patient.getTicket()] = patient
                self.__indicesAB.insert(1,patient.getTicket())  #insert est ici l'op��rateur sur les listes Python


    def size(self):
        return self.__nbrPatients


    def removeA(self):
        
        key = None

        try:
        
            #retourne 255 si seul l'��lement factice est pr��sent dans les sous-listes
            
            key2 = min(self.__indicesA[-1],self.__indicesAB[-1])
            
            #cherche le ticket minimum et pop en cons��quence   
            
            if type(key2) == int:
            
                if key2 == self.__indicesA[-1]:
                    self.__indicesA.pop()
                else:
                    self.__indicesAB.pop()
                
                key = key2
                self.__nbrPatients -= 1
            
            return self.__file.pop(key)

        except:
            
            return 255
            
        

    def removeB(self):
        key = None

        try:
        
            #retourne 255 si seul l'��lement factice est pr��sent dans les sous-listes
            
            key2 = min(self.__indicesB[-1],self.__indicesAB[-1])
            
            #cherche le ticket minimum et pop en cons��quence
            
            if type(key2) == int:
            
                if key2 == self.__indicesB[-1]:
                    self.__indicesB.pop()
                    
                else:
                    self.__indicesAB.pop()
                    
                key = key2
                self.__nbrPatients -= 1
            
            return self.__file.pop(key)

        except:
            
            return 255
        

    def remove(self):

        key = None

        try:
            #retourne 255 si seul l'��lement factice est pr��sent dans les sous-listes
            
            key2 = min(self.__indicesA[-1],self.__indicesB[-1],self.__indicesAB[-1])
            
            #cherche le ticket minimum et pop en cons��quence
            
            if type(key2) == int:
                
                if key2 == self.__indicesA[-1]:
                    self.__indicesA.pop()
                    
                elif key2 == self.__indicesB[-1]:
                    self.__indicesB.pop()
                    
                else:
                    self.__indicesAB.pop()
                    
                key = key2
                self.__nbrPatients -= 1
        
            return self.__file.pop(key)

        except:
            
            return 255
        


    def __repr__(self):


        out = ''
        keys = self.__file.keys()
        for key in keys:
            try:
                if self.__file[key].getDisposable(): #n'affiche pas les m��decins non disponibles
                    out += '#' + str(key) + ' ' + str(self.__file[key].getName()) + ' : ' + str(self.__file[key].getLanguage()) +'\n'
            except:
                out += '#' + str(key) + ' ' + str(self.__file[key].getName()) + ' : ' + str(self.__file[key].getLanguage()) +'\n'
        if out == '':
            out = 'Cette file est vide'
        return out

    
    
    
def display(filePatient,fileMedecin,cabinets):
    
    """
    Fonction qui affiche la file d'attente, les m��decins disponibles et les consultations en cours.
    """
    
    print "FILE D'ATTENTE :\n"
    print filePatient
    print
    print "MEDECINS DISPONIBLES :\n"
    print fileMedecin
    print
    print "CONSULTATIONS EN COURS :\n"
    if cabinets == []:
        print 'Il n\'y a aucune consulation en cours.'
    else:
        for consultation in cabinets:
            print '@ M��decin : ' + consultation[0].getName() + '  Patient : ' +  consultation[1].getName()
    print




def interface():

    done = False
    ticketPatient = 0       #ticket d��terminant l'ordre d'arriv��e
    ticketMedecin = 0       #Donne ��galement un ordre au m��decin pour que ceux-ci traitent un nombre ��gale de patients
    filePatient = FileLangues()
    fileMedecin = FileLangues()
    cabinets = []
    
    while not done:
        system('clear')
        CMD = '-1'
        while CMD not in '1234':
            display(filePatient,fileMedecin,cabinets)
            CMD = raw_input('1 -- > Rajouter un patient dans la file d\'attente\n\
2 -- > Indiquer qu\'un m��decin est arriv�� �� l\'h��pital\n\
3 -- > Indiquer qu\'un m��decin est disponible\n\
4 -- > Fermeture du programme\n\nCHOIX : ')
            system('clear')
        if CMD == '1':
            
            print 'Vous avez choisi de rajouter un patient �� la file d\'attente'
            ticketPatient += 1
            name = raw_input('Nom du patient : ')
            
            language = 'C'
            while language not in 'AB':
                system('clear')
                print 'Le nom du patient est : ' + name
                language = raw_input('Langue du patient (A, B ou AB) : ')

            filePatient.insert(Patient(ticketPatient,name,language))        

        elif CMD == '2':

            print 'Vous avez choisi d\'indiquer qu\'un m��decin venait d\'arriver �� l\'h��pital'
            ticketMedecin += 1
            name = raw_input('Nom du m��decin : ')
            language = 'C'
            while language not in 'AB':
                system('clear')
                print 'Le nom du m��decin est : ' + name
                language = raw_input('Langue du m��decin (A, B ou AB) : ')

            fileMedecin.insert(Docteur(ticketMedecin,name,language))              

        elif CMD == '3':

            name = raw_input('Nom du m��decin : ')
            system('clear')
            found = False
            
            for item in fileMedecin.getFile().items():
            
            
                if item[1].getName() == name:
                
                    if fileMedecin.getFile()[item[0]].getDisposable():
                        raw_input('Le m��decin '+ name +' est d��j�� disponible.')
                        found = True
                        
                    else:
                    
                        fileMedecin.getFile()[item[0]].setDisposable(True)
                        for tupIe in cabinets:
                        
                            if tupIe[0] == fileMedecin.getFile()[item[0]]:
                            
                                cabinets.remove(tupIe)
                                ticketMedecin += 1
                                fileMedecin.getFile()[item[0]].setTicket(ticketMedecin)                                
                                fileMedecin.getFile()[ticketMedecin] = fileMedecin.getFile().pop(item[0])
                                #update du ticket qui permet une bonne r��partition des patients entre les m��decins
                                
                        raw_input('Le m��decin '+ name+' est maintenant disponible.')
                        found = True

            if not found:
                raw_input('Il n\'existe aucun m��decin du nom de ' + name +'.')
            
        elif CMD == '4':
            done = True
        

        if CMD in '123':
        
            doctorAvailable = True
            
            if not fileMedecin.isEmpty():
            
            
                for index in fileMedecin.getFile().keys():
                    
                    if fileMedecin.getFile()[index].getDisposable():
                        
                        
                        if fileMedecin.getFile()[index].getLanguage() == 'A':
                        
                            patient = filePatient.removeA()
                                                       
                            if patient != 255:
                                
                                fileMedecin.getFile()[index].setDisposable(False)                                
                                cabinets.append((fileMedecin.getFile()[index],patient))                                                           
                            
                            
                        elif fileMedecin.getFile()[index].getLanguage() == 'B':
                        
                            patient = filePatient.removeB()
                            
                            if patient != 255:
                                
                                fileMedecin.getFile()[index].setDisposable(False)                                
                                cabinets.append((fileMedecin.getFile()[index],patient))
                                
                            
                        else:
                        
                            patient = filePatient.remove()
                            
                            if patient != 255:
                                
                                fileMedecin.getFile()[index].setDisposable(False)                                                             
                                cabinets.append((fileMedecin.getFile()[index],patient))
                                

interface()
