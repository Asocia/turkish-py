This is a side project which tries to translate most common error messages and builtin types to Turkish. The motivation behind this is to help my 12yo brother who doesn't know English learn Python. It is impossible to localize everything without touching the source code of Python but this is more than enough for our current needs.

Here is an example run of script:
```
❯ ./turkishPy.sh
>>> f
Hata geri izlemesi (son yapılan çağrı en sonda):
  "<stdin>" dosyasında, 1. satırda
İsimHatası: isim 'f' tanımlı değil

>>> doğum_yılı = değeral("Doğum yılınızı giriniz:)
Hata geri izlemesi (son yapılan çağrı en sonda):
  "<stdin>" dosyasında, 1. satırda
    doğum_yılı = değeral("Doğum yılınızı giriniz:)
                                                 ^
SözDizimiHatası: yazı'yı okurken satır sonuna ulaşıldı

>>> doğum_yılı = değeral("Doğum yılınızı giriniz: ")
Doğum yılınızı giriniz: 2009

>>> yardım(yazdır)
Help on function yazdır in module turkish:

yazdır(*değer, ayır=' ', son='\n', dosya=Ekran)
    Verilen değerleri dosyaya yazdırır. Eğer dosya belirtilmemişse, bu varsayılan olarak Ekran'dır.
    İsteğe bağlı parametreler:
    ayır:  değerlerin arasına yerleştirilecek yazı
    son:   en son değerden sonra yerleştirilecek yazı
    dosya: dosya-türevi bir nesne, varsayılan olarak Ekran'dır.

>>> yazdır("Yaşınız: {}".format(2021 - doğum_yılı))
Hata geri izlemesi (son yapılan çağrı en sonda):
  "<stdin>" dosyasında, 1. satırda
TipHatası: - işlemi için desteklenmeyen tip(ler): 'tamsayı' ve 'yazı'

>>> doğum_yılı = tamsayı(doğum_yılı)
>>> yazdır("Yaşınız: {}".format(2021 - doğum_yılı))
Yaşınız: 12
```
