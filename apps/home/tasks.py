
from apps.home.models import Courses, Tasks, Merchants, Geolocation
import pandas as pd
from django.core.cache import cache


def get_data_id():
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

    return df

def get_data_cydi():

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

    return df_geo_task



def num_delivery():
    # veryfy if the result is in cache
    cached_result = cache.get('num_delivery_result')
    if cached_result is not None:
        return cached_result
    else: 
        df = get_data_id()

        # count the number of deliveries
        num_finised_task = len(df)
        date_limit = df['end_date'].iloc[0] - pd.DateOffset(months=1)
        df_filtter = df[df['end_date'] >= date_limit]
        num_new_task = len(df_filtter)
        month_growth = round((num_new_task) / num_finised_task * 100, 2)
        result = (month_growth, num_finised_task)
    
    # save the result in cache
    cache.set('num_delivery_result', result, timeout=43200)

    return result



#def CO2():

    # veryfy if the result is in cache
 #   cached_result = cache.get('CO2_result')

  #  if cached_result is not None:
   #     return cached_result
    
    # charger the data
    # df_geo_task = get_data_cydi()

    #df_geo_task['inclination'] = 0

    # Assuming db is a list of dictionaries or a pandas DataFrame with 'inclination', 'elevationA', and 'elevationB' columns.
    #for i in range(len(df_geo_task)):
    #if df_geo_task['pickUpPoint_altitudes'][i] == 0 or df_geo_task['deliveryPoint_altitudes'][i] == 0:
       # df_geo_task.loc[i, 'inclination'] = 0
    #else:
     #   df_geo_task.loc[i, 'inclination'] = (df_geo_task.loc[i, 'deliveryPoint_altitudes'] - df_geo_task.loc[i, 'pickUpPoint_altitudes']) / df_geo_task.loc[i, 'pickUpPoint_altitudes']

    #def calculate_diffs(lst):
     #   return [b - a for a, b in zip_longest(lst, lst[1:], fillvalue=0)]

    # Apply the function to the 'speeds_cycling' column
    #vector_diffs_1 = df_geo_task['speeds_cycling'].apply(lambda x: x if isinstance(x, list) else [x]).apply(calculate_diffs).values.tolist()

    # Apply the function to the 'speeds_driving' column
    #vector_diffs_2 = df_geo_task['speeds_driving'].apply(lambda x: x if isinstance(x, list) else [x]).apply(calculate_diffs).values.tolist()

    #df_geo_task['acceleration_cycling'] = vector_diffs_1
    #df_geo_task['acceleration_driving'] = vector_diffs_2

    # Renault Master ==>> VUL termique data: https://www.vcalc.com/wiki/vCalc/Cost+to+Idle * 
    # https://www.engineeringtoolbox.com/fuels-higher-calorific-values-d_169.html *
    # The maximum load of a VUL is 3.5 tons, which is equivalent to 3500 kg.
    # Parameters:

    #alpha_vul = 0.8833 #ml/s
    #beta_1_vul_diseal = 1/37.3 #ml/kj avergae of max and minimum    
    #beta_2_vul_diseal = 0.0258 #ml/(kj.m/s^2) using the work theorem 

    #return

def eco_km():
     # veryfy if the result is in cache
    cached_result = cache.get('eco_km_result')
    if cached_result is not None:
        return cached_result
    else:
        #charger the data
        df_geo_task = get_data_cydi()

        # create the column of total distance
        df_geo_task['total_distance_cycling'] = df_geo_task['distances_cycling'].apply(lambda x: sum(x) if isinstance(x, list) else x)
        df_geo_task['total_distance_driving'] = df_geo_task['distances_driving'].apply(lambda x: sum(x) if isinstance(x, list) else x)

        distance_cycling = df_geo_task['total_distance_cycling'].sum()/1000
        distance_driving = df_geo_task['total_distance_driving'].sum()/1000

        # calculate the km saved by cycling instead of driving
        km_saved = round(((distance_driving - distance_cycling) / distance_driving) * 100, 2)*(-1)
        km_saved_total = round(distance_driving - distance_cycling, 2)
        result = (km_saved, km_saved_total)

    # save the result in cache
    cache.set('eco_km_result', result, timeout=43140)
    return result

def time_eco():
     # veryfy if the result is in cache
    cached_result = cache.get('time_eco_result')
    if cached_result is not None:
        return cached_result
    else:
        #charger the data
        df_geo_task = get_data_cydi()

        # summ the total time for cycling and driving
        time_cycling = df_geo_task['state'].sum()/3*21
        time_driving = df_geo_task['state'].sum()/3*30

        # calculate the time saved by cycling instead of driving
        time_saved = round(((time_driving - time_cycling) / time_driving) * 100, 2)
        time_saved_total = (round(time_driving - time_cycling, 2))/60
        result = (time_saved, time_saved_total)


    # save the result in cache
    cache.set('time_eco_result', result, timeout=43080)
    return result