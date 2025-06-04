import streamlit as st
import pandas as pd

# Limiares de alerta
LIMIAR_TEMPERATURA = 40
LIMIAR_CHUVA = 50

# Configuração da página
st.set_page_config(page_title="Dashboard de Monitoramento Climático", layout="wide")

# Título da página
st.markdown("# 🌦️ Dashboard de Monitoramento Climático")
st.markdown("Monitore os níveis de **temperatura** e **chuva** e visualize **alertas em tempo real**.")
st.markdown("---")

# Upload do arquivo
st.markdown("## 📁 Envio de Planilha")
uploaded_file = st.file_uploader("Envie o arquivo Excel (.xlsx) com os dados climáticos", type=["xlsx"])

if uploaded_file:
    try:
        # Leitura dos dados
        df = pd.read_excel(uploaded_file)

        # Exibe colunas detectadas
        st.info(f"📋 Colunas detectadas: `{df.columns.tolist()}`")

        # Normalização dos nomes esperados
        colunas_renomeadas = {}
        for col in df.columns:
            nome = col.strip().lower()
            if "data" in nome or "tempo" in nome:
                colunas_renomeadas[col] = "Tempo"
            elif "temperatura" in nome:
                colunas_renomeadas[col] = "Temperatura (°C)"
            elif "chuva" in nome:
                colunas_renomeadas[col] = "Chuva (mm)"

        df.rename(columns=colunas_renomeadas, inplace=True)

        # Verificação de colunas necessárias
        colunas_necessarias = ["Tempo", "Temperatura (°C)", "Chuva (mm)"]
        if not all(col in df.columns for col in colunas_necessarias):
            st.error("❌ Colunas obrigatórias não encontradas na planilha.")
        else:
            # Dados carregados
            st.markdown("## 📊 Dados Carregados")
            st.dataframe(df, use_container_width=True)
            st.markdown("---")

            # Análise de alertas
            st.markdown("## ⚠️ Alertas Climáticos")
            alertas = []
            for _, row in df.iterrows():
                if row["Temperatura (°C)"] > LIMIAR_TEMPERATURA:
                    alertas.append(f"🚨 Temperatura muito alta em {row['Tempo']}: {row['Temperatura (°C)']}°C")
                if row["Chuva (mm)"] > LIMIAR_CHUVA:
                    alertas.append(f"🌧️ Volume de chuva elevado em {row['Tempo']}: {row['Chuva (mm)']}mm")

            if alertas:
                for alerta in alertas:
                    st.error(alerta)
            else:
                st.success("✅ Nenhum alerta detectado.")
            st.markdown("---")

            # Gráficos
            st.markdown("## 📈 Gráficos de Monitoramento")

            # Conversão e definição de índice
            df["Tempo"] = pd.to_datetime(df["Tempo"], errors="coerce")
            df.set_index("Tempo", inplace=True)

            st.line_chart(df[["Temperatura (°C)", "Chuva (mm)"]])

    except Exception as e:
        st.error(f"❌ Erro ao ler o arquivo: {e}")
else:
    st.warning("⬆️ Envie um arquivo Excel para iniciar a análise.")
