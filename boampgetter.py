import requests
import json
from datetime import datetime
from datetime import timedelta

numerLineInAd = 4 # number of line for describe ad

class boampGetter:
    def __init__(self):
        self.__searchResponse = {}
        self.__dicAd = {}
        self.printAll = 0

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
        print('{} Response found'.format(self.__searchSize()))

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


    def pushAd(self, jsonDesc):
        """Push add in dicAd.
            jsonDesc is ad description supply by boamp in json format.
        """
        strList = []
        idweb = str(jsonDesc['gestion']['reference']['idweb'])
        # List 0 
        strList.append(str(jsonDesc['donnees']['identite']['denomination']))
        # List 1 
        strList.append(str(jsonDesc['donnees']['objet'][0]['titremarche']))
        # List 2 
        try:
            strList.append(str(jsonDesc['donnees']['objet'][0]['caracteristiques']['valeurtotale']['value']))
        except:
            try:
                strList.append(str(jsonDesc['donnees']['objet'][0]['lots']['lot'][0]['valeur']['value']))
            except:
                strList.append('N/C')
        # List 3 
        strList.append(str(jsonDesc['donnees']['objet'][0]['objetcomplet']))
        # List 4 
        strList.append(str(datetime.fromtimestamp(jsonDesc['donnees']['conditiondelai']['receptoffres']/1000)))
        # List 5 
        try:
            if (str(jsonDesc['donnees']['objet'][0]['lots']['lot'][0]['dureemois']) == 'None'): 
                strList.append('N/C')
            else:
                strList.append(str(jsonDesc['donnees']['objet'][0]['lots']['lot'][0]['dureemois']))
        except:
            strList.append('N/C')

        if idweb not in self.__dicAd:
            self.__dicAd[idweb] = strList
    
    def adIsReject(self, ad, rejectedWord = []):
        """Check if ad must be reject or valid.
            Return 1 if ad must be reject.
        """
        for word in rejectedWord:
            if word in ad[0] or word in ad[1]:
                return 1
        return 0
        
    def makeOutputFile(self, fileName, fileNameReject, rejectedWord = []):
        """Write all not rejected ad in filename and all rejected ad in fileNameReject.
            rejectedWord is the list of word for reject offer
        """

        fileValid = open(fileName, 'w', encoding='utf-8')
        fileReject = open(fileNameReject, 'w', encoding='utf-8')
        fileOut = 0
        for idweb, strList in self.__dicAd.items():
            if self.adIsReject(strList, rejectedWord):
                fileOut = fileReject
            else:
                fileOut = fileValid
            fileOut.write('{} \n'.format(strList[0]))
            fileOut.write('Valeur : {} € sur une durée de {} mois\n'.format(strList[2],strList[5]))
            if strList[1] == strList[3]:
                fileOut.write('{} \n'.format(strList[1]))
            else:
                if strList[1] == "None":
                    fileOut.write('{} \n'.format(strList[3]))
                else:
                    fileOut.write('{} \n'.format(strList[1]))
                    fileOut.write('{} \n'.format(strList[3]))
            fileOut.write('Date limite: {}\n'.format(strList[4]))
            fileOut.write('idWeb: {}\n'.format(idweb))
            fileOut.write('URL : https://www.boamp.fr/avis/detail/{}\n'.format(idweb))
            fileOut.write('-------------------------------------------------\n')
 
    def makeMarkdown(self, fileName, rejectedWord = []):
        """Write all not rejected ad in filename and all rejected ad in fileNameReject.
            rejectedWord is the list of word for reject offer
        """
        fileOut = open(fileName, 'w', encoding='utf-8')
        header = '| Référence | Dénomination | Montant | Durée | Deadline | Résumé |\n'
        fileOut.write(header)
        fileOut.write('|---|---|---|---|---|---|\n')
        for idweb, strList in self.__dicAd.items():
            if self.adIsReject(strList, rejectedWord):
                if self.printAll:
                    print(annonce['gestion']['reference']['idweb'] + ' rejected')
            else:
                if self.printAll:
                    print(annonce['gestion']['reference']['idweb'] + ' added')
            champ1 = '[{}](https://www.boamp.fr/avis/detail/{})'.format(idweb,idweb)
            champ2 = '{}'.format(strList[0])
            champ3 = '{} €'.format(strList[2])
            champ6 = '{}'.format(strList[1])
            if strList[1] == "None":
                champ6 = '{}'.format(strList[3])
            champ4 = '{} mois'.format(strList[5])
            if ((datetime.strptime(strList[4], '%Y-%m-%d %H:%M:%S')) < (datetime.now() + timedelta(days=10))):
                champ5 = '🔴 {}'.format(strList[4])
            elif ((datetime.strptime(strList[4], '%Y-%m-%d %H:%M:%S')) > (datetime.now() + timedelta(days=10))):
                champ5 = '🟢 {}'.format(strList[4])
            fileOut.write('| '+ champ1.rstrip() + ' | ' +  champ2.rstrip() + ' | ' + champ3.rstrip() + ' | ' + champ4.rstrip() +  ' | ' + champ5.rstrip() + ' | ' + champ6.rstrip() + ' |\n')
