#Cümleleri parçalama yapan algoritmam düzgün çalışmadığından dolayı NLTK(Natural Language Toolkit) kütüphanesi ile yapıldı
import nltk 
from nltk.tokenize import sent_tokenize
#Blok bitiş

#Metinden özel karakterlerin temizlenmesi için RE(Regular Expression) kütüphanesinde yardım alındı
import re
#Blok bitiş

#NLTK kütüphanesindeki stopwords içinde bulunan ve oradan temin edilen İngilizce gereksiz sözcükler
eng_stopwords={'same', 'between', 'can', "that'll", 'after', 'any', 'were', 'where', 'then', 'your', 'him', 'yours', "you'll", 'there', 'themselves', "you've", "you're", 'on', 'doing', 'to', 'isn', 'shouldn', 'we', 'before', 'ourselves', "hadn't", "haven't", 're', 'when', 'other', 'itself', 'than', 'yourself', 'my', 'down', 'yourselves', 'this', 'nor', 'too', 'through', 'here', 'a', 'their', 'of', 'its', 'by', 'hadn', "it's", 's', 'an', 'into', 'weren', 'why', 'such', 'own', 'now', 'it', 'they', 'been', 'i', 'needn', 've', 'wouldn', 'having', 'couldn', 'wasn', 'ours', "you'd", 'that', 'myself', 'she', 'each', 'haven', 'off', 'had', 'does', "shan't", 'her', 'up', 'in', 'during', 'will', "weren't", 'have', 'for', 'd', 'ma', "mightn't", 'against', 'under', 'as', 'he', 'few', "hasn't", 'more', 'doesn', 't', "didn't", 'about', 'be', "wouldn't", 'while', 'once', 'me', 'didn', "wasn't", 'won', 'the', 'you', 'was', 'if', 'most', 'is', 'from', 'further', 'over', 'at', 'until', 'aren', 'are', 'theirs', "mustn't", 'did', 'so', "needn't", 'what', "couldn't", 'out', 'mustn', 'y', 'shan', 'these', 'do', 'those', 'm', 'all', 'again', 'whom', 'no', 'just', 'below', 'or', 'which', "don't", 'very', 'should', 'being', 'because', 'ain', 'll', "isn't", 'only', "won't", 'and', 'how', 'herself', 'his', "she's", 'our', 'o', 'both', 'hasn', 'himself', 'them', 'has', 'but', 'not', 'don', "aren't", 'who', "shouldn't", 'with', 'hers', 'above', "should've", 'am', 'some', 'mightn', "doesn't"}
#Blok bitiş

#RE kütüphanesi ile metinden özel karakterleri kaldıran fonksiyon
def ozel_karakter_kaldirma(metin):
    metin=re.sub('[^a-zA-Z]',' ',metin)
    return metin
#Blok bitiş

#Metni küçük harflere çevirip ilk fonksiyon yardımıyla metni temizleme yapan fonksiyon
def metin_önislem(metin):
    metin=metin.lower()
    metin=ozel_karakter_kaldirma(metin)
    return metin
#Blok bitiş

#Daha önceki fonksiyonlar ile düzenlenen metni string fonksiyonları ile kelimelere ayırıp gereksiz sözcükler mevcut ise bu kelimeleri almadan metindeki tüm kelimeleri elde eden fonksiyon
def kelimelere_ayirma_ve_stopwords_kaldirma(metin):
    kelimeler=[kelime for kelime in metin.split(' ') if kelime!='']
    kelimeler=[kelime for kelime in kelimeler if kelime.lower() not in eng_stopwords]
    return kelimeler
#Blok bitiş

#Gereksiz sözcükler olmadan parçada anlam ifade edebilecek kelimeler bir önceki fonksiyon yardımıyla elde edildi.Bu kelimeler bu fonksiyonda kullanılarak en az 2 harften oluşan kelimeler, kelime_frekanslari sözlüğünde(dictionary) tutularak fonksiyondaki gerekli işlemler yapılır ve böylece kelimelerin elimizdeki metinde kaç kere geçtiği hesaplanır. Yani kelime frekanslarını bulmuş oluruz.
def frekans_hesaplama(kelimeler):
    kelime_frekanslari={}
    for kelime in kelimeler:
        if len(kelime)>=2:
            if kelime not in kelime_frekanslari.keys():
                kelime_frekanslari[kelime]=1
            else:
                kelime_frekanslari[kelime]+=1
    return kelime_frekanslari
#Blok bitiş

