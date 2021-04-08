import XLake

inflows_path = 'Inflows'
outflows_path = 'outflows'
Tempath = 'TemLight/WaterTemperature.csv'
Lightpath = 'TemLight/Light.csv'
V_path = 'Storage/V_Erie.csv'
Parapath = 'Parameters.csv'
initial_values = [0.2,0.10,0.01]
t_span = (0,153)
t_eval = [i for i in range(153)]
method = 'RK45'


W_tkn, W_tp, W_chla = XLake.net_loading(inflows_path, outflows_path)

N,P,chl = XLake.predict(t_span, initial_values, method, t_eval, (W_tp, W_tkn, W_chla), Tempath, Lightpath, V_path, Parapath)

print(N,P,chl)