# 1. İş Problemi (Business Problem)

# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
# pazarlama stratejileri belirlemek istiyor.
#
# Buna yönelik olarak müşterilerin davranışlarını tanımlayacağız ve
# bu davranışlarda öbeklenmelere göre gruplar oluşturacağız.
#
# Yani ortak davranışlar sergileyenleri aynı gruplara alacağız ve
# bu gruplara özel satış ve pazarlama teknikleri geliştirmeye çalışacağız.
#
# Veri Seti Hikayesi
#
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II
#
# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.
#
# Bu şirket hediyelik eşya satıyor. Promosyon ürünleri gibi düşünebilir.
#
# Müşterilerinin çoğu da toptancı.
#
# Değişkenler
#
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.


# Görev 1: Veriyi Anlama (Data Understanding)

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
# Bütün satırları göster
pd.set_option('display.max_rows', None)
# Bütün sutünları göster
pd.set_option('display.float_format', lambda x: '%.5f' % x)
# Virgülden sonra 5 basamak göster

# 1. Online Retail II excelindeki 2010-2011 verisini okuyunuz. Oluşturduğunuz dataframe’in kopyasını oluşturunuz.

df_ = pd.read_excel(r"C:\Users\Casper\PycharmProjects\DataScience\Proje\online_retail_II.xlsx",
                    sheet_name="Year 2010-2011")
df = df_.copy()

# 2. Veri setinin betimsel istatistiklerini inceleyiniz.

df.head()
df.shape
df.describe().T

# 3. Veri setinde eksik gözlem var mı? Varsa hangi değişkende kaç tane eksik gözlem vardır?

df.isnull().sum()

# 4. Eksik gözlemleri veri setinden çıkartınız. Çıkarma işleminde ‘inplace=True’ parametresini kullanınız.

df.isnull().sum()

# 5. Eşsiz ürün sayısı kaçtır?
df["Description"].nunique()

# 6. Hangi üründen kaçar tane vardır?

df["Description"].value_counts().head()

# 7. En çok sipariş edilen 5 ürünü çoktan aza doğru sıralayınız.

df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity", ascending=False).head()

# 8. Faturalardaki ‘C’ iptal edilen işlemleri göstermektedir. İptal edilen işlemleri veri setinden çıkartınız.

df = df[~df["Invoice"].str.contains("C", na=False)]

# 9. Fatura başına elde edilen toplam kazancı ifade eden ‘TotalPrice’ adında bir değişken oluşturunuz.

df["TotalPrice"] = df["Quantity"] * df["Price"]
df.head()
####################################################################################################

# Görev 2: RFM metriklerinin hesaplanması

# Recency, Frequency ve Monetary tanımlarını yapınız.

# Recency: Müşterinin kaç gün önce geldiği
# Frequency: Kaç ürün aldığının sıklığı
# Monetary: Bıraktığı parasal değer

# Müşteri özelinde Recency, Frequency ve Monetary metriklerini groupby, agg ve lambda ile
# hesaplayınız.

df["InvoiceDate"].max()

today_date = dt.datetime(2011,12,11)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                     'Invoice': lambda Invoice :  Invoice.nunique()  ,
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()}).head()

rfm.head()
# Hesapladığınız metrikleri rfm isimli bir değişkene atayınız.

# Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz.
rfm.columns = ['recency', 'frequency', 'monetary']

# İpucu:
# Not 1: recency değeri için bugünün tarihini (2011, 12, 11) olarak kabul ediniz.
# Not 2: rfm dataframe’ini oluşturduktan sonra veri setini "monetary>0" olacak şekilde filtreleyiniz.

#####################################################################

#Görev 3: RFM skorlarının oluşturulması ve tek bir değişkene çevrilmesi

# Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.


rfm["Recency"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["Frequency"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels= [1, 2, 3, 4, 5]
<#rfm["Monetary"] = pd.qcut(rfm['monetary'], 5, labels= [1, 2, 3, 4, 5])

rfm.columns

# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz.

rfm['recency_score'] = pd.qcut(rfm['recency'], 5, labels= [5, 4, 3, 2, 1])
rfm['frequency_score'] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels= [1, 2, 3, 4, 5])
rfm['monetary_score'] = pd.qcut(rfm['monetary'], 5, labels= [1, 2, 3, 4, 5])



# Oluşan 2 farklı değişkenin değerini tek bir değişken olarak ifade ediniz ve RFM_SCORE olarak kaydediniz.
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str)+
                    rfm['frequency_score'].astype(str)
                  )

rfm.head()

# Örneğin;
# Ayrı ayrı değişkenlerde sırasıyla 5, 2 olan recency_score, frequency_score skorlarını RFM_SCORE değişkeni
# isimlendirmesi ile oluşturunuz.
# DİKKAT! Monetary skoru dahil etmiyoruz

######################################################

# Görev 4: RFM skorlarının segment olarak tanımlanması

# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlamaları
# yapınız.

seg_map = {
    r'[1-2][1-2]': 'hibernating',          #kış uykusunda
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',               #Kaybedemem
    r'3[1-2]': 'about_to_sleep',           #Uyumak üzere
    r'33': 'need_attention',               #Dikkat gerekli
    r'[3-4][4-5]': 'loyal_customers',      #Sadık müşteriler
    r'41': 'promising',                    #Umut verici
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',  #Potansiyel sadıklar
    r'5[4-5]': 'champions'
}


# Aşağıdaki seg_map yardımı ile skorları segmentlere çeviriniz.
rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

rfm.head()

########################################
# Önemli bulduğunuz 3 segmenti seçiniz. Bu üç segmenti;
# Hem aksiyon kararları açısından,
# Hem de segmentlerin yapısı açısından (ortalama RFM değerleri)
# yorumlayınız.

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])


# "Loyal Customers" sınıfına ait customer ID'leri seçerek excel çıktısını alınız.

loyal_customers = pd.DataFrame()
loyal_customers["LoyalCustomersCustomerID"]= rfm[rfm["segment"]=='loyal_customers'].index
loyal_customers.head()


