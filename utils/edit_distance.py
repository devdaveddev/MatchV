from utils.phonetics import custom_substitution_cost

VOWELS = {"a", "e", "i", "o", "u", "aa", "ee", "oo"}

def is_vowel(token: str) -> bool:
    return token in VOWELS


# ---------------------------------------------------------
# 1) RAW DAMERAU-LEVENSHTEIN (Used mainly for surname)
# ---------------------------------------------------------
def raw_edit_distance(a: str, b: str) -> int:
    a = a.lower().strip()
    b = b.lower().strip()

    la, lb = len(a), len(b)
    dp = [[0] * (lb + 1) for _ in range(la + 1)]

    for i in range(la + 1):
        dp[i][0] = i
    for j in range(lb + 1):
        dp[0][j] = j

    for i in range(1, la + 1):
        for j in range(1, lb + 1):

            cost = 0 if a[i-1] == b[j-1] else 1

            dp[i][j] = min(
                dp[i-1][j] + 1,      # deletion
                dp[i][j-1] + 1,      # insertion
                dp[i-1][j-1] + cost  # substitution
            )

            # Damerau transposition
            if i > 1 and j > 1 and a[i-1] == b[j-2] and a[i-2] == b[j-1]:
                dp[i][j] = min(dp[i][j], dp[i-2][j-2] + 1)

    return dp[la][lb]


# ---------------------------------------------------------
# 2) SOFT PHONETIC EDIT DISTANCE (used for first name score)
# ---------------------------------------------------------
def soft_edit_distance(t1: list[str], t2: list[str], subst_cost_fn=custom_substitution_cost) -> float:
    n1, n2 = len(t1), len(t2)
    dp = [[0.0] * (n2 + 1) for _ in range(n1 + 1)]

    # Initialization: cost of deleting prefix
    for i in range(1, n1 + 1):
        dp[i][0] = dp[i-1][0] + (0.8 if is_vowel(t1[i-1]) else 0.5)

    # Initialization: cost of inserting prefix
    for j in range(1, n2 + 1):
        dp[0][j] = dp[0][j-1] + (0.8 if is_vowel(t2[j-1]) else 0.5)

    # DP computation
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):

            delete_cost = 0.8 if is_vowel(t1[i-1]) else 0.5
            insert_cost = 0.8 if is_vowel(t2[j-1]) else 0.5
            subst_cost = subst_cost_fn(t1[i-1], t2[j-1])

            dp[i][j] = min(
                dp[i-1][j] + delete_cost,    # delete
                dp[i][j-1] + insert_cost,    # insert
                dp[i-1][j-1] + subst_cost    # substitute
            )

            # Damerau transposition
            if i > 1 and j > 1 and t1[i-1] == t2[j-2] and t1[i-2] == t2[j-1]:
                dp[i][j] = min(dp[i][j], dp[i-2][j-2] + subst_cost)

    distance = dp[n1][n2]
    max_len = max(n1, n2)
    similarity = 1 - (distance / max_len if max_len > 0 else 1)
    return max(0.0, min(1.0, similarity))
