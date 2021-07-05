#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 21:11:29 2021

@author: harry
"""

import numpy as np
import pandas as pd
from datetime import datetime
import gzip
import re


    
  


""" cette fonction change les directions du vent en catégories."""

def cap(var):  
    
    if (var>337.5) and (var<=22.5):
        var=0
    elif (var>22.5) and (var<=67.5):
        var=45
    elif (var>67.5) and (var<=112.5):
        var=90
    elif (var>112.5) and (var<=157.5):
        var=135
    elif (var>157.5) and (var<=202.5):
        var=180
    elif (var>202.5) and (var<=247.5):
        var=225
    elif (var>247.5) and (var<=292.5):
        var=270
    else:
        var=315
        
    return var


""" celle fonction change la force du vent en catégories."""

def vent(var):   # change la force du vent en noeuds et en 7 catégories de force de vent.
    var=var*3600//1852
    if (var>=0) and (var<5):
        var=1
    
    elif (var>=5) and (var<10):
        var=2
        
    elif (var>=10) and (var<15):
        var=3
        
    elif (var>=15) and (var<20):
        var=4
        
    elif (var>=20) and (var<25):
        var=5
        
    elif (var>=25) and (var<30):
        var=6
        
    else:
        var=7
        
    return var




""" fonction pour changer les temperatures en catégories."""
        
def glagla(var):
    var=var-273.15
    if var<0:
        var=0
        
    elif (var>=0) and (var<5):
        var=1
        
    elif (var>=5) and (var<10):
        var=2
        
    elif (var>=10) and (var<15):
        var=3
        
    elif (var>=15) and (var<20):
        var=4
        
    elif (var>=20) and (var<25):
        var=5
        
    elif (var>=25) and (var<30):
        var=6
        
    elif var>=30:
        var=7
        
    return var

""" Cette classe permet de modifier le fichier d'origine pour avoir des données prêtes pour sikilearn. """


