#!/usr/bin/python3 
# -*- coding: utf-8 -*-
##################################################
## Class boampGetter  
##################z###############################
## License : MIT 
##################################################
## Author: #JMousqueton (Julien Mousqueton)
## Copyright: Copyright 2022
## Version: 3.5
## Maintainer: #JMousqueton (Julien Mousqueton)
## Email: julien_at_mousqueton.io 
##################################################
# Generic/Built-in 
import requests
import json
from datetime import datetime
from datetime import timedelta
import time
import os

# External/Other
import pymsteams

class boampGetter:
    def __init__(self):
        self.__searchResponse = {}
        self.__dicAd = {}
        self.printAll = 0
        self.DLRed = 10
        self.DLYellow = 20 
        self.NewFor = 5
        self.ShowKeyword = False
        self.cptKeyword = 0 
        self.Teams = False

    def __searchSize(self):
        """Return the number of ad send by Boamp.
        """
        if 'nbItemsRetournes' in self.__searchResponse:
            return self.__searchResponse['nbItemsRetournes']
        else:
            return 0
            
    def search(self,dateparution,strSearch):
        """Make a search request to Boamp.
            Store result in searchResponse.
        """
        print('Boamp search: \'{}\' after \'{}\''.format(strSearch,dateparution))
        lineOut = 'http://api.dila.fr/opendata/api-boamp/annonces/search?criterion=dateparution>{} ET {}'.format(dateparution,strSearch)
        self.__searchResponse = requests.get(lineOut).json()
        print('{} Responses found'.format(self.__searchSize()))
        for i in self
            print(i)

    def saveJsonFile(self, idweb):
        """Get ad represented by idweb(str) and save it in json file
        """
        strFile = '{}.json'.format(idweb)
        with open(strFile, 'w') as outfile:
            json.dump(requests.get('http://api.dila.fr/opendata/api-boamp/annonces/v230/' + idweb).json(), outfile)

    def extractValidAd(self):
        """Return array of json ad wich describe the ad if date recept offer if higher that today.
        """
        arrayReturn = []
        nbItem = self.__searchSize()
        i = 0
        while i < nbItem :
            date =0
            offre = self.__searchResponse['item'][i]
            annonce = requests.get('http://api.dila.fr/opendata/api-boamp/annonces/v230/' + offre['value']).json()
            try:
                date = annonce['donnees']['conditiondelai']['receptoffres']
            except:
                if self.printAll:
                    print(annonce['gestion']['reference']['idweb'])
            else:
                try:
                    dt_object = datetime.fromtimestamp(date/1000)   
                except:
                    if self.printAll:
                        print(annonce['gestion']['reference']['idweb'])
                else:
                    if self.printAll:
                        print(annonce['gestion']['reference']['idweb'])
                        print(dt_object)
                    if dt_object > datetime.today():
                        arrayReturn.append(annonce)
            i+=1
        return arrayReturn;
        

    def makeMarkdown(self, fileName, rejectedWord = []):
        """Write all not rejected ad in filename and all rejected ad in fileNameReject.
            rejectedWord is the list of word for reject offer
        """
        compteurnew = 0 
        compteurtotal = 0 
        compteurred = 0 
        compteuryellow = 0 
        compteurgreen = 0
        fileOut = open(fileName, 'w', encoding='utf-8')
        fileOut.write('# Extraction du BOAMP\n')
        fileOut.write('> **B**ulletin **o**fficiel des **a**nnonces de **m**archés **p**ublics\n\n')
        header = '| Référence | Acheteur | Montant | Durée | Deadline | Résumé | Mot clé|\n'
        fileOut.write(header)
        fileOut.write('|---|---|---|---|---|---|---|\n')
        for idweb, strList in self.__dicAd.items():
            if self.adIsReject(strList, rejectedWord):
                if self.printAll:
                    print(idweb + ' rejected')
            else:
                if self.printAll:
                    print(idweb + ' added')
            compteurtotal += 1
            champ1 = '[{}](https://www.boamp.fr/avis/detail/{})'.format(idweb,idweb)
            if ((datetime.strptime(strList[6], '%Y-%m-%d %H:%M:%S') + timedelta(days=int(self.NewFor))) > datetime.now()):
                champ1 = '🔥 [{}](https://www.boamp.fr/avis/detail/{})'.format(idweb,idweb)
                compteurnew += 1
                if self.Teams:
                    print('Teams Notification activated') 
                    if os.getenv('MSTEAMS_WEBHOOK'):
                        print('Teams notification configured')
                        TeamsMessage = pymsteams.connectorcard(os.getenv('MSTEAMS_WEBHOOK'))
                        TeamsTxt=('Un nouvel appel d\'offre de {} pour un montant de {} €, datant de moins de {} jour(s) et basé sur le mot clef \'{}\' a été détecté\n. https://www.boamp.fr/avis/detail/{}\n').format(strList[0],strList[2],self.NewFor,strList[7],idweb)
                        TeamsMessage.text(str(TeamsTxt))
                        TeamsMessage.send()
                        print('Teams Notification sent')
                    else:
                        print('Pas de variable d\'environnement pour Teams')
            if self.printAll == True: 
                champ1 = '[{}](https://www.boamp.fr/avis/detail/{}) [⚙️](http://api.dila.fr/opendata/api-boamp/annonces/v230/{})'.format(idweb,idweb,idweb)
                print('\nDate AO : {}'.format(strList[6]))
                print('Date Now : {}'.format(datetime.now()))
                print('Date Cible : {}'.format((datetime.strptime(strList[6], '%Y-%m-%d %H:%M:%S') + timedelta(days=int(self.NewFor)))))
                print('Date Delta : {}'.format(self.NewFor))
                print('Condition : {}'.format((datetime.strptime(strList[6], '%Y-%m-%d %H:%M:%S') + timedelta(days=int(self.NewFor))) > datetime.now()))
            champ2 = '{}'.format(strList[0])
            champ3 = '{} €'.format(strList[2])
            champ6 = '{}'.format(strList[1])
            if strList[1] == "None":
                champ6 = '{}'.format(strList[3])
            if (len(champ6) < 10 ):
                champ6 = '{}'.format(strList[3])
            champ4 = '{} mois'.format(strList[5])
            if ((datetime.strptime(strList[4], '%Y-%m-%d %H:%M:%S')) < (datetime.now() + timedelta(days=int(self.DLRed)))):
                champ5 = '🔴 {}'.format(strList[4])
                compteurred += 1
            elif ((datetime.strptime(strList[4], '%Y-%m-%d %H:%M:%S')) > (datetime.now() + timedelta(days=int(self.DLYellow)))):
                champ5 = '🟢 {}'.format(strList[4])
                compteurgreen += 1
            else:
                champ5 = '🟡 {}'.format(strList[4])
                compteuryellow += 1
            fileOut.write('| '+ champ1.rstrip() + ' | ' +  champ2.rstrip() + ' | ' + champ3.rstrip() + ' | ' + champ4.rstrip() +  ' | ' + champ5.rstrip() + ' | ' + champ6.rstrip() + ' | *' + str(strList[7]) + '*|\n')
        fileOut.write('\n\n_Dernière mise à jour : '+ time.strftime('%A %d/%m/%Y %H:%M:%S') + '_')
        if self.printAll == True:
            fileOut.write(' _[mode debug]_')
        """
        Fichier de statistiques
        """
        fileCounter = open('docs/stats.md', 'w', encoding='utf-8')
        fileCounter.write('# Statistiques\n')
        fileCounter.write('\n\n_Dernière mise à jour : '+ time.strftime('%A %d/%m/%Y %H:%M:%S') + ' (UTC)_ \n\n')
        fileCounter.write('Il y a `' + str(compteurtotal) + '`Appels d\'Offre référencés sur les mots clefs choisis\n\n')
        
        if (compteurnew > 1):
            fileCounter.write('- 🔥 `' + str(compteurnew) + '` nouveaux Appels d\'Offre sont appararus dans les derniers `'+ str(self.NewFor) + '` jours\n')
        else:
            fileCounter.write('- 🔥 `' + str(compteurnew) + '` nouvel Appel d\'Offre est apparu dans les derniers `'+ str(self.NewFor) + '` jours\n')

        if (compteurred > 1): 
            fileCounter.write('- 🔴  `' + str(compteurred) + '` Appels d\'Offre expirent dans moins de `'+ str(self.DLRed) + '` jours\n')
        else:
            fileCounter.write('- 🔴  `' + str(compteurred) + '` Appel d\'Offre expire dans moins de `'+ str(self.DLRed) + '` jours\n')
        
        if (compteuryellow > 1): 
            fileCounter.write('- 🟡  `' + str(compteuryellow) + '` Appels d\'Offre expirent dans moins de `'+ str(self.DLYellow) + '` jours\n')
        else:
            fileCounter.write('- 🟡  `' + str(compteuryellow) + '` Appel d\'Offre expire dans moins de `'+ str(self.DLYellow) + '` jours\n')
        

        if (compteurgreen > 1): 
            fileCounter.write('- 🟢  `' + str(compteurgreen) + '` Appels d\'Offre expirent dans plus de `'+ str(self.DLYellow) + '` jours\n')
        else:
            fileCounter.write('- 🟢  `' + str(compteurgreen) + '` Appel d\'Offre expire dans plus de `'+ str(self.DLYellow) + '` jours\n')
        
        fileCounter.write('\n- 🗝 `' + str(self.cptKeyword) + '` mots-clés')
        """
        Fichier changelog 
        """
        fileCounter = open('docs/changelog.md', 'a', encoding='utf-8')
        fileCounter.write('|' + time.strftime('%d/%m/%Y %H:%M:%S') + ' | ' + str(compteurtotal) + ' | '+ str(compteurnew) + ' | ' +  str(self.cptKeyword) + '|\n')
        """
        Fichier Légende
        """
        filelegende = open('docs/legende.md', 'w', encoding='utf-8')
        filelegende.write('| Symbole | Signification |\n')
        filelegende.write('|---|---|\n')
        filelegende.write('| 🔴 | Deadline dans moins de  `' + str(self.DLRed) + '` jours |\n')
        filelegende.write('| 🟡 | Deadline dans moins de `' + str(self.DLYellow) + '` jours |\n')
        filelegende.write('| 🟢 | DeadLine dans plus de `' + str(self.DLYellow) + '` jours |\n')
        filelegende.write('|  |  |\n')
        filelegende.write('| 🔥 | Nouvel AO (moins de `' + str(self.NewFor) + '` jours) |\n')
        filelegende.write('\n\n⚠️ Les données sont mises à jour toutes les `24` heures')


    def adIsReject(self, ad, rejectedWord = []):
        """Check if ad must be reject or valid.
            Return 1 if ad must be reject.
        """
        for word in rejectedWord:
            if word in ad[0] or word in ad[1]:
                return 1
        return 0


    def AnalyzeAO(self, jsonDesc,keyword):
            """Push add in dicAd.
                jsonDesc is ad description supply by boamp in json format.
            """
            strList = []
            idweb = str(jsonDesc['gestion']['reference']['idweb'])
            # List 0  : Donneur d'ordre 
            strList.append(str(jsonDesc['donnees']['identite']['denomination']))
            # List 1 : Titre de l'AO 
            strList.append(str(jsonDesc['donnees']['objet'][0]['titremarche']))
            # List 2 : Valeur de l'AO 
            try:
                strList.append(str(("{:,}".format(jsonDesc['donnees']['objet'][0]['caracteristiques']['valeurtotale']['value']))))
            except:
                try:
                    strList.append(str("{:,}".format(jsonDesc['donnees']['objet'][0]['lots']['lot'][0]['valeur']['value'])))
                except:
                    strList.append('N/C')
            # List 3 : Objet de l'AO 
            strList.append(str(jsonDesc['donnees']['objet'][0]['objetcomplet']))
            # List 4 : Date remise offre 
            strList.append(str(datetime.fromtimestamp(jsonDesc['donnees']['conditiondelai']['receptoffres']/1000)))
            # List 5 : Durée 
            try:
                if (str(jsonDesc['donnees']['objet'][0]['lots']['lot'][0]['dureemois']) == 'None'): 
                    strList.append('N/C')
                else:
                    strList.append(str(jsonDesc['donnees']['objet'][0]['lots']['lot'][0]['dureemois']))
            except:
                strList.append('N/C')
            # List 6 : Date de dépot AO 
            strList.append(str(datetime.fromtimestamp(jsonDesc['gestion']['indexation']['datepublication']/1000)))
            # List 7  : keyword 
            strList.append(str(keyword))
            if idweb not in self.__dicAd:
                self.__dicAd[idweb] = strList
