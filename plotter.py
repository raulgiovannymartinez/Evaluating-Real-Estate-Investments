import matplotlib.pyplot as plt
plt.rcParams['font.size'] = '14'

def plot_monthly_installments(df):
    
    for p in df.property_name.unique():
        df_temp = df[df.property_name==p]
        
        fig, ax1 = plt.subplots(figsize=(15, 10))

        colors = ['green', 'blue', 'orange', 'black']
        for idx, col in enumerate(['principal_payment', 'mortgage_payment', 'interest_payment', 'rent_profit']):
            ax1.plot(df_temp.months, df_temp[col], label=col, color=colors[idx])

        ax1.set_xlabel("month")
        ax1.set_ylabel("amount ($)")
        ax1.legend(bbox_to_anchor=(1.1,1), loc="upper left")

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        ax2.plot(df_temp.months, df_temp['remaining_principal'], label='remaining_principal', color='red')
        ax2.tick_params(axis='y', labelcolor='tab:red')
        ax2.legend(bbox_to_anchor=(1.1,0.8), loc="upper left")

        plt.tight_layout()
        plt.savefig('./plots/monthly_installments-{}.png'.format(p))


