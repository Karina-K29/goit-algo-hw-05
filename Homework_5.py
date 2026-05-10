import timeit

# Підгружаємо файли
with open("стаття 1.txt", encoding="utf-8") as f:
    text1 = f.read()

with open("стаття 2.txt", encoding="utf-8") as f:
    text2 = f.read()


# Алгоритм Боєра-Мура
def build_shift_table(pattern):
    table = {}
    length = len(pattern)

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1

    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)

    # Ініціалізуємо початковий індекс для основного тексту
    i = 0

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i

        # Зсуваємо індекс i на основі таблиці зсувів
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1


# Алгоритм Кнута-Морріса-Пратта
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


# Алгоритм Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0

    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus

    return hash_value


def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)

    # Базове число для хешування та модуль
    base = 256
    modulus = 101

    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus

    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus

            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


# Який підрядок шукаємо
existing_substring = "структури даних"
fake_substring = "суперквантовий_аналізатор"


# Тестуємо алгоритм
def test_algorithm(algorithm, text, pattern):
    return timeit.timeit(
        lambda: algorithm(text, pattern),
        number=100
    )


algorithms = {
    "Боєра-Мура": boyer_moore_search,
    "Кнута-Морріса-Пратта": kmp_search,
    "Рабіна-Карпа": rabin_karp_search
}

texts = {
    "Стаття 1": text1,
    "Стаття 2": text2
}


for text_name, text in texts.items():
    print(f"\n<<<<<<<<< {text_name} >>>>>>>>>")

    for pattern in [existing_substring, fake_substring]:
        print(f"\nПідрядок: '{pattern}'")

        for alg_name, alg_func in algorithms.items():
            time_taken = test_algorithm(alg_func, text, pattern)

            print(f"{alg_name}: {time_taken:.6f} секунд")