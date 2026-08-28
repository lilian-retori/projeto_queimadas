import joblib
import pandas as pd

def gerar_previsoes_modelo(df_modelo, caminho_modelo='modelos/modelo_queimadas_v1.joblib'):
    print(" -> Carregando modelo de Machine Learning...")
    try:
        modelo = joblib.load(caminho_modelo)
    except FileNotFoundError:
        print(f" ERRO: O arquivo do modelo não foi encontrado em {caminho_modelo}")
        print(" Lembre-se de rodar seu notebook_treinamento.ipynb primeiro para gerar este arquivo.")
        return df_modelo
    
    # IMPORTANTE: Estas colunas devem ter o mesmo nome das usadas no seu notebook de treinamento.
    colunas_treinamento = ['latitude', 'longitude', 'temperatura'] 
    
    # Filtra apenas as colunas que o modelo conhece
    X = df_modelo[colunas_treinamento]
    
    print(" -> Realizando previsões para as próximas 24h...")
    df_modelo['y_pred'] = modelo.predict(X)
    
    return df_modelo