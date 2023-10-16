import numpy as np
import pandas as pd
import holidays


def generate_holiday_df(dfs,years):
    """
    Generates a dataframe with the holidays for the given years and subdivisions. Is used in the function get_es_holidays

    Parameters
    ----------
    dfs: list
        List of dataframes with the holidays for each subdivision
    years: list
        List of years to obtain the holidays
    
    Returns
    -------
    pandas.DataFrame
        A dataframe with the holidays for the given years and subdivisions
    """
    df_hol=pd.concat(dfs).sort_index()
    df_hol['next_day']=df_hol.index+pd.Timedelta(days=1)
    years = df_hol.index.year.unique()
    index_=pd.date_range(start=str(min(years))+'-01-01', end=str(max(years)+1)+'-01-01', freq='H')[:-1]
    df_hol_hour_=pd.DataFrame(index=index_)
    df_hol_hour_['holiday_date']=df_hol_hour_.index.date
    df_hol_hour=df_hol_hour_.holiday_date.isin(df_hol.index.date)+(df_hol_hour_.index.dayofweek==6)
    df_hol_hour=df_hol_hour.to_frame()
    df_hol_hour["post_holiday_date"]=df_hol_hour_.holiday_date.isin(df_hol.next_day.dt.date.values)+(df_hol_hour_.index.dayofweek==0)
    return df_hol_hour



#obtain the spanish holidays
def get_es_holidays(years,subdivs=["MD","CT","AN","VC"]):
    """
    Returns a dataframe with the spanish holidays for the given years and subdivisions
    
    Parameters
    ----------
    years: list
        List of years to obtain the holidays
    subdivs: list
        List of subdivisions to obtain the holidays. If None, the holidays for the whole country are returned.
        The subdivisions are:
        AN, AR, AS, CB, CE, CL, CM, CN, CT, EX, GA, IB, MC, MD, ML, NC, PV, RI, VC
        AR(ARAGON), AS(ASTURIAS),MC (MURCIA), NC (NAVARRA), RI (RIOJA), PV (PAIS VASCO), ML (MELILLA),
        CB (CANTABRIA), CL (CASTILLA Y LEON), CM (CASTILLA LA MANCHA), CN (CANARIAS), CT (CATALUÑA), EX (EXTREMADURA), GA (GALICIA), IB (ISLAS BALEARES), MD (MADRID), AN (ANDALUCIA), VC (VALENCIA), CE (CEUTA)

    Returns
    -------
    pandas.DataFrame
        A dataframe with the holidays for the given years and subdivisions
    """
    dfs=[]
    dfs_strong=[]
    for year in years:

        if subdivs is not None and isinstance(subdivs, list):
            #generate the holidays for each region
            dfs_subdivs = []
            for subdiv in subdivs:
                subvid_holidays = holidays.ES(years=year,subdiv=subdiv)
                subvid_holidays_df = pd.DataFrame.from_dict(subvid_holidays, orient='index', columns=['holiday'])
                subvid_holidays_df = subvid_holidays_df.reset_index()
                subvid_holidays_df = subvid_holidays_df.rename(columns={'index':'ds'})
                subvid_holidays_df['ds'] = pd.to_datetime(subvid_holidays_df['ds'])
                dfs_subdivs.append(subvid_holidays_df)
            holidays_df=pd.concat(dfs_subdivs)
            holidays_df.drop_duplicates(subset=['ds'], keep='first', inplace=True)
            holidays_df.sort_values(by=['ds'], inplace=True)
            holidays_df.set_index('ds', inplace=True)
            dfs.append(holidays_df)
        
        #generate the holidays for the whole country
        es_holidays = holidays.ES(years=year)
        es_holidays_df = pd.DataFrame.from_dict(es_holidays, orient='index', columns=['holiday'])
        es_holidays_df = es_holidays_df.reset_index()
        es_holidays_df = es_holidays_df.rename(columns={'index':'ds'})
        es_holidays_df['ds'] = pd.to_datetime(es_holidays_df['ds'])
        es_holidays_df.sort_values(by=['ds'], inplace=True)
        es_holidays_df.set_index('ds', inplace=True)
        dfs_strong.append(es_holidays_df)
    
    #generate an hourly index depending on the years
    df_hol_strong=generate_holiday_df(dfs_strong,years)
    df_hol_strong.rename(columns={'holiday_date':'H_NA',"post_holiday_date":"P_NA"}, inplace=True)
    df_hol_hour = generate_holiday_df(dfs,years)
    subdivs.append("ES")
    df_hol_hour.rename(columns={'holiday_date':f'holiday_date_{subdivs}',f"post_holiday_date":f'post_holiday_date{subdivs}'}, inplace=True)
    df_hol_hour = pd.merge(df_hol_hour,df_hol_strong,how='left',left_index=True,right_index=True)

    return df_hol_hour



