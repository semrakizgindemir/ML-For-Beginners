"""
Bir veri seti üzerinden veri analiz işlemleri gerçekleştirilerek Github üzerinden paylaşılacaktır.

Veri Seti: Bike Sharing Dataset

- Veri setini tanıt (kolonlar, tipler, eksik veri var mı).
- Sayısal değişkenler için:
    1. dağılım grafiği
    2. histogram
    3. outlier analizi (IQR veya z-score)
- Kategorik değişkenler için:
    1. frekans grafikleri
    2. bar plot
- Korelasyon matrix’i oluştur ve yorumla.
- Heat map ile önemli ilişkileri işaretle.
- “Mevsim → Bisiklet sayısı”, “Hava durumu → Kullanım” gibi ilişkileri grafikle göster.
- Zaman içindeki trendi incele:
   1. saatlik
   2. günlük
   3. mevsimsel
"""

import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
from matplotlib import pyplot as plt
import missingno as msno
from datetime import date
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, StandardScaler, RobustScaler

data = pd.read_csv('datasets/hour.csv')
pd.set_option('display.max_columns', None)#butun sutunları goster
pd.set_option('display.max_rows', None)#tum satırları goster
pd.set_option('display.width', 500)#Bir satırda yazdırılacak maksimum karakter genişliğini 500 olarak ayarla.

print(data.head())

for col in data:
    print(f"{col} : sütunu --> veri tipi : {type(data[col].values[0])}")


print(data.isnull().values.any())#eksik var mı yok mu

print(data.isnull().sum())#her sutunda kaç tane eksik var

num_cols = [col for col in data.columns if data[col].dtypes != "O"]#sayısal verileri atadık bunların bazıları sınıflandırma
# yapmak için numaralandırmıs olabilir yani aslında kategorik değişkendir
print(num_cols)
num_but_cat = [col for col in data.columns if data[col].nunique() < 15 and data[col].dtypes != "O"]
num_cols = [col for col in num_cols if col not in num_but_cat]  # numerik ama kategorik olanları da içinden cıkarıyoruz içinde sadece numerik kolonlar kalıyor
cat_cols = [col for col in data if col not in num_cols]
print(num_cols)
print(cat_cols)

# Create scatter plot with regression line
for col in num_cols:
    plt.figure(figsize=(6, 4))
    sns.histplot(data[col],kde=True)#histplot histogram çizer (x ekseni degerler y ekseni frekans kaç tane var)
    #kde kernel density estimation
    plt.title(f"{col} dağılımı")
    plt.show()


######AYKIRI DEĞER İQR YONTEMİ
q1 = data["windspeed"].quantile(0.25)#genel değer %5 alınması daha uygundur
q3 = data["windspeed"].quantile(0.75)#0.95

iqr = q3 -q1

low = q1 - 1.5 * iqr
up = q3 + 1.5 * iqr

print("low" ,low)
print("up", up)

print(data[((data["windspeed"] < low) | (data["windspeed"] > up))])#aykırı değerleri yaz
print(len(data[((data["windspeed"] < low) | (data["windspeed"] > up))]))#kaç tane aykırı değer"""
#GENELLEŞTİRME İÇİN FOR DONGUSU

######AYKIRI DEĞER Z-SCORE YONTEMİ

z_score = (data["windspeed"] - data["windspeed"].mean() ) / data["windspeed"].std()

z_scores = stats.zscore(data["windspeed"])

print(data[((z_scores > 3) | (z_scores < -3))])#aykırı değerler
print(len(data[((z_scores > 3) | (z_scores < -3))]))#aykırı değer sayısı

#frekans grafikleri ---- barplot

plt.figure()
sns.countplot(x='holiday',data=data)
plt.title("holiday Frekans Grafiği")
plt.show()

sns.barplot(x='holiday', y='cnt', data=data, estimator='mean')
plt.title("tatil Durumuna Göre Ortalama Bisiklet kullanımı")
plt.show()

#korelasyon matrisi
corr = data[['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']].corr()
print(corr)

plt.figure(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Korelasyon Heatmap")
plt.show()

#- “Mevsim → Bisiklet sayısı”, “Hava durumu → Kullanım” gibi ilişkileri grafikle göster.

sns.boxplot(x='season', y='cnt', data=data) # kutu ne kadar uzunsa veriler o kadar geniş alana yayılmıs ortadaki çizgi ortanca değeri ifade eder
plt.title("mevsime gore bisiklet kullanımı")
plt.show()

sns.boxplot(x='weathersit', y='cnt', data=data)
plt.title("hava durumuna gore bisiklet kulanımı")
plt.show()


hourly_avg = data.groupby('hr')['cnt'].mean()#Veri setini hr sütununa göre gruplara ayır , sadece cnt sütununun ortalmasını ver
plt.figure()
plt.plot(hourly_avg)
plt.title("saatilk ort bisiklet kullanımı")
plt.xlabel("saat")
plt.ylabel("ortalama kullanım")
plt.show()

daily_avg = data.groupby('dteday')['cnt'].mean()
plt.figure()
plt.plot(daily_avg)
plt.title("gunluk ortalama kullanım")
plt.show()

weather_avg = data.groupby('weathersit')['cnt'].mean()
plt.figure()
plt.plot(weather_avg)
plt.title("hava durumuna gore kullanım")
plt.show()




