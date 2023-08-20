
from apps.home.models import Courses, Tasks, Merchants, Geolocation
import pandas as pd
from django.core.cache import cache
from itertools import zip_longest 
import numpy as np


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
                                                            647, 112, 83, 632, 648,70, 44, 649, 39, 651, 652, 653, 
                                                            32, 43, 45, 102, 26, 61, 27, 33, 36, 87, 75, 78, 105, 
                                                            200, 625, 629, 642, 626, 636, 8, 247, 238, 
                                                            643, 627, 631, 637, 638, 340, 123, 320, 639, 480, 402, 29, 
                                                            282, 141, 151, 154, 159, 305, 307, 335, 345, 125, 317, 359, 
                                                            385, 394, 414, 432, 441, 446, 544, 518, 530, 392, 559, 565, 
                                                            287, 572, 352, 574, 591, 279, 403, 583, 49, 364, 148, 569, 
                                                            128, 324, 597, 437, 533, 376, 331, 620, 274, 621, 602, 622, 623, 31,
                                                            604,605,606,607,617,608,609,610])]
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
        id_f = df['merchant_id_course'].unique()

        # merge the data geo and task and clean the data just to real merchants
        df_geo_task = pd.merge(df_task, df_geolocation, right_on='task_id', left_on='id', how='right', suffixes=('_task', '_geo'))
        df_geo_task = df_geo_task[df_geo_task['merchant_id'].isin(id_f)]

        # JSON to dict and column 
        df_normalized_1 = pd.json_normalize(df_geo_task['cycling'])
        df_normalized_1 = df_normalized_1.add_suffix('_cycling')
        df_geo_task.reset_index(drop=True, inplace=True)
        df_normalized_1.reset_index(drop=True, inplace=True)
        df_geo_task = pd.concat([df_geo_task, df_normalized_1], axis=1)

        df_normalized_2 = pd.json_normalize(df_geo_task['driving'])
        df_normalized_2 = df_normalized_2.add_suffix('_driving')
        df_geo_task.reset_index(drop=True, inplace=True)
        df_normalized_2.reset_index(drop=True, inplace=True)
        df_geo_task = pd.concat([df_geo_task, df_normalized_2], axis=1)

        df_normalized_3 = pd.json_normalize(df_geo_task['altitudes'])
        df_normalized_3 = df_normalized_3.add_suffix('_altitudes')
        df_geo_task.reset_index(drop=True, inplace=True)
        df_normalized_3.reset_index(drop=True, inplace=True)
        df_geo_task = pd.concat([df_geo_task, df_normalized_3], axis=1)

        df_geo_task = df_geo_task.sort_values(by='end_date', ascending=False)
        df_geo_task['end_date'] = pd.to_datetime(df_geo_task['end_date'])
        df_geo_task = df_geo_task.dropna(subset=['end_date'])
        result = df_geo_task
    
    # save the result in cache
    cache.set('get_data_2', result, timeout=42000)
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

            # Assuming db is a list of dictionaries or a pandas DataFrame with 'inclination', 'elevationA', and 'elevationB' columns.
            for i in range(len(df_geo_task)):
                if df_geo_task['pickUpPoint_altitudes'][i] == 0 or df_geo_task['deliveryPoint_altitudes'][i] == 0:
                    df_geo_task.loc[i, 'inclination'] = df_geo_task['pickUpPoint_altitudes'][i] + df_geo_task['deliveryPoint_altitudes'][i]
                else:
                    df_geo_task.loc[i, 'inclination'] = (df_geo_task.loc[i, 'deliveryPoint_altitudes'] - df_geo_task.loc[i, 'pickUpPoint_altitudes']) / df_geo_task.loc[i, 'pickUpPoint_altitudes']
  
            def calculate_diffs(lst):
               return [b - a for a, b in zip_longest(lst, lst[1:], fillvalue=0)]
                        
            # Apply the function to the 'speeds_cycling' column
            vector_diffs_1 = df_geo_task['speeds_cycling'].apply(lambda x: x if isinstance(x, list) else [x]).apply(calculate_diffs).values.tolist()

            # Apply the function to the 'speeds_driving' column
            vector_diffs_2 = df_geo_task['speeds_driving'].apply(lambda x: x if isinstance(x, list) else [x]).apply(calculate_diffs).values.tolist()

            df_geo_task['acceleration_cycling'] = vector_diffs_1
            df_geo_task['acceleration_driving'] = vector_diffs_2

            # Renault Master ==>> VUL termique data: https://www.vcalc.com/wiki/vCalc/Cost+to+Idle * 
            # https://www.engineeringtoolbox.com/fuels-higher-calorific-values-d_169.html *
            # https://x-engineer.org/rolling-resistance/#formula *
            # https://www.mdpi.com/2032-6653/14/6/134 *
            # https://www.aerodinamicaf1.com/2019/09/las-fuerzas-sobre-el-monoplaza-drag-y-lift-o-downforce/ *
            # https://base-empreinte.ademe.fr/donnees/jeu-donnees *
            # The maximum load of a VUL is 3.5 tons, which is equivalent to 3500 kg.
            # Parameters:

            alpha_vul = 0.8833 #ml/s
            beta_1_vul_diseal = 1/37.3 #ml/kj avergae of max and minimum    
            beta_2_vul_diseal = 0.0258 #ml/(kj.m/s^2) using the work theorem 
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
            VUL = 1.16 #kg eq. CO2/t.km

            b2 = []
            for n in range(len(df_geo_task)):
                list_cell = df_geo_task.at[n, 'speeds_driving']
                b2_value = []
                if isinstance(list_cell, list):
                    for i in range(len(list_cell)):
                        b2_value.append((0.5 * Density_wind * area_front_vul * list_cell[i] * cd) / 1000)  # drag arodinamic force kN/m/s
                else:
                    b2_value.append((0.5 * Density_wind * area_front_vul * list_cell * cd) / 1000)  # drag arodinamic force kN/m/s
                b2.append(b2_value)

            for i, sublist in enumerate(b2):
                if all(item == 0 for item in sublist):
                    b2[i] = 0  # Replace the sublist with a list containing a single 0
                
            rt = []
            for n in range(len(df_geo_task)):
                list_cell = df_geo_task.at[n, 'acceleration_driving']
                list_cell2 = df_geo_task.at[n, 'speeds_driving']
                rt_ap = []
                if isinstance(list_cell, list) and isinstance(list_cell2, list):
                    for i in range(len(list_cell)):
                        b2_list = b2[n]
                        if isinstance(list_cell2[i], (int, float)) and isinstance(list_cell[i], (int, float)):
                            if list_cell[i] != 0 and list_cell2[i] != 0:  # Verificar si list_cell y list_cell2 son diferentes de cero
                                rt_value = b1 +  b2_list[i] * (list_cell2[i] ** 2) + (sum_weight_vul * list_cell[i]) / 1000 + (gravity * sum_weight_vul * df_geo_task['inclination'][n]) / 100000
                            else:
                                rt_value = 0  # Reemplazar por cero si list_cell o list_cell2 son cero
                            rt_ap.append(rt_value)
                else:
                    b2_list = b2[n]
                    if isinstance(list_cell2, (int, float)) and isinstance(list_cell, (int, float)):
                        if list_cell != 0 and list_cell2 != 0:  # Verificar si list_cell y list_cell2 son diferentes de cero
                            rt_value = b1 + b2_list * (list_cell2 ** 2) + (sum_weight_vul * list_cell) / 1000 + (gravity * sum_weight_vul * df_geo_task['inclination'][n]) / 100000
                        else:
                            rt_value = 0  # Reemplazar por cero si list_cell o list_cell2 son cero
                        rt_ap.append(rt_value)
                rt.append(rt_ap)

            for i in range(len(rt)):
                if not rt[i]:  # Verifica si la lista en rt[i] está vacía
                    rt[i] = 0


            ft = []
            for n in range(len(rt)):
                list_cell = rt[n]
                list_cell2 = df_geo_task.at[n, 'acceleration_driving']
                list_cell3 = df_geo_task.at[n, 'speeds_driving']
                ft_value = []
                if isinstance(list_cell2,list) and isinstance(list_cell,list):
                    for i in range(len(list_cell2)):
                        if list_cell[i] <= 0:
                            ft_value.append(alpha_vul)
                        else:
                            ft_value.append(alpha_vul + beta_1_vul_diseal * list_cell[i] * list_cell3[i] + (beta_2_vul_diseal * sum_weight_vul * (list_cell2[i]** 2) * list_cell3[i]) / 1000)
                    ft.append(ft_value)
                else: 
                    if list_cell <=0: 
                        ft_value.append(alpha_vul)
                    else: 
                        ft_value.append(alpha_vul + beta_1_vul_diseal * list_cell * list_cell3 + (beta_2_vul_diseal * sum_weight_vul * (list_cell2 ** 2) * list_cell3[i]) / 1000)
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

            BSP = []
            for n in range(len(df_geo_task)):
                list_cell = df_geo_task.at[n, 'acceleration_cycling']
                list_cell2 = df_geo_task.at[n, 'speeds_cycling']
                list_cell3 = df_geo_task.at[n,'durations_cycling']
                BSP_ap = []
                if isinstance(list_cell, list) and isinstance(list_cell2, list):
                    for i in range(len(list_cell)):
                        inclination = df_geo_task.at[n, 'inclination']
                        if isinstance(list_cell2[i], (int, float)) and isinstance(list_cell[i], (int, float)):
                            if list_cell[i] != 0 and list_cell2[i] != 0:  # Verificar si list_cell y list_cell2 son diferentes de cero
                                BSP_value = list_cell2[i] * (1.01 * list_cell[i] + 9.81 * np.sin(np.radians(inclination)) + 0.078) + new_cof * (list_cell2[i] ** 3)
                                BSP_value = BSP_value*list_cell3[i]
                            else:
                                BSP_value = 0  # Reemplazar por cero si list_cell o list_cell2 son cero
                            BSP_ap.append(BSP_value)
                else:
                    inclination = df_geo_task.at[n, 'inclination']
                    if isinstance(list_cell2, (int, float)) and isinstance(list_cell, (int, float)):
                        if list_cell != 0 and list_cell2 != 0:  # Verificar si list_cell y list_cell2 son diferentes de cero
                            BSP_value = list_cell2 * (1.01 * list_cell + 9.81 * np.sin(np.radians(inclination)) + 0.078) + new_cof * (list_cell2 ** 3)
                            BSP_value = BSP_value*list_cell3
                        else:
                            BSP_value = 0  # Reemplazar por cero si list_cell o list_cell2 son cero
                        BSP_ap.append(BSP_value)
                BSP.append(BSP_ap) # joulios 

            for i in range(len(BSP)):
                if not BSP[i]:  # Verifica si la lista en rt[i] está vacía
                    BSP[i] = [0]


            BSP_total = []
            for sublist in BSP:
                BSP_sum = sum(sublist)
                BSP_total.append(BSP_sum)


            BSP_j = []
            for i in range(len(BSP_total)):
                energy= BSP_total[i]/3600000 # kW/h
                BSP_j.append(energy)

            CO2_cycling = [bsp * 0.0520 for bsp in BSP_total] # C02 ADEME kWh france

            # Final step for CO2 saved 
            CO2_driving_total = sum(CO2_driving)
            CO2_cycling_total =  sum(CO2_cycling)
            if CO2_driving_total != 0:
                emi = round(((CO2_driving_total - CO2_cycling_total) / CO2_driving_total), 2) * 100
            else:
                emi = 0 
            emi_total = (round(CO2_driving_total - CO2_cycling_total, 2))
            result = (emi,emi_total,CO2_driving_total,CO2_cycling_total)

    # save the result in cache
    cache.set(cache_key, result, timeout= 40020)
    return result


