from django.shortcuts import render, HttpResponse,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from inception.forms import Raspon,igraci
import pandas as pd
import urllib.parse
import requests
import json
from datetime import *
import csv
noProxy = {"http":None,"https":None,"ftp": None}

def rfc3339_u_lokalno(ulazRFC):
    vrijeme1 = datetime.strptime(ulazRFC, "%Y-%m-%dT%H:%M:%SZ")
    vrijemeUTC = vrijeme1.replace(tzinfo=timezone.utc) #pridijeli vremenu utc oznaku
    vrijemeLokalno = vrijemeUTC.astimezone(tz=None)
    return vrijemeLokalno

def doznaj_sat(ulaz):
    return str(ulaz.strftime("%H.%M"))
def doznaj_datum(ulaz):
    return str(ulaz.strftime("%Y-%m-%d"))





##----------------------------------------------------------------------------------------

class Opterecenje(TemplateView):
    
    template_name='accounts/nba.html'

    def get(self,request):
        form = igraci()
        return render(request, self.template_name, {'form':form, 'text':'prvo ucitavanje'})

    def post(self,request):
                
        form = igraci(request.POST)
        
              
        if form.is_valid():
            ime=  "{0}".format( form.cleaned_data['ime'])
            sezona=  "{0}".format( form.cleaned_data['sezona'])
           
            print(ime)
            print(sezona)
            
           

        ##-------------------------------------------------------------------------------------------------------------   

        ime_igraca="bogdanovic"
        print(ime)
        api_igraci_svi = 'http://www.balldontlie.io/api/v1/players?search='+str(ime)+'' 
        json_data_0 = requests.get(api_igraci_svi, proxies=noProxy).json()        
        df_svi_igraci=pd.DataFrame(json_data_0.items())
        df_svi_igraci.columns =['indeks', 'kolone']
        df_svi_igraci = df_svi_igraci[['kolone']]
        podaci=df_svi_igraci.iloc[0][0]
        df_svi_igraci = pd.DataFrame(podaci)

        print(df_svi_igraci.head())



        print("==================================")
        print("==================================")
        #id_igraca=df_svi_igraci.iloc[0][0]
        #print(id_igraca)
        igraci_pojedinacno=list(df_svi_igraci.id.unique())
        print("Ukupno_igrača naziva "+str(ime_igraca)+":")
        print(len(igraci_pojedinacno))
        id_igraca_prvog=igraci_pojedinacno[0]
        #print(igraci)
        df_ukupno=pd.DataFrame()
        for i in igraci_pojedinacno:
              api_pojedini_igraci = 'http://www.balldontlie.io/api/v1/players/'+str(i)+'' 
              json_data_1 = requests.get(api_pojedini_igraci, proxies=noProxy).json()        
              df_igrac=pd.DataFrame.from_dict(json_data_1)
              df_igrac.reset_index(level=0, inplace=True)
              print(df_igrac.head(1))
              df_igrac=df_igrac.head(1)
              
              statistika = 'http://www.balldontlie.io/api/v1/season_averages?season='+str(sezona)+'&player_ids[]='+str(i)+'' 
              json_data_2 = requests.get(statistika, proxies=noProxy).json()        
              df_statistika=pd.DataFrame(json_data_2.items())
     
              df_statistika.columns =['indeks', 'kolone']
              df_statistika = df_statistika[['kolone']]
              podaci2=df_statistika.iloc[0][0]
              df_statistika = pd.DataFrame(podaci2)
              df_statistika = df_statistika.rename(columns={'player_id': 'id'})
              print(df_statistika.head())
              print("==================================")
              print("==================================")
              
              if not df_statistika.empty:
                  ukupno=df_igrac.merge(df_statistika, how='right', on='id')
                  print(ukupno.head())
                  print("\n\n")
                  ukupno = ukupno.drop(['index','id'], axis=1)  
                  df_ukupno=df_ukupno.append(ukupno)


        print("Nakon svega")
        print(df_ukupno)
        ekstremi=df_ukupno
        skok=ekstremi.iloc[0][18]
        asisti=ekstremi.iloc[0][19]
        poeni=ekstremi.iloc[0][24]
        
        
        
        df_ukupno = df_ukupno.to_html()


        print("Po tekmi:")
        potekmi = 'http://www.balldontlie.io/api/v1/stats?seasons[]='+str(sezona)+'&player_ids[]='+str(id_igraca_prvog)+'' 
        json_data_3 = requests.get(potekmi, proxies=noProxy).json()        
        df_po_utakmici=pd.DataFrame(json_data_3.items())
        #print(df_statistika.head())
        df_po_utakmici.columns =['indeks', 'kolone']
        df_po_utakmici = df_po_utakmici[['kolone']]
        podaci3=df_po_utakmici.iloc[0][0]
        df_po_utakmici = pd.DataFrame(podaci3)
        #df_po_utakmici = df_po_utakmici.rename(columns={'player_id': 'id'})
        df_po_utakmici = df_po_utakmici.drop(['game','player','team'], axis=1)
        print(df_po_utakmici.head())
        df_po_utakmici_stats=df_po_utakmici
        
        df_po_utakmici_graf=df_po_utakmici
        kolo=[]
        for i in range(1,26):
            kolo.append(i)
        df_po_utakmici_graf['Kolo']=kolo
        df_po_utakmici_graf=df_po_utakmici_graf.values
        
        df_po_utakmici= df_po_utakmici.to_html()


        df_po_utakmici_stats=df_po_utakmici_stats.sort_values('pts')
        df_po_utakmici_stats=df_po_utakmici_stats.dropna()
        df_po_utakmici_stats=df_po_utakmici_stats.values

                
        args= { 'form':form,
                'statistika':df_ukupno,
                'ekstremi':ekstremi,
                'df_po_utakmici':df_po_utakmici,
                'df_po_utakmici_stats':df_po_utakmici_stats,
                'skok':skok,
                'asisti':asisti,
                'poeni':poeni,
                'df_po_utakmici_graf':df_po_utakmici_graf,
                'sezona':sezona}
       
        return render(request, self.template_name, args) 
