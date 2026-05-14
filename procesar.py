import pandas as pd
import numpy as np
import json

def generar_estadisticas():
    try:
        
        df = pd.read_csv('examenpractivo.csv')
        
        #Limpio
        df['peso'] = pd.to_numeric(df['peso'], errors='coerce')
        peso_clean = df['peso'].dropna()

        #MTC
        media = float(peso_clean.mean())
        mediana = float(peso_clean.median())
        moda = float(peso_clean.mode()[0])

        #Fuera NA
        df_color = df.dropna(subset=['color'])
        freq_abs_color = df_color['color'].value_counts().to_dict()
        total_colores = sum(freq_abs_color.values())
        freq_rel_color = {k: round((v / total_colores) * 100, 2) for k, v in freq_abs_color.items()}

        counts, bin_edges = np.histogram(peso_clean, bins=5)
        
        intervalos = []
        for i in range(len(counts)):
            label = f"{bin_edges[i]:.1f} - {bin_edges[i+1]:.1f}"
            intervalos.append(label)

        freq_rel_peso = [(v / len(peso_clean)) * 100 for v in counts]
        freq_acum_peso = np.cumsum(counts).tolist()

        #JSON
        datos_finales = {
            "tendencia_central": {
                "media": round(media, 2),
                "mediana": round(mediana, 2),
                "moda": round(moda, 2)
            },
            "frecuencias_color": {
                "labels": list(freq_abs_color.keys()),
                "absoluta": list(freq_abs_color.values()),
                "relativa": list(freq_rel_color.values())
            },
            "frecuencias_peso": {
                "intervalos": intervalos,
                "absoluta": counts.tolist(),
                "relativa": [round(x, 2) for x in freq_rel_peso],
                "acumulada": freq_acum_peso
            }
        }

        #Guardar en JSON
        with open('datos.json', 'w', encoding='utf-8') as f:
            json.dump(datos_finales, f, indent=4, ensure_ascii=False)

        print("✅ Éxito: Se ha generado 'datos.json' con todos los cálculos.")

    except Exception as e:
        print(f"❌ Error al procesar los datos: {e}")

if __name__ == "__main__":
    generar_estadisticas()