def eco_km(stored_selected_date ): 

    cache_key = f'eco_km_result{stored_selected_date }'
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
            # create the column of total distance
            df_geo_task['total_distance_cycling'] = df_geo_task['distances_cycling'].apply(lambda x: sum(x) if isinstance(x, list) else x)
            df_geo_task['total_distance_driving'] = df_geo_task['distances_driving'].apply(lambda x: sum(x) if isinstance(x, list) else x)

            distance_cycling = df_geo_task['total_distance_cycling'].sum()/1000
            distance_driving = df_geo_task['total_distance_driving'].sum()/1000

            # calculate the km saved by cycling instead of driving
            if distance_driving > 0:
                km_saved = round(((distance_driving - distance_cycling) / distance_driving) * 100, 2) * (-1)
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
            time_cycling = sum(val for sublist in df_geo_task['durations_cycling'] if isinstance(sublist, list) for val in sublist)
            time_driving = sum(val for sublist in df_geo_task['durations_driving'] if isinstance(sublist, list) for val in sublist)

            # calculate the time saved by cycling instead of driving
            if time_driving > 0:
                time_saved = round(((time_driving - time_cycling) / time_driving) * 100, 2)
            else:
                time_saved = 0 
            time_saved_total = round((round(time_driving - time_cycling, 2))/60,2)
            result = (time_saved, time_saved_total)

    # save the result in cache
    cache.set(cache_key , result, timeout= 38020 )
    return result

