from apps.home.models import Courses, Tasks, Merchants, Geolocation, Packages
import pandas as pd
from django.core.cache import cache
from itertools import zip_longest 
import numpy as np
import copy
import re
import json
from statistics import mean
import requests


def get_data_id():

    # veryfy if the result is in cache
    cached_result = cache.get('get_data_4')

    if cached_result is not None:
        return cached_result
    else:
        # convert the data in dataframe
        df_courses = pd.DataFrame(list(Courses.objects.all().values()))
        df_tasks = pd.DataFrame(list(Tasks.objects.all().values()))
        df_merchants = pd.DataFrame(list(Merchants.objects.all().values()))

        # merge the data
        df = pd.merge(df_courses, df_tasks, right_on='course_id', left_on='id', how='inner', suffixes=('_course', '_task'))

        # fitter the data
        merchant_trd = df_merchants[df_merchants['group_0_id'] == 1]
        merchant_trd = merchant_trd[['id']]
        merchant_id = df_merchants[~df_merchants['id'].isin([19, 20, 54, 77, 63, 85, 21, 37, 66, 645, 646, 603, 624, 628,
                                                            647, 112, 83, 632, 648,70, 44, 39,
                                                            32, 43, 45, 102, 26, 61, 27, 33, 36, 87, 75, 78, 105, 
                                                            200, 625, 629, 642, 626, 636, 8, 247, 238, 
                                                            643, 627, 631, 637, 638, 340, 123, 320, 639, 480, 402, 29, 
                                                            282, 141, 151, 154, 159, 305, 307, 335, 345, 125, 317, 359, 
                                                            385, 394, 414, 432, 441, 446, 544, 518, 530, 392, 559, 565, 
                                                            287, 572, 352, 574, 591, 279, 403, 583, 49, 364, 148, 569, 
                                                            128, 324, 597, 437, 533, 376, 331, 620, 274, 621, 602, 622, 623, 31,
                                                            604,608,663])]
        merchant_id = merchant_id[['id']]

        df = df.sort_values(by='end_date', ascending=False)
        df['end_date'] = pd.to_datetime(df['end_date'])
        df = df.dropna(subset=['end_date'])
        df = df[df['state_task'] == 3]
        df = df[df['type'] != "collecte"]
        merchant_trd_ids = merchant_trd['id'].tolist()
        merchant_id_ids = merchant_id['id'].tolist()
        df = df[(df['created_by_id'] == 1) | (df['merchant_id_course'].isin(merchant_trd_ids)) | (df['merchant_id_course'].isin(merchant_id_ids))]
        df = df.dropna(subset=['merchant_id_course'])
        df = df[~df['merchant_id_course'].isin([8,200,604])]
        result = df
    
    # save the result in cache
    cache.set('get_data_4', result, timeout=50000)
    return result

def get_data_cydi():

    # veryfy if the result is in cache
    cached_result = cache.get('get_data_2')
    if cached_result is not None:
        return cached_result
    else:
        # charger the data
        df_geolocation = pd.DataFrame(list(Geolocation.objects.all().values()))
        df_task = pd.DataFrame(list(Tasks.objects.all().values())) 
        df = get_data_id()
        id_f_task = df['id_task']

        # merge the data geo and task and clean the data just to real merchants
        df_geo_task = pd.merge(df_task, df_geolocation, right_on='task_id', left_on='id', how='right', suffixes=('_task', '_geo'))
        df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
        df_task = df_task[df_task['id'].isin(id_f_task)]
        df_geo_task =  df_geo_task[["odometer", "timestamp", "id", "coordinates", "history"]]
    
        # JSON to dict and column 
        df_normalized_1 = pd.json_normalize(df_task['cycling'])
        df_normalized_1 = df_normalized_1.add_suffix('_cycling')
        df_task.reset_index(drop=True, inplace=True)
        df_normalized_1.reset_index(drop=True, inplace=True)
        df_task = pd.concat([df_task, df_normalized_1], axis=1)

        df_normalized_2 = pd.json_normalize(df_task['driving'])
        df_normalized_2 = df_normalized_2.add_suffix('_driving')
        df_task.reset_index(drop=True, inplace=True)
        df_normalized_2.reset_index(drop=True, inplace=True)
        df_task = pd.concat([df_task, df_normalized_2], axis=1)

        df_normalized_3 = pd.json_normalize(df_task['altitudes'])
        df_normalized_3 = df_normalized_3.add_suffix('_altitudes')
        df_task.reset_index(drop=True, inplace=True)
        df_normalized_3.reset_index(drop=True, inplace=True)
        df_task = pd.concat([df_task, df_normalized_3], axis=1)

        df_task = df_task.sort_values(by='end_date', ascending=False)
        df_task['end_date'] = pd.to_datetime(df_task['end_date'])
        df_task = df_task.dropna(subset=['end_date'])

        # https://ijbnpa.biomedcentral.com/articles/10.1186/s12966-017-0513-z time
        # https://www.semanticscholar.org/paper/Speed-characteristics-of-speed-pedelecs%2C-pedelecs-Twisk-Stelling/1873dba382e26727f54d352c338f120802ea1e2e speed

        flat = 0.15 # Porcentage of time save in electric cycling in flat road 
        hilly = 0.35 # Porcentage of time save in electric cyucling in hilly road  
        mean_time = 1- (flat+hilly)/2
        speed_mean_cycling = 1+ 2.8/17.8 # Porcentage of speed more fast than normal cycling 

        df_task['durations_cycling_copy'] = df_normalized_1['durations_cycling'].apply(lambda x: copy.deepcopy(x) if isinstance(x, list) else [])
        df_task['speeds_cycling_copy'] = df_normalized_1['speeds_cycling'].apply(lambda x: copy.deepcopy(x) if isinstance(x, list) else [])
        df_task['distances_cycling_copy'] = df_normalized_1['distances_cycling'].apply(lambda x: copy.deepcopy(x) if isinstance(x, list) else [])
        
        df_task['durations_cycling_copy'] = df_task['durations_cycling_copy'].apply(lambda x: [value * mean_time for value in x] if isinstance(x, list) and all(isinstance(value, (int, float)) for value in x) else x)  
        df_task['speeds_cycling_copy'] = df_task['speeds_cycling_copy'].apply(lambda x: [value * speed_mean_cycling for value in x] if isinstance(x, list) and all(isinstance(value, (int, float)) for value in x) else x)
        df_task['distances_cycling_copy'] = df_task.apply(lambda row: [a * b if isinstance(a, (int, float)) and isinstance(b, (int, float)) else None for a, b in zip(row['durations_cycling_copy'], row['speeds_cycling_copy'])] if isinstance(row['durations_cycling_copy'], list) and isinstance(row['speeds_cycling_copy'], list) else row['durations_cycling_copy'], axis=1)

        df_grouped = (df_geo_task
            .groupby('id')
            .apply(lambda group: group.sort_values(by='timestamp'))
            )
        
        df_grouped = df_grouped.reset_index(drop=True)
        df_grouped['num_rows'] = df_grouped.groupby('id')['id'].transform('count')
        df_grouped = df_grouped[~((df_grouped['num_rows'] == 1))]
        df_grouped = df_grouped.drop(columns=['num_rows'])
        df_normalized_4 = pd.json_normalize(df_grouped['history'])
        df_normalized_4 = df_normalized_4.add_suffix('_history')
        df_grouped.reset_index(drop=True, inplace=True)
        df_normalized_4.reset_index(drop=True, inplace=True)
        df_grouped = pd.concat([df_grouped, df_normalized_4], axis=1)
        df_grouped['three.datetime_history'] = pd.to_datetime(df_grouped['three.datetime_history'], format='%Y-%m-%dT%H:%M')
        df_grouped['two.datetime_history'] = pd.to_datetime(df_grouped['two.datetime_history'], format='%Y-%m-%dT%H:%M')
        df_grouped['timestamp'] = pd.to_datetime(df_grouped['timestamp'], format='%Y-%m-%dT%H:%M')

        id_gr = df_grouped['id'].unique()
        list_1 = []
        list_2 = []
        list_3 = []
        list_4 = []
        for i in range(len(id_gr)):
            df_ex = df_grouped[df_grouped['id'] == id_gr[i]]
            vector = []
            vector_1 = []
            vector_2 = []
            for r in range(len(df_ex) - 1):  # Resta 1 para evitar un índice fuera de rango
                a = df_ex.iloc[r + 1]['odometer'] - df_ex.iloc[r]['odometer']
                if pd.isna(df_ex.iloc[r]['three.datetime_history']):
                    t = (df_ex.iloc[r + 1]['timestamp'] - df_ex.iloc[r]['timestamp']).total_seconds()
                else: 
                    t = (df_ex.iloc[r]['three.datetime_history'] - df_ex.iloc[r]['two.datetime_history']).total_seconds()
                c = a / t
                vector.append(a)
                vector_1.append(t)
                vector_2.append(c)
            list_1.append(vector)
            list_2.append(vector_1)
            list_3.append(vector_2) 
            list_4.append(id_gr[i])

        df_geo_task = pd.DataFrame({ 'id': list_4, 'distance_deki': list_1, 'durations_deki': list_2, 'speeds_deki': list_3})

        for i in range(len(df_geo_task)): 
            df_geo_task.loc[i,'Total_distance_deki'] = sum(df_geo_task.loc[i, 'distance_deki'])
            df_geo_task.loc[i,'Total_durations_deki'] = sum(df_geo_task.loc[i, 'durations_deki'])

        df_geo_task = pd.merge(df_task, df_geo_task, right_on='id', left_on='id', how='left', suffixes=('_task', '_geo'))
        
        columns_prona = ['speeds_cycling_copy','distances_cycling_copy', 'durations_cycling_copy', 'totalDistance_cycling', 'totalDuration_cycling', 
                         'speeds_driving', 'distances_driving', 'durations_driving', 'totalDistance_driving', 'totalDuration_driving', 
                         'deliveryPoint_altitudes', 'pickUpPoint_altitudes']
        df_geo_task = df_geo_task.dropna(subset= columns_prona, how= 'any')
        df_geo_task = df_geo_task[(df_geo_task['totalDuration_driving'] != 0 ) | (df_geo_task['totalDuration_cycling'] != 0)]
        df_geo_task = df_geo_task[(df_geo_task['totalDistance_driving'] != 0 ) | (df_geo_task['totalDistance_driving'] != 0)]

        address = pd.json_normalize(df_geo_task['address'])['text']

        def find_postal_code(address):
            # Define the search pattern for postal codes (format: five digits)
            pattern = r'\b\d{5}\b'

            if not pd.isna(address):
                # Search for the pattern in the address
                result = re.search(pattern, address)
            else:
                result = None
            # If a postal code is found, return the result
            if result:
                return result.group()
            else:
                return None

        df_geo_task['postal'] = address

        df_geo_task['postal'] = df_geo_task['postal'].apply(find_postal_code)

        def get_id_city(postal_code):
            if postal_code is not None and len(postal_code) >= 2:
                return postal_code[:2]  # Get the first two digits
            else:
                return None

        df_geo_task['id_city'] = df_geo_task['postal'].apply(get_id_city)
        
        result = df_geo_task
    
    # save the result in cache
    cache.set('get_data_2', result, timeout=50000)
    return result

def get_data_livra():
    # veryfy if the result is in cache
    cached_result = cache.get('get_data_3')

    if cached_result is not None:
        return cached_result
    else:
        # convert the data in dataframe
        df_packages = pd.DataFrame(list(Packages.objects.all().values()))
        df = get_data_id()
        id_f = df['id_task'].unique()

        df_packages  = df_packages[df_packages['delivery_id'].isin(id_f)]
        result = df_packages
    
    # save the result in cache
    cache.set('get_data_3', result, timeout=50000)
    return result

def get_data_merchants():

    # veryfy if the result is in cache
    cached_result = cache.get('get_data_merchants')

    if cached_result is not None:
        return cached_result
    else:
        df_merchants = pd.DataFrame(list(Merchants.objects.all().values()))
        result = df_merchants
    
    # save the result in cache
    cache.set('get_data_merchants' , result, timeout=50000)
    return result

def get_data_courses():
    # veryfy if the result is in cache
    cached_result = cache.get('get_data_courses')

    if cached_result is not None:
        return cached_result
    else:
        df_courses = pd.DataFrame(list(Courses.objects.all().values()))
        result = df_courses
    
    # save the result in cache
    cache.set('get_data_courses' , result, timeout=50000)
    return result

def get_data_task():
    # veryfy if the result is in cache
    cached_result = cache.get('get_data_task')

    if cached_result is not None:
        return cached_result
    else:
        df_tasks = pd.DataFrame(list(Tasks.objects.all().values()))
        result = df_tasks

    # save the result in cache
    cache.set('get_data_task' , result, timeout=50000)
    return result