class Meteo_Marine_Classeur:
    
    
    def __init__(self, name, jours=1, var_corbeille=[], vue=12, selection=[62001, 62163], cible='direction'):
        self.name=name
        numb_vars=6
        stations_meteo=[]
        
        stations_meteo_2=[]
        stations_meteo_3=[]
        
        data_good_shape=[]
        target=[]
        
        compteur=[]
        
        indexage_heures=list(pd.date_range('1996-01-01 00:00:00', '2020-12-31 23:00:00', freq='h'))
        time_heures=pd.DataFrame({'date': indexage_heures}) 
        time_heures=time_heures.set_index('date')
        
        indexage_jours=list(pd.date_range('1996-01-01', '2020-12-31', freq='d'))
        time_jours=pd.DataFrame({'date': indexage_jours})
        
        if cible=='direction':
            ci=5
        elif cible=='force':
            ci=6
        elif cible=='humidité':
            ci=4
        elif cible=='température':
            ci=2
        elif cible=='point_rosée':
            ci=3
        elif cible=='pression':
            ci=7
                
        
    
        for station in self.name.loc[:,'numer_sta']:
           
           station_data=self.name.loc[self.name['numer_sta']==station]
           station_data=station_data.drop(['tmer', 'HwaHwa', 'PwaPwa', 'dwadwa', 'Hw1Hw1', 'Pw1Pw1', 'dw1dw1', 'Hw2Hw2', 'Pw2Pw2', 'dw2dw2', 'tend', 'cod_tend', 'vv', 'ww', 'w1', 'w2', 'n', 'nbas', 'hbas', 'cl', 'rafper', 'per', 'phenspe1', 'phenspe2', 'cm', 'ch', 'Unnamed: 36'], axis=1)
           for name in ['numer_sta', 't', 'td', 'u', 'dd', 'ff', 'pmer']:
               station_data[str(name)]=station_data[str(name)].astype('str')
               station_data[str(name)]=station_data[str(name)].str.replace('mq', str(np.nan))
           for name in ['t', 'td', 'u', 'dd', 'ff', 'pmer']:
               station_data[str(name)]=station_data[str(name)].astype('float')
           station_data.numer_sta=station_data.numer_sta.str.replace('BATFR', '').astype('float')
           
           
           station_data["dd"]=station_data["dd"].apply(lambda x: cap(x) if np.isnan(x)==False else x)
           station_data['lat']=station_data['lat'].apply(lambda x: int(x*100) if np.isnan(x)==False else x)
           station_data['lon']=station_data['lon'].apply(lambda x:int(x*100) if np.isnan(x)==False else x)
           station_data['dd']=station_data['dd'].apply(lambda x:int(x) if np.isnan(x)==False else x)
           station_data['ff']=station_data['ff'].apply(lambda x:int(round(x)) if np.isnan(x)==False else x)
           station_data['u']=station_data['u'].apply(lambda x:int(round(x)) if np.isnan(x)==False else x)
           station_data['pmer']=station_data['pmer'].apply(lambda x:int(x/100) if np.isnan(x)==False else x)
           station_data['td']=station_data['td'].apply(lambda x:int(round(x)) if np.isnan(x)==False else x)
           station_data['t']=station_data['t'].apply(lambda x:int(round(x)) if np.isnan(x)==False else x)
           station_data=station_data.drop_duplicates(subset='date')
           station_data.date=station_data.date.apply(lambda x: datetime.strptime(str(x),'%Y%m%d%H%M%S'))
           station_data=station_data.sort_values(['date'],ascending=True)
           station_data=station_data.set_index('date')
           station_data.index=pd.to_datetime(station_data.index)
           station_data_df=time_heures.join(station_data, how='outer')
           
           
           if station_data['numer_sta'].unique() not in compteur:
           
              stations_meteo.append(station_data_df)
           
           
           else: break
       
           compteur.append(station_data['numer_sta'].unique())
           
        
     
        
     
        for station_data in stations_meteo:
            
            station_data=station_data.dropna(axis=1, how='all')
            station_data=station_data.dropna(axis=0, how='any')
            station_data=time_heures.join(station_data, how='outer')
            
            if (station_data.shape[1]==9) and (station_data['numer_sta'].mean()==selection[0] or station_data['numer_sta'].mean()==selection[1]):
                
                stations_meteo_2.append(station_data)
        
        
        for station_data in stations_meteo_2:
            
            liste_heures=[station_data[(station_data.index.hour==i) & (station_data.index.minute==0) & (station_data.index.second==0) ] for i in range(0,24)]
            
        

            station_data=np.concatenate(liste_heures,axis=1)
            station_data=pd.DataFrame(station_data)
            
            station_data.columns=list(np.arange(0, station_data.shape[1]))
            
            

            
            station_data=station_data.drop([0+(i*9) for i in range(int(24))],axis=1) 
            station_data=station_data.drop([10+(i*9) for i in range(int(23))],axis=1) 
            station_data=station_data.drop([11+(i*9) for i in range(int(23))],axis=1) 
            
            
            station_data=time_jours.join(station_data)
            station_data=station_data.set_index('date')
            station_data['mois']=station_data.index.month
            
            station_data.columns=list(np.arange(0, station_data.shape[1]))
            
            liste_jours=[station_data.iloc[i:(i-jours),:] for i in range(jours)]      
            station_data=np.concatenate(liste_jours, axis=1)
            station_data=pd.DataFrame(station_data)
            
            
            station_data.columns=list(np.arange(0, station_data.shape[1]))
            
            
            
          
            
            lat=[(((24)*6+3)*n) for n in range(1,jours)]
            lon=[(((24)*6+3)*n)+1 for n in range(1,jours)]
            mon=[((24)*6+3)*n-1 for n in range(1,jours)]
                
            station_data=station_data.drop(lat, axis=1)
            station_data=station_data.drop(lon, axis=1)
            station_data=station_data.drop(mon, axis=1)
                
            
                
            
            
            station_data.columns=list(np.arange(0,station_data.shape[1]))
            
            liste_decalage_jours_station=[]
            for jour in range(jours):
                station_data=station_data.iloc[jour::jours]
                liste_decalage_jours_station.append(station_data)
                
                
            
            for station_data in liste_decalage_jours_station:
                
            
          
              liste_decalage_heures_station=[]
              for decalage in range(24):
                  part_1=station_data.iloc[0:(station_data.shape[0]-1),0:2].reset_index(drop=True)
                  part_2=station_data.iloc[0:(station_data.shape[0]-1),2+6*decalage:-1].reset_index(drop=True)
                  part_3=station_data.iloc[1:(station_data.shape[0]),2:2+6*decalage].reset_index(drop=True)
                  part_4=station_data.iloc[1:(station_data.shape[0]),-1].reset_index(drop=True)
                
                  total=part_1.join(part_2)
                  total=total.join(part_3)
                  total=total.join(part_4)
                
                  

                  total.columns=list(np.arange(0, total.shape[1]))
                
                  liste_decalage_heures_station.append(total)
                
             
              stations_meteo_3.append(liste_decalage_heures_station)
            
            
         
        for station_data in stations_meteo_3:
            
            for station_decalage in station_data:
                
                station_decalage=station_decalage.reset_index(drop=True)
                                  
                for val in range(station_decalage.shape[0]-1):
                        
                    row=station_decalage.iloc[val,:]
                    row2=station_decalage.iloc[val+1,ci+6*vue]
                    
                    
                    if np.isnan(row).sum()==0 and np.isnan(row2).sum()==0:
                            
                        
                        
                            data_good_shape.append(row)
                            target.append(row2)
                            
                            
                        
                    
                    else:
                        continue
        
        
        
        
        data_good_shape=pd.DataFrame(data_good_shape)
        
        for name in var_corbeille:
                              
                if name.find("force")!=-1:
                    data_good_shape=data_good_shape.drop([i*numb_vars for i in range(1,jours*24+1)], axis=1)
                
                elif name.find("direction")!=-1:
                    data_good_shape=data_good_shape.drop([5+i*numb_vars for i in range(0,jours*24)], axis=1)
                  
                    
                elif name.find("humidité")!=-1:
                    data_good_shape=data_good_shape.drop([4+i*numb_vars for i in range(0,jours*24)], axis=1)
                    
                elif name.find("point_rosée")!=-1:
                    data_good_shape=data_good_shape.drop([3+i*numb_vars for i in range(0,jours*24)], axis=1)
                    
                elif name.find("température")!=-1:
                    data_good_shape=data_good_shape.drop([2+i*numb_vars for i in range(0,jours*24)], axis=1)
                    
                elif name.find("pression")!=-1:
                    data_good_shape=data_good_shape.drop([7+i*numb_vars for i in range(0,jours*24)], axis=1)
                    
                elif name.find("latitude")!=-1:
                    data_good_shape=data_good_shape.drop([0], axis=1)
                    
                elif name.find("longitude")!=-1:
                    data_good_shape=data_good_shape.drop([1], axis=1)
                    
                elif name.find("temps")!=-1:
                    data_good_shape=data_good_shape.drop([2+24*numb_vars*jours], axis=1)
        
        data_good_shape=np.array(data_good_shape)
        target_2=[]
        if cible=='force':
            for val in target:
                val2=int(vent(val))
                target_2.append(val2)
            target=target_2
        elif cible=='température':
            for val in target:
                val2=int(glagla(val))
                target_2.append(val2)
            target=target_2
        
        target=np.transpose(target)
        target=target.astype('int32')
        data_good_shape=data_good_shape.astype('int32')
            
        
        
        
        
        self.dimensions=data_good_shape.shape
        self.target=target
        self.data_good_shape=data_good_shape
        
      
        






