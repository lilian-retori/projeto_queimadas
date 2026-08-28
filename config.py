# config.py
# Sistemas de Referência de Coordenadas (CRS)
CRS_PADRAO = "EPSG:4326"     # Lat/Lon em graus (Padrão Web/GPS)
CRS_PROJETADO = "EPSG:31983" # SIRGAS 2000 UTM Zone 23S (Medido em metros, ideal para o Brasil)

# Configurações de Dados
ESTADO_ALVO = "MT"           # Exemplo: Mato Grosso
URL_NASA_FIRMS = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_South_America_24h.csv"