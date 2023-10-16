import pandas as pd

class SLADetermination:
    def __init__(self, df):
        self.df = df
   
    def filter_and_convert_dates(self, st, et):
        selected_columns = ['Lead2FirstIntr_datedifference_Minute', 'lead_source', 'saleflag', 'salesman_id', 'order_date', 'order_term', 'net_amount', 'matched_table', 'lead_date', 'interactions']
        self.df = self.df[selected_columns]
       
        self.df = self.df[(self.df['saleflag'] == 1) & ((self.df['order_date'] >= st) & (self.df['order_date'] < et))]
       
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])
        self.df['lead_date'] = pd.to_datetime(self.df['lead_date'])
   
    def calculate_lead_to_sale_diff(self):
        self.df['Lead_to_Sale_diff'] = (self.df['order_date'] - self.df['lead_date']).dt.days
        self.df = self.df[self.df['Lead_to_Sale_diff'] > 0]

    def categorize_lead_to_sale_calculate(self):
        bins = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        labels = ['7 days', '8 days', '9 days', '10 days', '11 days', '12 days', '13 days', '14 days', '15 days', '16 days', '17 days']
   
        self.df['Lead_to_Sale_Group'] = pd.cut(self.df['Lead_to_Sale_diff'], bins=bins, labels=labels, right=False)
        self.df_sale_inter = self.df.copy()
       
        bins_int = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        labels = ['2 Interactions', '3 Interactions', '4 Interactions', '5 Interactions', '6 Interactions', '7 Interactions', '8 Interactions', '9 Interactions']
       
        self.df_sale_inter['Lead_to_Sale_Interactions_Group'] = pd.cut(self.df_sale_inter['interactions'], bins=bins_int, labels=labels, right=False)

        self.df_sale_age_cum = self.df.groupby('Lead_to_Sale_Group').size().reset_index(name='Count')
        self.df_sale_age_cum['Cumulative_Count'] = self.df_sale_age_cum['Count'].cumsum()
        self.df_sale_age_cum['Cumulative_Percentage'] = (self.df_sale_age_cum['Count'].cumsum() / self.df_sale_age_cum['Count'].sum()) * 100

        self.df_sale_int_cum = self.df_sale_inter.groupby('Lead_to_Sale_Interactions_Group').size().reset_index(name='Count')
        self.df_sale_int_cum['Cumulative_Count'] = self.df_sale_int_cum['Count'].cumsum()
        self.df_sale_int_cum['Cumulative_Percentage'] = (self.df_sale_int_cum['Count'].cumsum() / self.df_sale_int_cum['Count'].sum()) * 100
   
        return self.df_sale_age_cum, self.df_sale_int_cum