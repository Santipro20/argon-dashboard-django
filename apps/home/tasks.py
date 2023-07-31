from celery import shared_task
import pandas as pd
import time


@shared_task
def num_delivery(df_courses, df_tasks, df_merchants):
    time.sleep(10)

    # Convert to pandas dataframe
    df_courses = pd.DataFrame(df_courses)
    df_tasks = pd.DataFrame(df_tasks)
    df_merchants = pd.DataFrame(df_merchants)

    # Merge dataframes
    df = pd.merge(df_courses, df_tasks, right_on='course_id', left_on='id', how='inner', suffixes=('_course', '_task'))

    # Id Terrasse du port's merchants 
    merchant_trd = df_merchants[df_merchants['group_0_id'] == 1]
    merchant_trd = merchant_trd[['id']]
  
    # Id Deki's clients (eliminate all the false merchants)
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

    # Filtering df by the following statements:

    ## 1. state_task == 3 means that we are gonna take into account just finished tasks.
    ## 2. type != "collecte" means that we are gonna take into account just tasks marked as delivery.
    ## 3. created_by == 1 | merchant_id %in% merchant_trd | merchant_id %in% merchants_id this statement is devided in three parts.
    ## 3.1. The first one means that we are gonna take into account just tasks created by user 1 which is admin.
    ## 3.2. The second one means that we are gonna take into account just tasks which were created by any merchant of TDP.
    ## 3.3. The Third one means that we are gonna take into account just tasks which were created by any merchat of our clients.
    ## Note: | means the logic term "or". Does not matter which of those three statement are true inside each observation if at least
    ## one of them is True.

    # Ordering all dates
    df = df.sort_values(by= 'end_date', ascending=False)

    # converting all dates in the same format
    df['end_date'] = pd.to_datetime(df['end_date'])
    df = df.dropna(subset=['end_date'])
    df = df[df['state_task'] == 3]
    df = df[df['type'] != "collecte"]
    merchant_trd_ids = merchant_trd['id'].tolist()
    merchant_id_ids = merchant_id['id'].tolist()
    df = df[(df['created_by_id'] == 1) | (df['merchant_id_course'].isin(merchant_trd_ids)) | (df['merchant_id_course'].isin(merchant_id_ids))]
    df = df.dropna(subset= ['merchant_id_course'])
    df = df[~df['merchant_id_course'].isin([8,200,604])]

    # Principals clients
    df_id_merchant = df[['merchant_id_course']]

    # Counting the number of tasks per merchant finished
    num_finised_task = len(df)
    
    # Counting the increase of tasks per merchant finished the last month
    date_limit= df['end_date'].iloc[0] - pd.DateOffset(months=1)
    df_filtter = df[df['end_date'] >= date_limit]
    num_new_task = len(df_filtter)
    month_growth = round((num_new_task)/num_finised_task*100,2)

    return num_finised_task, month_growth, df_id_merchant



