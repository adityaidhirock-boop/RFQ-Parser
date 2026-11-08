import re

def parse_rfq(text: str) -> dict:
    text_lower = text.lower()
    
    category = "woven_sack"
    if any(k in text_lower for k in ["bopp", "bop"]):
        category = "bopp_bag"
    elif any(k in text_lower for k in ["fibc", "jumbo", "bulk"]):
        category = "fibc"
    elif any(k in text_lower for k in ["carton", "mono"]):
        category = "mono_carton"
    elif any(k in text_lower for k in ["box", "corrugated"]):
        category = "corrugated_box"
    elif any(k in text_lower for k in ["shrink", "stretch", "film", "ldpe", "sheet"]):
        category = "film"
    elif any(k in text_lower for k in ["pouch"]):
        category = "pouch"
    elif any(k in text_lower for k in ["woven", "sack", "cement", "ad star", "bag"]):
        category = "woven_sack"

    quantity = None
    cleaned_text = re.sub(r'(\d),(\d)', r'\1\2', text)
    match_lac = re.search(r'([\d.]+)\s*(?:lac|lakh)', cleaned_text, re.IGNORECASE)
    match_hazaar = re.search(r'([\d.]+)\s*(?:hazaar|thousand|k)', cleaned_text, re.IGNORECASE)

    if match_lac:
        quantity = float(match_lac.group(1)) * 100000
    elif match_hazaar:
        quantity = float(match_hazaar.group(1)) * 1000
    else:
        nums = re.findall(r'\b(\d+)\b', cleaned_text)
        for n in nums:
            val = int(n)
            if val not in [50, 60, 70, 75, 80, 90, 100, 120, 150, 200, 250]:
                quantity = val
                break
        if quantity is None and nums:
            quantity = int(nums[0])

    if quantity is not None and isinstance(quantity, float) and quantity.is_integer():
        quantity = int(quantity)

    unit = None
    if re.search(r'\b(kg|kilogram)\b', text_lower):
        unit = "kg"
    elif re.search(r'\b(mt|ton|tonnes|tonne)\b', text_lower):
        unit = "mt"
    elif re.search(r'\b(pcs|pieces|bags)\b', text_lower) or quantity is not None:
        unit = "pcs"

    gsm = None
    gsm_match = re.search(r'(\d+)\s*gsm', text_lower)
    if gsm_match:
        gsm = int(gsm_match.group(1))

    micron = None
    mic_match = re.search(r'(\d+)\s*(?:mic|micron|microns)', text_lower)
    if mic_match:
        micron = int(mic_match.group(1))

    location = None
    cities = ["nashik", "patna", "lucknow", "ludhiana", "raipur", "mumbai", "jaipur", "delhi", "surat", "gwalior", "pune", "indore", "bhopal", "nagpur", "vadodara", "chennai"]
    for city in cities:
        if city in text_lower:
            location = city.capitalize()
            break

    return {
        "category": category,
        "quantity": quantity,
        "unit": unit,
        "gsm": gsm,
        "micron": micron,
        "location": location
    }