def num_delivery(stored_selected_date, selected_city,newuser=None):

    cache_key =f'num_delivery_{stored_selected_date}_{newuser}_{selected_city}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        df = get_data_id()
        df_merchants = get_data_merchants()
        df_geo_task = get_data_cydi()

        if selected_city is not None:
            def city_to_id(selected_city):
                city_mapping = {
                    'marseille': '13',
                    'lyon': '69',
                    'lille': '59',
                    'paris': '75',
                    'bordeaux': '33',
                    'toulouse': '31',
                    'dijon': '21',  # Ensure 'dijon' is lowercase for consistency
                }
                return [city_mapping.get(city.lower(), None) for city in selected_city]
            
            city_id = city_to_id(selected_city)

            df_geo_task = df_geo_task[df_geo_task['id_city'].isin(city_id)]
            id_tf = df_geo_task['id']
            df = df[df['id_task'].isin(id_tf)]
        else: 
            df=df

        if newuser is not None:
            if newuser == 'group_id=1' or newuser == 1 or newuser == 'index2.html/group_id=1':
                merchant_trd = df_merchants[df_merchants['group_0_id'] == 1]
                merchant_trd = merchant_trd[['id']]
                merchant_trd_ids = merchant_trd['id'].tolist()
                df = df[df['merchant_id_course'].isin(merchant_trd_ids)]
            elif newuser == 'team_id=2' or newuser == 2 :
                df = df[df['team_id'] == 2]
            elif newuser == 'team_id=3' or newuser == 3 :
                df = df[df['team_id'] == 3]
            elif newuser == 'team_id=4' or newuser == 4 : 
                df = df[df['team_id'] == 4]
            elif newuser == 'team_id=6' or newuser == 6:
                df = df[df['team_id'] == 6]
            elif newuser == 'team_id=9' or newuser == 9 :
                df = df[df['team_id'] == 9]
            elif newuser == 'team_id=10' or newuser == 10 :
                df = df[df['team_id'] == 10]
            elif newuser == 'team_id=11' or newuser == 11 :
                df = df[df['team_id'] == 11]
            elif newuser == 'team_id=13' or newuser == 13 :
                df = df[df['team_id'] == 13]
            elif newuser == 'team_id=14' or newuser == 14:
                df = df[df['team_id'] == 14]
            elif newuser == 'team_id=15' or newuser == 15 :
                df = df[df['team_id'] == 15]
            elif newuser == 'team_id=16' or newuser == 16 :
                df = df[df['team_id'] == 16]
            elif newuser == 'team_id=17' or newuser == 17 :
                df = df[df['team_id'] == 17]
            elif newuser == 'team_id=18' or newuser == 18 :
                df = df[df['team_id'] == 18]
            elif newuser == 'team_id=19' or newuser == 19 :
                df = df[df['team_id'] == 19]
            elif newuser == 'team_id=20' or newuser == 20 :
                df = df[df['team_id'] == 20]
            elif newuser == 'team_id=22' or newuser == 22:
                df = df[df['team_id'] == 22]
            elif newuser == 'merchant_id=606' or newuser == 606 :
                df = df[df['merchant_id_course'] == 606]
            elif newuser == 'merchant_id=605' or newuser == 605 :
                df = df[df['merchant_id_course'] == 605]
            elif newuser == 'merchant_id=607' or newuser == 607 :
                df = df[df['merchant_id_course'] == 607]
            elif newuser == 'merchant_id=609' or newuser == 609 :
                df = df[df['merchant_id_course'] == 609]
            elif newuser == 'merchant_id=610' or newuser == 610 :
                df = df[df['merchant_id_course'] == 610]
            elif newuser == 'merchant_id=617' or newuser == 617 :
                df = df[df['merchant_id_course'] == 617]
            elif newuser == 'merchant_id=630' or newuser == 630 :
                df = df[df['merchant_id_course'] == 630]
            elif newuser == 'merchant_id=635' or newuser == 635 :
                df = df[df['merchant_id_course'] == 635]
            elif newuser == 'merchant_id=640' or newuser == 640 :
                df = df[df['merchant_id_course'] == 640]
            elif newuser == 'merchant_id=641' or newuser == 641:
                df = df[df['merchant_id_course'] == 641]
            elif newuser == 'merchant_id=649' or newuser == 649 :
                df = df[df['merchant_id_course'] == 649]
            elif newuser == 'merchant_id=650' or newuser == 650 :
                df = df[df['merchant_id_course'] == 650]
            elif newuser == 'merchant_id=651' or newuser == 651 :
                df = df[df['merchant_id_course'] == 651]
            elif newuser == 'merchant_id=652' or newuser == 652 :
                df = df[df['merchant_id_course'] == 652]
            else:
                df= pd.DataFrame(columns=df.columns)
        else:
            df=df
        

        if stored_selected_date is not None:
            st, en = stored_selected_date.strip('()[]').split(' to ')
            st = pd.to_datetime(st, format='%d/%m/%Y')
            en = pd.to_datetime(en, format='%d/%m/%Y')
            df['end_date'] = pd.to_datetime(df['end_date'])
            st = st.tz_localize(df['end_date'].dt.tz)
            en = en.tz_localize(df['end_date'].dt.tz)
            df = df[(df['end_date'] >= st) & (df['end_date'] <= en)]
        else: 
            df = df


        if df.empty:
            result = 0
        else: 
            num_finished_task = len(df)
            result = num_finished_task

    # save the result in cache
    cache.set(cache_key , result, timeout=41020)
    return result

