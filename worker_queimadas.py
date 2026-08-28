import schedule
import time
import pandas as pd
import geopandas as gpd
from datetime import datetime
from shapely.geometry import Point

# Importando a sua arquitetura
from config import CRS_PADRAO
from etl import extrair_e_limpar_dados
from features import fabricar_features_espaciais
from predict import gerar_previsoes_modelo

def pipeline_previsao_queimadas():
    print(f"\n[{datetime.now()}] Iniciando a coleta e previsão autônoma...")

    try:
        # 1. ETL (Extração e Limpeza)
        print(" Passo 1: Extraindo dados recentes...")
        gdf_focos = extrair_e_limpar_dados()
        
        if gdf_focos.empty:
            print(" Nenhum foco no estado hoje. Fim do ciclo.")
            return

        # 2. FEATURES (Cruzamento Espacial)
        print(" Passo 2: Cruzando com dados climáticos...")
        # Simulando uma leitura de API de clima para o código não quebrar na primeira execução
        gdf_clima_api = gpd.GeoDataFrame(
            {'estacao_id': ['EST-01'], 'temperatura': [35.0]},
            geometry=[Point(-55.0, -12.0)], crs=CRS_PADRAO
        )
        df_features = fabricar_features_espaciais(gdf_focos, gdf_clima_api)

        # 3. PREDIÇÃO (Chamando o modelo .joblib)
        print(" Passo 3: Rodando o modelo de Machine Learning...")
        # Garante que as colunas que o predict.py espera existam na tabela final
        if 'temperatura' not in df_features.columns:
            df_features['temperatura'] = 35.0 
            
        df_final = gerar_previsoes_modelo(df_features)

        # 4. ARMAZENAMENTO
        print(f" -> Sucesso! {len(df_final)} previsões geradas prontas para o Dashboard.")
        # Opcional: df_final.to_sql('tabela_previsoes', engine, if_exists='append', index=False)
        print(f"[{datetime.now()}] Ciclo finalizado!\n")

    except Exception as e:
        print(f"[{datetime.now()}] ERRO CRÍTICO no pipeline: {e}")

# Configura para rodar sozinho a cada 6 horas
schedule.every(6).hours.do(pipeline_previsao_queimadas)

if __name__ == "__main__":
    print("Serviço de Previsão de Queimadas iniciado. Aguardando a janela de agendamento...")
    
    # Descomente a linha abaixo se quiser que ele rode na mesma hora em que ligar o script, 
    # antes de começar a esperar as 6 horas
    # pipeline_previsao_queimadas()

    while True:
        schedule.run_pending()
        time.sleep(60)