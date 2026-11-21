#actual category values
DEFAULT_RULES = {
    "grab": "Transport", "comfortdelgro": "Transport", "simplygo": "Transport",
    "fairprice": "Groceries", "ntuc": "Groceries", "sheng siong": "Groceries",
    "mcdonald": "Food", "starbucks": "Food", "foodpanda": "Food", "deliveroo": "Food",
    "netflix": "Subscriptions", "spotify": "Subscriptions", "cinema": "Leisure",
    "guardian": "Shopping", "watsons": "Shopping", "clinic": "Health",
    "247 Fitness": "Fitness", "activesg": "Fitness",
    "agoda": "Travel", "scoot": "Travel", "airbnb": "Travel",
    "shopee": "Shopping", "lazada": "Shopping", "amazon": "Shopping",
    "starhub": "Subscriptions","AIA": "Insurance"
}

def categorise(description, rules):
    text = str(description).lower()
    for keyword in sorted(rules, key=len, reverse=True):
        if keyword in text:
            return rules[keyword]
    return "Other"

def keyword_from(description):
    words = [w for w in str(description).lower().split() if w.isalpha()]
    return " ".join(words[:2])