def CO2(stored_selected_date, selected_city, newuser=None):

    cache_key =f'CO2_result{stored_selected_date}_{newuser}_{selected_city}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        # charger the data
        df_geo_task = get_data_cydi()
        df = get_data_id()
        df_merchants = get_data_merchants()

        if stored_selected_date is not None:
            st, en = stored_selected_date.strip('()[]').split(' to ')
            st = pd.to_datetime(st, format='%d/%m/%Y')
            en = pd.to_datetime(en, format='%d/%m/%Y')
            st = st.tz_localize(df_geo_task['end_date'].dt.tz)
            en = en.tz_localize(df_geo_task['end_date'].dt.tz)
            df_geo_task = df_geo_task[(df_geo_task['end_date'] >= st) & (df_geo_task['end_date'] <= en)]
            df_geo_task = df_geo_task.reset_index(drop=True)
        else: 
            df_geo_task=df_geo_task

        if selected_city is not None:

            def city_to_id(selected_city):
                city_mapping = {
                    'marseille': '13',
                    'lyon': '69',
                    'lille': '59',
                    'paris': '75',
                    'bordeaux': '33',
                    'toulouse': '31',
                    'dijon': '21',  # Ensure 'dijon' is lowercase for consistency
                }
                return [city_mapping.get(city.lower(), None) for city in selected_city]
            
            city_id = city_to_id(selected_city)

            df_geo_task = df_geo_task[df_geo_task['id_city'].isin(city_id)]
        else: 
            df_geo_task=df_geo_task

        if newuser is not None:
            if newuser == 'group_id=1' or newuser == 1:
                merchant_trd = df_merchants[df_merchants['group_0_id'] == 1]
                merchant_trd = merchant_trd[['id']]
                merchant_trd_ids = merchant_trd['id'].tolist()
                df = df[df['merchant_id_course'].isin(merchant_trd_ids)]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=2' or newuser == 2:
                df = df[df['team_id'] == 2]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=3' or newuser == 3:
                df = df[df['team_id'] == 3]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=4' or newuser == 4:
                df = df[df['team_id'] == 4]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=6' or newuser == 6:
                df = df[df['team_id'] == 6]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=9' or newuser == 9:
                df = df[df['team_id'] == 9]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=10' or newuser == 10:
                df = df[df['team_id'] == 10]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=11' or newuser == 11:
                df = df[df['team_id'] == 11]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=13' or newuser == 13:
                df = df[df['team_id'] == 13]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=14' or newuser == 14:
                df = df[df['team_id'] == 14]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=15' or newuser == 15:
                df = df[df['team_id'] == 15]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=16' or newuser == 16:
                df = df[df['team_id'] == 16]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=17' or newuser == 17:
                df = df[df['team_id'] == 17]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=18' or newuser == 18:
                df = df[df['team_id'] == 18]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=19' or newuser == 19:
                df = df[df['team_id'] == 19]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=20' or newuser == 20:
                df = df[df['team_id'] == 20]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=22' or newuser ==22:
                df = df[df['team_id'] == 22]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=606' or newuser == 606:
                df = df[df['merchant_id_course'] == 606]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=605' or newuser == 605:
                df = df[df['merchant_id_course'] == 605]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=607' or newuser == 607:
                df = df[df['merchant_id_course'] == 607]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=609' or newuser == 609:
                df = df[df['merchant_id_course'] == 609]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=610' or newuser == 610:
                df = df[df['merchant_id_course'] == 610]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=617' or newuser == 617:
                df = df[df['merchant_id_course'] == 617]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=630' or newuser == 630:
                df = df[df['merchant_id_course'] == 630]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=635' or newuser == 635:
                df = df[df['merchant_id_course'] == 635]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=640' or newuser == 640:
                df = df[df['merchant_id_course'] == 640]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=641' or newuser == 641:
                df = df[df['merchant_id_course'] == 641]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=649' or newuser == 649:
                df = df[df['merchant_id_course'] == 649]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=650' or newuser == 650:
                df = df[df['merchant_id_course'] == 650]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=651' or newuser == 651:
                df = df[df['merchant_id_course'] == 651]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=652' or newuser == 652:
                df = df[df['merchant_id_course'] == 652]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            else:
                df_geo_task = pd.DataFrame(columns=df_geo_task.columns)
        else: 
            df_geo_task=df_geo_task

            
        if df_geo_task.empty:
            emi = 'non calculable'     
            emi_total= 'non calculable'
            CO2_driving_total = 0
            CO2_cycling_total =  0
            CO2_deki_vul_total = 0
            result = (emi,emi_total,CO2_driving_total,CO2_cycling_total,CO2_deki_vul_total )          
        else:
            df_geo_task['inclination'] = 0

            mask = (df_geo_task['pickUpPoint_altitudes'] == 0) | (df_geo_task['deliveryPoint_altitudes'] == 0)
            df_geo_task.loc[mask, 'inclination'] = df_geo_task['pickUpPoint_altitudes'] + df_geo_task['deliveryPoint_altitudes']

            mask = ~mask
            df_geo_task.loc[mask, 'inclination'] = ((df_geo_task['deliveryPoint_altitudes'] - df_geo_task['pickUpPoint_altitudes']) / df_geo_task['totalDistance_driving']) * 100


            def calculate_diffs(lst):
                if not lst:
                    return []  # Devolver una lista vacía si lst está vacía
                lst = [0 if x is None else x for x in lst]
                diffs = [b - a for a, b in zip_longest(lst, lst[1:], fillvalue=0)]
                diffs.insert(0, lst[0])  # Insertar el valor inicial al principio
                diffs = diffs[:-1]  # Eliminar el último elemento
                return diffs
            
            def clean_speeds_cycling(x):
                if isinstance(x, list):
                    return x
                elif isinstance(x, float):
                    return [x]
                elif pd.isna(x):
                    return None  # Handle missing values
                else:
                    # Handle unexpected data types (e.g., strings)
                    return None 
                
            
          
            # Apply the function to the 'speeds_cycling' column
            df_geo_task['speeds_cycling_copy'] = df_geo_task['speeds_cycling_copy'].apply(lambda x: [x] if isinstance(x, int) else x)
            vector_diffs_1 = df_geo_task['speeds_cycling_copy'].apply(calculate_diffs).tolist()

            df_geo_task['speeds_deki'] = df_geo_task['speeds_deki'].apply(clean_speeds_cycling)
            df_geo_task['speeds_deki'] = df_geo_task['speeds_deki'].apply(lambda x: [x] if isinstance(x, int) else x)
            vector_diffs_1_1 = df_geo_task['speeds_deki'].apply(calculate_diffs).tolist()

            # Apply the function to the 'speeds_driving' column
            df_geo_task['speeds_driving'] = df_geo_task['speeds_driving'].apply(lambda x: [x] if isinstance(x, int) else x)
            vector_diffs_2 = df_geo_task['speeds_driving'].apply(calculate_diffs).tolist()
            df_geo_task['acceleration_driving'] = vector_diffs_2


            condition = ((df_geo_task['Total_distance_deki'] > df_geo_task['totalDistance_cycling']) |
             (df_geo_task['Total_distance_deki'] == 0) |
             (df_geo_task['Total_durations_deki'] > df_geo_task['totalDuration_cycling']) |
             (df_geo_task['Total_durations_deki'] == 0) |
             pd.isna(df_geo_task['Total_distance_deki']))
            
            df_geo_task.reset_index(drop=True, inplace=True)

            df_geo_task['acceleration_cycling'] = [[] for _ in range(len(df_geo_task))]

            for i, row in df_geo_task.iterrows():
                if condition.iloc[i]:
                    df_geo_task.at[i, 'acceleration_cycling'] = vector_diffs_1[i]
                else:
                    df_geo_task.at[i, 'acceleration_cycling'] = vector_diffs_1_1[i]      

            for i, row in df_geo_task.iterrows():
                if condition.iloc[i]:
                    df_geo_task.at[i, 'speeds_cycling_copy'] = df_geo_task['speeds_cycling_copy'][i]
                else:
                    df_geo_task.at[i, 'speeds_cycling_copy'] = df_geo_task['speeds_deki'][i] 

            for i, row in df_geo_task.iterrows():
                if condition.iloc[i]:
                    df_geo_task.at[i, 'distances_cycling_copy'] = df_geo_task['distances_cycling_copy'][i]
                else:
                    df_geo_task.at[i, 'distances_cycling_copy'] = df_geo_task['distance_deki'][i] 

            for i, row in df_geo_task.iterrows():
                if condition.iloc[i]:
                    df_geo_task.at[i, 'durations_cycling_copy'] = df_geo_task['durations_cycling_copy'][i]
                else:
                    df_geo_task.at[i, 'durations_cycling_copy'] = df_geo_task['durations_deki'][i]          

            # Renault Master ==>> VUL termique data: https://www.vcalc.com/wiki/vCalc/Cost+to+Idle * 
            # https://www.engineeringtoolbox.com/fuels-higher-calorific-values-d_169.html *
            # https://x-engineer.org/rolling-resistance/#formula *
            # https://www.mdpi.com/2032-6653/14/6/134 *
            # https://www.aerodinamicaf1.com/2019/09/las-fuerzas-sobre-el-monoplaza-drag-y-lift-o-downforce/ *
            # https://base-empreinte.ademe.fr/donnees/jeu-donnees *
            # The maximum load of a VUL is 3.5 tons, which is equivalent to 3500 kg.
            # Parameters:

            ### FMC

            alpha_vul = 0.8833 #ml/s
            beta_1_vul_diseal = 1/37.3 #ml/kj avergae of max and minimum   
            beta_2_vul_diseal = 0.0258
            crr = 0.013 # rolling resistance coefficient
            weight_vul = 2066 #kg
            weigth_vul_delivery = 70 #kg
            weight_vul_35 = 1434*0.35 #kg
            sum_weight_vul = weight_vul + weigth_vul_delivery + weight_vul_35 #kg
            gravity = 9.81 #m/s^2
            area_front_vul = 6.31 #m^2
            Density_wind = 1.225 #kg/m^3
            cd = 0.1 # drag coefficient
            b1 = (crr*sum_weight_vul*gravity)/1000 # rolling resistance force kN
            VUL = 2.7 #kg éq. CO2/litre

            b2 = []
            for n in range(len(df_geo_task)):
                list_cell = df_geo_task.at[n, 'speeds_driving']
                b2_value = []
                if isinstance(list_cell, list):
                    for i in range(len(list_cell)):
                        speed_value = list_cell[i]
                        if speed_value is not None:
                            b2_value.append((0.5 * Density_wind * area_front_vul * speed_value * cd) / 1000)
                        else:
                            b2_value.append(None)  # You can choose to keep None if needed
                else:
                    if list_cell is not None:
                        b2_value.append((0.5 * Density_wind * area_front_vul * list_cell * cd) / 1000)
                    else:
                        b2_value.append(None)  # You can choose to keep None if needed   
                b2.append(b2_value)


            rt = []
            for n in range(len(df_geo_task)):
                list_cell = df_geo_task.at[n, 'acceleration_driving']
                list_cell2 = df_geo_task.at[n, 'speeds_driving']
                rt_ap = []
                if isinstance(list_cell, list) and isinstance(list_cell2, list):
                    for i in range(len(list_cell)):
                        b2_list = b2[n]
                        if isinstance(list_cell2[i], (int, float)) and isinstance(list_cell[i], (int, float)):
                            rt_value = b1 +  b2_list[i] * (list_cell2[i] ** 2) + ((sum_weight_vul * list_cell[i])/1000) + ((gravity * sum_weight_vul * df_geo_task['inclination'][n])/100000)
                            rt_ap.append(rt_value)
                else:
                    b2_list = b2[n]
                    if isinstance(list_cell2, (int, float)) and isinstance(list_cell, (int, float)):
                        rt_value = b1 + b2_list * (list_cell2 ** 2) + ((sum_weight_vul * list_cell)/1000) + ((gravity * sum_weight_vul * df_geo_task['inclination'][n]) / 100000)
                        rt_ap.append(rt_value)
                rt.append(rt_ap)


            for n in range(len(rt)):
                if not rt[n]:  # Check if the list at index n is empty
                    rt[n] = [0]  # Replace the empty list with a list containing a single zero

            ft = []
            for n in range(len(rt)):
                list_cell = rt[n]
                list_cell2 = df_geo_task.at[n, 'acceleration_driving']
                list_cell3 = df_geo_task.at[n, 'speeds_driving']
                list_cell4 = df_geo_task.at[n, 'durations_driving']
                ft_value = []
                if isinstance(list_cell2,list) and isinstance(list_cell,list):
                    for i in range(len(list_cell2)):
                        if list_cell[i] <= 0:
                            ft_value.append((alpha_vul/1000)*list_cell4[i])
                        else:
                            ft_value.append(((alpha_vul + beta_1_vul_diseal * list_cell[i] * list_cell3[i] + (beta_2_vul_diseal * sum_weight_vul * (list_cell2[i]** 2) * list_cell3[i]) / 1000)* list_cell4[i])/1000 )
                    ft.append(ft_value)
                else: 
                    if list_cell <=0: 
                        ft_value.append((alpha_vul/1000)*list_cell4)
                    else: 
                        ft_value.append(((alpha_vul + beta_1_vul_diseal * list_cell * list_cell3 + (beta_2_vul_diseal * sum_weight_vul * (list_cell2 ** 2) * list_cell3) / 1000)* list_cell4)/1000 )
                    ft.append(ft_value)

            FT = []
            for sublist in ft:
                ft_sum = sum(sublist)
                FT.append(ft_sum)

            CO2_driving = []
            for i in range(len(FT)):
                CO2_driving.append(FT[i]*VUL)
                
            # Vule and electric bicycle 
            # https://base-empreinte.ademe.fr/donnees/jeu-donnees * 
            
            cof = 0.0041*88
            load_velo = 180*0.35 #kg
            weight_velo = 24 #kg
            sum_weight_velo =  weigth_vul_delivery + load_velo + weight_velo
            new_cof = cof/ sum_weight_velo
            velo = 0.0520 # kg éq. CO2/kWh

            df_geo_task['totalDistance_cycling'] = df_geo_task['distances_cycling_copy'].apply(sum)

            # The inclination here is not the same that above
            df_geo_task['inclination_cycling'] = 0

            mask = (df_geo_task['pickUpPoint_altitudes'] == 0) | (df_geo_task['deliveryPoint_altitudes'] == 0)
            df_geo_task.loc[mask, 'inclination_cycling'] = df_geo_task['pickUpPoint_altitudes'] + df_geo_task['deliveryPoint_altitudes']

            mask = ~mask
            df_geo_task.loc[mask,'inclination_cycling'] = ((df_geo_task['deliveryPoint_altitudes'] - df_geo_task['pickUpPoint_altitudes']) / df_geo_task['totalDistance_cycling'])

            BSP = []
            for n in range(len(df_geo_task)):
                list_cell = df_geo_task.at[n, 'acceleration_cycling']
                list_cell2 = df_geo_task.at[n, 'speeds_cycling_copy']
                list_cell3 = df_geo_task.at[n,'durations_cycling_copy']
                BSP_ap = []
                if isinstance(list_cell, list) and isinstance(list_cell2, list):
                    for i in range(len(list_cell)):
                        inclination = df_geo_task.at[n, 'inclination_cycling']
                        if isinstance(list_cell2[i], (int, float)) and isinstance(list_cell[i], (int, float)):
                            BSP_value = list_cell2[i] * (1.01 * list_cell[i] + 9.81 * np.sin(inclination) + 0.078) + new_cof * (list_cell2[i] ** 3)
                            BSP_value = BSP_value*sum_weight_velo*list_cell3[i]/1000
                            BSP_ap.append(BSP_value)
                else:
                    inclination = df_geo_task.at[n, 'inclination_cycling']
                    if isinstance(list_cell2, (int, float)) and isinstance(list_cell, (int, float)):
                        BSP_value = list_cell2 * (1.01 * list_cell + 9.81 * np.sin(inclination) + 0.078) + new_cof * (list_cell2 ** 3)
                        BSP_value = BSP_value*sum_weight_velo*list_cell3/1000 
                        BSP_ap.append(BSP_value)
                BSP.append(BSP_ap) # kWs

           

            for i in range(len(BSP)):
                if not BSP[i]: 
                    BSP[i] = [0]

            for i in range(len(BSP)):
                for j in range(len(BSP[i])):
                    if BSP[i][j] < 0:
                        BSP[i][j] = 0

            BSP_total = []
            for sublist in BSP:
                BSP_sum = sum(sublist)/3600
                BSP_total.append(BSP_sum) # kWs

            CO2_cycling = [bsp * velo for bsp in BSP_total] # C02 ADEME kWh france

            #### VSP
            new_cof2 = 0.00302
            deki_vul = 0.0520 # kg éq. CO2/kWh

            VSP = []
            for n in range(len(df_geo_task)):
                list_cell = df_geo_task.at[n, 'acceleration_driving']
                list_cell2 = df_geo_task.at[n, 'speeds_driving']
                list_cell3 = df_geo_task.at[n,'durations_driving']
                VSP_ap = []
                if isinstance(list_cell, list) and isinstance(list_cell2, list):
                    for i in range(len(list_cell)):
                        inclination = df_geo_task.at[n, 'inclination']
                        if isinstance(list_cell2[i], (int, float)) and isinstance(list_cell[i], (int, float)):
                            VSP_value = list_cell2[i] * (1.1 * list_cell[i] + 9.81 * np.sin(inclination) + 0.132)+ new_cof2 * (list_cell2[i] ** 3)
                            VSP_value = VSP_value*sum_weight_vul*list_cell3[i]/1000
                            VSP_ap.append(VSP_value)
                else:
                    inclination = df_geo_task.at[n, 'inclination']
                    if isinstance(list_cell2, (int, float)) and isinstance(list_cell, (int, float)):
                        VSP_value = list_cell2 * (1.1 * list_cell + 9.81 * np.sin(inclination) + 0.132)+ new_cof2 * (list_cell2 ** 3)
                        VSP_value = VSP_value*sum_weight_vul*list_cell3/1000 
                        VSP_ap.append(VSP_value)
                VSP.append(VSP_ap)
                
            for i in range(len(VSP)):
                if not VSP[i]: 
                    VSP[i] = [0]

            for i in range(len(VSP)):
                for j in range(len(VSP[i])):
                    if VSP[i][j] < 0:
                        VSP[i][j] = 0
                        
            VSP_total = []
            for sublist in VSP:
                VSP_sum = sum(sublist)/3600
                VSP_total.append(VSP_sum) 
                
            CO2_deki_vul = [vsp * deki_vul for vsp in VSP_total] # C02 ADEME kWh france
        
            # Final step for CO2 saved 
            CO2_driving_total = sum(CO2_driving)
            CO2_cycling_total =  sum(CO2_cycling)
            CO2_deki_vul_total = sum(CO2_deki_vul)
            if CO2_driving_total != 0:
                emi = round(((CO2_driving_total - CO2_cycling_total) / CO2_driving_total) * 100, 2)
            else:
                emi = 0 
            emi_total = (round(CO2_driving_total - CO2_cycling_total, 2))
            result = (emi,emi_total,round(CO2_driving_total,2),round(CO2_cycling_total,2),round(CO2_deki_vul_total,2))

    # save the result in cache
    cache.set(cache_key, result, timeout= 36000)
    return result

