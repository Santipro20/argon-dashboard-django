from apps.home.models import Courses, Tasks, Merchants, Geolocation, Packages
import pandas as pd
from django.core.cache import cache
from itertools import zip_longest 
import numpy as np
import copy



def get_data_id():

    # veryfy if the result is in cache
    cached_result = cache.get('get_data')

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
    cache.set('get_data', result, timeout=43020)
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
        
        df_task['durations_cycling_copy'] = df_task['durations_cycling_copy'].apply(lambda x: [value * mean_time for value in x] if isinstance(x, list) else x)  
        df_task['speeds_cycling_copy'] = df_task['speeds_cycling_copy'].apply(lambda x: [value * speed_mean_cycling for value in x] if isinstance(x, list) else x)
        df_task['distances_cycling_copy'] = df_task.apply(lambda row: [a * b for a, b in zip(row['durations_cycling_copy'], row['speeds_cycling_copy'])] if isinstance(row['durations_cycling_copy'], list) and isinstance(row['speeds_cycling_copy'], list) else row['durations_cycling_copy'], axis=1)

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
        
        result = df_geo_task
    
    # save the result in cache
    cache.set('get_data_2', result, timeout=45000)
    return result

def get_data_livra():
    # veryfy if the result is in cache
    cached_result = cache.get('get_data')

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
    cache.set('get_data', result, timeout=42000)
    return result

def num_delivery(stored_selected_date):  

    cache_key =f'num_delivery_{stored_selected_date}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        df = get_data_id()

        if stored_selected_date is not None:
            st, en = stored_selected_date.strip('()[]').split(' to ')
            st = pd.to_datetime(st, format='%d/%m/%Y')
            en = pd.to_datetime(en, format='%d/%m/%Y')
            st = st.tz_localize(df['end_date'].dt.tz)
            en = en.tz_localize(df['end_date'].dt.tz)
            df = df[(df['end_date'] >= st) & (df['end_date'] <= en)]

        else: 
            df = df
        # count the number of deliveries
        num_finished_task = len(df)
        result = num_finished_task
    
    # save the result in cache
    cache.set(cache_key , result, timeout=41020)
    return result

def CO2(stored_selected_date):

    cache_key =f'CO2_result{stored_selected_date}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        # charger the data
        df_geo_task = get_data_cydi()

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
            
        if df_geo_task.empty:
            emi = 'non calculable'     
            emi_total= 'non calculable'
            CO2_driving_total = 0
            CO2_cycling_total =  0
            result = (emi,emi_total,CO2_driving_total,CO2_cycling_total )          
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

def eco_km(stored_selected_date ): 

    cache_key = f'eco_km_result{stored_selected_date}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        #charger the data
        df_geo_task = get_data_cydi()

        if stored_selected_date is not None:
            st, en = stored_selected_date.strip('()[]').split(' to ')
            st = pd.to_datetime(st, format='%d/%m/%Y')
            en = pd.to_datetime(en, format='%d/%m/%Y')
            st = st.tz_localize(df_geo_task['end_date'].dt.tz)
            en = en.tz_localize(df_geo_task['end_date'].dt.tz)
            df_geo_task = df_geo_task[(df_geo_task['end_date'] >= st) & (df_geo_task['end_date'] <= en)]
        else: 
            df_geo_task=df_geo_task
            
        if df_geo_task.empty:
            km_saved = 'non calculable'     
            km_saved_total= 'non calculable'
            result = (km_saved, km_saved_total)        
        else:
            df_geo_task['totalDistance_cycling'] = df_geo_task['distances_cycling_copy'].apply(sum) 

            distance_cycling = df_geo_task['totalDistance_cycling'].sum()/1000
            distance_driving = df_geo_task['totalDistance_driving'].sum()/1000

            # calculate the km saved by cycling instead of driving
            if distance_driving > 0:
                km_saved = round(((distance_driving - distance_cycling) / distance_driving) * 100, 2)
            else:
                km_saved = 0
            km_saved_total = round(distance_driving - distance_cycling, 2)
            result = (km_saved, km_saved_total)

    # save the result in cache
    cache.set(cache_key , result, timeout= 39020)
    return result

