import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime

# Definir features
features_sim = ["avg_pace_s_per_km", "avg_hr", "total_ascent", "total_descent", "distance_km"]
features_model = features_sim + ["days_ago"]

def predecir_tiempos_tres_distancias(df, carreras_nuevo_usuario):
    def segundos_a_hhmmss(seg):
        h = int(seg // 3600)
        m = int((seg % 3600) // 60)
        s = int(seg % 60)
        return f"{h:02}:{m:02}:{s:02}"

    def estimar_tiempo_riegel_promedio(df_carreras, distancia_objetivo_km):
        df_validas = df_carreras[df_carreras["distance_km"] >= 5].copy()
        if df_validas.empty:
            return None

        df_validas["dist_diff"] = np.abs(df_validas["distance_km"] - distancia_objetivo_km)
        top_n = df_validas.nsmallest(3, "dist_diff")  # Usar las 3 carreras más cercanas

        tiempos_estimados = []
        for _, row in top_n.iterrows():
            t = row["time_s"]
            d = row["distance_km"]
            riegel = t * (distancia_objetivo_km / d) ** 1.06
            tiempos_estimados.append(riegel)

        return np.mean(tiempos_estimados)

    # Procesamiento inicial
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    fecha_max = df["date"].max()

    df["days_ago"] = (fecha_max - df["date"]).dt.days.clip(lower=0).fillna(0)
    df["days_ago_log"] = np.log1p(df["days_ago"])

    features_sim = ["avg_pace_s_per_km", "avg_hr", "total_ascent", "total_descent"]
    features_model = features_sim + ["distance_km", "days_ago"]

    user_profiles = df.groupby("user_id")[features_sim].mean().fillna(0)

    nuevo_usuario_df = pd.DataFrame(carreras_nuevo_usuario)
    nuevo_usuario_df["date"] = pd.to_datetime(nuevo_usuario_df["date"], errors="coerce")
    nuevo_usuario_df["days_ago"] = (fecha_max - nuevo_usuario_df["date"]).dt.days.clip(lower=0).fillna(0)
    nuevo_usuario_df["days_ago_log"] = np.log1p(nuevo_usuario_df["days_ago"])
    nuevo_usuario_df = nuevo_usuario_df.dropna(subset=["time_s", "distance_km"])

    nuevo_usuario_promedio = nuevo_usuario_df[features_model].mean().to_frame().T.fillna(user_profiles.mean())

    distancias = euclidean_distances(nuevo_usuario_promedio[features_sim], user_profiles)[0]
    user_similarity = pd.Series(distancias, index=user_profiles.index).sort_values()
    user_id_mas_parecido = user_similarity.index[0]

    df_similar = df[df["user_id"] == user_id_mas_parecido].copy()
    if df_similar.empty or "time_s" not in df_similar:
        return {"predicciones": {}, "usuario_mas_parecido": None}

    X_sim = df_similar[features_model]
    y_sim = df_similar["time_s"]

    modelo = RandomForestRegressor(random_state=42)
    modelo.fit(X_sim, y_sim)

    distancias_objetivo = {
        "10K": 10.0,
        "21K": 21.097,
        "42K": 42.195
    }

    resultados = {}
    tiempos_previos = {}

    for nombre, dist in distancias_objetivo.items():
        entrada = nuevo_usuario_promedio.copy()
        entrada["distance_km"] = dist

        tiempo_riegel = estimar_tiempo_riegel_promedio(nuevo_usuario_df, dist)
        tiempo_modelo = modelo.predict(entrada[features_model])[0]

        if tiempo_riegel:
            tiempo_final = (tiempo_riegel + tiempo_modelo) / 2
        else:
            tiempo_final = tiempo_modelo

        # Validaciones cruzadas
        if nombre == "21K" and "10K" in tiempos_previos:
            tiempo_final = max(tiempo_final, tiempos_previos["10K"] * 2 * 0.98)
        if nombre == "42K" and "21K" in tiempos_previos:
            tiempo_final = max(tiempo_final, tiempos_previos["21K"] * 2 * 0.98)

        resultados[nombre] = {
            "segundos": int(tiempo_final),
            "minutos": round(tiempo_final / 60, 2),
            "hh:mm:ss": segundos_a_hhmmss(tiempo_final)
        }

        tiempos_previos[nombre] = tiempo_final

    return {
        "usuario_mas_parecido": user_id_mas_parecido,
        "predicciones": resultados
    }

# Función para transformar
def time_to_seconds(t):
    if pd.isna(t):
        return np.nan
    parts = str(t).split(":")
    try:
        parts = [int(p) for p in parts]
        if len(parts) == 3:  # HH:MM:SS
            return parts[0]*3600 + parts[1]*60 + parts[2]
        elif len(parts) == 2:  # MM:SS
            return parts[0]*60 + parts[1]
        else:
            return np.nan
    except:
        return np.nan

def clean_df():
    file_path = "/Users/andresdossantos/Desktop/Coding/backTFM/predictions/data/activitiesDataSet.csv"
    df = pd.read_csv(file_path, encoding='UTF-8')

    df["Time (s)"] = df["Time"].apply(time_to_seconds)
    df["Elapsed Time (s)"] = df["Elapsed Time"].apply(time_to_seconds)
    df["Avg Pace (s/km)"] = df["Avg Pace"].apply(time_to_seconds)
    df["Best Pace (s/km)"] = df["Best Pace"].apply(time_to_seconds)

    # Eliminar las columnas originales
    df = df.drop(["Time", "Elapsed Time", "Avg Pace", "Best Pace"], axis=1)

    # Lista de las columnas a rellenar
    cols_to_fill = ["Time (s)", "Elapsed Time (s)", "Avg Pace (s/km)", "Best Pace (s/km)"]

    # Rellenar NaN con el promedio de cada usuario
    for col in cols_to_fill:
        df[col] = df.groupby("User ID")[col].transform(lambda x: x.fillna(x.mean()))

    # Reemplazar "--" con np.nan
    df["Calories"] = df["Calories"].replace("--", np.nan)
    df["Avg HR"] = df["Avg HR"].replace("--", np.nan)
    df["Max HR"] = df["Max HR"].replace("--", np.nan)
    df["Total Ascent"] = df["Total Ascent"].replace("--", np.nan)
    df["Total Descent"] = df["Total Descent"].replace("--", np.nan)
    df["Steps"] = df["Steps"].replace("--", np.nan)
    df["Min Elevation"] = df["Min Elevation"].replace("--", np.nan)
    df["Max Elevation"] = df["Max Elevation"].replace("--", np.nan)

    # Convertir la columna a numérico (por si hay strings aún)
    df["Calories"] = pd.to_numeric(df["Calories"], errors='coerce')
    df["Avg HR"] = pd.to_numeric(df["Avg HR"], errors='coerce')
    df["Max HR"] = pd.to_numeric(df["Max HR"], errors='coerce')
    df["Total Ascent"] = pd.to_numeric(df["Total Ascent"], errors='coerce')
    df["Total Descent"] = pd.to_numeric(df["Total Descent"], errors='coerce')
    df["Steps"] = pd.to_numeric(df["Steps"], errors='coerce')
    df["Min Elevation"] = pd.to_numeric(df["Min Elevation"], errors='coerce')
    df["Max Elevation"] = pd.to_numeric(df["Max Elevation"], errors='coerce')

    # Rellenar NaN con el promedio por User ID
    df["Calories"] = df.groupby("User ID")["Calories"].transform(lambda x: x.fillna(x.mean()))
    df["Avg HR"] = df.groupby("User ID")["Avg HR"].transform(lambda x: x.fillna(x.mean()))
    df["Max HR"] = df.groupby("User ID")["Max HR"].transform(lambda x: x.fillna(x.mean()))
    df["Total Ascent"] = df.groupby("User ID")["Total Ascent"].transform(lambda x: x.fillna(x.mean()))
    df["Total Descent"] = df.groupby("User ID")["Total Descent"].transform(lambda x: x.fillna(x.mean()))
    df["Steps"] = df.groupby("User ID")["Steps"].transform(lambda x: x.fillna(x.mean()))
    df["Min Elevation"] = df.groupby("User ID")["Min Elevation"].transform(lambda x: x.fillna(x.mean()))
    df["Max Elevation"] = df.groupby("User ID")["Max Elevation"].transform(lambda x: x.fillna(x.mean()))

    # Reemplazar ',' por '.' si aún no lo has hecho
    df["Distance"] = df["Distance"].astype(str).str.replace(",", ".", regex=False)

    # Convertir a float
    df["Distance"] = pd.to_numeric(df["Distance"], errors="coerce")

    # Reemplazar ',' por '.' en la columna Steps
    df["Steps"] = df["Steps"].astype(str).str.replace(",", ".", regex=False)

    # Convertir a float
    df["Steps"] = pd.to_numeric(df["Steps"], errors="coerce")

    df = df.rename(columns={
        "User ID": "user_id",
        "User Name": "user_name",
        "Activity Type": "activity_type",
        "Date": "date",
        "Title": "title",
        "Distance": "distance_km",
        "Calories": "calories",
        "Avg HR": "avg_hr",
        "Max HR": "max_hr",
        "Total Ascent": "total_ascent",
        "Total Descent": "total_descent",
        "Steps": "steps",
        "Min Elevation": "min_elevation",
        "Max Elevation": "max_elevation",
        "Time (s)": "time_s",
        "Elapsed Time (s)": "elapsed_time_s",
        "Avg Pace (s/km)": "avg_pace_s_per_km",
        "Best Pace (s/km)": "best_pace_s_per_km"
    })

    # Limpiamos la fecha date para poder trabajar con ella en el modelo.
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

    hoy = pd.Timestamp(datetime.today())
    df["days_ago"] = (hoy - df["date"]).dt.days
    df["peso_reciente"] = 1 / (df["days_ago"] + 1)  # Le sumas 1 para evitar división por cero

    return df

def final_result(df_user):
    df_user["Time (s)"] = df_user["Time"].apply(time_to_seconds)
    df_user["Elapsed Time (s)"] = df_user["Elapsed Time"].apply(time_to_seconds)
    df_user["Avg Pace (s/km)"] = df_user["Avg Pace"].apply(time_to_seconds)
    df_user["Best Pace (s/km)"] = df_user["Best Pace"].apply(time_to_seconds)
    df_user = df_user.drop(["Time", "Elapsed Time", "Avg Pace", "Best Pace"], axis=1)

    columnas_reemplazo = [
        "Calories", "Avg HR", "Max HR", "Total Ascent", "Total Descent",
        "Steps", "Min Elevation", "Max Elevation"
    ]
    for col in columnas_reemplazo:
        df_user[col] = df_user[col].replace("--", np.nan)
        df_user[col] = pd.to_numeric(df_user[col], errors='coerce')
        df_user[col] = df_user[col].fillna(df_user[col].mean())

    df_user["Distance"] = df_user["Distance"].astype(str).str.replace(",", ".", regex=False)
    df_user["Distance"] = pd.to_numeric(df_user["Distance"], errors="coerce")
    df_user["Steps"] = df_user["Steps"].astype(str).str.replace(",", ".", regex=False)
    df_user["Steps"] = pd.to_numeric(df_user["Steps"], errors="coerce")

    df_user = df_user.rename(columns={
        "Activity Type": "activity_type",
        "Date": "date",
        "Title": "title",
        "Distance": "distance_km",
        "Calories": "calories",
        "Avg HR": "avg_hr",
        "Max HR": "max_hr",
        "Total Ascent": "total_ascent",
        "Total Descent": "total_descent",
        "Steps": "steps",
        "Min Elevation": "min_elevation",
        "Max Elevation": "max_elevation",
        "Time (s)": "time_s",
        "Elapsed Time (s)": "elapsed_time_s",
        "Avg Pace (s/km)": "avg_pace_s_per_km",
        "Best Pace (s/km)": "best_pace_s_per_km"
    })

    df_user["date"] = pd.to_datetime(df_user["date"], errors="coerce")
    hoy = pd.Timestamp(datetime.today())

     # Calcular días desde la fecha
    df_user["days_ago"] = (hoy - df_user["date"]).dt.days

    # Eliminar fechas no válidas o negativas
    df_user = df_user[df_user["days_ago"].notna()]
    df_user = df_user[df_user["days_ago"] >= 0]

    # Asegurarse de que days_ago es tipo numérico entero
    df_user["days_ago"] = pd.to_numeric(df_user["days_ago"], errors="coerce").fillna(0).astype(int)

    # Calcular log de forma segura (solo donde sea posible)
    df_user["days_ago_log"] = df_user["days_ago"].apply(lambda x: np.log1p(x) if x >= 0 else np.nan)

    # Calcular peso basado en recencia
    df_user["peso_reciente"] = 1 / (df_user["days_ago"] + 1)

    columnas_modelo = [
        "avg_pace_s_per_km",
        "avg_hr",
        "total_ascent",
        "total_descent",
        "distance_km",
        "date",
        "time_s"
    ]

    df_valid = df_user[columnas_modelo].dropna().copy()

    # Aseguramos que 'date' es string en formato ISO
    df_valid["date"] = df_valid["date"].dt.strftime("%Y-%m-%d")

    carreras_nuevo_usuario = df_valid.to_dict(orient="records")

    # Llama al modelo
    resultado = predecir_tiempos_tres_distancias(clean_df(), carreras_nuevo_usuario)

    r10 = resultado["predicciones"]["10K"]["hh:mm:ss"]
    r21 = resultado["predicciones"]["21K"]["hh:mm:ss"]
    r42 = resultado["predicciones"]["42K"]["hh:mm:ss"]

    return r10, r21, r42