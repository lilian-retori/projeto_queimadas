import pytest
import geopandas as gpd
from shapely.geometry import Point, Polygon
from config import CRS_PADRAO

def test_configuracao_crs_correta():
    assert CRS_PADRAO == "EPSG:4326", "O CRS padrão deve ser em graus para a Web!"

def test_intersecao_espacial_funcionando():
    # Simulando o contorno de um Estado (quadrado simples)
    estado_falso = gpd.GeoDataFrame(
        {'nome': ['Estado Teste']}, 
        geometry=[Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])],
        crs=CRS_PADRAO
    )
    
    # Simulando dois focos de incêndio: um dentro (5,5), outro fora (15,15)
    focos_falsos = gpd.GeoDataFrame(
        {'id': [1, 2]},
        geometry=[Point(5, 5), Point(15, 15)], 
        crs=CRS_PADRAO
    )
    
    resultado = gpd.overlay(focos_falsos, estado_falso, how='intersection')
    
    # Exige que apenas 1 foco (o de dentro) tenha sobrado no dataframe
    assert len(resultado) == 1
    assert resultado.iloc[0]['id'] == 1