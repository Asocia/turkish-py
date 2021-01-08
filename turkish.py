import sys
import traceback
import re

builtins = {
    "string": "yazı",
    "str": "yazı",
    "int": "tamsayı",
    "float": "noktalısayı",
    "dict": "sözlük",
    "list": "liste",
    "type": "tip",
    "function": "fonksiyon",
    "tuple": "demet",
    "set": "küme",
}

compiled = re.compile("|".join(rf"\b{i}\b" for i in builtins.keys()))

catch_indentation_errors = False


def change_types(obj):
    b = obj.group()
    return builtins[b]


def translate_types(text):
    return compiled.sub(change_types, text)


def simplify_error_location(text):
    return re.sub(r'File "(?:.*/)?(.*)", line (\d+).*', r'"\1" dosyasında, \2. satırda', text)

def get_type(type_):
    type_name = type_.__name__
    exceptions = {
        "ValueError": "DeğerHatası",
        "NameError": "İsimHatası",
        "TypeError": "TipHatası",
        "SyntaxError": "SözDizimiHatası",
        "IndentationError": "GirintilemeHatası",
        "IndexError": "İndeksHatası",
        "KeyError": "AnahtarHatası",
        "ZeroDivisionError": "SıfıraBölmeHatası",
        "FileNotFoundError": "DosyaBulunamadıHatası",
        "AttributeError": "NitelikHatası",
        "ModuleNotFoundError": "ModülBulunamadıHatası",
        "MemoryError": "BellekHatası",
        "UnboundLocalError": "AtanmamışYerelHatası",
        "KeyboardInterrupt": "KlavyeMüdahalesi",
    }
    turkish_type_name = exceptions.get(type_name)
    if turkish_type_name is None:
        return type_
    else:
        return type(turkish_type_name, (type_,), {})


def turkish_excepthook(type_, value, tb):
    type_ = get_type(type_)

    error_explanations = {
        r"invalid literal for int\(\) with base (\d+): ([\"'])([^\2]+)\2": r"taban-> \1 tabanındaki tamsayı() için geçersiz değer: \2\3\2",
        r"could not convert string to float: ([\"'])([^\1]+)\1": r"yazı-> \1\2\1 noktalısayı'ya çevrilemiyor",
        r"(\S+)\(\) argument must be a string.* or a number, not (\S+)": r"\1()'nın parametresi yazı veya sayı olmalı, \2 değil",
        r"name (\S+) is not defined": r"isim \1 tanımlı değil",
        r"object of type (\S+) has no len\(\)": r"\1 tipindeki nesnenin uzunluk()'u yok",
        r"invalid syntax": r"geçersiz söz dizimi",
        r"can only concatenate (\S+) \(not (\S+)\) to (\S+)": r"sadece \1 ile \3 birleştirilebilir (\2 değil)",
        r"unsupported operand type\(s\) for (\S+).*: (\S+) and (\S+)": r"\1 işlemi için desteklenmeyen tip(ler): \2 ve \3",
        # r"unsupported operand type\(s\) for \*\* or pow\(\): (\S+) and (\S+)": r"** işlemi için desteklenmeyen tip(ler): \1 ve \2",
        r"(\S+) not supported between instances of (\S+) and (\S+)": r"\2 ve \3 tipindeki nesneler arasında \1 işlemi desteklenmiyor",
        r"unexpected indent": "beklenmedik girinti",
        r"expected an indented block": "girintilenmiş bir blok bekleniyordu",
        r"(\S+) index out of range": r"\1 indeksi aralık dışı",
        "EOL while scanning string literal": "yazı'yı okurken satır sonuna ulaşıldı",
        "EOF while scanning triple-quoted string literal": "üçlü tırnakla başlayan yazıyı okurken dosya sonuna ulaşıldı",
        "unexpected EOF while parsing": "beklenmedik dosya sonu",
        r"argument of type (\S+) is not iterable": r"\1 tipindeki nesne gezilebilir değil",  # couldn't find a better term
        r"(\S+) object is not iterable": r"\1 nesnesi gezilebilir değil",
        r"(\S+) object cannot be interpreted as an integer": r"\1 nesnesi tamsayı olarak yorumlanamıyor",
        "cannot assign to function call": "fonksiyon çağrısına atama yapılamaz",
        "division by zero": "sayı sıfıra bölünemez",
        r"\[Errno 2\] No such file or directory: ([\"'])([^\1]+)\1": r"\1\2\1 diye bir dosya ya da dizin yok",
        r"(\S+) object has no attribute (\S+)": r"\1 nesnesinin \2 diye bir niteliği yok",
        r"No module named (\S+)": r"\1 diye bir modül yok",
        "(\S+) takes (\d+) positional arguments? but (\d+) .* given": r"\1 \2 konumsal parametre alıyor ama \3 verildi",
        r"(\S+) got an unexpected keyword argument (\S+)": r"\1 beklenmedik bir anahtar kelime parametresi aldı: \2",
        r"local variable (\S+) referenced before assignment": r"yerel değişkene (\1) atama yapmadan önce atıfta bulunuldu",
        # r"too many values to unpack \(expected (\d+)\)":r"patlatmak için çok fazla değer",
    }

    try:
        value.msg = value.args[0]
    except IndexError:
        value.msg = ""
    # print("traceback".center(50, "*"))
    result = ["Hata geri izlemesi (son yapılan çağrı en sonda):\n"]
    tb = traceback.format_tb(tb)
    tb_slice = slice(1 if catch_indentation_errors else 0, len(tb))
    for line in tb[tb_slice]:
        line = simplify_error_location(line)
        result.append(line)
    # print(tb[-1], end="")
    # print("".join(traceback.format_tb(tb)),end="")
    # print("only exc".center(50, "*"))
    exc = traceback.format_exception_only(type_, value)
    exc[0] = simplify_error_location(exc[0])

    exc_name, colon, exc_exp = exc[-1].partition(":")
    exc[-1] = exc_name.split(".")[-1] + colon + exc_exp

    for err, exp in error_explanations.items():
        err_txt = exc[-1]
        # if actual_type is FileNotFoundError:
        #     print(err_txt)
        #     err_txt = f"[Errno {value.args[0]}] {value.args[1]}: 'dsad'"
        #     break
        if re.search(err, err_txt):
            err_txt = re.sub(err, exp, err_txt)
            err_txt = translate_types(err_txt)
            exc[-1] = err_txt
            break
    result.extend(exc)
    print("".join(result), file=sys.stderr)
    # print("traceback with exc".center(50, "*"))
    # print("".join(traceback.format_exception(type_, value, tb)))
    # print(trace + "\n" + exc)
    # print("".join(exc), file=sys.stderr)


