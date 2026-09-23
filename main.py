"""Практична №1. Варіант 4: N=37, F=0.2, A=70, B=10, C=100.25"""
import math
import struct

N, F, A, B, C = 37, 0.2, 70, 10, 100.25
DIGITS = "0123456789ABCDEF"


def int_to_base(n, base, verbose=False):
    """Ціле -> система з основою 2..16 діленням на основу."""
    if not 2 <= base <= 16:
        raise ValueError("основа має бути 2..16")
    if n == 0:
        return "0"
    res, x = "", n
    while x > 0:
        x, r = divmod(x, base)
        if verbose:
            print(f"   {x * base + r} : {base} = {x}, остача {r} ({DIGITS[r]})")
        res = DIGITS[r] + res
    return res


def frac_to_base(f, base, places=6, verbose=False):
    """Дріб -> система з основою 2..16 множенням на основу."""
    res, x = "", f
    for _ in range(places):
        x *= base
        d = int(x)
        if verbose:
            print(f"   {x:.6f} -> цифра {DIGITS[d]}")
        res += DIGITS[d]
        x -= d
    return "0." + res


def to_twos(n, bits=8):
    return format(n & (2 ** bits - 1), f"0{bits}b")


def add_twos(a, b, bits=8):
    """Додавання в додатковому коді з прапорцем переповнення."""
    mask = 2 ** bits - 1
    ua, ub = a & mask, b & mask
    total = (ua + ub) & mask
    sign = 1 << (bits - 1)
    # переповнення: однакові знаки доданків, а знак суми інший
    overflow = (ua & sign) == (ub & sign) and (total & sign) != (ua & sign)
    signed = total - (1 << bits) if total & sign else total
    return total, signed, overflow


def ieee754_parse(c):
    bits = format(struct.unpack(">I", struct.pack(">f", c))[0], "032b")
    s, e, m = bits[0], bits[1:9], bits[9:]
    exp = int(e, 2)
    value = (-1) ** int(s) * (1 + int(m, 2) / 2 ** 23) * 2 ** (exp - 127)
    return bits, s, e, m, exp, value


if __name__ == "__main__":
    print("=== Крок 1-2: системи числення ===")
    print(f"N = {N}: ділення на 2:")
    b2 = int_to_base(N, 2, True)
    print(f"N = {N}: ділення на 8:")
    b8 = int_to_base(N, 8, True)
    print(f"N = {N}: ділення на 16:")
    b16 = int_to_base(N, 16, True)
    print(f"{N} = {b2}(2) = {b8}(8) = {b16}(16)")
    print("перевірка:", bin(N)[2:], oct(N)[2:], hex(N)[2:].upper())
    print(f"\nF = {F}: множення на 2:")
    print("F =", frac_to_base(F, 2, 6, True), "(2)")

    print("\n=== Крок 3: додатковий код ===")
    total, signed, ovf = add_twos(A, B)
    print(f"A = {A:>4} = {to_twos(A)}")
    print(f"B = {B:>4} = {to_twos(B)}")
    print(f"A+B    = {format(total, '08b')} = {signed} (дес.)")
    print("Переповнення:", "ТАК" if ovf else "НІ")
    print("(обидва доданки додатні, сума додатна -> знак не змінився)")

    print("\n=== Крок 4: IEEE 754 single ===")
    bits, s, e, m, exp, val = ieee754_parse(C)
    print(f"C = {C}")
    print(f"знак = {s}, порядок = {e} ({exp}, p = {exp - 127}), мантиса = {m}")
    print(f"32 біти: {s} {e} {m}")
    print(f"HEX: {int(bits, 2):08X}")
    print(f"відновлене значення: {val}  (збіг з C: {val == C})")
    print("struct.pack('>f', C) =", struct.pack('>f', C).hex().upper())

    print("\n=== Крок 5: похибка дробів ===")
    s_ = 0.1 + 0.2
    print(f"0.1 + 0.2 = {s_!r}")
    print(f"0.1 + 0.2 == 0.3 -> {s_ == 0.3}")
    print(f"різниця: {s_ - 0.3:.3e}")
    print(f"math.isclose(0.1+0.2, 0.3) -> {math.isclose(s_, 0.3)}")
    print("Причина: 0.1, 0.2, 0.3 - нескінченні періодичні дроби у двійковій\n"
          "системі, тому зберігаються з округленням; суму порівнюють з допуском.")
