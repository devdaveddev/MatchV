from utils.phonetics import normalise_prefix, tokenize_phonemes, custom_substitution_cost

from utils.edit_distance import raw_edit_distance, soft_edit_distance


def split_name(full_name: str):
    parts = full_name.strip().lower().split()
    if len(parts) == 1:
        return parts[0], ""   
    return parts[0], parts[-1]  


def first_name_score(query_first: str, cand_first: str) -> float:
    
    if query_first == cand_first:
        return 1.0

    
    qn = normalise_prefix(query_first)
    cn = normalise_prefix(cand_first)

    score = 0.0

    
    if qn == cn:
        score += 0.35

    
    if qn and cn and qn in cn:
        score += 0.15

    
    q_tokens = tokenize_phonemes(query_first)
    c_tokens = tokenize_phonemes(cand_first)
    phonetic_sim = soft_edit_distance(q_tokens, c_tokens, custom_substitution_cost)
    score += 0.45 * phonetic_sim

    max_len = max(len(q_tokens), len(c_tokens))
    length_diff = abs(len(q_tokens) - len(c_tokens))
    score -= 0.1 * (length_diff / max_len)

    return max(0.0, min(1.0, score))


def surname_score(query_last: str, cand_last: str) -> float:
    
    if not query_last:
        return 0.0

    
    if query_last == cand_last:
        return 1.0

    dist = raw_edit_distance(query_last, cand_last)
    max_len = max(len(query_last), len(cand_last))
    sim = 1 - (dist / max_len)

    return max(0.0, min(1.0, sim))


def final_score(query: str, candidate: str) -> float:
    q_first, q_last = split_name(query)
    c_first, c_last = split_name(candidate)

    first_sim = first_name_score(q_first, c_first)
    last_sim  = surname_score(q_last, c_last)

    
    return 0.65 * first_sim + 0.35 * last_sim
 