def time_eco(stored_selected_date): 

    cache_key = f'time_eco_result{stored_selected_date}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        #charger the data
        df_geo_task = get_data_cydi()

        if stored_selected_date is not None:
            st, en = stored_selected_date.strip('()[]').split(' to ')
            st = pd.to_datetime(st, format='%d/%m/%Y')
            en = pd.to_datetime(en, format='%d/%m/%Y')
            st = st.tz_localize(df_geo_task['end_date'].dt.tz)
            en = en.tz_localize(df_geo_task['end_date'].dt.tz)
            df_geo_task = df_geo_task[(df_geo_task['end_date'] >= st) & (df_geo_task['end_date'] <= en)]
        else: 
            df_geo_task=df_geo_task
            
        if df_geo_task.empty:
            time_saved = 'non calculable'     
            time_saved_total= 'non calculable'
            result = (time_saved, time_saved_total)      
        else:
            # summ the total time for cycling and driving
            df_geo_task['durations_cycling_copy'] = df_geo_task['durations_cycling_copy'].apply(lambda x: [x] if isinstance(x, int) else x)
            df_geo_task['durations_driving'] = df_geo_task['durations_driving'].apply(lambda x: [x] if isinstance(x, int) else x)
            time_cycling = sum(val for sublist in df_geo_task['durations_cycling_copy'] if isinstance(sublist, list) for val in sublist)
            time_driving = sum(val for sublist in df_geo_task['durations_driving'] if isinstance(sublist, list) for val in sublist)

            # calculate the time saved by cycling instead of driving
            if time_driving > 0:
                time_saved = round(((time_driving - time_cycling) / time_driving) * 100, 2)
            else:
                time_saved = 0 
            time_saved_total = round((round(time_driving - time_cycling, 2))/3600,2)
            result = (time_saved, time_saved_total)

    # save the result in cache
    cache.set(cache_key , result, timeout= 38020 )
    return result

def graph_CO2(stored_selected_date):

    cache.delete(f'graph_CO2{stored_selected_date}')

    cache_key = f'graph_CO2{stored_selected_date}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        CO2_fun = CO2(stored_selected_date)
        emi,emi_total,driving,cycling,deki_vul  = CO2_fun

        #charger the data
        df_geo_task = get_data_cydi()

        if stored_selected_date is not None:
            st, en = stored_selected_date.strip('()[]').split(' to ')
            st = pd.to_datetime(st, format='%d/%m/%Y')
            en = pd.to_datetime(en, format='%d/%m/%Y')
            st = st.tz_localize(df_geo_task['end_date'].dt.tz)
            en = en.tz_localize(df_geo_task['end_date'].dt.tz)
            df_geo_task = df_geo_task[(df_geo_task['end_date'] >= st) & (df_geo_task['end_date'] <= en)]
        else: 
            df_geo_task=df_geo_task
            
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
            NOxP = 420/1000 #g / kWH
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

def equivalence(stored_selected_date): 

    cache_key = f'equivalence{stored_selected_date}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        emi,emi_total,driving,cycling,deki_vul = CO2(stored_selected_date)
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

            charger_iphone = round(emi_total/(f_iphone*cp_iphone),0)
            charger_mac = round(emi_total/(battery_mac*f_mac),0)
            trees = round(emi_total/f_trees * (-1),0)
            train = round(emi_total/(f_train * distance_train),0)
            diesel = round(emi_total/f_diesel,0)
            uber =  round(emi_total/f_uber,0)
            print_sheet = round(emi_total/f_print,0)
            emails = round(emi_total/f_emails,0)
            labor = round(emi_total/f_labor,0)
            water = round(emi_total/f_water,0)
            pain = round(emi_total/f_pain,0)
            fromage = round(emi_total/f_fromage,0)
        result = (charger_iphone,charger_mac,trees,train,diesel,uber,print_sheet,emails,labor,water,pain,fromage)
            

    # save the result in cache
    cache.set(cache_key , result, timeout= 37000 )
    return result

def space_eco(stored_selected_date): 

    cache_key = f'space_eco{stored_selected_date}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        #charger the data
        df_geo_task = get_data_cydi()

        if stored_selected_date is not None:
            st, en = stored_selected_date.strip('()[]').split(' to ')
            st = pd.to_datetime(st, format='%d/%m/%Y')
            en = pd.to_datetime(en, format='%d/%m/%Y')
            st = st.tz_localize(df_geo_task['end_date'].dt.tz)
            en = en.tz_localize(df_geo_task['end_date'].dt.tz)
            df_geo_task = df_geo_task[(df_geo_task['end_date'] >= st) & (df_geo_task['end_date'] <= en)]
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