def eco_km(stored_selected_date, selected_city, newuser=None ): 

    cache_key = f'eco_km_result{stored_selected_date}_{newuser}_{selected_city}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        #charger the data
        df_geo_task = get_data_cydi()
        df = get_data_id()
        df_merchants = get_data_merchants()

        if stored_selected_date is not None:
            st, en = stored_selected_date.strip('()[]').split(' to ')
            st = pd.to_datetime(st, format='%d/%m/%Y')
            en = pd.to_datetime(en, format='%d/%m/%Y')
            st = st.tz_localize(df_geo_task['end_date'].dt.tz)
            en = en.tz_localize(df_geo_task['end_date'].dt.tz)
            df_geo_task = df_geo_task[(df_geo_task['end_date'] >= st) & (df_geo_task['end_date'] <= en)]
        else: 
            df_geo_task=df_geo_task
        
        if selected_city is not None:

            def city_to_id(selected_city):
                city_mapping = {
                    'marseille': '13',
                    'lyon': '69',
                    'lille': '59',
                    'paris': '75',
                    'bordeaux': '33',
                    'toulouse': '31',
                    'dijon': '21',  # Ensure 'dijon' is lowercase for consistency
                }
                return [city_mapping.get(city.lower(), None) for city in selected_city]
            
            city_id = city_to_id(selected_city)

            df_geo_task = df_geo_task[df_geo_task['id_city'].isin(city_id)]
        else: 
            df_geo_task=df_geo_task

        if newuser is not None:
            if newuser == 'group_id=1' or newuser == 1:
                merchant_trd = df_merchants[df_merchants['group_0_id'] == 1]
                merchant_trd = merchant_trd[['id']]
                merchant_trd_ids = merchant_trd['id'].tolist()
                df = df[df['merchant_id_course'].isin(merchant_trd_ids)]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=2' or newuser == 2:
                df = df[df['team_id'] == 2]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=3' or newuser == 3:
                df = df[df['team_id'] == 3]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=4' or newuser == 4:
                df = df[df['team_id'] == 4]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=6' or newuser == 6:
                df = df[df['team_id'] == 6]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=9' or newuser == 9:
                df = df[df['team_id'] == 9]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=10' or newuser == 10:
                df = df[df['team_id'] == 10]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=11' or newuser == 11:
                df = df[df['team_id'] == 11]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=13' or newuser == 13:
                df = df[df['team_id'] == 13]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=14' or newuser == 14:
                df = df[df['team_id'] == 14]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=15' or newuser == 15:
                df = df[df['team_id'] == 15]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=16' or newuser == 16:
                df = df[df['team_id'] == 16]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=17' or newuser == 17:
                df = df[df['team_id'] == 17]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=18' or newuser == 18:
                df = df[df['team_id'] == 18]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=19' or newuser == 19:
                df = df[df['team_id'] == 19]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=20' or newuser == 20:
                df = df[df['team_id'] == 20]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=22' or newuser == 22:
                df = df[df['team_id'] == 22]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=606' or newuser == 606:
                df = df[df['merchant_id_course'] == 606]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=605' or newuser == 605:
                df = df[df['merchant_id_course'] == 605]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=607' or newuser == 607:
                df = df[df['merchant_id_course'] == 607]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=609' or newuser == 609:
                df = df[df['merchant_id_course'] == 609]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=610' or newuser == 610:
                df = df[df['merchant_id_course'] == 610]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=617' or newuser == 617:
                df = df[df['merchant_id_course'] == 617]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=630' or newuser == 630:
                df = df[df['merchant_id_course'] == 630]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=635' or newuser == 635:
                df = df[df['merchant_id_course'] == 635]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=640' or newuser == 640:
                df = df[df['merchant_id_course'] == 640]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=641' or newuser == 641:
                df = df[df['merchant_id_course'] == 641]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=649' or newuser == 649:
                df = df[df['merchant_id_course'] == 649]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=650' or newuser == 650:
                df = df[df['merchant_id_course'] == 650]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=651' or newuser == 651:
                df = df[df['merchant_id_course'] == 651]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=652' or newuser == 652:
                df = df[df['merchant_id_course'] == 652]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            else:
                df_geo_task = pd.DataFrame(columns=df_geo_task.columns)
        else: 
            df_geo_task=df_geo_task
            
        if df_geo_task.empty:
            km_saved = 0    
            km_saved_total= 0
            distance_cycling  = 0  
            distance_driving = 0  
            mean_cycling = 0
        else:
            df_geo_task['totalDistance_cycling'] = df_geo_task['distances_cycling_copy'].apply(sum) 

            distance_cycling = df_geo_task['totalDistance_cycling'].sum()/1000
            distance_driving = df_geo_task['totalDistance_driving'].sum()/1000
            mean_cycling = df_geo_task['totalDistance_cycling'].mean()/1000

            # calculate the km saved by cycling instead of driving
            if distance_driving > 0:
                km_saved = round(((distance_driving - distance_cycling) / distance_driving) * 100, 2)
            else:
                km_saved = 0
            km_saved_total = round(distance_driving - distance_cycling, 2)
        result = (km_saved, km_saved_total, round(distance_cycling), round(distance_driving), round(mean_cycling ))

    # save the result in cache
    cache.set(cache_key , result, timeout= 39020)
    return result

def time_eco(stored_selected_date, selected_city, newuser=None): 
    cache.delete(f'time_eco_result{stored_selected_date}_{newuser}_{selected_city}')
    cache_key = f'time_eco_result{stored_selected_date}_{newuser}_{selected_city}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        #charger the data
        df_geo_task = get_data_cydi()
        df = get_data_id()
        df_merchants = get_data_merchants()

        if stored_selected_date is not None:
            st, en = stored_selected_date.strip('()[]').split(' to ')
            st = pd.to_datetime(st, format='%d/%m/%Y')
            en = pd.to_datetime(en, format='%d/%m/%Y')
            st = st.tz_localize(df_geo_task['end_date'].dt.tz)
            en = en.tz_localize(df_geo_task['end_date'].dt.tz)
            df_geo_task = df_geo_task[(df_geo_task['end_date'] >= st) & (df_geo_task['end_date'] <= en)]
        else: 
            df_geo_task=df_geo_task
        
        if selected_city is not None:

            def city_to_id(selected_city):
                city_mapping = {
                    'marseille': '13',
                    'lyon': '69',
                    'lille': '59',
                    'paris': '75',
                    'bordeaux': '33',
                    'toulouse': '31',
                    'dijon': '21',  # Ensure 'dijon' is lowercase for consistency
                }
                return [city_mapping.get(city.lower(), None) for city in selected_city]
            
            city_id = city_to_id(selected_city)

            df_geo_task = df_geo_task[df_geo_task['id_city'].isin(city_id)]
        else: 
            df_geo_task=df_geo_task
        
        if newuser is not None:
            if newuser == 'group_id=1' or newuser == 1:
                merchant_trd = df_merchants[df_merchants['group_0_id'] == 1]
                merchant_trd = merchant_trd[['id']]
                merchant_trd_ids = merchant_trd['id'].tolist()
                df = df[df['merchant_id_course'].isin(merchant_trd_ids)]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=2' or newuser == 2:
                df = df[df['team_id'] == 2]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=3'or newuser == 3:
                df = df[df['team_id'] == 3]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=4' or newuser == 4:
                df = df[df['team_id'] == 4]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=6' or newuser == 6:
                df = df[df['team_id'] == 6]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=9' or newuser == 9:
                df = df[df['team_id'] == 9]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=10' or newuser == 10:
                df = df[df['team_id'] == 10]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=11' or newuser == 11:
                df = df[df['team_id'] == 11]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=13' or newuser == 13:
                df = df[df['team_id'] == 13]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=14'or newuser == 14:
                df = df[df['team_id'] == 14]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=15'or newuser == 15:
                df = df[df['team_id'] == 15]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=16' or newuser == 16:
                df = df[df['team_id'] == 16]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=17' or newuser == 17:
                df = df[df['team_id'] == 17]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=18' or newuser == 18:
                df = df[df['team_id'] == 18]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=19' or newuser == 19:
                df = df[df['team_id'] == 19]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=20' or newuser == 20:
                df = df[df['team_id'] == 20]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=22' or newuser == 21:
                df = df[df['team_id'] == 22]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=606' or newuser == 606:
                df = df[df['merchant_id_course'] == 606]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=605' or newuser == 605:
                df = df[df['merchant_id_course'] == 605]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=607' or newuser == 607:
                df = df[df['merchant_id_course'] == 607]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=609' or newuser == 609:
                df = df[df['merchant_id_course'] == 609]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=610' or newuser == 610:
                df = df[df['merchant_id_course'] == 610]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=617' or newuser == 617:
                df = df[df['merchant_id_course'] == 617]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=630' or newuser == 630:
                df = df[df['merchant_id_course'] == 630]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=635' or newuser == 635:
                df = df[df['merchant_id_course'] == 635]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=640' or newuser == 640:
                df = df[df['merchant_id_course'] == 640]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=641' or newuser == 641:
                df = df[df['merchant_id_course'] == 641]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=649' or newuser == 649:
                df = df[df['merchant_id_course'] == 649]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=650' or newuser == 650:
                df = df[df['merchant_id_course'] == 650]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=651' or newuser == 651:
                df = df[df['merchant_id_course'] == 651]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=652' or newuser == 652:
                df = df[df['merchant_id_course'] == 652]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            else:
                df_geo_task = pd.DataFrame(columns=df_geo_task.columns)
        else: 
            df_geo_task=df_geo_task
            
        if df_geo_task.empty:
            time_saved = 0     
            time_saved_total= 0
            time_cycling = 0
            time_driving = 0
            media_time_cycling = 0
            result = (time_saved, time_saved_total,time_cycling,time_driving, media_time_cycling )      
        else:
            # summ the total time for cycling and driving
            df_geo_task['durations_cycling_copy'] = df_geo_task['durations_cycling_copy'].apply(lambda x: [x] if isinstance(x, int) else x)
            df_geo_task['durations_driving'] = df_geo_task['durations_driving'].apply(lambda x: [x] if isinstance(x, int) else x)
            time_cycling = sum(val for sublist in df_geo_task['durations_cycling_copy'] if isinstance(sublist, list) for val in sublist)
            time_driving = sum(val for sublist in df_geo_task['durations_driving'] if isinstance(sublist, list) for val in sublist)
            rounded_time_cycling = round(time_cycling/3600)

            # calculate the time saved by cycling instead of driving
            if time_driving > 0:
                time_saved = round(((time_driving - time_cycling) / time_driving) * 100, 2)
            else:
                time_saved = 0 
            time_saved_total = round((round(time_driving - time_cycling, 2))/3600,2)

            def sum_list(sublist):
                if isinstance(sublist, list):
                    return sum(sublist)
                return 0  

            df_geo_task['sum_of_durations'] = df_geo_task['durations_cycling_copy'].apply(sum_list)

            media_time_cycling = round(df_geo_task['sum_of_durations'].mean()/60)

            result = (time_saved, time_saved_total, rounded_time_cycling , round(time_driving/3600), media_time_cycling )

    # save the result in cache
    cache.set(cache_key , result, timeout= 38020 )
    return result

