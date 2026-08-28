# features.py
import pandas as pd
import geopandas as gpd
from config import CRS_PADRAO, CRS_PROJETADO

def fabricar_features_espaciais(gdf_focos, gdf_clima):
    # 1. Reprojeção (to_crs) para CRS medido em metros
    gdf_focos_proj = gdf_focos.to_crs(CRS_PROJETADO)
    gdf_clima_proj = gdf_clima.to_crs(CRS_PROJETADO)
    
    # 2. Criar Buffer de 5km (5000 metros) ao redor das áreas de medição climática
    gdf_clima_proj['geometry'] = gdf_clima_proj.buffer(5000)
    
    # 3. Spatial Join (sjoin): Cruzamento exato entre os pontos de fogo e os buffers de clima
    focos_com_clima = gpd.sjoin(
        gdf_focos_proj, 
        gdf_clima_proj, 
        how='inner', 
        predicate='intersects'
    )
    
    # 4. Desestruturação de Geometrias
    # Voltar para o CRS padrão e extrair colunas numéricas de lat/lon para o modelo
    focos_com_clima = focos_com_clima.to_crs(CRS_PADRAO)
    focos_com_clima['latitude'] = focos_com_clima.geometry.y
    focos_com_clima['longitude'] = focos_com_clima.geometry.x
    
    # Criar variável alvo (exemplo) e remover a coluna geométrica pesada
    focos_com_clima['fire_binary_tomorrow'] = 1 
    df_tabular = pd.DataFrame(focos_com_clima.drop(columns=['geometry']))
    
    return df_tabular