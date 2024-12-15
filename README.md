schema.sql:
Bu dosya veritabanı şemasını oluşturan SQL komutlarını içerir. Tüm CREATE TABLE ifadeleri, gerekli CONSTRAINT’ler, INDEX’ler vb. burada yer alacak.

mrp_queries.sql:
Burada MRP hesaplamaları için kullanılacak SQL sorguları bulunur. Örneğin, MRP hesaplaması sonucunda bir mrp_results tablosu oluşturmak veya güncellemek için gerekli sorgular

test_data.sql:
Bu dosya, test aşamasında veritabanına eklenecek örnek veri girişlerini içerir. Basit INSERT ifadeleri bulunabilir. Böylece test yaparken hızla örnek veriyi yükleyebilirsiniz.

main.py:
Veritabanına bağlanma fonksiyonları
setup_database() fonksiyonu (schema.sql’yi okuyup tablo oluşturma)
run_mrp() fonksiyonu (mrp_queries.sql’yi okuyup çalıştırma)
Gerekirse yardımcı fonksiyonlar (örneğin veritabanına ekleme, okuma işlemleri)

test.py:
setup_database() fonksiyonunu çağırarak boş bir DB kurarsınız.
test_data.sql içindeki test verisini veritabanına yüklersiniz (ya da Python koduyla da ekleyebilirsiniz).
run_mrp() fonksiyonunu çağırırsınız.
Sonrasında SELECT sorguları ile beklenen sonuçları karşılaştırarak assert ifadesiyle doğrulama yaparsınız.

ui.py:
Streamlit arayüz dosyası. Burada:
Kullanıcıdan gerekli girdiler alınır (ürün, tarih aralığı, vb.)
Bir butonla run_mrp() çağrılır
Sonuç tabloları ekrana yazdırılır.

---

Gerekli adımlar
Kurulum bilgileri
Çalıştırma komutları (ör. streamlit run ui.py)
Testin nasıl yapılacağı vb.