def graph_CO2(stored_selected_date, selected_city, newuser=None):

    cache_key = f'graph_CO2{stored_selected_date}_{newuser}_{selected_city}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:      
        #charger the data
        df_geo_task = get_data_cydi()
        df = get_data_id()
        df_merchants = get_data_merchants()

        if stored_selected_date is not None:
            st, en = stored_selected_date.strip('()[]').split(' to ')
            st = pd.to_datetime(st, format='%d/%m/%Y')
            en = pd.to_datetime(en, format='%d/%m/%Y')
            st = st.tz_localize(df_geo_task['end_date'].dt.tz)
            en = en.tz_localize(df_geo_task['end_date'].dt.tz)
            df_geo_task = df_geo_task[(df_geo_task['end_date'] >= st) & (df_geo_task['end_date'] <= en)]
        else: 
            df_geo_task=df_geo_task

        
        if selected_city is not None:

            def city_to_id(selected_city):
                city_mapping = {
                    'marseille': '13',
                    'lyon': '69',
                    'lille': '59',
                    'paris': '75',
                    'bordeaux': '33',
                    'toulouse': '31',
                    'dijon': '21',  # Ensure 'dijon' is lowercase for consistency
                }
                return [city_mapping.get(city.lower(), None) for city in selected_city]
            
            city_id = city_to_id(selected_city)

            df_geo_task = df_geo_task[df_geo_task['id_city'].isin(city_id)]
        else: 
            df_geo_task=df_geo_task    

        if newuser is not None:
            CO2_fun = CO2(stored_selected_date,selected_city, newuser)
            emi,emi_total,driving,cycling,deki_vul  = CO2_fun
            if newuser == 'group_id=1'or newuser == 1:
                merchant_trd = df_merchants[df_merchants['group_0_id'] == 1]
                merchant_trd = merchant_trd[['id']]
                merchant_trd_ids = merchant_trd['id'].tolist()
                df = df[df['merchant_id_course'].isin(merchant_trd_ids)]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=2' or newuser == 2:
                df = df[df['team_id'] == 2]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=3' or newuser == 3:
                df = df[df['team_id'] == 3]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=4' or newuser == 4:
                df = df[df['team_id'] == 4]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=6' or newuser == 6:
                df = df[df['team_id'] == 6]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=9' or newuser == 9:
                df = df[df['team_id'] == 9]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=10' or newuser == 10:
                df = df[df['team_id'] == 10]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=11' or newuser == 11:
                df = df[df['team_id'] == 11]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=13' or newuser == 13 :
                df = df[df['team_id'] == 13]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=14' or newuser == 14:
                df = df[df['team_id'] == 14]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=15' or newuser == 15 :
                df = df[df['team_id'] == 15]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=16' or newuser == 16:
                df = df[df['team_id'] == 16]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=17' or newuser == 17:
                df = df[df['team_id'] == 17]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=18' or newuser == 18:
                df = df[df['team_id'] == 18]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=19' or newuser == 19:
                df = df[df['team_id'] == 19]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=20' or newuser == 20 :
                df = df[df['team_id'] == 20]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=22' or newuser == 22 :
                df = df[df['team_id'] == 22]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=606' or newuser == 606:
                df = df[df['merchant_id_course'] == 606]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=605' or newuser == 605 :
                df = df[df['merchant_id_course'] == 605]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=607' or newuser == 607 :
                df = df[df['merchant_id_course'] == 607]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=609' or newuser == 609 :
                df = df[df['merchant_id_course'] == 609]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=610' or newuser == 610 :
                df = df[df['merchant_id_course'] == 610]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=617' or newuser == 617:
                df = df[df['merchant_id_course'] == 617]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=630' or newuser == 630:
                df = df[df['merchant_id_course'] == 630]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=635' or newuser == 635:
                df = df[df['merchant_id_course'] == 635]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=640' or newuser == 640:
                df = df[df['merchant_id_course'] == 640]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=641'or newuser == 641:
                df = df[df['merchant_id_course'] == 641]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=649' or newuser == 649:
                df = df[df['merchant_id_course'] == 649]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=650' or newuser == 650 :
                df = df[df['merchant_id_course'] == 650]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=651' or newuser == 651 :
                df = df[df['merchant_id_course'] == 651]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=652' or newuser == 652 :
                df = df[df['merchant_id_course'] == 652]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            else:
                df_geo_task = pd.DataFrame(columns=df_geo_task.columns)
        else: 
            df_geo_task=df_geo_task
            CO2_fun = CO2(stored_selected_date, selected_city)
            emi,emi_total,driving,cycling,deki_vul  = CO2_fun
            
        if df_geo_task.empty:
            VUL_met = 0
            VUL_no2 = 0
            VUL_NOx = 0
            VUL_CO = 0
            VUL_PM = 0

            deki_met = 0
            deki_no2 = 0
            deki_NOx = 0
            deki_CO = 0
            deki_PM = 0
            
            deki_vul_met = 0
            deki_vul_no2 = 0
            deki_vul_NOx = 0 
            deki_vul_CO = 0
            deki_vul_PM = 0
            
            result = (VUL_met, VUL_no2, VUL_NOx, VUL_CO, VUL_PM,deki_met, deki_no2,deki_NOx,deki_CO, deki_PM,deki_vul_met,deki_vul_no2,deki_vul_NOx,deki_vul_CO,deki_vul_PM)        
        else:
            
            df_geo_task['totalDistance_cycling'] = df_geo_task['distances_cycling_copy'].apply(sum) 
            distance_cycling = df_geo_task['totalDistance_cycling'].sum()/1000
            distance_driving = df_geo_task['totalDistance_driving'].sum()/1000

            VUL = 2.7 #kg éq. CO2/litre
            ener = 0.0520 
            driving =  driving/ VUL * 0.89 # kg
            cycling = cycling/ener
            deki_vul = deki_vul/ener
            CH4 = 0.365 # g  CH4/kg             
            N2O = 0.056 # g  N2O/kg
            NOx = 14.91 # g NOx/kg
            CO = 7.4 # g CO/kg
            PM = 0.0009 # g PM/km

            # https://ww2.arb.ca.gov/sites/default/files/classic/cc/inventory/pubs/reports/2000_2014/ghg_inventory_00-14_technical_support_document.pdf *
            N2OP =  0.0007518 #g / kWh
            NOxP = 420/1000 #Kg / kWH
            # The French electricity grid only produces gases and pollutants related to power plants, and other renewable sources


            VUL_met = round(driving*CH4,2)
            VUL_no2 = round(driving*N2O,2)
            VUL_NOx = round(driving*NOx,2)
            VUL_CO = round(driving*CO,2)
            VUL_PM = round(distance_driving*PM,2)

            deki_met = round(0,2)
            deki_no2 = round(cycling*N2OP,2)
            deki_NOx = round(cycling*NOxP,2)
            deki_CO = round(0,2)
            deki_PM = round(distance_cycling*PM,2)
            
            deki_vul_met = round(0,2)
            deki_vul_no2 = round(deki_vul*N2OP,2)
            deki_vul_NOx = round(deki_vul*NOxP,2)
            deki_vul_CO = round(0,2)
            deki_vul_PM = round(distance_driving*PM,2)

            result = (VUL_met, VUL_no2, VUL_NOx, VUL_CO, VUL_PM,deki_met, deki_no2,deki_NOx,deki_CO, deki_PM,deki_vul_met,deki_vul_no2,deki_vul_NOx,deki_vul_CO,deki_vul_PM)      
            
    # save the result in cache
    cache.set(cache_key , result, timeout= 38020 )
    return result

def equivalence(stored_selected_date, selected_city,newuser=None): 

    cache_key = f'equivalence{stored_selected_date}_{newuser}_{selected_city}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        if newuser is not None:
            emi,emi_total,driving,cycling,deki_vul = CO2(stored_selected_date, selected_city,newuser)
        else:
            emi,emi_total,driving,cycling,deki_vul = CO2(stored_selected_date, selected_city)

        if emi_total == 'non calculable': 
            charger_iphone = 'non calculable'
            charger_mac = 'non calculable'
            trees = 'non calculable'
            train = 'non calculable'
            diesel = 'non calculable'
            uber = 'non calculable'
            print_sheet = 'non calculable'
            emails = 'non calculable'
            labor = 'non calculable'
            water = 'non calculable'
            pain = 'non calculable'
            fromage = 'non calculable'
        else: 
            battery_iphone = 3279 #mAh
            battery_mac = 0.05753 # kWh
            tension_iphone = 5 
            f_iphone = 0.052 # kg eq. CO2/kWh
            f_mac = 0.052 # kg eq. CO2/kWh
            cp_iphone = (battery_iphone*tension_iphone)/1000000
            f_trees = -0.00416
            distance_train =  660 # km Paris - Marseille
            f_train = 0.00334 # kg eq. CO2/passager*km
            f_diesel = 2.7 #kg éq. CO2/litre
            f_uber = 1.02 # kg éq. CO2/repas
            f_print = 0.01022 # kg éq. CO2 / feuille
            f_emails = 0.004 # kg éq. CO2/unité
            f_labor = 6.19 # kg CO2/jour
            f_water = 0.268 # kg éq. CO2/kg de poids net
            f_pain = 0.00152 # kg éq. CO2/g
            f_fromage = 0.00494 # kg éq. CO2/g

            charger_iphone = round(emi_total/(f_iphone*cp_iphone))
            charger_mac = round(emi_total/(battery_mac*f_mac))
            trees = round(emi_total/f_trees * (-1))
            train = round(emi_total/(f_train * distance_train))
            diesel = round(emi_total/f_diesel)
            uber =  round(emi_total/f_uber)
            print_sheet = round(emi_total/f_print)
            emails = round(emi_total/f_emails)
            labor = round(emi_total/f_labor)
            water = round(emi_total/f_water)
            pain = round(emi_total/f_pain)
            fromage = round(emi_total/f_fromage)
        result = (charger_iphone,charger_mac,trees,train,diesel,uber,print_sheet,emails,labor,water,pain,fromage)
            

    # save the result in cache
    cache.set(cache_key , result, timeout= 37000 )
    return result

def space_eco(stored_selected_date, selected_city, newuser=None): 

    cache_key = f'space_eco{stored_selected_date}_{newuser}_{selected_city}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        #charger the data
        df_geo_task = get_data_cydi()
        df = get_data_id()
        df_merchants = get_data_merchants()

        if stored_selected_date is not None:
            st, en = stored_selected_date.strip('()[]').split(' to ')
            st = pd.to_datetime(st, format='%d/%m/%Y')
            en = pd.to_datetime(en, format='%d/%m/%Y')
            st = st.tz_localize(df_geo_task['end_date'].dt.tz)
            en = en.tz_localize(df_geo_task['end_date'].dt.tz)
            df_geo_task = df_geo_task[(df_geo_task['end_date'] >= st) & (df_geo_task['end_date'] <= en)]
        else: 
            df_geo_task=df_geo_task
        
        if selected_city is not None:

            def city_to_id(selected_city):
                city_mapping = {
                    'marseille': '13',
                    'lyon': '69',
                    'lille': '59',
                    'paris': '75',
                    'bordeaux': '33',
                    'toulouse': '31',
                    'dijon': '21',  # Ensure 'dijon' is lowercase for consistency
                }
                return [city_mapping.get(city.lower(), None) for city in selected_city]
            
            city_id = city_to_id(selected_city)

            df_geo_task = df_geo_task[df_geo_task['id_city'].isin(city_id)]
        else: 
            df_geo_task=df_geo_task    

        if newuser is not None:
            if newuser == 'group_id=1' or newuser == 1:
                merchant_trd = df_merchants[df_merchants['group_0_id'] == 1]
                merchant_trd = merchant_trd[['id']]
                merchant_trd_ids = merchant_trd['id'].tolist()
                df = df[df['merchant_id_course'].isin(merchant_trd_ids)]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=2' or newuser == 2:
                df = df[df['team_id'] == 2]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=3' or newuser == 3:
                df = df[df['team_id'] == 3]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=4' or newuser == 4:
                df = df[df['team_id'] == 4]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=6' or newuser == 6:
                df = df[df['team_id'] == 6]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=9' or newuser == 9:
                df = df[df['team_id'] == 9]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=10' or newuser == 10:
                df = df[df['team_id'] == 10]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=11' or newuser == 11:
                df = df[df['team_id'] == 11]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=13' or newuser == 13:
                df = df[df['team_id'] == 13]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=14' or newuser == 14:
                df = df[df['team_id'] == 14]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=15' or newuser == 15:
                df = df[df['team_id'] == 15]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=16' or newuser == 16:
                df = df[df['team_id'] == 16]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=17' or newuser == 17:
                df = df[df['team_id'] == 17]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=18' or newuser == 18:
                df = df[df['team_id'] == 18]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=19' or newuser == 19:
                df = df[df['team_id'] == 19]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=20' or newuser == 20:
                df = df[df['team_id'] == 20]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'team_id=22' or newuser == 22:
                df = df[df['team_id'] == 22]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=606' or newuser == 606:
                df = df[df['merchant_id_course'] == 606]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=605' or newuser == 605:
                df = df[df['merchant_id_course'] == 605]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=607' or newuser == 607:
                df = df[df['merchant_id_course'] == 607]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=609' or newuser == 609:
                df = df[df['merchant_id_course'] == 609]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=610' or newuser == 610:
                df = df[df['merchant_id_course'] == 610]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=617' or newuser == 617:
                df = df[df['merchant_id_course'] == 617]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=630' or newuser == 630:
                df = df[df['merchant_id_course'] == 630]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=635' or newuser == 635:
                df = df[df['merchant_id_course'] == 635]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=640' or newuser == 640:
                df = df[df['merchant_id_course'] == 640]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=641' or newuser == 641:
                df = df[df['merchant_id_course'] == 641]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=649' or newuser == 649:
                df = df[df['merchant_id_course'] == 649]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=650' or newuser == 650:
                df = df[df['merchant_id_course'] == 650]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=651' or newuser == 651:
                df = df[df['merchant_id_course'] == 651]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            elif newuser == 'merchant_id=652' or newuser == 652:
                df = df[df['merchant_id_course'] == 652]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
            else:
                df_geo_task = pd.DataFrame(columns=df_geo_task.columns)
        else: 
            df_geo_task=df_geo_task
            
        if df_geo_task.empty:
            SC_s = 'non calculable'    
            SC_vul = 'non calculable'   
            SC_deki = 'non calculable'   
            result = (SC_s,SC_vul,SC_deki)     
        else:
            # summ the total time for cycling and driving
            df_geo_task['durations_cycling_copy'] = df_geo_task['durations_cycling_copy'].apply(lambda x: [x] if isinstance(x, int) else x)
            df_geo_task['durations_driving'] = df_geo_task['durations_driving'].apply(lambda x: [x] if isinstance(x, int) else x)
            time_cycling = sum(val for sublist in df_geo_task['durations_cycling_copy'] if isinstance(sublist, list) for val in sublist)
            time_driving = sum(val for sublist in df_geo_task['durations_driving'] if isinstance(sublist, list) for val in sublist) 

            time_cycling = time_cycling/3600
            time_driving = time_driving/3600

            SC_vul = 89.6 #m2/h
            SC_velo = 25.3 #m2/h
            
            SC_s = round(time_cycling*(SC_vul-SC_velo),0)
            SC_vul = round(SC_vul*time_driving,0)
            SC_deki = round(SC_velo*time_cycling,0)
            
            result = (SC_s,SC_vul,SC_deki)
            
    # save the result in cache
    cache.set(cache_key , result, timeout= 33444 )
    return result

