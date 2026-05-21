# BİLET-BUL | Otobüs Biletleme ve Rezervasyon Sistemi

[cite_start]BİLET-BUL, şehirlerarası yolcu taşımacılığı sektöründe biletleme süreçlerini dijitalleştiren ve otomatize eden web tabanlı bir merkezi rezervasyon sistemidir[cite: 62, 76]. [cite_start]Python tabanlı Django Framework kullanılarak Model-View-Template (MVT) mimarisinde kurgulanmıştır[cite: 64]. 

[cite_start]Bu proje, Ankara Üniversitesi Bilgisayar Mühendisliği Araştırma Projesi kapsamında geliştirilmiştir[cite: 1, 2, 3].

## Öne Çıkan Özellikler

* [cite_start]**Dinamik Koltuk Haritalama:** 2+1 ve 2+2 otobüs yerleşimlerini dinamik olarak destekler[cite: 65].
* [cite_start]**Cinsiyet Temelli Kısıtlamalar:** Koltuk seçimlerinde cinsiyete (Erkek/Kadın) dayalı yerleşim kurallarını gerçek zamanlı olarak uygular[cite: 65].
* [cite_start]**Çifte Rezervasyon Koruması:** Veritabanı seviyesinde uygulanan `unique_together` algoritmaları sayesinde aynı koltuğun aynı anda iki kişiye satılmasını (Race Condition) kesin olarak engeller[cite: 66].
* [cite_start]**Esnek Biletleme:** Hem kayıtlı üyeler hem de sisteme giriş yapmamış misafir kullanıcılar (Guest) için biletleme desteği sunar[cite: 154, 155].
* [cite_start]**Dinamik Çıktı Üretimi:** Biletleme sonrası tarayıcı tabanlı entegre motor ile PDF formatında bilet çıktısı üretir[cite: 68].

## Kullanılan Teknolojiler

* [cite_start]**Backend:** Python, Django 5.2 Framework [cite: 89]
* [cite_start]**Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5 [cite: 90, 102]
* [cite_start]**Veritabanı:** SQLite / PostgreSQL (İlişkisel Veri Modeli) [cite: 70, 144]
* [cite_start]**Mimari:** İstemci-Sunucu (Client-Server), MVT [cite: 77, 105]

## Yerel Ortamda Kurulum (Installation)

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla izleyebilirsiniz:

**1. Depoyu Klonlayın**
```bash
git clone [https://github.com/Impasbaa/bilet-bul-django.git](https://github.com/Impasbaa/bilet-bul-django.git)
cd bilet-bul-django
