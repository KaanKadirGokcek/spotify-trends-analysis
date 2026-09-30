import os
import pandas as pd  
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Veriyi Oku ve Temizle
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "spotify_hits.csv")

df = pd.read_csv(csv_path)

# Milisaniyeyi dakikaya çevir
df["duration_min"] = df["duration_ms"] / 60000

# 1999-2019 arasını filtrele
df = df[(df["year"] >= 1999) & (df["year"] <= 2019)].copy()

# 2. Yıllara Göre Özet Metrikleri Hesapla (groupby gücü!)
yearly = df.groupby("year").agg({
    "duration_min": "mean",
    "danceability": "mean",
    "energy": "mean",
    "valence": "mean",
    "explicit": lambda x: (x == True).mean() * 100  # Yüzdelik oran
}).reset_index()

# 3. Konsola Eğlenceli Özet Yazdır
top_artist = df["artist"].value_counts().index[0]
top_artist_count = df["artist"].value_counts().iloc[0]
dur_2000 = yearly[yearly["year"] == 2000]["duration_min"].values[0]
dur_2019 = yearly[yearly["year"] == 2019]["duration_min"].values[0]
exp_2000 = yearly[yearly["year"] == 2000]["explicit"].values[0]
exp_2019 = yearly[yearly["year"] == 2019]["explicit"].values[0]

print("--- 🎧 SPOTIFY 2000-2019 ANALİZ ÖZETİ ---")
print(f"🏆 Dönemin En Çok Hit Çıkaran Sanatçısı: {top_artist} ({top_artist_count} şarkı)")
print(f"⏱️ 2000 Yılı Ort. Süre: {dur_2000:.2f} dk  -->  2019 Yılı: {dur_2019:.2f} dk")
print(f"🤬 Sansürlü (Explicit) Şarkı Oranı: %{exp_2000:.1f} (2000) --> %{exp_2019:.1f} (2019)")

# 4. 4 Parçalı İnteraktif Dashboard (2x2 Grid)
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "⏱️ Şarkı Süreleri Kısaldı mı? (Ort. Dakika)",
        "🎭 Müzikal Ruh Hali: Dans Edilebilirlik vs Neşe (Valence)",
        "🎤 En Çok Hit Şarkısı Olan 10 Sanatçı",
        "🔞 Sansürlü (Explicit) Şarkıların Yıllara Göre Artışı (%)"
    ),
    vertical_spacing=0.15,
    horizontal_spacing=0.12
)

# Grafik 1: Süre Değişimi
fig.add_trace(
    go.Scatter(x=yearly["year"], y=yearly["duration_min"], mode="lines+markers",
               name="Şarkı Süresi (dk)", line=dict(color="#1DB954", width=3),
               marker=dict(size=7)),
    row=1, col=1
)

# Grafik 2: Dans Edilebilirlik & Valence (Mutluluk)
fig.add_trace(
    go.Scatter(x=yearly["year"], y=yearly["danceability"], mode="lines+markers",
               name="Dans Edilebilirlik", line=dict(color="#00E5FF", width=2.5)),
    row=1, col=2
)
fig.add_trace(
    go.Scatter(x=yearly["year"], y=yearly["valence"], mode="lines+markers",
               name="Neşe / Mutluluk (Valence)", line=dict(color="#FF007F", width=2.5, dash="dot")),
    row=1, col=2
)

# Grafik 3: En Popüler 10 Sanatçı (Yatay Bar)
top_10_artists = df["artist"].value_counts().head(10).sort_values(ascending=True)
fig.add_trace(
    go.Bar(x=top_10_artists.values, y=top_10_artists.index, orientation="h",
           name="Hit Şarkı Sayısı", marker=dict(color="#FFD700")),
    row=2, col=1
)

# Grafik 4: Explicit Şarkı Oranı
fig.add_trace(
    go.Bar(x=yearly["year"], y=yearly["explicit"],
           name="Explicit Oranı (%)", marker=dict(color="#FF4500")),
    row=2, col=2
)

# 5. Profesyonel Yerleşim ve Koyu Tema
fig.update_layout(
    margin=dict(t=100, b=50, l=60, r=60),
    title=dict(
        text="<b>Spotify Trendleri: 2000–2019 Arasında Müzik Nasıl Değişti?</b>",
        x=0.01, y=0.98,
        font=dict(size=19, color="#ffffff")
    ),
    template="plotly_dark",
    hovermode="x unified",
    showlegend=True
)

fig.update_yaxes(title_text="Dakika", row=1, col=1)
fig.update_yaxes(title_text="Skor (0-1)", row=1, col=2)
fig.update_xaxes(title_text="Şarkı Sayısı", row=2, col=1)
fig.update_yaxes(title_text="Oran (%)", row=2, col=2)

# 6. HTML Kaydet
output_file = os.path.join(current_dir, "spotify_analiz.html")
fig.write_html(output_file)
print(f"\nGrafik paneli başarıyla oluşturuldu: {output_file}")