def KPI_CO2(stored_selected_date,selected_city ,newuser=None): 
    cache.delete(f'KPI_CO2{stored_selected_date}_{newuser}_{selected_city}')
    cache_key = f'KPI_CO2{stored_selected_date}_{newuser}_{selected_city}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        #charger the data
        df_geo_task = get_data_cydi()
        df_packages =  get_data_livra()
        df = get_data_id()
        df_merchants = get_data_merchants()


        if stored_selected_date is not None:
            st, en = stored_selected_date.strip('()[]').split(' to ')
            st = pd.to_datetime(st, format='%d/%m/%Y')
            en = pd.to_datetime(en, format='%d/%m/%Y')
            st = st.tz_localize(df_geo_task['end_date'].dt.tz)
            en = en.tz_localize(df_geo_task['end_date'].dt.tz)
            df_geo_task = df_geo_task[(df_geo_task['end_date'] >= st) & (df_geo_task['end_date'] <= en)]
            df_packages = df_packages[(df_packages['created_at'] >= st) & (df_packages['created_at'] <= en)]
            df = df[(df['end_date'] >= st) & (df['end_date'] <= en)]
        else: 
            df_geo_task=df_geo_task
            df_packages = df_packages
            df=df

        if selected_city is not None:

            def city_to_id(selected_city):
                city_mapping = {
                    'marseille': '13',
                    'lyon': '69',
                    'lille': '59',
                    'paris': '75',
                    'bordeaux': '33',
                    'toulouse': '31',
                    'dijon': '21',  # Ensure 'dijon' is lowercase for consistency
                }
                return [city_mapping.get(city.lower(), None) for city in selected_city]
            
            city_id = city_to_id(selected_city)

            df_geo_task = df_geo_task[df_geo_task['id_city'].isin(city_id)]
            id_f_task = df_geo_task['id']
            df = df[df['id_task'].isin(id_f_task)]
            df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
        else: 
            df_geo_task=df_geo_task   
            df_packages = df_packages 
            df=df 
        
        if newuser is not None:
            emi,emi_total,driving,cycling,deki_vul = CO2(stored_selected_date, selected_city ,newuser)
            num_delivery_result = num_delivery(stored_selected_date,selected_city,newuser)
            km_saved, km_saved_total, driving, l,m = eco_km(stored_selected_date,selected_city , newuser)
            time_saved, time_saved_total, d, c, f = time_eco(stored_selected_date, selected_city , newuser)
            SC_s,SC_vul,SC_deki = space_eco(stored_selected_date, selected_city ,newuser)
            if newuser == 'group_id=1' or newuser == 1:
                merchant_trd = df_merchants[df_merchants['group_0_id'] == 1]
                merchant_trd = merchant_trd[['id']]
                merchant_trd_ids = merchant_trd['id'].tolist()
                df = df[df['merchant_id_course'].isin(merchant_trd_ids)]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)] 
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=2' or newuser == 2:
                df = df[df['team_id'] == 2]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=3' or newuser == 3:
                df = df[df['team_id'] == 3]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=4' or newuser == 4:
                df = df[df['team_id'] == 4]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=6' or newuser == 6:
                df = df[df['team_id'] == 6]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=9' or newuser == 9:
                df = df[df['team_id'] == 9]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=10' or newuser == 10:
                df = df[df['team_id'] == 10]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=11' or newuser == 11:
                df = df[df['team_id'] == 11]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=13' or newuser == 13:
                df = df[df['team_id'] == 13]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=14' or newuser == 14:
                df = df[df['team_id'] == 14]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=15' or newuser == 15:
                df = df[df['team_id'] == 15]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=16' or newuser == 16:
                df = df[df['team_id'] == 16]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=17' or newuser == 17:
                df = df[df['team_id'] == 17]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=18' or newuser == 18:
                df = df[df['team_id'] == 18]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=19' or newuser == 19:
                df = df[df['team_id'] == 19]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=20' or newuser == 20:
                df = df[df['team_id'] == 20]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'team_id=22' or newuser == 22:
                df = df[df['team_id'] == 22]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=606' or newuser == 606:
                df = df[df['merchant_id_course'] == 606]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=605' or newuser == 605:
                df = df[df['merchant_id_course'] == 605]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=607' or newuser == 607:
                df = df[df['merchant_id_course'] == 607]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=609' or newuser == 609:
                df = df[df['merchant_id_course'] == 609]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=610' or newuser == 610:
                df = df[df['merchant_id_course'] == 610]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=617' or newuser == 617:
                df = df[df['merchant_id_course'] == 617]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=630' or newuser == 630:
                df = df[df['merchant_id_course'] == 630]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=635' or newuser == 635:
                df = df[df['merchant_id_course'] == 635]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=640' or newuser == 640:
                df = df[df['merchant_id_course'] == 640]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=641' or newuser == 641:
                df = df[df['merchant_id_course'] == 641]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=649' or newuser == 649:
                df = df[df['merchant_id_course'] == 649]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=650' or newuser == 650:
                df = df[df['merchant_id_course'] == 650]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=651' or newuser == 651:
                df = df[df['merchant_id_course'] == 651]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            elif newuser == 'merchant_id=652' or newuser == 652:
                df = df[df['merchant_id_course'] == 652]
                id_f_task = df['id_task']
                df_geo_task = df_geo_task[df_geo_task['id'].isin(id_f_task)]
                df_packages = df_packages[df_packages['delivery_id'].isin(id_f_task)]
            else:
                df_geo_task = pd.DataFrame(columns=df_geo_task.columns)
                df_packages = pd.DataFrame(columns=df_packages.columns)
                df= pd.DataFrame(columns=df.columns)
        else: 
            df_geo_task = df_geo_task
            df_packages = df_packages
            df= df
            emi,emi_total,driving,cycling,deki_vul = CO2(stored_selected_date, selected_city )
            num_delivery_result = num_delivery(stored_selected_date, selected_city) 
            km_saved, km_saved_total, driving,l,m = eco_km(stored_selected_date, selected_city )
            time_saved, time_saved_total,d,c,f = time_eco(stored_selected_date, selected_city )
            SC_s,SC_vul,SC_deki = space_eco(stored_selected_date, selected_city )

        
        if df_geo_task.empty or df_packages.empty :
            livra_eco_CO2 = 0
            km_eco_CO2 = 0
            coli_eco_CO2 = 0
            weight_eco_CO2 = 0
            time_eco_CO2 = 0
            congestion_eco_CO2 = 0
            total_colis = 0
            weight_colis = 0
            df_colis_detec =pd.DataFrame(columns=df.columns)
            df_colis=pd.DataFrame(columns=df.columns)
            df= pd.DataFrame(columns=df.columns)
            result = (livra_eco_CO2,km_eco_CO2,coli_eco_CO2,weight_eco_CO2,time_eco_CO2,congestion_eco_CO2, total_colis, weight_colis,df_colis_detec,df_colis, df)     
        else:
            livra_eco_CO2 = round(emi_total/num_delivery_result,3)
            km_eco_CO2 = round(emi_total/km_saved_total,3)
            
            # colis 
            df_geo_task['notes'] = df_geo_task['notes'].str.lower()
            df_geo_task['notes'] = df_geo_task['notes'].str.replace(',', '.')
            
            df_geo_task['new_weight']=0
            def extract_weight(text):
                match1 = re.search(r' [0-9]+\.*[0-9]+kg', text)
                match2 = re.search(r' [0-9]+\.*[0-9]+ kg', text)
                match3 = re.search(r'[0-9]+k', text)
                match4 = re.search(r'[0-9]+ k', text)
                match5 = re.search(r'[0-9]+  k', text)

                if match1:
                    return match1.group(0)[-8:]
                elif match2:
                    return match2.group(0)[-8:]
                elif match3:
                    return match3.group(0)[-3:]
                elif match4:
                    return match4.group(0)[-3:]
                elif match5:
                    return match5.group(0)[-4:]
                else:
                    return None

            # Aplicar la función a la columna 'notes' y crear una nueva columna 'new_weight'
            df_geo_task['new_weight'] = df_geo_task['notes'].apply(lambda x: extract_weight(x) if pd.notna(x) else None)
            df_geo_task['new_weight'] = df_geo_task['new_weight'].str.replace(r'\D', '', regex=True).astype(float)

            df_geo_task['cartons'] = 0

            def extract_cartons(text):
                match1 = re.search(r'[0-9]+ carton', text)
                match2 = re.search(r'[0-9]+carton',text)

                if match1:
                    return match1.group(0)
                elif match2:
                    return match2.group(0)
                else:
                    return None

            df_geo_task['cartons'] = df_geo_task['notes'].apply(lambda x: extract_cartons(x) if pd.notna(x) else None)
            df_geo_task['cartons'] = df_geo_task['cartons'].str.replace(r'\D', '', regex=True).astype(float)
            
            df_geo_task['bidons'] = 0

            def extract_cartons(text):
                match1 = re.search(r'[0-9]+ bido', text)
                match2 = re.search(r'[0-9]+bido',text)

                if match1:
                    return match1.group(0)
                elif match2:
                    return match2.group(0)
                else:
                    return None

            df_geo_task['bidons'] = df_geo_task['notes'].apply(lambda x: extract_cartons(x) if pd.notna(x) else None)
            df_geo_task['bidons'] = df_geo_task['bidons'].str.replace(r'\D', '', regex=True).astype(float)
            
            df_geo_task['sceaux'] = 0

            def extract_cartons(text):
                match1 = re.search(r'[0-9]+ scea', text)
                match2 = re.search(r'[0-9]+scea',text)

                if match1:
                    return match1.group(0)
                elif match2:
                    return match2.group(0)
                else:
                    return None

            df_geo_task['sceaux'] = df_geo_task['notes'].apply(lambda x: extract_cartons(x) if pd.notna(x) else None)
            df_geo_task['sceaux'] = df_geo_task['sceaux'].str.replace(r'\D', '', regex=True).astype(float)
            
            df_geo_task['bouteilles'] = 0

            def extract_cartons(text):
                match1 = re.search(r'[0-9]+ boutei', text)
                match2 = re.search(r'[0-9]+boutei',text)

                if match1:
                    return match1.group(0)
                elif match2:
                    return match2.group(0)
                else:
                    return None

            df_geo_task['bouteilles'] = df_geo_task['notes'].apply(lambda x: extract_cartons(x) if pd.notna(x) else None)
            df_geo_task['bouteilles'] = df_geo_task['bouteilles'].str.replace(r'\D', '', regex=True).astype(float)
            
            df_geo_task['sacs'] = 0

            def extract_cartons(text):
                match1 = re.search(r'[0-9]+ sac', text)
                match2 = re.search(r'[0-9]+sac',text)

                if match1:
                    return match1.group(0)
                elif match2:
                    return match2.group(0)
                else:
                    return None

            df_geo_task['sacs'] = df_geo_task['notes'].apply(lambda x: extract_cartons(x) if pd.notna(x) else None)
            df_geo_task['sacs'] = df_geo_task['sacs'].str.replace(r'\D', '', regex=True).astype(float)
            
            df_geo_task['bonbonnes'] = 0

            def extract_cartons(text):
                match1 = re.search(r'[0-9]+ bonbonn', text)
                match2 = re.search(r'[0-9]+bonbonn',text)

                if match1:
                    return match1.group(0)
                elif match2:
                    return match2.group(0)
                else:
                    return None

            df_geo_task['bonbonnes'] = df_geo_task['notes'].apply(lambda x: extract_cartons(x) if pd.notna(x) else None)
            df_geo_task['bonbonnes'] = df_geo_task['bonbonnes'].str.replace(r'\D', '', regex=True).astype(float)

            count_colis = df_packages['delivery_id'].value_counts()
            df_counts_colis = pd.DataFrame({'delivery_id': count_colis.index, 'colis_number': count_colis.values})
            df['delivery_id'] = df_counts_colis['delivery_id'].astype(np.int64)
            df_colis = pd.merge(df_counts_colis, df, right_on='id_task', left_on='delivery_id', how='right', suffixes=('_colis', '_df'))
            df_colis_detec = df_geo_task[['cartons', 'bidons', 'sceaux','bouteilles', 'sacs', 'bonbonnes', 'end_date']]
            col_num = ['cartons', 'bidons', 'sceaux', 'bouteilles', 'sacs', 'bonbonnes']
            df_colis_detec['colis_number'] = df_geo_task[col_num].sum(axis=1, skipna=True)
            df_colis_detec['colis_number'] = df_colis_detec['colis_number'].replace(0.0, np.nan)
            df_colis_detec['id'] = df_geo_task['id']
            df_colis = df_colis[df_colis['id_task'].isin(df_geo_task['id'])]
            
            df_colis['colis_number_updated'] = np.nan
            df_colis.reset_index(drop=True, inplace=True)
            df_colis_detec.reset_index(drop=True, inplace=True)

            def update_colis_number(row):
                if pd.isna(row['colis_number']):
                    return df_colis_detec.at[row.name, 'colis_number']
                else:
                    return row['colis_number']

            df_colis['colis_number_updated'] = df_colis.apply(update_colis_number, axis=1)
            total_colis = sum(df_colis['colis_number_updated'].dropna())
            
            coli_eco_CO2 = round(emi_total/total_colis,3)
            
            summarized_df = df_packages.groupby('delivery_id')['weight'].sum().reset_index()
            summarized_df.columns = ['delivery_id', 'weight']
            summarized_df[summarized_df == 0] = np.nan
            summarized_df = summarized_df.dropna()
            
            df_colis_detec.fillna(0, inplace=True)
            df_colis_detec['new_weight'] = df_geo_task['new_weight']
            df_colis_detec['final_weight'] = None

            def weight(row):
                if pd.isna(row['new_weight']):
                    result =(df_colis_detec.at[row.name,'bidons']*3 + 
                             df_colis_detec.at[row.name,'sceaux']*7 + 
                             df_colis_detec.at[row.name,'bouteilles']*1.2 + 
                             df_colis_detec.at[row.name,'sacs']*5 + 
                             df_colis_detec.at[row.name,'bonbonnes']*10 +
                             df_colis_detec.at[row.name,'cartons']*7.2)
                    return  result
                else: 
                    return df_colis_detec.at[row.name,'new_weight']

            df_colis_detec['final_weight'] = df_colis_detec.apply(weight, axis=1)
            df_colis_detec[df_colis_detec == 0] = np.nan
            
            def final_weight(row):
                if pd.isna(row['final_weight']):
                    if df_colis_detec.at[row.name, 'id'] in summarized_df['delivery_id'].values:
                        matching_rows = summarized_df.loc[summarized_df['delivery_id'] == df_colis_detec.at[row.name, 'id'], 'weight']
                        if not matching_rows.empty:
                            return matching_rows.values[0]
                        else:
                            return None
                    else: 
                        return None 
                else:
                    return row['final_weight']

            df_colis_detec['final_weight_2'] = df_colis_detec.apply(final_weight, axis=1)
            weight_colis = sum(df_colis_detec['final_weight_2'].fillna(0))
            weight_eco_CO2 = round(emi_total/weight_colis*1000, 3)
            time_eco_CO2 = round(emi_total/time_saved_total, 3)
            congestion_eco_CO2 = round(emi_total/SC_s, 3)

            result = (livra_eco_CO2,km_eco_CO2,coli_eco_CO2,weight_eco_CO2,time_eco_CO2,congestion_eco_CO2,round(total_colis), round(weight_colis),df_colis_detec,df_colis, df)

    # save the result in cache
    cache.set(cache_key , result, timeout= 23020 )
    return result

