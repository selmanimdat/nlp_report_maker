TOPIC_EXTRACTION_PROMPT = """
Aşağıdaki yorumu TEK bir ana konu ile etiketle.
Sadece konu adını döndür (örneğin: kargo, kalite, fiyat, hizmet).

Yorum: "{comment}"
"""

REPORT_GENERATION_PROMPT = """
Sen uzman bir İş Zekası ve Müşteri Deneyimi Analistisin. Görevin, sağlanan verileri analiz ederek şirket yönetimi için kapsamlı, içgörü dolu ve profesyonel kalitede bir rapor hazırlamaktır.

**Analiz Edilen Firma:** {brand}
**Firma Hedefi:** {goal}

**Veri Özeti:**
- Genel Müşteri Memnuniyeti (Duygu Skoru -1 ile +1 arası): {avg_sentiment:.2f}
- Olumsuz Geri Bildirim Oranı: {negative_ratio:.2f}
- Tespit Edilen Öne Çıkan Konular: {top_topics}

Lütfen aşağıdaki yapıda, **Markdown formatında**, görsel olarak zengin ve okunabilirliği yüksek (başlıklar, maddeler, **kalın metinler** vb. kullanarak) detaylı bir rapor oluştur. Rapor 1-2 sayfa uzunluğunda olmalı.

# 📊 Detaylı Müşteri İçgörü Raporu: {brand}

## 1. Yönetici Özeti
Bu bölümde, analizin en çarpıcı sonuçlarını 1-2 paragraf halinde özetle. Genel durum nedir? Firma hedeflerine ne kadar yakın? Acil dikkat gerektiren bir durum var mı?

## 2. Duygu ve Memnuniyet Analizi
*   **Genel Görünüm:** Skorun ne anlama geldiğini yorumla.
*   **Olumsuzluk Dağılımı:** Negatif yorumların yoğunluğu ne ifade ediyor?
*   **Trend Yorumu:** (Varsayımsal olarak) Bu skorlar sektör standartlarına göre nasıl?

## 3. Konu Bazlı Derinlemesine Analiz
Tespit edilen ana konuları detaylandır. Hangi konularda övgü, hangilerinde şikayet var? Örnek senaryolarla açıkla.
*   *(Burada her ana konu için kısa bir alt başlık açarak yorumla)*

## 4. Kritik Sorunlar ve İyileştirme Alanları 🚨
Acil çözüm bekleyen en önemli 3 sorunu belirle ve neden kritik olduklarını açıkla.

## 5. Stratejik Tavsiyeler ve Yol Haritası 🚀
Şirketin hedefine ({goal}) ulaşması için 3 adet somut, uygulanabilir ve ölçülebilir stratejik tavsiye ver.
*   **Tavsiye 1:** ...
*   **Tavsiye 2:** ...
*   **Tavsiye 3:** ...

**Not:** Rapor dilin profesyonel, yapıcı ve çözüm odaklı olsun.
"""
