# etl.py
import pandas as pd
import geopandas as gpd
import geobr
from config import CRS_PADRAO, ESTADO_ALVO, URL_NASA_FIRMS

def extrair_e_limpar_dados():
    # 1. Leitura direta de endpoints para a memória
    df_nasa = pd.read_csv(URL_NASA_FIRMS)
    
    # 2. Converter Pandas DataFrame para GeoDataFrame
    gdf_focos = gpd.GeoDataFrame(
        df_nasa, 
        geometry=gpd.points_from_xy(df_nasa.longitude, df_nasa.latitude),
        crs=CRS_PADRAO
    )
    
    # 3. Baixar contorno do estado usando geobr e padronizar o CRS
    gdf_estado = geobr.read_state(code_state=ESTADO_ALVO, year=2020)
    gdf_estado = gdf_estado.to_crs(CRS_PADRAO)
    
    # 4. Interseção Espacial (Limpeza)
    # Mantém apenas os focos de incêndio que caíram dentro do estado alvo
    gdf_focos_limpos = gpd.overlay(gdf_focos, gdf_estado, how='intersection')
    
    return gdf_focos_limpos