def graph_line(stored_selected_date,selected_city,newuser=None,season=None): 
   
    cache_key = f'graph_line{stored_selected_date}_{newuser}_{selected_city}_{season}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        KPI = KPI_CO2(stored_selected_date,selected_city ,newuser)
        df_colis_detec = KPI[8]
        df_colis = KPI[9]
        df = KPI[10]
    
        def convert_to_json(det):
            data = []
            for i in range(len(det)):
                data.append({
                    'x': det.iloc[i]['date'],
                    'y': float(det.iloc[i]['count'])
                })
            return json.dumps(data, default=str)
        
        if df.empty:
            if season == 'Journalier' or season is None:
                day_delivery = pd.DataFrame({'date': [0], 'count': [0]})
                day_delivery_json = convert_to_json(day_delivery)
                day_colis = pd.DataFrame({'date': [0], 'count': [0]})
                day_colis_json = convert_to_json(day_colis)
                day_weight = pd.DataFrame({'date': [0], 'count': [0]})
                day_weight_json =convert_to_json(day_weight )
                json_string = pd.DataFrame({'x': [0], 'y': [0]})
                json_string = json_string.to_json(orient='records')
                result = (day_delivery_json,day_colis_json,day_weight_json, json_string)
            elif season == 'Hebdomadaire':
                week_delivery = pd.DataFrame({'date': [0], 'count': [0]})
                week_delivery_json = convert_to_json(week_delivery)
                week_colis = pd.DataFrame({'date': [0], 'count': [0]})
                week_colis_json = convert_to_json(week_colis)
                week_weight = pd.DataFrame({'date': [0], 'count': [0]})
                week_weight_json = convert_to_json(week_weight)
                json_string = pd.DataFrame({'x': [0], 'y': [0]})
                json_string = json_string.to_json(orient='records')
                result = (week_delivery_json,week_colis_json,week_weight_json, json_string)
            elif season == 'Mensuel':
                month_delivery = pd.DataFrame({'date': [0], 'count': [0]})
                month_delivery_json = convert_to_json(month_delivery)
                month_colis = pd.DataFrame({'date': [0], 'count': [0]})
                month_colis_json = convert_to_json(month_colis)
                month_weight = pd.DataFrame({'date': [0], 'count': [0]})
                month_weight_json = convert_to_json(month_weight)
                json_string = pd.DataFrame({'x': [0], 'y': [0]})
                json_string = json_string.to_json(orient='records')
                result = (month_delivery_json,month_colis_json,month_weight_json,json_string)
        else:
            df['end_date']= pd.to_datetime(df['end_date'])
            df['day_of_week'] = df['end_date'].dt.dayofweek
            ds_delivery = df['day_of_week'].value_counts().reset_index()
            ds_delivery.columns = ['day_of_week', 'count']
            ds_delivery = ds_delivery.sort_values(by='day_of_week')
            ds_delivery = ds_delivery.reset_index(drop=True)

            name_week_france = {
                    0: 'Lundi',
                    1: 'Mardi',
                    2: 'Mercredi',
                    3: 'Jeudi',
                    4: 'Vendredi',
                    5: 'Samedi',
                    6: 'Dimanche'
            }

            ds_delivery['day_of_week_fr'] = ds_delivery['day_of_week'].map(name_week_france)
            ds_delivery = ds_delivery[['day_of_week_fr', 'count']] 

            json_data = ds_delivery[['day_of_week_fr', 'count']]
            json_data = json_data.rename(columns={'day_of_week_fr': 'x', 'count': 'y'})
            json_string = json_data.to_json(orient='records', force_ascii=False)
            json_string = '[' + json_string[1:-1] + ']'

            if season == 'Journalier' or season is None:
                df['end_date']= pd.to_datetime(df['end_date'])
                df['end_date'] = df['end_date'].dt.date
                day_delivery = df['end_date'].value_counts().reset_index()
                day_delivery.columns = ['date','count']
                day_delivery = day_delivery.sort_values(by='date')
                day_delivery = day_delivery.reset_index(drop=True)
                day_delivery['count']= day_delivery['count'].cumsum()
               
                day_delivery_json = convert_to_json(day_delivery)

                df_colis['colis_number_updated'] = df_colis['colis_number_updated'].fillna(0)
                day_colis =  df_colis.groupby(df_colis['end_date'].dt.date)['colis_number_updated'].sum().reset_index()
                day_colis = day_colis[day_colis['colis_number_updated']>0]
                day_colis.columns = ['date','count']
                day_colis = day_colis.sort_values(by='date')
                day_colis = day_colis.reset_index(drop=True)
                day_colis['count'] = day_colis['count'].cumsum()
                
                day_colis_json = convert_to_json(day_colis)
                
                df_colis_detec['final_weight_2'] =  df_colis_detec['final_weight_2'].fillna(0)
                day_weight = df_colis_detec.groupby(df_colis_detec['end_date'].dt.date)['final_weight_2'].sum().reset_index()
                day_weight = day_weight[day_weight['final_weight_2']>0]
                day_weight.columns = ['date','count']
                day_weight = day_weight.sort_values(by='date')
                day_weight = day_weight.reset_index(drop=True)
                day_weight['count'] = day_weight['count'].cumsum()
                
                day_weight_json = convert_to_json(day_weight)

                result = (day_delivery_json,day_colis_json,day_weight_json,json_string)
                
            elif season == 'Hebdomadaire':
                week_delivery = df.groupby(df['end_date'].dt.to_period('W')).size().reset_index()
                week_delivery.columns = ['date','count']
                week_delivery = week_delivery.sort_values(by='date')
                week_delivery = week_delivery.reset_index(drop=True)
                week_delivery['count'] = week_delivery['count'].cumsum()
                
                week_delivery_json = convert_to_json(week_delivery)
                
                df_colis['colis_number_updated'] = df_colis['colis_number_updated'].fillna(0)
                week_colis = df_colis.groupby(df_colis['end_date'].dt.to_period('W-Mon'))['colis_number_updated'].sum().reset_index()
                week_colis = week_colis[week_colis['colis_number_updated']>0]
                week_colis.columns = ['date','count']
                week_colis = week_colis.sort_values(by='date')
                week_colis = week_colis.reset_index(drop=True)
                week_colis['count'] = week_colis['count'].cumsum()
                
                week_colis_json = convert_to_json(week_colis)
                
                df_colis_detec['final_weight_2'] =  df_colis_detec['final_weight_2'].fillna(0)
                week_weight = df_colis_detec.groupby(df_colis_detec['end_date'].dt.to_period('W-Mon'))['final_weight_2'].sum().reset_index()
                week_weight = week_weight[week_weight['final_weight_2']>0]
                week_weight.columns = ['date','count']
                week_weight = week_weight.sort_values(by='date')
                week_weight = week_weight.reset_index(drop=True)
                week_weight['count'] =week_weight['count'].cumsum()

                week_weight_json = convert_to_json(week_weight)
                result = (week_delivery_json,week_colis_json,week_weight_json, json_string)
                
            elif season == 'Mensuel':
                month_delivery = df.groupby(df['end_date'].dt.to_period('M')).size().reset_index()
                month_delivery.columns = ['date','count']
                month_delivery = month_delivery.sort_values(by='date')
                month_delivery = month_delivery.reset_index(drop=True)
                month_delivery['count'] = month_delivery['count'].cumsum()
                
                month_delivery_json = convert_to_json(month_delivery)
                
                df_colis['colis_number_updated'] = df_colis['colis_number_updated'].fillna(0)
                month_colis = df_colis.groupby(df_colis['end_date'].dt.to_period('M'))['colis_number_updated'].sum().reset_index()
                month_colis = month_colis[month_colis['colis_number_updated']>0]
                month_colis.columns = ['date','count']
                month_colis = month_colis.sort_values(by='date')
                month_colis = month_colis.reset_index(drop=True)
                month_colis['count'] = month_colis['count'].cumsum()
                
                month_colis_json = convert_to_json(month_colis)
                
                df_colis_detec['final_weight_2'] =  df_colis_detec['final_weight_2'].fillna(0)
                month_weight = df_colis_detec.groupby(df_colis_detec['end_date'].dt.to_period('M'))['final_weight_2'].sum().reset_index()
                month_weight = month_weight[month_weight['final_weight_2']>0]
                month_weight.columns = ['date','count']
                month_weight = month_weight.sort_values(by='date')
                month_weight = month_weight.reset_index(drop=True)
                month_weight['count'] = month_weight['count'].cumsum()

                month_weight_json = convert_to_json(month_weight)

                result = (month_delivery_json,month_colis_json,month_weight_json,json_string)

    # save the result in cache
    cache.set(cache_key , result, timeout= 22020 )
    return result

