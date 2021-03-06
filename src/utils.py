import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

MAX_VALUE = 360

DEFAULT_GROUPS = [0,90,180,270,360]
DEFAULT_GROUPS_NR_VISIT = [0,5,10,15,20]


def add_grouped_by_time_column(df, GROUPS = DEFAULT_GROUPS, increment = 90):
    '''
    Take in DataFrame.
    Create a new column representing time bucket to which each visit (each df row) gets assigned

    This function isn't very robust.
    GROUPS have to be in sync with increment
    '''
    labeled_group = []
    for time in df.time:
        group = min(GROUPS, key=lambda x:abs(x-time)) // increment
        labeled_group.append(group)
    df['time_group'] = labeled_group
    return df


def add_grouped_by_nr_visit_column(df, GROUPS = DEFAULT_GROUPS_NR_VISIT, increment = 5):
    '''
    Similarly like function above - but assign to column based 
    '''
    labeled_group = []
    for visit_number in df.visit_number:
        group = min(GROUPS, key=lambda x:abs(x-visit_number)) // increment
        labeled_group.append(group)
    df['nr_visit_group'] = labeled_group
    return df



def get_visits_after_wait_time_x(df_, x, limit_on = True):
    '''
    df - pd.DataFrame with data
    x - int time after visits (put a min limit to x - to be 90 days), althought that limit can be turned off
    '''
    if limit_on:
        if x < 90:
            raise Exception('The min x limit is on. The X (nr of days) should be 90 or bigger.')


    df = df_.copy(deep = True)
    # Get data
    return_df = pd.DataFrame()
    for surname in df.surname.unique():
        sub_df = df.loc[df['surname'] == surname]
        # print('sub_df:')
        # display(sub_df)
        # print()
        for index, data in enumerate(sub_df.iterrows()):
            _, visit = data
            if visit['time'] >= x:
                # print('sub_df,iloc[index:')
                # print(index)
                # display(sub_df.iloc[index:])
                # print()
                return_df = return_df.append(sub_df.iloc[index:], ignore_index = True)
                break
    return return_df