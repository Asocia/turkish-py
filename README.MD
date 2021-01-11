This project aims to translate most common error messages and builtin types to Turkish. The motivation behind this is to help my 12yo brother who doesn't know English [learn Python](https://github.com/beratakkaya0/python-alistirmalari). It is impossible to localize everything without touching the source code of Python but this is more than enough for our current needs.

Here is an example run of the script:
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

>>> yaş = 2021 - doğum_yılı
Hata geri izlemesi (son yapılan çağrı en sonda):
  "<stdin>" dosyasında, 1. satırda
TipHatası: - işlemi için desteklenmeyen tip(ler): 'tamsayı' ve 'yazı'

>>> yardım(tip)
Help on function tip in module turkish:

tip(nesne)
    Verilen nesne'nin tipini döndürür.

>>> tip(doğum_yılı)
<sınıf 'yazı'>
>>> doğum_yılı = tamsayı(doğum_yılı)
>>> tip(doğum_yılı)
<sınıf 'tamsayı'>
>>> yaş = 2021 - doğum_yılı
>>> yaş
12
>>> yaş == 12
Doğru
```
