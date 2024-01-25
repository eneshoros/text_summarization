#Gerekli kütüphanelerin eklenmesi
from PyQt5 import QtWidgets#Arayüz tasarımı için PyQt5
import sys#Arayüz işleminin kapanması için sys
from arayuz import Ui_Form#PyQt5 ile oluşturulan arayüzün, arayuz.py dosyasındaki Ui_Form class'ını dahil ediyoruz
from deep_translator import GoogleTranslator,single_detection#Metindeki translate işlemleri için deep_translator'dan GoogleTranslator çağırma. Verilen metnin dilini algılamak için sigle_detection fonksiyonu dahil edilir
import nltk#Doğal dil işleme için nltk kütüphanesini ekliyoruz
import math#Matematiksel işlemler için math kütüphanesi ekleniyor
from nltk import word_tokenize,sent_tokenize#Kelime ve cümle parçalama fonksiyonları nltk'den dahil ediliyor
from nltk.stem import WordNetLemmatizer#Kelime kökünü lemmatization ile bulmak için nltk.stem'den WordNetLemmatizer çağırıyoruz
from nltk.corpus import stopwords#Metindeki gereksiz sözcükleri atmak için nltk.corpus'dan stopwords'leri alıyoruz
#Blok bitiş

#Fonksiyonlar başlangıç
#Frekans matrisini oluşturmak için fonksiyon
def frekans_matrisi_olusturma(cumleler):
    frekans_matrisi={}#Frekans matrisi için set(küme) değişkeni
    stopWords=set(stopwords.words('english'))#Frekans matrisinde gereksiz sözcüklerin olmaması için bu sözcükleri tutan değişken
    lemmatizer=WordNetLemmatizer()#Kök bulmak için class'dan değişken türetme
    for cumle in cumleler:#Metindeki bütün cümleleri tek tek geziyoruz
        frekans_tablosu={}#Her cümle için frekans tablosu set(küme) değişkeni
        kelimeler=word_tokenize(cumle)#Her cümle için kelimelere parçalama(tokenize) işlemi
        for kelime in kelimeler:#Cümledeki her kelimeyi tek tek geziyoruz
            kelime=kelime.lower()#Kelimeyi küçült
            kelime=lemmatizer.lemmatize(kelime)#Kelime kökünü bul
            if kelime in stopWords:#Kökü bulunan kelime gereksiz bir kelime mi
                continue
            if kelime in frekans_tablosu:#Kökü bulunan kelime tabloda var mı
                frekans_tablosu[kelime]+=1
            else:#Tabloda yok ise oluştur
                frekans_tablosu[kelime]=1
        frekans_matrisi[cumle[:19]]=frekans_tablosu#Her cümle için oluşturulan frekans tablosunu, o cümlenin ilk 19 karakteri key olacak şekilde value değeri olarak atanır
    return frekans_matrisi#Oluşturulan matrisi döndür
#Blok bitiş

#Kelime frekans(Term Frequency) matrisi oluşturmak için fonksiyon
def tf_matrisi_olustur(frekans_matrisi):
    tf_matrisi={}#Kelime frekans matrisi için set(küme) değişkeni
    for cumle,freq_tablosu in frekans_matrisi.items():#Frekans matrisi elemanlarına ulaşıyoruz
        tf_tablosu={}#Her cümlenin kelime frekansı değerlerini tutacak set(küme) değişkeni
        cks=len(freq_tablosu)#Her eleman için frekans tablosunun eleman sayısı o cümledeki kelime sayısını verir
        for kelime,kts in freq_tablosu.items():#Frekans tablosu elemanlarına ulaşıyoruz,kts=kelime tekrar sayısı
            tf_tablosu[kelime]=kts/cks#Kelime tekrar sayısı, cümledeki kelime sayısına bölünerek o kelimenin frekansı bulunur. Kelime frekans tablosuna bu kelimenin frekansı atanır
        tf_matrisi[cumle]=tf_tablosu#Her cümle için oluşturulan kelime frekans tablosunu, o cümle key değeri olacak şekilde value değeri olarak atanır
    return tf_matrisi#Oluşturulan matrisi döndür
#Blok bitiş

#Kelimenin kaç cümlede geçtiğini hesaplama için fonksiyon
def kelime_basina_cumle_say(frekans_matrisi):
    kbcs_tablosu={}#Kelimeleri ve kaç cümlede geçtiğini tutacak set(küme) değişkeni
    for cumle,freq_tablosu in frekans_matrisi.items():#Frekans matrisinin tüm elemanlarını tek tek geziyoruz
        for kelime,kts in freq_tablosu.items():#Frekans matrisinin her elemanı için, frekans tablosu elemanlarını tek tek geziyoruz
            if kelime in kbcs_tablosu:#Kelime, kbcs_tablo değişkeni içinde var mı
                kbcs_tablosu[kelime]+=1
            else:#Tabloda yok ise oluştur
                kbcs_tablosu[kelime]=1
    return kbcs_tablosu#Her kelimenin kaç cümlede geçtiği bilgisini key,value olarak tutan değişkeni döndür
