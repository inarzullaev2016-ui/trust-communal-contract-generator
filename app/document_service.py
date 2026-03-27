from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation
import re

from docx import Document

from app.paths import GENERATED_DIR


def normalize_amount(text: str) -> Decimal:
    normalized = text.replace(" ", "").replace(",", ".")
    return Decimal(normalized)


def _triad_to_words(number: int, female: bool = False) -> list[str]:
    ones_male = ["", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять"]
    ones_female = ["", "одна", "две", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять"]
    teens = ["десять", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать", "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать"]
    tens = ["", "", "двадцать", "тридцать", "сорок", "пятьдесят", "шестьдесят", "семьдесят", "восемьдесят", "девяносто"]
    hundreds = ["", "сто", "двести", "триста", "четыреста", "пятьсот", "шестьсот", "семьсот", "восемьсот", "девятьсот"]

    words: list[str] = [hundreds[number // 100]]
    rem = number % 100

    if 10 <= rem <= 19:
        words.append(teens[rem - 10])
    else:
        words.append(tens[rem // 10])
        ones = ones_female if female else ones_male
        words.append(ones[rem % 10])

    return [part for part in words if part]


def _morph(value: int, forms: tuple[str, str, str]) -> str:
    n = abs(value) % 100
    if 11 <= n <= 19:
        return forms[2]
    n = n % 10
    if n == 1:
        return forms[0]
    if 2 <= n <= 4:
        return forms[1]
    return forms[2]


def rub_amount_to_words(amount: Decimal) -> str:
    if amount < 0:
        return "минус " + rub_amount_to_words(abs(amount))

    rubles = int(amount)
    kopeks = int((amount - rubles) * 100)

    if rubles == 0:
        rub_words = ["ноль"]
    else:
        rub_words: list[str] = []
        billions = rubles // 1_000_000_000
        millions = (rubles // 1_000_000) % 1000
        thousands = (rubles // 1000) % 1000
        units = rubles % 1000

        if billions:
            rub_words.extend(_triad_to_words(billions))
            rub_words.append(_morph(billions, ("миллиард", "миллиарда", "миллиардов")))

        if millions:
            rub_words.extend(_triad_to_words(millions))
            rub_words.append(_morph(millions, ("миллион", "миллиона", "миллионов")))

        if thousands:
            rub_words.extend(_triad_to_words(thousands, female=True))
            rub_words.append(_morph(thousands, ("тысяча", "тысячи", "тысяч")))

        if units:
            rub_words.extend(_triad_to_words(units))

    rub_words.append(_morph(rubles, ("рубль", "рубля", "рублей")))
    return f"{' '.join(rub_words)} {kopeks:02d} копеек"


def safe_filename(name: str) -> str:
    cleaned = re.sub(r"[^\w\-]+", "_", name.strip(), flags=re.UNICODE)
    return cleaned.strip("_") or "contract"


def build_context(contract_data: dict[str, str], landlord_data: dict[str, str]) -> dict[str, str]:
    context = {**contract_data, **landlord_data}
    amount_text = contract_data.get("rent_amount", "0")

    try:
        amount = normalize_amount(amount_text)
        context["rent_amount_words"] = rub_amount_to_words(amount)
    except InvalidOperation:
        context["rent_amount_words"] = ""

    return context


def render_text_template(template_text: str, context: dict[str, str]) -> str:
    rendered = template_text
    for key, value in context.items():
        rendered = rendered.replace(f"{{{key}}}", str(value or ""))
    return rendered


def generate_docx(template_text: str, context: dict[str, str], contract_number: str) -> str:
    rendered = render_text_template(template_text, context)
    document = Document()

    for line in rendered.splitlines():
        document.add_paragraph(line)

    today = datetime.now().strftime("%Y%m%d")
    filename = f"{safe_filename(contract_number)}_{today}.docx"
    output_path = GENERATED_DIR / filename
    document.save(output_path)
    return str(output_path)