def get_es_holiday_classification(date_start,date_end):
    date_start = pd.to_datetime(date_start)
    date_end = pd.to_datetime(date_end)
    #generate a list with the years between the start and end date
    years = list(range(date_start.year,date_end.year+1))
    df1=get_es_holidays(years=years,subdivs=["MD","CT","AN","VC"])

    df1["H_ST"]=df1["holiday_date_['MD', 'CT', 'AN', 'VC', 'ES']"] ^ df1["H_NA"]
    df1["P_ST"]=df1["post_holiday_date['MD', 'CT', 'AN', 'VC', 'ES']"] ^ df1["P_NA"]

    df2=get_es_holidays(years=years,subdivs=["GA","PV","CL","CM","AR","AS","MC"])
    df2["H_NO"]=df2["holiday_date_['GA', 'PV', 'CL', 'CM', 'AR', 'AS', 'MC', 'ES']"] ^ df2["H_NA"]
    df2["P_NO"]=df2["post_holiday_date['GA', 'PV', 'CL', 'CM', 'AR', 'AS', 'MC', 'ES']"] ^ df2["P_NA"]
    df2.drop(columns=["H_NA","P_NA","holiday_date_['GA', 'PV', 'CL', 'CM', 'AR', 'AS', 'MC', 'ES']","post_holiday_date['GA', 'PV', 'CL', 'CM', 'AR', 'AS', 'MC', 'ES']"], inplace=True)

    
    df3=get_es_holidays(years=years,subdivs=["CB","EX","NC","RI"])

    df3["H_W"]=df3["holiday_date_['CB', 'EX', 'NC', 'RI', 'ES']"] ^ df3["H_NA"]
    df3["P_W"]=df3["post_holiday_date['CB', 'EX', 'NC', 'RI', 'ES']"] ^ df3["P_NA"]
    df3.drop(columns=["H_NA","P_NA","holiday_date_['CB', 'EX', 'NC', 'RI', 'ES']","post_holiday_date['CB', 'EX', 'NC', 'RI', 'ES']"], inplace=True)

    df=pd.merge(df1,df2,how='left',left_index=True,right_index=True)
    df=pd.merge(df,df3,how='left',left_index=True,right_index=True)
    df=df.iloc[:,2:]
    df["DS"]=df.index.dayofweek==5
    df["classification_1"]=""

    for i in range(len(df)):
        if df.iloc[i, 0]==True: # Si es Holiday Nacional siempre será Holiday Nacional
            df.iloc[i,-1]="H_NA"

        elif df.iloc[i,0]==False and df.iloc[i,2]==True : #Si es Holiday Strong 
            if  df.iloc[i,8]==True: #Si es Holiday Strong y Weak y es sABADO l será Holiday Nacional
                df.iloc[i,-1]="H_NA"
            else: #Si es Holiday Strong  y no es sabado será Holiday Strong
                df.iloc[i,-1]="H_ST"
        #Ahora si solo es Post Festivo Nacional
        elif df.iloc[i,0]==False and df.iloc[i,2]==False and df.iloc[i,4]==False and df.iloc[i,6]==False and df.iloc[i,1]==True: #Si es Post Holiday Nacional
            df.iloc[i,-1]="P_NA"
        elif df.iloc[i,0]==False and df.iloc[i,2]==False and df.iloc[i,4]==False and df.iloc[i,6]==False and df.iloc[i,1]==False and df.iloc[i,3]==True: #Si es Post Holiday Strong
                df.iloc[i,-1]="P_ST"
        elif df.iloc[i,0]==False and df.iloc[i,2]==False and df.iloc[i,4]==False and df.iloc[i,6]==False and df.iloc[i,1]==False and df.iloc[i,3]==False and df.iloc[i,5]==False and df.iloc[i,8]==True: #Si es Post Holiday Normal
                df.iloc[i,-1]="DS"
        else:
            df.iloc[i,-1]="D"
    # Generate classification_only_nationals column
    df["classification_only_nationals"]=""

    # vectorize the conditionals using NumPy
    conditionals = [
        (df.iloc[:, 0] == True),
        (df.iloc[:, 1] == True),
        (df.iloc[:,8]==True),
        np.ones(len(df), dtype=bool),
    ]

    # vectorize the values to set for "only_nationals" based on the conditionals
    values = [
        "H_NA",
        "P_NA",
        "DS",
        "D",
    ]

    # use NumPy's select function to set "only_nationals" based on the conditionals
    df["classification_only_nationals"] = np.select(conditionals, values)

    # update the DataFrame in place using .iloc
    df.iloc[:, -1] = df["classification_only_nationals"]

    df.drop(columns=["H_NA","P_NA","H_ST","P_ST","H_NO","P_NO","H_W","P_W","DS"], inplace=True)

    return df.loc[date_start.strftime("%Y-%m-%d"):date_end.strftime("%Y-%m-%d")]