#Blok bitiş

#Ters cümle frekans(Inverse Sentence Frequency) matrisi oluşturmak için fonksiyon
def isf_matrisi_olustur(frekans_matrisi,cbks,toplam_cumle_sayisi):
    isf_matrisi={}#Ters cümle frekans matrisi için set(küme) değişkeni
    for cumle,freq_tablosu in frekans_matrisi.items():#Frekans matrisi elemanlarına ulaşıyoruz
        isf_tablosu={}#Her cümlenin, ters cümle frekansı değerlerini tutacak set(küme) değişkeni
        for kelime in freq_tablosu.keys():#Frekans tablosunun key değerlerine yani kelimelere ulaşıyoruz
            isf_tablosu[kelime]=math.log10(toplam_cumle_sayisi/float(cbks[kelime]))#Cümledeki her kelimenin isf değeri, metindeki toplam cümle sayısının o kelimenin kaç cümlede geçtiğine bölünerek hesaplanır
        isf_matrisi[cumle]=isf_tablosu#Her cümlenin isf değeri o cümleye ait isf matrisine atanır
    return isf_matrisi#Hesaplanan isf matrisini döndür
#Blok bitiş

#Kelime frekansı ve isf değerlerini kullanarak tf*isf değeri oluşturan fonksiyon
def tf_isf_matrisi_olustur(tf_matrisi,isf_matrisi):
    tf_isf_matrisi={}#Tf*isf değerlerini tutmak için set(küme) değişkeni
    for (cumle1,freq_tablosu1),(cumle2,freq_tablosu2) in zip(tf_matrisi.items(),isf_matrisi.items()):#Kelime frekans matrisi ile isf matrisini zip ile tek matris yaparak bu matris üzerinde tek tek geziyoruz
        tf_isf_tablosu={}#Her elemanın tf*isf değerlerini tutmak için set(küme) değişkeni
        for (kelime1,deger1),(kelime2,deger2) in zip(freq_tablosu1.items(),freq_tablosu2.items()):#Her cümlenin kelime frekans ve isf değerlerini zip ile tek matris yapıp bu matris üzerinde tek tek geziyoruz
            tf_isf_tablosu[kelime1]=float(deger1*deger2)#Her kelimenin frekansı ile isf değeri çarpılarak o kelimeye ait tablo değişkene atanır
        tf_isf_matrisi[cumle1]=tf_isf_tablosu#Cümledeki her kelimenin hesaplanmış tf*isf değeri o cümleye ait matris değişkenine atanır
    return tf_isf_matrisi#Hesaplanan tf*isf matrisini döndür
#Blok bitiş

#Cümle puanlarını hesaplayan fonksiyon
def cumle_puanlama(tf_isf_matrisi):
    cumleDegeri={}#Cümle değerlerini tutacak set(küme) değişkeni
    for cumle,freq_tablosu in tf_isf_matrisi.items():#Tf*isf matrisi elemanlarını tek tek geziyoruz
        cbtp=0#Her cümle için cümle başına toplam puanı tutacak değişken
        cks=len(freq_tablosu)#Her cümle için cümledeki kelime sayısını tutacak değişken
        for kelime,puan in freq_tablosu.items():#Cümlenin frekans tablosu elemanlarına ulaşıyoruz
            cbtp+=puan#Kelimelerin puanlarını toplam puan değişkenine atıyoruz
        cumleDegeri[cumle]=cbtp/cks#Toplam puanı cümledeki kelime sayısına bölerek cümlenin değerini hesaplayıp o cümleye ait değişkene atıyoruz
    return cumleDegeri#Tüm cümlelerin değerlerini tutan değişkeni döndür
#Blok bitiş

#Tüm cümlelerin ortalama puanını hesaplayan fonksiyon
def ortalama_puan_bulma(cumleDegeri):
    toplam_cumle_degeri=0#Ortalamayı bulmak için gerekli olan toplam cümle değeri değişkeni
    for cumle in cumleDegeri:#Cümle değerlerini tek tek geziyoruz
        toplam_cumle_degeri+=cumleDegeri[cumle]#Her cümlenin cümle değerini toplam değişkenine ekliyoruz
    ortalama=(toplam_cumle_degeri/len(cumleDegeri))#Toplam cümle değerini, toplam cümle sayısına bölerek ortalama cümle değerinin hesaplıyoruz
    return ortalama#Ortalama cümle değerini döndür
#Blok bitiş

#Metindeki cümleleri, cümle değerlerinin cümle eşik puanına eşit veya büyük olduğu durumlarda özetleyen fonksiyon
def ozet_olustur(cumleler,cumleDegeri,cumle_esik_puani):
    ozet=''#Oluşturulacak özetin tutulacağı değişken
    for cumle in cumleler:#Cümleleri tek tek geziyoruz
        if cumle[:19] in cumleDegeri and cumleDegeri[cumle[:19]]>= cumle_esik_puani:#Gelen cümle, cümle değerleri içerisindeyse ve cümle değeri, cümle eşik puanına eşit veya büyükse
            ozet+= ' ' + cumle#Şartı sağlayan cümle özete eklenir
    ozet=ozet.strip()#Özetin sol,sağ kısmındaki boşlukları kaldır
    return ozet#Şartı sağlayan bütün cümlelerin oluşturduğu özeti döndür
