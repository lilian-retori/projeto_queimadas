import geopandas as gpd
import pandas as pd
import schedule
import time
from datetime import datetime

# Substitua pela URL da API que fornecerá os dados (ex: INPE, NASA FIRMS)
# O GeoPandas consegue ler arquivos GeoJSON diretamente da web.
API_URL = "https://api.exemplo.com/focos_calor.geojson"

def pipeline_previsao_queimadas():
    print(f"[{datetime.now()}] Iniciando a coleta e previsão de queimadas...")

    try:
        # 1. INGESTÃO: Leitura direta da API para a memória (sem baixar arquivo físico)
        print(" -> Baixando dados...")
        gdf = gpd.read_file(API_URL)

        # 2. LIMPEZA: Remover dados corrompidos ou sem localização
        gdf = gdf[gdf.geometry.notnull()]

        # 3. TRANSFORMAÇÃO: Desestruturação da geometria (Lat/Lon)
        # Modelos de Machine Learning geralmente exigem colunas numéricas em vez de objetos geométricos.
        gdf['latitude'] = gdf.geometry.y
        gdf['longitude'] = gdf.geometry.x

        # Remover a coluna geométrica para focar apenas nos dados tabulares
        df_tabular = pd.DataFrame(gdf.drop(columns='geometry'))

        # 4. PREDIÇÃO: Integração com o seu modelo de Machine Learning
        # Exemplo hipotético de injeção de dados no modelo:
        # df_tabular['risco_predito'] = meu_modelo_ml.predict(df_tabular[['latitude', 'longitude', 'temperatura', 'umidade']])
        
        print(f" -> Processados e analisados {len(df_tabular)} registros.")

        # 5. ARMAZENAMENTO: Salvar no seu banco de dados (ex: PostgreSQL/PostGIS)
        # from sqlalchemy import create_engine
        # engine = create_engine('postgresql://usuario:senha@localhost:5432/meubanco')
        # df_tabular.to_sql('tabela_previsoes', engine, if_exists='append', index=False)

        print(f"[{datetime.now()}] Ciclo finalizado com sucesso!\n")

    except Exception as e:
        print(f"[{datetime.now()}] Erro durante o processamento: {e}")

# AGENDAMENTO: Configura a rotina para rodar autonomamente (ex: a cada 6 horas)
schedule.every(6).hours.do(pipeline_previsao_queimadas)

if __name__ == "__main__":
    print("Serviço de Previsão de Queimadas iniciado. Aguardando a janela de agendamento...")
    
    # Executa a função uma vez imediatamente ao ligar o servidor (opcional)
    # pipeline_previsao_queimadas()

    # Loop infinito que mantém o script vivo verificando o relógio
    while True:
        schedule.run_pending()
        time.sleep(60) # Pausa de 1 minuto para não sobrecarregar a CPU