from datetime import datetime as dt    
import numpy as np
import pandas as pd

class cust_seg:
    def __init__(self, df,today_date):
        self.df = df
        self.today_date=today_date
    
    def Daily (self):
        df=self.df
        # Convert data types of specific columns to strings
        df[["VISIT_ID", "SKU_ID", "SKU_DESC", "DEPT_DESC"]] = df[["VISIT_ID", "SKU_ID", "SKU_DESC", "DEPT_DESC"]].astype("string")
        # Convert CUST_ID to integer
        df["CUST_ID"] = df["CUST_ID"].astype(int)
        # Defining today date as max(InvoiceDate) + 2 days
        #date_input = input("Enter a date in the format YYYY-MM-DD: ")
        today_date = dt.strptime(self.today_date, "%Y-%m-%d")
        df["VISIT_DT"]=pd.to_datetime(df["VISIT_DT"],format='%Y-%m-%d')
        df['week']=pd.PeriodIndex(df.VISIT_DT, freq='W')
        df['day']=pd.PeriodIndex(df.VISIT_DT, freq='D')
        df_pivot = self.df.pivot_table(index='CUST_ID', columns='week', aggfunc={'VISIT_DT': 'nunique'}, fill_value=0)
        # Format pivot table
        df_pivot.columns = df_pivot.columns.droplevel(0)  # remove date
        df_pivot.columns.name = None  # remove week
        for i in df_pivot.index:
            for j in df_pivot.columns:
                if df_pivot.loc[i, j] >= 1:
                    break
                else:
                    df_pivot.loc[i][j] = -1
        # Replace -1 (indicating no purchase) with NaN
        df_pivot = df_pivot.replace(-1, np.nan)
        perc_25 = np.nanquantile(df_pivot, 0.25, axis=1)
        df_perc_25 = pd.DataFrame()
        df_perc_25["CUST_ID"] = df_pivot.index
        df_perc_25["Perc_25"] = perc_25
        df_daily = df_perc_25[df_perc_25["Perc_25"] >1.0]
        df_daily.drop(columns = {"Perc_25"}, axis=1, inplace=True)
        #RFM Calculation 
        rfm = df.groupby("CUST_ID").agg({"VISIT_DT":lambda date: (today_date - date.max()).days,
                                    "VISIT_ID": lambda num: num.nunique(),
                                    "SALES": lambda price: price.sum()}) #total price per customer
        rfm.columns = ['Recency', 'Frequency', "Monetary"]
        rfm_daily=rfm[rfm["Recency"]<30]
        self.df_daily_active= rfm_daily[rfm_daily.index.isin(df_daily["CUST_ID"])]
        rfm_daily_inactive=rfm[rfm["Recency"]>30]
        df_daily_inactive = rfm_daily_inactive[rfm_daily_inactive.index.isin(df_daily.CUST_ID)]
        q2_F=self.df_daily_active["Frequency"].quantile(0.50)
        q2_M = self.df_daily_active["Monetary"].quantile(0.50)
        # create a list of our conditions
        conditions = [
            (self.df_daily_active['Frequency'] <= q2_F) & (self.df_daily_active['Monetary']<=q2_M),
            (self.df_daily_active['Frequency'] <= q2_F) & (self.df_daily_active['Monetary']>q2_M),
            (self.df_daily_active['Frequency']>q2_F) & (self.df_daily_active['Monetary']<=q2_M),
            (self.df_daily_active['Frequency']>q2_F) & (self.df_daily_active['Monetary']>q2_M)
            ]
        # create a list of the values we want to assign for each condition
        values = ['LFLM', 'LFHM', 'HFLM', 'HFHM']
        # create a new column and use np.select to assign values to it using our lists as arguments
        self.df_daily_active['Customer_segments'] = np.select(conditions, values)
        df_daily_active_fn=self.df_daily_active.groupby('Customer_segments').median().rename(columns= {'Recency':"Median Recency","Frequency":"Median Frequency","Monetary":'Median Monetary'}).join(self.df_daily_active.Customer_segments.value_counts().rename('count'))
        return self.df_daily_active.round(2),df_daily_inactive.round(2),df_daily_active_fn.round(2)
    
    def Weekly (self):
        df=self.df
        # Convert data types of specific columns to strings
        df[["VISIT_ID", "SKU_ID", "SKU_DESC", "DEPT_DESC"]] = df[["VISIT_ID", "SKU_ID", "SKU_DESC", "DEPT_DESC"]].astype("string")
        # Convert CUST_ID to integer
        df["CUST_ID"] = df["CUST_ID"].astype(int)
        # Defining today date as max(InvoiceDate) + 2 days
        #date_input = input("Enter a date in the format YYYY-MM-DD: ")
        today_date = dt.strptime(self.today_date, "%Y-%m-%d")
        df["VISIT_DT"]=pd.to_datetime(df["VISIT_DT"],format='%Y-%m-%d')
        df['month']=pd.PeriodIndex(df.VISIT_DT, freq='M')
        df['week']=pd.PeriodIndex(df.VISIT_DT, freq='W')
        df['day']=pd.PeriodIndex(df.VISIT_DT, freq='D')
        df_pivot = self.df.pivot_table(index='CUST_ID', columns='week', aggfunc={'VISIT_DT': 'nunique'}, fill_value=0)
        # Format pivot table
        df_pivot.columns = df_pivot.columns.droplevel(0)  # remove date
        df_pivot.columns.name = None  # remove week
        for i in df_pivot.index:
            for j in df_pivot.columns:
                if df_pivot.loc[i, j] >= 1:
                    break
                else:
                    df_pivot.loc[i][j] = -1
        # Replace -1 (indicating no purchase) with NaN
        df_pivot = df_pivot.replace(-1, np.nan)
        perc_25 = np.nanquantile(df_pivot, 0.25, axis=1)
        df_perc_25=pd.DataFrame(perc_25).reset_index()
        df_perc_25.columns=["Customer ID","Perc_25"]
        df_perc_25["CUST_ID"]=df_pivot.index
        df_perc_25 = pd.DataFrame()     
        df_perc_25["CUST_ID"] = df_pivot.index  
        df_perc_25["Perc_25"] = perc_25    
        df_nondaily = df_perc_25[df_perc_25["Perc_25"] <=1.0] 
        #df_daily = df_perc_25[df_perc_25["Perc_25"] >=2.00]
        df_sub = df[df['CUST_ID'].isin(df_nondaily["CUST_ID"])]
        df_pivot = df_sub.pivot_table(index='CUST_ID', columns='month', aggfunc={'VISIT_DT': 'nunique'}, fill_value=0)
        df_pivot.columns = df_pivot.columns.droplevel(0)  # remove date
        df_pivot.columns.name = None  # remove week
        for i in df_pivot.index:
            for j in df_pivot.columns:
                if df_pivot.loc[i, j] >= 1:
                    break
                else:
                    df_pivot.loc[i][j] = -1
        # Replace -1 (indicating no purchase) with NaN
        df_pivot = df_pivot.replace(-1, np.nan)
        # 25th percentile of number of purchase days for each customer
        perc_25=np.nanquantile(df_pivot, 0.25, axis=1)
        df_perc_25=pd.DataFrame()
        df_perc_25["CUST_ID"]=df_pivot.index
        df_perc_25["Perc_25"]=perc_25
        df_weekly = df_perc_25[df_perc_25["Perc_25"] >= 2.0]
        #RFM Calculation 
        rfm = df.groupby("CUST_ID").agg({"VISIT_DT":lambda date: (today_date - date.max()).days,
                                    "VISIT_ID": lambda num: num.nunique(),
                                    "SALES": lambda price: price.sum()}) #total price per customer
        rfm.columns = ['Recency', 'Frequency', "Monetary"]
        df_weekly.drop(columns = {"Perc_25"}, axis=1, inplace=True)
        rfm_weekly_active=rfm[rfm["Recency"]<60]
        df_weekly_active= rfm_weekly_active[rfm_weekly_active.index.isin(df_weekly["CUST_ID"])]
        rfm_weekly_inactive=rfm[rfm["Recency"]>=60]
        df_weekly_inactive = rfm_weekly_inactive[rfm_weekly_inactive.index.isin(df_weekly.CUST_ID)]
        q2_F=df_weekly_active["Frequency"].quantile(0.50)
        q2_M = df_weekly_active["Monetary"].quantile(0.50)
        # create a list of our conditions
        conditions = [
            (df_weekly_active['Frequency'] <= q2_F) & (df_weekly_active['Monetary']<=q2_M),
            (df_weekly_active['Frequency'] <= q2_F) & (df_weekly_active['Monetary']>q2_M),
            (df_weekly_active['Frequency']>q2_F) & (df_weekly_active['Monetary']<=q2_M),
            (df_weekly_active['Frequency']>q2_F) & (df_weekly_active['Monetary']>q2_M)
            ]
        # create a list of the values we want to assign for each condition
        values = ['LFLM', 'LFHM', 'HFLM', 'HFHM']
        # create a new column and use np.select to assign values to it using our lists as arguments
        df_weekly_active['Customer_segments'] = np.select(conditions, values)
        df_weekly_active_fn=df_weekly_active.groupby('Customer_segments').median().rename(columns= {'Recency':"Median Recency","Frequency":"Median Frequency","Monetary":'Median Monetary'}).join(df_weekly_active.Customer_segments.value_counts().rename('count'))
        return df_weekly_active.round(2),df_weekly_inactive.round(2),df_weekly_active_fn.round(2)
    
    def Monthly (self):
        df=self.df
        # Convert data types of specific columns to strings
        df[["VISIT_ID", "SKU_ID", "SKU_DESC", "DEPT_DESC"]] = df[["VISIT_ID", "SKU_ID", "SKU_DESC", "DEPT_DESC"]].astype("string")
        # Convert CUST_ID to integer
        df["CUST_ID"] = df["CUST_ID"].astype(int)
        # Defining today date as max(InvoiceDate) + 2 days
        #date_input = input("Enter a date in the format YYYY-MM-DD: ")
        today_date = dt.strptime(self.today_date, "%Y-%m-%d")
        df["VISIT_DT"]=pd.to_datetime(df["VISIT_DT"],format='%Y-%m-%d')
        df['quarter'] = pd.PeriodIndex(df.VISIT_DT, freq='Q')
        df['month']=pd.PeriodIndex(df.VISIT_DT, freq='M')
        df['week']=pd.PeriodIndex(df.VISIT_DT, freq='W')
        df['day']=pd.PeriodIndex(df.VISIT_DT, freq='D')
        df_pivot = self.df.pivot_table(index='CUST_ID', columns='week', aggfunc={'VISIT_DT': 'nunique'}, fill_value=0)
        # Format pivot table
        df_pivot.columns = df_pivot.columns.droplevel(0)  # remove date
        df_pivot.columns.name = None  # remove week
        for i in df_pivot.index:
            for j in df_pivot.columns:
                if df_pivot.loc[i, j] >= 1:
                    break
                else:
                    df_pivot.loc[i][j] = -1
        # Replace -1 (indicating no purchase) with NaN
        df_pivot = df_pivot.replace(-1, np.nan)
        perc_25 = np.nanquantile(df_pivot, 0.25, axis=1)
        df_perc_25=pd.DataFrame(perc_25).reset_index()
        df_perc_25.columns=["Customer ID","Perc_25"]
        df_perc_25["CUST_ID"]=df_pivot.index
        df_perc_25 = pd.DataFrame()     
        df_perc_25["CUST_ID"] = df_pivot.index  
        df_perc_25["Perc_25"] = perc_25    
        df_nondaily = df_perc_25[df_perc_25["Perc_25"] <=1.0] 
        #df_daily = df_perc_25[df_perc_25["Perc_25"] >=2.00]
        df_sub = df[df['CUST_ID'].isin(df_nondaily["CUST_ID"])]
        df_pivot = df_sub.pivot_table(index='CUST_ID', columns='month', aggfunc={'VISIT_DT': 'nunique'}, fill_value=0)
        df_pivot.columns = df_pivot.columns.droplevel(0)  # remove date
        df_pivot.columns.name = None  # remove week
        for i in df_pivot.index:
            for j in df_pivot.columns:
                if df_pivot.loc[i, j] >= 1:
                    break
                else:
                    df_pivot.loc[i][j] = -1
        # Replace -1 (indicating no purchase) with NaN
        df_pivot = df_pivot.replace(-1, np.nan)
        # 25th percentile of number of purchase days for each customer
        perc_25=np.nanquantile(df_pivot, 0.25, axis=1)
        df_perc_25=pd.DataFrame()
        df_perc_25["CUST_ID"]=df_pivot.index
        df_perc_25["Perc_25"]=perc_25
        df_nonweekly = df_perc_25[df_perc_25["Perc_25"] < 2.0]
        #df_weekly = df_perc_25[df_perc_25["Perc_25"] >= 2.0]
        df_nonweekly.drop(columns = {"Perc_25"}, axis=1, inplace=True)
        df_sub= df[df['CUST_ID'].isin(df_nonweekly["CUST_ID"])]
        df_pivot = df_sub.pivot_table(index='CUST_ID', columns='quarter', aggfunc={'VISIT_DT': 'nunique'}, fill_value=0)
        df_pivot.columns = df_pivot.columns.droplevel(0)  # remove date
        df_pivot.columns.name = None  # remove week
        for i in df_pivot.index:
            for j in df_pivot.columns:
                if df_pivot.loc[i, j] >= 1:
                    break
                else:
                    df_pivot.loc[i][j] = -1
        # Replace -1 (indicating no purchase) with NaN
        df_pivot = df_pivot.replace(-1, np.nan)
        perc_25=np.nanquantile(df_pivot, 0.25, axis=1)
        df_perc_25=pd.DataFrame()
        df_perc_25["CUST_ID"]=df_pivot.index
        df_perc_25["Perc_25"]=perc_25
        df_monthly = df_perc_25[df_perc_25["Perc_25"] >=2.0]
        #RFM Calculation 
        rfm = df.groupby("CUST_ID").agg({"VISIT_DT":lambda date: (today_date - date.max()).days,
                                    "VISIT_ID": lambda num: num.nunique(),
                                    "SALES": lambda price: price.sum()}) #total price per customer

        #rfm.columns = rfm.columns.droplevel(0)
        rfm.columns = ['Recency', 'Frequency', "Monetary"]
        df_monthly.drop(columns = {"Perc_25"}, axis=1, inplace=True)
        rfm_monthly_active=rfm[rfm["Recency"]<90]
        df_monthly_active= rfm_monthly_active[rfm_monthly_active.index.isin(df_monthly["CUST_ID"])]
        rfm_monthly_inactive=rfm[rfm["Recency"]>=90]
        df_monthly_inactive= rfm_monthly_inactive[rfm_monthly_inactive.index.isin(df_monthly.CUST_ID)]
        q2_F=df_monthly_active["Frequency"].quantile(0.50)
        q2_M = df_monthly_active["Monetary"].quantile(0.50)
        # create a list of our conditions
        conditions = [
            (df_monthly_active['Frequency'] <= q2_F) & (df_monthly_active['Monetary']<=q2_M),
            (df_monthly_active['Frequency'] <= q2_F) & (df_monthly_active['Monetary']>q2_M),
            (df_monthly_active['Frequency']>q2_F) & (df_monthly_active['Monetary']<=q2_M),
            (df_monthly_active['Frequency']>q2_F) & (df_monthly_active['Monetary']>q2_M)
            ]
        # create a list of the values we want to assign for each condition
        values = ['LFLM', 'LFHM', 'HFLM', 'HFHM']
        # create a new column and use np.select to assign values to it using our lists as arguments
        df_monthly_active['Customer_segments'] = np.select(conditions, values)
        df_monthly_active_fn=df_monthly_active.groupby('Customer_segments').median().rename(columns={"Recency":"Median Recency","Frequency":"Median Frequency","Monetary":"Median Monetary"}).join(df_monthly_active.Customer_segments.value_counts().rename('count'))
        return df_monthly_active.round(2),df_monthly_inactive.round(2),df_monthly_active_fn.round(2)
    
    def Quarterly (self):
        df=self.df
        # Convert data types of specific columns to strings
        df[["VISIT_ID", "SKU_ID", "SKU_DESC", "DEPT_DESC"]] = df[["VISIT_ID", "SKU_ID", "SKU_DESC", "DEPT_DESC"]].astype("string")
        # Convert CUST_ID to integer
        df["CUST_ID"] = df["CUST_ID"].astype(int)
        # Defining today date as max(InvoiceDate) + 2 days
        #date_input = input("Enter a date in the format YYYY-MM-DD: ")
        today_date = dt.strptime(self.today_date, "%Y-%m-%d")
        df["VISIT_DT"]=pd.to_datetime(df["VISIT_DT"],format='%Y-%m-%d')
        df['year']=pd.PeriodIndex(df.VISIT_DT,freq='Y')
        df['quarter'] = pd.PeriodIndex(df.VISIT_DT, freq='Q')
        df['month']=pd.PeriodIndex(df.VISIT_DT, freq='M')
        df['week']=pd.PeriodIndex(df.VISIT_DT, freq='W')
        df['day']=pd.PeriodIndex(df.VISIT_DT, freq='D')
        df_pivot = self.df.pivot_table(index='CUST_ID', columns='week', aggfunc={'VISIT_DT': 'nunique'}, fill_value=0)
        # Format pivot table
        df_pivot.columns = df_pivot.columns.droplevel(0)  # remove date
        df_pivot.columns.name = None  # remove week
        for i in df_pivot.index:
            for j in df_pivot.columns:
                if df_pivot.loc[i, j] >= 1:
                    break
                else:
                    df_pivot.loc[i][j] = -1
        # Replace -1 (indicating no purchase) with NaN
        df_pivot = df_pivot.replace(-1, np.nan)
        perc_25 = np.nanquantile(df_pivot, 0.25, axis=1)
        df_perc_25=pd.DataFrame(perc_25).reset_index()
        df_perc_25.columns=["Customer ID","Perc_25"]
        df_perc_25["CUST_ID"]=df_pivot.index
        df_perc_25 = pd.DataFrame()     
        df_perc_25["CUST_ID"] = df_pivot.index  
        df_perc_25["Perc_25"] = perc_25    
        df_nondaily = df_perc_25[df_perc_25["Perc_25"] <=1.0] 
        #df_daily = df_perc_25[df_perc_25["Perc_25"] >=2.00]
        df_sub = df[df['CUST_ID'].isin(df_nondaily["CUST_ID"])]
        df_pivot = df_sub.pivot_table(index='CUST_ID', columns='month', aggfunc={'VISIT_DT': 'nunique'}, fill_value=0)
        df_pivot.columns = df_pivot.columns.droplevel(0)  # remove date
        df_pivot.columns.name = None  # remove week
        for i in df_pivot.index:
            for j in df_pivot.columns:
                if df_pivot.loc[i, j] >= 1:
                    break
                else:
                    df_pivot.loc[i][j] = -1
        # Replace -1 (indicating no purchase) with NaN
        df_pivot = df_pivot.replace(-1, np.nan)
        # 25th percentile of number of purchase days for each customer
        perc_25=np.nanquantile(df_pivot, 0.25, axis=1)
        df_perc_25=pd.DataFrame()
        df_perc_25["CUST_ID"]=df_pivot.index
        df_perc_25["Perc_25"]=perc_25
        df_nonweekly = df_perc_25[df_perc_25["Perc_25"] < 2.0]
        #df_weekly = df_perc_25[df_perc_25["Perc_25"] >= 2.0]
        df_nonweekly.drop(columns = {"Perc_25"}, axis=1, inplace=True)
        df_sub= df[df['CUST_ID'].isin(df_nonweekly["CUST_ID"])]
        df_pivot = df_sub.pivot_table(index='CUST_ID', columns='quarter', aggfunc={'VISIT_DT': 'nunique'}, fill_value=0)
        df_pivot.columns = df_pivot.columns.droplevel(0)  # remove date
        df_pivot.columns.name = None  # remove week
        for i in df_pivot.index:
            for j in df_pivot.columns:
                if df_pivot.loc[i, j] >= 1:
                    break
                else:
                    df_pivot.loc[i][j] = -1
        # Replace -1 (indicating no purchase) with NaN
        df_pivot = df_pivot.replace(-1, np.nan)
        perc_25=np.nanquantile(df_pivot, 0.25, axis=1)
        df_perc_25=pd.DataFrame()
        df_perc_25["CUST_ID"]=df_pivot.index
        df_perc_25["Perc_25"]=perc_25
        df_nonmonthly = df_perc_25[df_perc_25["Perc_25"] <2.0]
        df_nonmonthly.drop(columns = {"Perc_25"}, axis=1, inplace=True)
        df_sub= df[df['CUST_ID'].isin(df_nonmonthly["CUST_ID"])]
        df_pivot = df_sub.pivot_table(index='CUST_ID', columns='year', aggfunc={'VISIT_DT': 'nunique'}, fill_value=0)
        df_pivot.columns = df_pivot.columns.droplevel(0)  # remove date
        df_pivot.columns.name = None  # remove week
        # Replace redundant values before the first purchase for each customer
        for i in df_pivot.index:
            for j in df_pivot.columns:
                if df_pivot.loc[i, j] >= 1:
                    break
                else:
                    df_pivot.loc[i][j] = -1
        # Replace -1 (indicating no purchase) with NaN
        df_pivot = df_pivot.replace(-1, np.nan)
        perc_25=np.nanquantile(df_pivot, 0.25, axis=1)
        df_perc_25=pd.DataFrame()
        df_perc_25["CUST_ID"]=df_pivot.index
        df_perc_25["Perc_25"]=perc_25
        df_quarterly = df_perc_25[df_perc_25["Perc_25"] >=3.0]
        #RFM Calculation 
        rfm = df.groupby("CUST_ID").agg({"VISIT_DT":lambda date: (today_date - date.max()).days,
                                    "VISIT_ID": lambda num: num.nunique(),
                                    "SALES": lambda price: price.sum()}) #total price per customer
        rfm.columns = ['Recency', 'Frequency', "Monetary"]
        df_quarterly.drop(columns = {"Perc_25"}, axis=1, inplace=True)
        rfm_quarterly_active=rfm[rfm["Recency"]<180]
        df_quarterly_active = rfm_quarterly_active[rfm_quarterly_active.index.isin(df_quarterly["CUST_ID"])]
        rfm_quarterly_inactive=rfm[rfm["Recency"]>=180]
        df_quarterly_inactive = rfm_quarterly_inactive[rfm_quarterly_inactive.index.isin(df_quarterly["CUST_ID"])]
        q2_F=df_quarterly_active["Frequency"].quantile(0.50)
        q2_M = df_quarterly_active["Monetary"].quantile(0.50)
        # create a list of our conditions
        conditions = [
            (df_quarterly_active['Frequency'] <= q2_F) & (df_quarterly_active['Monetary']<=q2_M),
            (df_quarterly_active['Frequency'] <= q2_F) & (df_quarterly_active['Monetary']>q2_M),
            (df_quarterly_active['Frequency']>q2_F) & (df_quarterly_active['Monetary']<=q2_M),
            (df_quarterly_active['Frequency']>q2_F) & (df_quarterly_active['Monetary']>q2_M)
            ]
        # create a list of the values we want to assign for each condition
        values = ['LFLM', 'LFHM', 'HFLM', 'HFHM']
        # create a new column and use np.select to assign values to it using our lists as arguments
        df_quarterly_active['Customer_segments'] = np.select(conditions, values)
        df_quarterly_active_fn=df_quarterly_active.groupby('Customer_segments').median().rename(columns={"Recency":"Median Recency","Frequency":"Median Frequency","Monetary":"Median Monetary"}).join(df_quarterly_active.Customer_segments.value_counts().rename('count'))
        return df_quarterly_active.round(2),df_quarterly_inactive.round(2),df_quarterly_active_fn.round(2)