#Blok bitiş
#Fonksiyonlar bitiş

#Class Başlangıç
class ozet_class(QtWidgets.QMainWindow):
    #Constructor oluşturma
    def __init__(self):
        super(ozet_class,self).__init__()#Üst sınıftan miras alma
        self.ui=Ui_Form()#arayuz.py içindeki Ui_Form class'ına artık self.ui diyerek erişebiliriz
        self.ui.setupUi(self)#setupUi fonksiyonu self ile çağırılarak, self.ui artık arayüz elemetlerine erişim sağlayabilir
        self.ui.ozetle_btn.clicked.connect(self.ozet_hazirlik)#Arayüzde "ozetle_btn" butonuna tıklandığında "ozet_hazirlik" fonksiyonunu çağırır
    #Constructor bitiş
        
    #Özet metni verecek fonksiyon. Parametre self alarak bütün fonksiyonlara ve class'a erişim sağlayabiliyor.
    def ozet_hazirlik(self):
        metin=self.ui.arayuz_metin.toPlainText()#"arayuz_metin" elementinin içeriği text olarak alınarak metine ata
        # metin=''.join([i for i in metin if not i.isdigit()])#Metindeki sayısal değerleri temizle
        metin_dili=single_detection(metin,api_key='2a10ac925bb4a61c23099549ee1404de')#"single_detection" fonksiyonu ile metnin dili algılandı
        dil_secim=self.ui.comboBox.currentText()#"comboBox" elementinin içeriği alınarak hangi dilde özet istenildiği bilgisi değişkene atandı
        metin=GoogleTranslator(source=metin_dili,target='en').translate(metin)#Metnin dili ne olursa olsun İngilizce'ye çevirilerek kelimelere ve cümlelere parçalama, kök bulma işlemi İngilizce'ye göre yapıldı
        cumleler=sent_tokenize(metin)#Metni cümlelere parçalama
        toplam_cumle_sayisi=len(cumleler)#Cümleler listesinin uzunluğundan toplam cümle sayısı
        frekans_matrisi=frekans_matrisi_olusturma(cumleler)#Cümleler listesi ile frekans matrisi oluşturma
        tf_matrisi=tf_matrisi_olustur(frekans_matrisi)#Frekans matrisi ile kelime frekans matrisi hesaplama
        kbcs=kelime_basina_cumle_say(frekans_matrisi)#Frekans matrisi ile kelimenin geçtiği cümle sayısını bulma
        isf_matrisi=isf_matrisi_olustur(frekans_matrisi,kbcs,toplam_cumle_sayisi)#Isf matrisini hesaplama
        tf_isf_matrisi=tf_isf_matrisi_olustur(tf_matrisi,isf_matrisi)#Tf*isf matrisini hesaplama
        cumle_puanlari=cumle_puanlama(tf_isf_matrisi)#Her cümlenin cümle puanını hesaplama
        ortalama=ortalama_puan_bulma(cumle_puanlari)#Cümlelerin ortalama cümle puanını hesaplama
        ozet_katsayi=0.0
        ozet_oran=(int)(self.ui.comboBox_2.currentText())
        if ozet_oran!=50: ozet_katsayi=ozet_oran/50
        else : ozet_katsayi=1.0
        ozet=ozet_olustur(cumleler,cumle_puanlari,ozet_katsayi*ortalama)#Belirli bir ortalamanın üstünde daha doğru bir özet çıkarmasını sağlayarak özeti oluşturmak
        if(dil_secim=='Türkçe'):#Özet istenen dil Türkçe ise 
            ozet=GoogleTranslator(source='en',target='tr').translate(ozet)#Daha önceden İngilizce'ye çevirilen metni Türkçe'ye çevir
        self.ui.arayuz_ozet_metin.setPlainText(ozet)#"arayuz_ozet_metin" elementine metnin özeti setPlainText fonksiyonu ile yazdırılır
        self.ui.label_2.setText(f'Metindeki kelime sayısı: {len(metin.split(" "))}')#Özeti istenen metinin kelime sayısı "label_2" elementinde gösterilir
        self.ui.label_4.setText(f'Özet metindeki kelime sayısı: {len(ozet.split(" "))}')#Özet metninin kelime sayısı "label_4" elementinde gösterilir
#Class Bitiş

#Arayüzü gösterme fonksiyonu
def app():
    app=QtWidgets.QApplication(sys.argv)#Arayüz uygulamasını yöneten sınıftan nesne türetimi
    win=ozet_class()#Arayüz olarak gösterilecek class'dan nesne türetimi
    win.show()#Arayüz nesnesini göster
    sys.exit(app.exec_())#Arayüz kapatılırsa uygulamayı durdur

app()#app fonksiyonunu çağır ve uygulamayı başlatarak arayüzü göster
#Blok bitiş