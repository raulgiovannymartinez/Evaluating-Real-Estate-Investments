import pandas as pd
import numpy as np


def get_initial_investment(config_dict):
    property_dict = {}
    for p in config_dict.keys():
        curr_dict = config_dict[p]
        
        if curr_dict['discount_perc'] and curr_dict['discount_perc']>0:
            home_value = curr_dict['home_value']*(100-curr_dict['discount_perc'])/100
        else:
            home_value = curr_dict['home_value']

        property_dict[p] = (home_value*curr_dict['down_payment_perc']/100 + 
                            home_value*curr_dict['service_fee_perc']/100 + 
                            curr_dict['misc_fee_amount'])

    return property_dict



def build_mortgage_investment_plan(config_dict):

    for p in config_dict.keys():
        curr_dict = config_dict[p]

        months = np.arange(1, curr_dict['target_payment_period_yrs']*12+1)
        financed_amnt = curr_dict['home_value']*(100-curr_dict['down_payment_perc'])/100
        
        additions_principal_amnt_month = [(float(i.split(',')[0]), float(i.split(',')[1])) for i in curr_dict['additions_to_principal']]
        
        principal_payment = []
        interest_payment = []
        remaining_principal = []
        mortgage_payment = []

        for m in months:
            # remaining
            if m == 1:
                remaining_principal.append(financed_amnt)
            else:
                remaining_amnt = remaining_principal[-1]-principal_payment[-1]
                remaining_amnt = remaining_amnt if remaining_amnt>0 else 0
                if m in [i[1] for i in additions_principal_amnt_month]: # additions to principal
                    remaining_amnt-= sum([i[0] for i in additions_principal_amnt_month if i[1]==m])
                remaining_principal.append(remaining_amnt)

            # interest
            interest_payment.append(remaining_principal[-1]*curr_dict['interest_perc']/100/12)

            # principal
            monthly_principal = remaining_principal[-1]/(len(months)-m)
            min_payment_allowed = curr_dict['min_morgage_payment']
            if min_payment_allowed and min_payment_allowed>0:
                if ((monthly_principal+interest_payment[-1])<min_payment_allowed) and monthly_principal>0: # min principal payment
                    monthly_principal = min_payment_allowed - interest_payment[-1]
            principal_payment.append(monthly_principal)

        mortgage_payment = np.array(interest_payment) + np.array(principal_payment)
        property_name = [p]*len(mortgage_payment)
        rent_profit = curr_dict['rent_opportunity']-np.array(mortgage_payment)

    df =  pd.DataFrame({'months': months,
                        'principal_payment': principal_payment,
                        'remaining_principal':remaining_principal,
                        'interest_payment': interest_payment,
                        'mortgage_payment': mortgage_payment,
                        'property_name': property_name,
                        'rent_profit':rent_profit}).fillna(0)

    return df 