#İlk başta yaptığım açıklama kapsamında benim geliştirdiğim cümlelere ayırma algoritması ve fonksiyonu. Cursor değişkeni metnin başlangıcı için 0'a atandı. Daha sonra benim algoritmama bağlı olarak cümlede (.!?) ifadelerini bulma durumunda sağında bir boşluk varsa yani kurallı ve düzgün bir cümle ise cumleler dizi değişkenine cursordan itibaren metnin o noktasına kadar alacak. Cursor değişkenine i değişkenini arttırarak verdiğimizde diğer cümlede başlangıç noktamızı belirtmiş oluyoruz. İlk if bloğunda ise metnin sonunda (.!?) ifadeleri bulunmuyorsa, kullanıcınında düzgün metin vermeme olasılığı öngörülerek harf veya farklı bir özel karakter ile bitiyorsa metin sonuna nokta ve boşluk eklenerek metnin son cümlesini almama durumunu engelledim.Bu algoritmanın açığına örnek verecek olursam:"e.g." gibi cümle içinde bir kısaltma var ise "e."ya kadar bir cümle "g." ayrı bir cümle olarak algılanıyor. Diğer bir durum ise "1. grafikteki şekilde de anlaşılacağı bir özel bir durum vardır." cümlesindeki gibi "1." ilk cümle kalanı ise diğer cümle olarak algılanıyor.Şimdilik geliştirme yapana kadar kütüphane desteği ile bu bölümü halledeceğim.
# def cumlelere_ayirma(metin):
#     cursor=0
#     cumleler=[]
#     if(metin[-1]!="." or metin[-1]!="!" or metin[-1]!="?"):
#         metin+=". "
#     for i in range(len(metin)):
#         if (metin[i]=="." or metin[i]=="!" or metin[i]=="?") and (metin[i+1]==' '):
#             cumleler.append(metin[cursor:i+1])
#             i+=1
#             cursor=i
#     return cumleler
#Blok Bitiş

#NLTK ile parçalanan cümleler ve daha önceki fonksiyonlar ile hazırlanan kelime frekansları fonksiyona parametre olarak veriliyor. Sonuçlar cumle_puanlari sözlüğünde tutulacak. Cümleler üzerinde for döngüsü ile baştan sona geziniyoruz. Bunun içinde kelime frekansları dictionary fonksiyonu items ile elemanları üzerinde geziniyoruz. Daha önceki fonksiyonlarda kelimeleri küçülterek tuttuğumuz için cümleyi de küçülterek, kelimemiz cümle içinde var mı şartını koyuyoruz. Bu durumda ikinci şartımızı ise cümlemiz daha önceden cumle_puanlari sözlüğüne atılmış mı diye koyuyoruz. Eğer iki şartta sağlıyor ise sözlüğümüzde bu cümle vardır ve kelimenin frekans değerini sözlüğün value kısmında arttırırız. Eğer cümlemiz sözlükte mevcut değilse sözlükte key kısmı cümlemiz olan ve value kısmı kelimenin frekansı ile oluşturulur.Böylece kelimelerin frekansları ile cümlelerin puan değerleri hesaplanır.
def cumle_puan_hesaplama(cumleler,kelime_frekanslari):
    cumle_puanlari={}
    for cumle in cumleler:
        for kelime,frekans in kelime_frekanslari.items():
            if kelime in cumle.lower():
                if cumle in cumle_puanlari:
                    cumle_puanlari[cumle]+=frekans
                else:
                    cumle_puanlari[cumle]=frekans
    return cumle_puanlari
#Blok bitiş

#Daha önceki fonksiyonların kullanılmasıyla sonuç olarak özet metni verecek fonksiyon. Parametre olarak inputtan gelen metin ve kendi belirlediğimiz özetin kaç cümle içereği bilgilerini alıyor.
def ozet_olustur(metin,cumle_sayisi=5):
    islenmis_metin=metin_önislem(metin)#Metni küçült ve özel karakterleri kaldır
    kelimeler=kelimelere_ayirma_ve_stopwords_kaldirma(islenmis_metin)#İşlenmiş metinden, tüm metinde anlam ifade eden kelimeler
    kelime_frekanslari=frekans_hesaplama(kelimeler)#Anlamlı kelimelerin metindeki frekansları(tekrar sayıları)
    cumleler=sent_tokenize(metin)#NLTK ile metindeki cümleleri parçalama
    cumle_puanlari=cumle_puan_hesaplama(cumleler,kelime_frekanslari)#Cümleler ve kelime frekansları ile cümle puanı hesaplama

    #Cümle puanlarının elemanlarının büyükten küçüğe sıralanması (key=lambda => burası anonim bir fonksiyona göre sıralanacağını belirtir ve x:x[1] => bu kısım ise anonim fonksiyonun 1. indise göre sıralama yapacağını söyler. reverse=True => sıralamayı tersine çevirir. )
    sirali_cumleler=sorted(cumle_puanlari.items(),key=lambda x:x[1],reverse=True)
    #Blok bitiş

    ozet_cumleleri=[cumle[0] for cumle in sirali_cumleler[:cumle_sayisi]]#Sıralı cümlelerin belirlenen cümle sayısına kadar olan kısmı alınarak özet cümleleri oluşturulur. cumle[0] değişkeni ile sıralı cümlelerin 0. indisi yani cümleler alınır. Eğer cumle[1] deseydik elimizde cümlelerin frekans değerleri olurdu.

    ozet=" ".join(ozet_cumleleri)#Özet cümleleri elimizde list biçiminde mevcut. Join fonksiyonu yardımıyla list biçimindeki veriyi stringe yani tekdüze bir metne dönüştürüyoruz.
    return ozet

if __name__=="__main__":
    metin=input("Metni girin: ")#İnputtan metin alındı
    ozet=ozet_olustur(metin)#Özet oluşturma fonksiyonu çağırıldı
    print("\nÖzet metin:\n",ozet)#Özet metni ekrana yazıldı