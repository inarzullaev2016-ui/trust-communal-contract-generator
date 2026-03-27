from __future__ import annotations


UNITS_MALE = [
    "ноль",
    "один",
    "два",
    "три",
    "четыре",
    "пять",
    "шесть",
    "семь",
    "восемь",
    "девять",
]
UNITS_FEMALE = UNITS_MALE.copy()
UNITS_FEMALE[1] = "одна"
UNITS_FEMALE[2] = "две"

TEENS = {
    10: "десять",
    11: "одиннадцать",
    12: "двенадцать",
    13: "тринадцать",
    14: "четырнадцать",
    15: "пятнадцать",
    16: "шестнадцать",
    17: "семнадцать",
    18: "восемнадцать",
    19: "девятнадцать",
}

TENS = {
    2: "двадцать",
    3: "тридцать",
    4: "сорок",
    5: "пятьдесят",
    6: "шестьдесят",
    7: "семьдесят",
    8: "восемьдесят",
    9: "девяносто",
}

HUNDREDS = {
    1: "сто",
    2: "двести",
    3: "триста",
    4: "четыреста",
    5: "пятьсот",
    6: "шестьсот",
    7: "семьсот",
    8: "восемьсот",
    9: "девятьсот",
}


def _plural_form(n: int, forms: tuple[str, str, str]) -> str:
    n = abs(n) % 100
    if 11 <= n <= 14:
        return forms[2]
    remainder = n % 10
    if remainder == 1:
        return forms[0]
    if 2 <= remainder <= 4:
        return forms[1]
    return forms[2]


def _triplet_to_words(number: int, female: bool = False) -> list[str]:
    words: list[str] = []
    if number == 0:
        return words

    h = number // 100
    if h:
        words.append(HUNDREDS[h])

    remainder = number % 100
    if 10 <= remainder <= 19:
        words.append(TEENS[remainder])
        return words

    t = remainder // 10
    if t:
        words.append(TENS[t])

    u = remainder % 10
    if u:
        units = UNITS_FEMALE if female else UNITS_MALE
        words.append(units[u])

    return words


def number_to_russian_words(number: int) -> str:
    if number == 0:
        return "ноль"

    if number < 0:
        return f"минус {number_to_russian_words(abs(number))}"

    words: list[str] = []
    millions = number // 1_000_000
    thousands = (number // 1_000) % 1_000
    remainder = number % 1_000

    if millions:
        words.extend(_triplet_to_words(millions))
        words.append(_plural_form(millions, ("миллион", "миллиона", "миллионов")))

    if thousands:
        words.extend(_triplet_to_words(thousands, female=True))
        words.append(_plural_form(thousands, ("тысяча", "тысячи", "тысяч")))

    if remainder:
        words.extend(_triplet_to_words(remainder))

    return " ".join(words)


def rubles_to_words(value: str) -> str:
    cleaned = value.replace(" ", "").replace(",", ".")
    amount = float(cleaned)
    rubles = int(amount)
    kopecks = int(round((amount - rubles) * 100))

    rub_word = _plural_form(rubles, ("рубль", "рубля", "рублей"))
    kop_word = _plural_form(kopecks, ("копейка", "копейки", "копеек"))

    return f"{number_to_russian_words(rubles)} {rub_word} {kopecks:02d} {kop_word}"
