import pandas as pd

class SlaDetermination:
    def __init__(self, df_selected):
        self.df_selected = df_selected

    def calculate_sla(self, st, et):
        df_sale = self.df_selected[(self.df_selected.saleflag == 1) & ((self.df_selected.order_date >= st) & (self.df_selected.order_date < et))]
        df_sale_perc = pd.DataFrame(data=df_sale['Lead2FirstIntr_datedifference_Minute'].quantile(q=[i/100 for i in range(75, 96)]))

        df_nosale = self.df_selected[(self.df_selected.saleflag == 0) & ((self.df_selected.lead_date >= st) & (self.df_selected.lead_date < et))]
        df_nosale_perc = pd.DataFrame(data=df_nosale['Lead2FirstIntr_datedifference_Minute'].quantile(q=[i/100 for i in range(75, 96)]))

        df_perc_diff = df_nosale_perc.Lead2FirstIntr_datedifference_Minute - df_sale_perc.Lead2FirstIntr_datedifference_Minute
        diff = pd.DataFrame(df_perc_diff)

        df_describe_sale = df_sale.describe()[["Lead2FirstIntr_datedifference_Minute"]].round(0)
        df_describe_sale = pd.concat([df_describe_sale.loc[['min', 'max', 'mean'], :], df_sale_perc.loc[[0.75, 0.80, 0.85, 0.90, 0.95], :]])
        df_describe_sale.index = ['Minimum', 'Maximum', 'Mean', '75th Perc', '80th Perc', '85th Perc', '90th Perc', '95th Perc']
        df_describe_sale.rename(columns={'Lead2FirstIntr_datedifference_Minute': 'Sale'}, inplace=True)

        df_describe_nosale = df_nosale.describe()[["Lead2FirstIntr_datedifference_Minute"]].round(0)
        df_describe_nosale = pd.concat([df_describe_nosale.loc[['min', 'max', 'mean'], :], df_nosale_perc.loc[[0.75, 0.80, 0.85, 0.90, 0.95], :]])
        df_describe_nosale.index = ['Minimum', 'Maximum', 'Mean', '75th Perc', '80th Perc', '85th Perc', '90th Perc', '95th Perc']
        df_describe_nosale.rename(columns={'Lead2FirstIntr_datedifference_Minute': 'Lead'}, inplace=True)
    
        df_table = pd.merge(df_describe_sale, df_describe_nosale, left_index=True, right_index=True)
        df_table = df_table.T.round(0)
        df_table.insert(0, 'Category', ['Sale', 'Non-Sale'])

        return df_sale_perc, df_nosale_perc, diff, df_table
