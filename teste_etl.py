import pytest
import geopandas as gpd
from shapely.geometry import Point, Polygon
from config import CRS_PADRAO

# 1. Teste de Configuração: Garante que ninguém alterou o CRS por engano
def test_configuracao_crs_correta():
    assert CRS_PADRAO == "EPSG:4326", "O CRS padrão deve ser em graus para a Web!"

# 2. Teste de Lógica Espacial: Cria um dado falso para testar intersecções
def test_intersecao_espacial_funcionando():
    # Simulando o contorno de um Estado (um quadrado simples)
    estado_falso = gpd.GeoDataFrame(
        {'nome': ['Estado Teste']}, 
        geometry=[Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])],
        crs=CRS_PADRAO
    )
    
    # Simulando dois focos de incêndio: um dentro, outro fora
    focos_falsos = gpd.GeoDataFrame(
        {'id': [1, 2]},
        geometry=[Point(5, 5), Point(15, 15)], # Ponto 1 dentro, Ponto 2 fora
        crs=CRS_PADRAO
    )
    
    # Executa o cruzamento espacial (a mesma lógica usada no etl.py)
    resultado = gpd.overlay(focos_falsos, estado_falso, how='intersection')
    
    # O teste exige que apenas 1 foco (o que estava dentro) tenha sobrado
    assert len(resultado) == 1
    assert resultado.iloc[0]['id'] == 1