from yaml import load, FullLoader
from analysis_provider import get_initial_investment, build_mortgage_investment_plan
import plotter

config_dict = load(open('config.yaml'), Loader=FullLoader)

print(get_initial_investment(config_dict))

df_mortgage = build_mortgage_investment_plan(config_dict)
df_mortgage.to_csv('./data/mortgage_plan.csv', index=False)

plotter.plot_monthly_installments(df_mortgage)


