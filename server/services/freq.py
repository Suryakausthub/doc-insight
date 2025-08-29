import re
from collections import Counter

STOP = set("""a an the and or but if in on at for to of from by with is are was were be been being this that these those it its as not no""".split())

def top5_words(text: str):
    words = re.findall(r"[a-zA-Z']+", text.lower())
    words = [w for w in words if w not in STOP and len(w) > 1]
    return Counter(words).most_common(5)
