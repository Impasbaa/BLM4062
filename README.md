# BİLET-BUL | Otobüs Biletleme ve Rezervasyon Sistemi

BİLET-BUL, şehirlerarası yolcu taşımacılığı sektöründe biletleme süreçlerini dijitalleştiren ve otomatize eden web tabanlı bir merkezi rezervasyon sistemidir. Python tabanlı Django Framework kullanılarak Model-View-Template (MVT) mimarisinde kurgulanmıştır. 

Bu proje, Ankara Üniversitesi Bilgisayar Mühendisliği Araştırma Projesi kapsamında geliştirilmiştir.

## Öne Çıkan Özellikler

* **Dinamik Koltuk Haritalama:** 2+1 ve 2+2 otobüs yerleşimlerini dinamik olarak destekler.
* **Cinsiyet Temelli Kısıtlamalar:** Koltuk seçimlerinde cinsiyete (Erkek/Kadın) dayalı yerleşim kurallarını gerçek zamanlı olarak uygular.
* **Çifte Rezervasyon Koruması:** Veritabanı seviyesinde uygulanan `unique_together` algoritmaları sayesinde aynı koltuğun aynı anda iki kişiye satılmasını (Race Condition) kesin olarak engeller.
* **Esnek Biletleme:** Hem kayıtlı üyeler hem de sisteme giriş yapmamış misafir kullanıcılar (Guest) için biletleme desteği sunar.
* **Dinamik Çıktı Üretimi:** Biletleme sonrası tarayıcı tabanlı entegre motor ile PDF formatında bilet çıktısı üretir.

## Kullanılan Teknolojiler

* **Backend:** Python, Django 5.2 Framework
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
* **Veritabanı:** SQLite / PostgreSQL (İlişkisel Veri Modeli)
* **Mimari:** İstemci-Sunucu (Client-Server), MVT

## Yerel Ortamda Kurulum (Installation)

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla izleyebilirsiniz:

**1. Depoyu Klonlayın**
```bash
git clone [https://github.com/Impasbaa/bilet-bul-django.git](https://github.com/Impasbaa/bilet-bul-django.git)
cd bilet-bul-django
