import time, requests


GMT_OFFSET = -3 * 3600  # 3 horas en segundos

# Convertir la fecha y hora de inicio y fin de los períodos a tiempo UNIX
ts_doce2024 = time.mktime(time.strptime("2024-03-01 12:00:00", "%Y-%m-%d %H:%M:%S")) + GMT_OFFSET
ts_trece2024 = time.mktime(time.strptime("2024-03-01 13:00:00", "%Y-%m-%d %H:%M:%S")) + GMT_OFFSET
ts_doce2023 = time.mktime(time.strptime("2023-03-01 12:00:00", "%Y-%m-%d %H:%M:%S")) + GMT_OFFSET
ts_trece2023 = time.mktime(time.strptime("2023-03-01 13:00:00", "%Y-%m-%d %H:%M:%S")) + GMT_OFFSET


# Realizar solicitudes a la API para obtener las transacciones en el mercado BTC-CLP
market_id = 'btc-clp'
url = f'https://www.buda.com/api/v2/markets/{market_id}/trades'
response2024 = requests.get(url, params={
    'timestamp': int(ts_trece2024) * 1000,
    'last_timestamp': int(ts_doce2024) * 1000
})
trades2024 = response2024.json()

response2023 = requests.get(url, params={
    'timestamp': int(ts_trece2023) * 1000,
    'last_timestamp': int(ts_doce2023) * 1000
})
trades2023 = response2023.json()


# Inicializar variables para el cálculo
total_clp_2024 = 0
total_btc_2024 = 0
total_btc_2023 = 0
total_comisiones_clp = 0


# Calcular el dinero transado en BlackBuda año 2024
total_clp_2024 = sum(float(transaccion[1]) * float(transaccion[2]) for transaccion in trades2024['trades']['entries'])
total_clp_2024 = round(total_clp_2024, 2)
print(f'Dinero transado en BlackBuda: {total_clp_2024} CLP')


# Calcular el volumen de las transacciones año 2024 y 2023 y luego el aumento BTC
total_btc_2024 = sum(float(transaccion[1]) for transaccion in trades2024['trades']['entries'])
total_btc_2023 = sum(float(transaccion[1]) for transaccion in trades2023['trades']['entries'])
aumento_btc = ((total_btc_2024 - total_btc_2023) / total_btc_2023) * 100
aumento_btc = round(aumento_btc, 2)
print(f'Aumento porcentual de transacciones (BTC): {aumento_btc}%')


# Calcular dinero que se dejó de ganar por liberación de comisiones
comision = 0.008
total_comisiones_clp = round(total_clp_2024 * comision, 2)
print(f'Dinero que se dejó de ganar: {total_comisiones_clp} CLP')