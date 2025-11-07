def normalise_prefix(name: str) -> str: 

 name = name.lower().strip() 
 name = name.replace(" ", "")

 if name.endswith("h"):
        name = name[:-1] 

  
 vowels = "aeiou"
 results = [] 

 for char in name:
     if results:
        prev = results[:-1] 

        if char in vowels and prev[-1] in vowels:
            continue

        if char not in vowels and prev[-1] not in vowels:
            continue 

        results.append(char)

 return "".join(results) 

def tokenize_phonemes(name: str ) -> list[str]: 
    name = name.lower().strip().replace(" ", "")

    phonemes = ["sh", "ch", "th", "dh", "bh", "gh", "ph", "kh", "aa", "ee", "oo"]

    tokens = [] 
    i = 0
    n = len(name)

    while i < n:
        if i + 1 < n:
            two = name[i:i+2]
            if two in phonemes:
                tokens.append(two)
                i +=2
                continue 

        tokens.append(name[i]) 
        i += 1

    return tokens 

def custom_substitution_cost(a: str, b: str) -> float: 
    if a == b: 
        return 0.0 

    aspirated_pairs = {("t", "th"), ("th", "t"),
                       ("d", "dh"), ("dh", "d"),
                       ("b", "bh"), ("bh", "b"),
                       ("g", "gh"), ("gh", "g")}   
    if (a , b) in aspirated_pairs: 
        return 0.4  
    
    if (a == "j" and b == "z") or (a == "z" and b == "j"):
        return 0.4

    sibilants = {"s" , "sh" , "ch"}
    if a in sibilants and b in sibilants: 
        return 0.3
    
    vowel_variants = {("i", "ee"), ("ee", "i"),
                      ("u", "oo"), ("oo", "u"),
                      ("a", "aa"), ("aa", "a")} 
    
    if (a, b) in vowel_variants:
        return 0.6 
    
    return 1.0

          

 



