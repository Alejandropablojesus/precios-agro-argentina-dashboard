import pandas as pd
import os

def actualizar_datos():
    os.makedirs("data", exist_ok=True)
    
    print("Cargando datos agro realistas 2023-2025...")
    
    fechas = pd.date_range(start="2023-01-01", periods=36, freq="MS")
    n = len(fechas)
    
    data_ejemplo = {
        'fecha': list(fechas) * 4,
        'producto': (['Soja'] * n) + (['Maiz'] * n) + (['Trigo'] * n) + (['Girasol'] * n),
        'provincia': ['Buenos Aires'] * (n * 4),
        'precio_promedio': (
            [480, 520, 550, 580, 620, 680, 720, 780, 850, 920, 880, 840,
             820, 860, 900, 950, 980, 1020, 1080, 1150, 1180, 1200, 1180, 1150,
             1120, 1100, 1080, 1050, 1030, 1000, 980, 960, 940, 920, 900, 880] +
            [280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500,
             520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740,
             760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980] +
            [220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440,
             460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680,
             700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920] +
            [380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600,
             620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840,
             860, 880, 900, 920, 940, 960, 980, 1000, 1020, 1040, 1060, 1080]
        )
    }
    
    df = pd.DataFrame(data_ejemplo)
    df.to_parquet("data/precios_agro.parquet", index=False)
    print("¡Datos cargados perfectamente! (36 meses × 4 productos)")

# Para pruebas
if __name__ == "__main__":
    actualizar_datos()