def graph_jk(stored_selected_date,selected_city,newuser=None): 

    cache_key = f'graph_jk{stored_selected_date}_{newuser}_{selected_city}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        KPI = KPI_CO2(stored_selected_date,selected_city ,newuser=None)
        df_colis_detec = KPI[8]
        df_colis = KPI[9]
        df = KPI[10]
        
        if df.empty: 
            j_1 = 0
            j_0 = 0
            j_2 = 0
            k_1 = 0
            k_2 = 0
            k_3 = 0
            k_4 = 0
            k_5 = 0
            result = (j_0,j_1,j_2,k_1,k_2,k_3,k_4,k_5)
        else: 
            df['created_at_task'] = pd.to_datetime(df['created_at_task'])
            df['end_date'] = pd.to_datetime(df['end_date'])
            df['diff_days'] = ((df['start_date'] - df['created_at_task']).dt.total_seconds() / 3600)
            df['diff_days'] = df['diff_days'].abs()
            df['created_hour'] = df['created_at_task'].dt.hour
            df['end_hour'] = df['end_date'].dt.hour
            def asig(row):
                if (row['created_hour'] < 9 or row['created_hour'] > 18) and row['diff_days'] <= 24 and (row['end_hour'] >= 8 or row['end_hour'] <= 18):
                    return 'a'
                elif (row['created_hour'] >= 9 and row['created_hour'] <= 18) and row['diff_days'] <= 33:
                    return 'b'
                elif row['diff_days'] > 33 :
                    return 'c'
                return None

            df['retard'] = df.apply(asig, axis=1)
            a = df['retard'].value_counts()

            if 'a' in a:
                j_0 = int(a['a'])
            else:
                j_0 = 0

            if 'b' in a:
                j_1 =int(a['b'])
            else:
                j_1 = 0

            if 'c' in a:
                j_2 = int(a['c'])
            else:
                j_2 = 0

            df_colis['colis_number_updated'] = df_colis['colis_number_updated'].fillna(0)
            def kilos(row):
                if 0 <= row['final_weight_2'] < 5:
                    return 'a'
                elif 5 <= row['final_weight_2'] < 40:
                    return 'b'
                elif 40 <= row['final_weight_2'] < 150:
                    return 'c'
                elif 150 <= row['final_weight_2'] < 300:
                    return 'd'
                elif row['final_weight_2'] >= 300:
                    return 'f'
                return None

            df_colis_detec['kilos'] = df_colis_detec.apply(kilos, axis=1)
            b = df_colis_detec['kilos'].value_counts()

            if 'a' in b:
                k_1 = int(b['a'])
            else:
                k_1 = 0

            if 'b' in b:
                k_2 = int(b['b'])
            else:
                k_2 = 0

            if 'c' in b:
                k_3 = int(b['c'])
            else:
                k_3 = 0

            if 'd' in b:
                k_4 = int(b['d'])
            else:
                k_4 = 0

            if 'f' in b:
                k_5 = int(b['f'])
            else:
                k_5 = 0

            result = (j_0,j_1,j_2,k_1,k_2,k_3,k_4,k_5)

    # save the result in cache
    cache.set(cache_key , result, timeout= 21020 )
    return result

def livra_state(stored_selected_date, selected_city,newuser=None):
    
    cache_key = f'livra_state{stored_selected_date}_{newuser}_{selected_city}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        df_tasks = get_data_task()
        df_geo_task = get_data_cydi()
        df_courses = get_data_courses()
        df_merchants = get_data_merchants()
        df_task = pd.merge(df_courses, df_tasks, right_on='course_id', left_on='id', how='inner', suffixes=('_course', '_task'))
        merchant_trd = df_merchants[df_merchants['group_0_id'] == 1]
        merchant_trd = merchant_trd[['id']]
        merchant_id = df_merchants[~df_merchants['id'].isin([19, 20, 54, 77, 63, 85, 21, 37, 66, 645, 646, 603, 624, 628,
                                                                    647, 112, 83, 632, 648,70, 44, 39,
                                                                    32, 43, 45, 102, 26, 61, 27, 33, 36, 87, 75, 78, 105, 
                                                                    200, 625, 629, 642, 626, 636, 8, 247, 238, 
                                                                    643, 627, 631, 637, 638, 340, 123, 320, 639, 480, 402, 29, 
                                                                    282, 141, 151, 154, 159, 305, 307, 335, 345, 125, 317, 359, 
                                                                    385, 394, 414, 432, 441, 446, 544, 518, 530, 392, 559, 565, 
                                                                    287, 572, 352, 574, 591, 279, 403, 583, 49, 364, 148, 569, 
                                                                    128, 324, 597, 437, 533, 376, 331, 620, 274, 621, 602, 622, 623, 31,
                                                                    604,608,663])]
        merchant_id = merchant_id[['id']]

        df_task  = df_task.sort_values(by='end_date', ascending=False)
        df_task['end_date'] = pd.to_datetime(df_task['end_date'])
        df_task = df_task.dropna(subset=['end_date'])
        df_task  = df_task[df_task['type'] != "collecte"]
        merchant_trd_ids = merchant_trd['id'].tolist()
        merchant_id_ids = merchant_id['id'].tolist()
        df_task  = df_task[(df_task['created_by_id'] == 1) | (df_task['merchant_id_course'].isin(merchant_trd_ids)) | (df_task['merchant_id_course'].isin(merchant_id_ids))]
        df_task  = df_task.dropna(subset=['merchant_id_course'])
        df_task  = df_task[~df_task['merchant_id_course'].isin([8,200,604])]
        
        if selected_city is not None:
            def city_to_id(selected_city):
                city_mapping = {
                    'marseille': '13',
                    'lyon': '69',
                    'lille': '59',
                    'paris': '75',
                    'bordeaux': '33',
                    'toulouse': '31',
                    'dijon': '21',  # Ensure 'dijon' is lowercase for consistency
                }
                return [city_mapping.get(city.lower(), None) for city in selected_city]
            
            city_id = city_to_id(selected_city)
            df_geo_task = df_geo_task[df_geo_task['id_city'].isin(city_id)]
            id_f_task = df_geo_task['id']
            df_task = df_task[df_task['id_task'].isin(id_f_task)]
        else: 
            df_task=df_task

        if newuser is not None:
            if newuser == 'group_id=1' or newuser == 1:
                merchant_trd = df_merchants[df_merchants['group_0_id'] == 1]
                merchant_trd = merchant_trd[['id']]
                merchant_trd_ids = merchant_trd['id'].tolist()
                df_task  = df_task[df_task['merchant_id_course'].isin(merchant_trd_ids)]
            elif newuser == 'team_id=2' or newuser == 2 :
                df_task = df_task[df_task['team_id'] == 2]
            elif newuser == 'team_id=3' or newuser == 3 :
                df_task = df_task[df_task['team_id'] == 3]
            elif newuser == 'team_id=4' or newuser == 4 : 
                df_task  = df_task[df_task['team_id'] == 4]
            elif newuser == 'team_id=6' or newuser == 6:
                df_task = df_task[df_task['team_id'] == 6]
            elif newuser == 'team_id=9' or newuser == 9 :
                df_task  = df_task[df_task['team_id'] == 9]
            elif newuser == 'team_id=10' or newuser == 10 :
                df_task  = df_task[df_task['team_id'] == 10]
            elif newuser == 'team_id=11' or newuser == 11 :
                df_task  = df_task[df_task['team_id'] == 11]
            elif newuser == 'team_id=13' or newuser == 13 :
                df_task  = df_task[df_task['team_id'] == 13]
            elif newuser == 'team_id=14' or newuser == 14:
                df_task  = df_task[df_task['team_id'] == 14]
            elif newuser == 'team_id=15' or newuser == 15 :
                df_task  = df_task[df_task['team_id'] == 15]
            elif newuser == 'team_id=16' or newuser == 16 :
                df_task  = df_task[df_task['team_id'] == 16]
            elif newuser == 'team_id=17' or newuser == 17 :
                df_task = df_task[df_task['team_id'] == 17]
            elif newuser == 'team_id=18' or newuser == 18 :
                df_task  = df_task[df_task['team_id'] == 18]
            elif newuser == 'team_id=19' or newuser == 19 :
                df_task  = df_task[df_task['team_id'] == 19]
            elif newuser == 'team_id=20' or newuser == 20 :
                df_task  = df_task[df_task['team_id'] == 20]
            elif newuser == 'team_id=22' or newuser == 22:
                df_task  = df_task[df_task['team_id'] == 22]
            elif newuser == 'merchant_id=606' or newuser == 606 :
                df_task = df_task[df_task['merchant_id_course'] == 606]
            elif newuser == 'merchant_id=605' or newuser == 605 :
                df_task  = df_task[df_task['merchant_id_course'] == 605]
            elif newuser == 'merchant_id=607' or newuser == 607 :
                 df_task  = df_task[df_task['merchant_id_course'] == 607]
            elif newuser == 'merchant_id=609' or newuser == 609 :
                df_task  = df_task[df_task['merchant_id_course'] == 609]
            elif newuser == 'merchant_id=610' or newuser == 610 :
                df_task  = df_task[df_task['merchant_id_course'] == 610]
            elif newuser == 'merchant_id=617' or newuser == 617 :
                df_task = df_task[df_task['merchant_id_course'] == 617]
            elif newuser == 'merchant_id=630' or newuser == 630 :
                df_task  = df_task[df_task['merchant_id_course'] == 630]
            elif newuser == 'merchant_id=635' or newuser == 635 :
                df_task  = df_task[df_task['merchant_id_course'] == 635]
            elif newuser == 'merchant_id=640' or newuser == 640 :
                df_task  = df_task[df_task['merchant_id_course'] == 640]
            elif newuser == 'merchant_id=641' or newuser == 641:
                df_task  = df_task[df_task['merchant_id_course'] == 641]
            elif newuser == 'merchant_id=649' or newuser == 649 :
                df_task  = df_task[df_task['merchant_id_course'] == 649]
            elif newuser == 'merchant_id=650' or newuser == 650 :
                df_task  = df_task[df_task['merchant_id_course'] == 650]
            elif newuser == 'merchant_id=651' or newuser == 651 :
                df_task  = df_task[df_task['merchant_id_course'] == 651]
            elif newuser == 'merchant_id=652' or newuser == 652 :
                df_task  = df_task[df_task['merchant_id_course'] == 652]
            else:
                df_task= pd.DataFrame(columns=df_task.columns)
        else:
            df_task=df_task
        

        if stored_selected_date is not None:
            st, en = stored_selected_date.strip('()[]').split(' to ')
            st = pd.to_datetime(st, format='%d/%m/%Y')
            en = pd.to_datetime(en, format='%d/%m/%Y')
            df_task['end_date'] = pd.to_datetime(df_task['end_date'])
            st = st.tz_localize(df_task['end_date'].dt.tz)
            en = en.tz_localize(df_task['end_date'].dt.tz)
            df_task = df_task[(df_task['end_date'] >= st) & (df_task['end_date'] <= en)]
        else: 
            df_task = df_task

        if df_task.empty:
            num_0 = 0
            num_1 = 0
            num_2 = 0 
            num_3 = 0
            num_4 = 0
            result = (num_0, num_1, num_2, num_3, num_4)
        else: 
            df_task_1 = df_task['state_task'].dropna()
            a = df_task_1.value_counts()
            
            if 0 in a:
                num_0 = int(a[0])
            else:
                num_0 = 0

            if 1 in a:
                num_1 = int(a[1])
            else:
                num_1 = 0

            if 2 in a:
                num_2 = int(a[2])
            else:
                num_2 = 0

            if 3 in a:
                num_3 = int(a[3])
            else:
                num_3 = 0

            if 4 in a:
                num_4 = int(a[4])
            else:
                num_4 = 0
        
            result = (num_0, num_1, num_2, num_3, num_4)

    # save the result in cache
    cache.set(cache_key , result, timeout=41020)
    return result

def KPI_livra(stored_selected_date,selected_city,newuser=None): 
   
    cache_key = f'KPI_livra{stored_selected_date}_{newuser}_{selected_city}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        KPI = KPI_CO2(stored_selected_date,selected_city ,newuser)
        df_colis_detec = KPI[8]
        df_colis = KPI[9]
        
        if df_colis.empty:
            colis_m = 0
            weight = 0
            result = (colis_m, weight)
        else:
            colis_m = round(df_colis['colis_number_updated'].mean())
            weight = round(df_colis_detec['final_weight_2'].mean())
            result = (colis_m, weight)

    # save the result in cache
    cache.set(cache_key , result, timeout= 33020 )
    return result