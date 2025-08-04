import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, silhouette_samples
import seaborn as sns
from datetime import datetime
from sqlalchemy import inspect

# Optional: database
from database import get_connection, get_sqlalchemy_engine

def clustering_page():
    st.title("Clustering Data Parfum dengan K-Means dan PCA")

    uploaded_file = st.file_uploader("Unggah File CSV", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file, delimiter=';')
            st.success("Data berhasil dimuat!")

            # Data Cleaning
            X = df.drop(['VARIAN NAME', 'FRAGRANT', 'GENDER', 'JENIS'], axis=1)
            X['HARGA'].fillna(X['HARGA'].median(), inplace=True)
            st.write("Data setelah dibersihkan:")
            st.dataframe(X)

            # Elbow Method
            st.subheader("Visualisasi Elbow Method")
            clusters = []
            for i in range(1, 16):
                km = KMeans(n_clusters=i, random_state=42).fit(X)
                clusters.append(km.inertia_)

            fig, ax = plt.subplots(figsize=(12, 8))
            sns.lineplot(x=list(range(1, 16)), y=clusters, ax=ax)
            ax.set_title('Mencari Elbow (Elbow Method)')
            ax.set_xlabel('Number of Clusters')
            ax.set_ylabel('Inertia')
            ax.annotate('Possible elbow point', xy=(4, clusters[3]), xytext=(6, clusters[3] + 1e7),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='blue'))
            st.pyplot(fig)

            # Clustering + PCA
            st.subheader("K-Means Clustering dan Visualisasi PCA")
            n_clusters = st.slider("Pilih jumlah cluster:", 2, 10, 4)
            pca = PCA(n_components=2)
            pca_result = pca.fit_transform(X[['FORMULA', 'AQUADEST', 'ALKOHOL', 'UKURAN', 'HARGA']])
            X['PCA1'] = pca_result[:, 0]
            X['PCA2'] = pca_result[:, 1]

            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            X['Labels'] = kmeans.fit_predict(X[['FORMULA', 'AQUADEST', 'ALKOHOL', 'UKURAN', 'HARGA']])

            plt.figure(figsize=(12, 8))
            sns.scatterplot(x=X['PCA1'], y=X['PCA2'], hue=X['Labels'], palette='hls', s=100)

            centroids_pca = pca.transform(kmeans.cluster_centers_)
            for i, (x_c, y_c) in enumerate(centroids_pca):
                plt.scatter(x_c, y_c, s=300, c='black', marker='X')
                plt.text(x_c, y_c, f'C{i+1}', fontsize=12, weight='bold', color='white',
                         ha='center', va='center', bbox=dict(facecolor='black', edgecolor='white', boxstyle='circle'))

            plt.title(f"Visualisasi Clustering Parfum Menggunakan PCA (K={n_clusters})")
            plt.xlabel("Komponen Utama 1")
            plt.ylabel("Komponen Utama 2")
            plt.legend(title='Cluster')
            plt.grid(True)
            plt.tight_layout()
            st.pyplot(plt)

            # Evaluasi Clustering
            st.subheader("Evaluasi Clustering dengan Silhouette Score")
            silhouette_avg = silhouette_score(X[['FORMULA', 'AQUADEST', 'ALKOHOL', 'UKURAN', 'HARGA']], X['Labels'])
            X['Silhouette'] = silhouette_samples(X[['FORMULA', 'AQUADEST', 'ALKOHOL', 'UKURAN', 'HARGA']], X['Labels'])

            st.markdown(f"**Rata-rata Silhouette Coefficient:** `{silhouette_avg:.4f}`")
            cluster_means = X.groupby('Labels')['Silhouette'].mean().reset_index()
            st.dataframe(cluster_means.style.format({"Silhouette": "{:.4f}"}))

            # Simpan ke CSV
            if st.button("Unduh Hasil Clustering CSV"):
                result_file = f"hasil_clustering_{datetime.today().strftime('%Y%m%d')}.csv"
                X.to_csv(result_file, index=False)
                with open(result_file, "rb") as f:
                    st.download_button("Klik untuk Unduh", f, result_file, "text/csv")

            # Simpan ke MySQL
            if st.button("Simpan ke Database"):
                try:
                    engine = get_sqlalchemy_engine()
                    today = datetime.today().strftime('%Y_%m_%d')
                    base_table = f"clustering_result_{today}"
                    inspector = inspect(engine)
                    tables = inspector.get_table_names()

                    counter = 1
                    while f"{base_table}_{counter}" in tables:
                        counter += 1
                    final_table = f"{base_table}_{counter}"

                    X.to_sql(final_table, con=engine, index=False, if_exists='replace')
                    st.success(f"Data berhasil disimpan ke database dengan nama tabel: {final_table}")
                except Exception as e:
                    st.error(f"Gagal menyimpan ke database: {e}")

        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses file: {e}")

if __name__ == "__main__":
    clustering_page()