def graph_CO2(stored_selected_date):
    cache_key = f'graph_CO2{stored_selected_date}'
    # veryfy if the result is in cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    else:
        CO2_fun = CO2(stored_selected_date)
        emi,emi_total,driving,cycling  = CO2_fun

        if driving > 0  or cycling >0:
            # Like the comparation is how the damage this CO2 is equal in others emissions then we need to think 
            # the effect in at leats 100 years 
            # The Global Warm Potential for this period for gas is :
            Metano= 28
            NO2 = 268
            ozone= 1.130

            VUL_met= round(driving/Metano,2)
            VUL_no2 = round(driving/NO2,2)
            VUL_oz = round(driving/ozone,2)  

            deki_met= round(cycling/Metano,2)
            deki_no2= round(cycling/NO2,2)
            deki_oz= round(cycling/ozone,2 )

            result= (VUL_met,VUL_no2,VUL_oz,deki_met,deki_no2,deki_oz)
        else:
            VUL_met= 0  
            VUL_no2 = 0
            VUL_oz = 0

            deki_met= 0
            deki_no2= 0
            deki_oz= 0
            result= (VUL_met,VUL_no2,VUL_oz,deki_met,deki_no2,deki_oz)

    # save the result in cache
    cache.set(cache_key , result, timeout= 38020 )
    return result