oldhook = sys.excepthook
sys.excepthook = turkish_excepthook

yardım = help


class ekran:
    def __repr__(self):
        return "Ekran"


class yanlış:
    value = False

    def __repr__(self):
        return "Yanlış"


class doğru:
    value = True

    def __repr__(self):
        return "Doğru"


Ekran = ekran()
Doğru = doğru()
Yanlış = yanlış()


def göster():
    """
    Kullanılabilecek şeyleri gösterir.
    """
    print(
        *[
            "değeral",
            "yazdır",
            "uzunluk",
            "tip",
            "tamsayı",
            "noktalısayı",
            "yazı",
            "Ekran",
        ],
        sep="\n",
    )


def değeral(yazı=""):
    """
    Kullanıcıdan bir değer girmesini bekler ve girilen değeri yazı olarak döndürür.
    """
    return input(yazı)


def yazdır(*değer, ayır=" ", son="\n", dosya=Ekran):
    """
    Verilen değerleri dosyaya yazdırır. Eğer dosya belirtilmemişse, bu varsayılan olarak Ekran'dır.
    İsteğe bağlı parametreler:
    ayır:  değerlerin arasına yerleştirilecek yazı
    son:   en son değerden sonra yerleştirilecek yazı
    dosya: dosya-türevi bir nesne, varsayılan olarak Ekran'dır.
    """
    if dosya is Ekran:
        dosya = sys.stdout
    return print(*değer, sep=ayır, end=son, file=dosya)


def uzunluk(nesne):
    """
    Verilen nesne'nin uzunluğunu döndürür.
    """
    return len(nesne)


def tip(nesne):
    """
    Verilen nesne'nin tipini söyler.
    """
    x = str(type(nesne))
    x = x.replace("class", "sınıf")
    x = translate_types(x)
    print(x)
    """
    Actually type returns a 'type' but it is impossible to do in our case
    because we actually don't have types.
    """


def yazı(nesne):
    """
    Verilen nesne'nin yazı'ya çevrilmiş halini döndürür.
    """
    return str(nesne)


def tamsayı(x=0):
    """
    Verilen bir sayı ya da yazı'yı tamsayı'ya çevirir. Eğer hiçbir parametre verilmezse 0 döndürür.
    Eğer x bir noktalısayı ise noktadan sonraki kısmını siler.
    """
    return int(x)


def noktalısayı(x=0):
    """
    Verilen sayı ya da yazı'yı eğer mümkünse noktalısayı'ya çevirir.
    """
    return float(x)


def liste(gezilebilir=()):
    """
    gezilebilir'in elemanlarından oluşan bir liste döndürür.
    """
    return list(gezilebilir)


def demet(gezilebilir):
    return tuple(gezilebilir)


def sözlük(gezilebilir=()):
    """
    gezilebilir'in elemanlarından oluşan bir sözlük döndürür
    """
    return dict(gezilebilir)


def numaralandır(gezilebilir, başlangıç=0):
    """
    numaralandır fonksiyonu varsayılan olarak 0 olan başlangıç değerinden
    başlayarak bir sayı ve gezilebilir'in ilgili indeksteki değerinden oluşan
    ikilileri verir.
    """
    return enumerate(gezilebilir, başlangıç)
