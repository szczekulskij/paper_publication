import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.utils import add_grouped_by_time_column, DEFAULT_GROUPS

POSSIBLE_INPUTS = ['all', 'moved_to_0', 'all_without_0s']

def get_data(format_type, remove_minus_ones = True):

    '''
    format_type = 'all' or 'moved_to_0' or 'all_without_0s'
    '''
    if format_type not in POSSIBLE_INPUTS:
        raise Exception(f'Wrong format_type input Jan! You input: {format_type}, but has to be one of {POSSIBLE_INPUTS}')

    # df = pd.read_csv('12.11 malformacje kapilarne lon.csv')
    try : 
        df = pd.read_csv('nowe_poprawione_dane.csv') 
    except : 
        try : 
            df = pd.read_csv('src/nowe_poprawione_dane.csv') 
        except :
            raise Exception('Data reading went wrong! Fix it !')


    # Fill in data to have surnames at each column
    new_nazwisko = []
    current_surname = ''
    for i in df['nazwisko']:
        if type(i) == str:
            current_surname = i
        new_nazwisko.append(current_surname)
    df['nazwisko'] = new_nazwisko
    df.rename(columns = {'wizyta po ilu zabiegach' : 'visit_number',
                        'total clearence pomiedzy wizytami' : 'total_clearance_effect_between_visit',
                        'czas ' : 'time',
                        'nazwisko' : 'surname',
                        'total clearence effect wzgledem poczatku' : 'total_clearence_effect_wzgledem_poczatku'
                        }, inplace = True)


    #Format column order:
    df = get_summed_time_column(df)
    df = add_grouped_by_time_column(df, DEFAULT_GROUPS)
    df['------------'] = ''
    print('default time group has GROUPS defined as:',DEFAULT_GROUPS)
    df = df[['surname', 'time','summed_time','time_group', 'visit_number','total_clearance_effect_between_visit', 'total_clearence_effect_wzgledem_poczatku',  '------------']]

    if remove_minus_ones:
        df = df.loc[df['total_clearance_effect_between_visit'] != -1]

    if format_type == 'all':
        pass

    elif format_type == 'moved_to_0':
        df = format_by_moving_to_0(df)

    elif format_type == 'all_without_0s':
        df = format_by_removing_non_0s(df)
        
    else :
        raise Exception(f'Wrong format_type input Jan! You input: {format_type}, but has to be one of {POSSIBLE_INPUTS}')

    df = df.reset_index(drop=True)
    return df


def format_by_moving_to_0(df):
    unique_surnames = set()
    current_decreament = 0
    moved_to_0_visit_nr = []
    for surname, visit_nr in zip(df['surname'], df['visit_number']):
        if surname not in unique_surnames:
            unique_surnames.add(surname)
            current_decreament = visit_nr - 1
        moved_to_0_visit_nr.append(visit_nr - current_decreament)

    df['unmoved_visit_nr'] = df['visit_number']
    df['visit_number'] = moved_to_0_visit_nr
    return df

def format_by_removing_non_0s(df):
    df = format_by_moving_to_0(df) # Returns df that has changed visitor_nr to moved_visitor_nr and have old visitor_nr saved as unmoved_visit_nr
    df = df.loc[df['visit_number'] == df['unmoved_visit_nr']] # Gets rid of all moved rows - aka, all people that didnt start from 0
    return df

def get_summed_time_column(df):
    summed_time = []
    current_surname = '1.Gasek'
    current_summed_time = 0
    for surname, time in zip(df.surname, df.time):
        if surname == current_surname:
            current_summed_time+=time
        else:
            current_surname = surname
            current_summed_time = time
        summed_time.append(current_summed_time)
    df['summed_time'] = summed_time
    return df


def get_visits_after_wait_time_x(df_, x, limit_on = True):
    '''
    df - pd.DataFrame with data
    x - int time after visits (put a min limit to x - to be 90 days), althought that limit can be turned off
    '''
    if limit_on:
        if x < 90:
            raise Exception('The min x limit is on. The X (nr of days) should be 90 or bigger.')


    # Get data
    df = get_data(format_type='all')
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