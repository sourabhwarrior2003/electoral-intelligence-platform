from fuzzywuzzy import fuzz
from modules.muslim_castes import MUSLIM_CASTES

# Add known Hindi-script Muslim first names
HINDI_MUSLIM_NAMES = [
    "अब्दुल", "मोहम्मद", "फैज़", "रहमान", "शरीफ", "सलीम", "रफीक", "रहमत", "अल्ताफ", "साबिर", "मुनव्वर",
    "नसीम", "शकील", "फारूक", "इस्माईल", "हुसैन", "यूसुफ", "ज़ैद", "ज़हीर", "इमरान", "आरिफ", "अज़ीज़",
    "मुस्लिम", "नूर", "रुकैया", "आयशा", "फ़ातिमा", "ज़ोया", "ख़दीजा", "शहनाज़""खदीजा", "आयशा", "ज़ोया", "ज़हरा", "इनाया", "सफ़ा", "बुशरा", "अरवा", "हुदा", "अमीना", "यास्मिन",
"नईमा", "लुबना", "हिबा", "आफ़रीन", "फ़राह", "ज़ोहरा", "समीरा", "हना", "ईमान", "आयत", "महीरा",
"मेहर", "अलीना", "रानिया", "हफ़सा", "मुहम्मद", "इब्राहिम", "हसन", "उमर", "अब्दुल्लाह", "ज़ैद",
"अयान", "बिलाल", "रेहान", "हम्ज़ा", "सैफ़", "फ़रहान", "इदरीस", "मलिक", "जुनैद", "फ़हीम", "करीम",
"ज़ुबैर", "तारिक़", "रय्यान", "रयान", "अदील", "फ़ारिस", "माहिर", "हसन", "इस्माइल", "आयशा",
"फ़ातिमा", "ज़ैनब", "सना", "लैला", "हिना", "मरियम", "राबिया", "इकरा", "शाइस्ता", "अहमद", "अहमद",
"अली", "इमरान", "खालिद", "सलमान", "यूसुफ", "ज़ीशान", "आमिर", "फ़ैज़ान", "इरफ़ान", "नूर", "अमन",
"सामी", "ईसा", "इक़बाल", "अब्दुल", "मोहम्मद", "मुहम्मद", "ख़ान", "अकबर", "आमिर", "अरशद", "आसिफ़",
"अज़हर", "अज़ीज़", "फ़ैसल", "फ़रीद", "फ़िरोज़", "हबीब", "हैदर", "हकीम", "हामिद", "हारून", "हुसैन",
"हुसैन", "जाफ़र", "जावेद", "कबीर", "कमाल", "महमूद", "महमूद", "मंसूर", "मेहबूब", "मोहमद",
"मोहम्मद", "मोईन", "मुजतबा", "मुख़्तार", "मुर्तज़ा", "मुश्ताक़", "मुस्तफ़ा", "नदीम", "नजीब", "नसीर",
"नवाज़", "नज़ीर", "ओमर", "ओसामा", "ओस्मान", "क़ासिम", "रफ़ीक़", "रहीम", "रहमान", "रशीद", "रहमान",
"रियाज़", "सईद", "सलीम", "समीर", "शहीद", "शकीर", "शमशाद", "शारिक़", "शोएब", "सिकंदर",
"सुभान", "सुफ़ियान", "सुल्तान", "उबैद", "उमर", "उस्मान", "वहाब", "यासीन", "यूनुस", "ज़फ़र", "ज़ाहिद", "ज़ाकिर"
]

def infer_religion_from_name(name):
    if not name or not name.strip():
        return "Unknown"

    name = name.strip().lower()
    name = name.replace(".", "").replace(",", "")

    # Check if any known Muslim caste keyword is in the name
    for caste in MUSLIM_CASTES:
        if caste.lower() in name:
            return "Muslim"

    # Check Hindi Muslim name matches
    for hindi_name in HINDI_MUSLIM_NAMES:
        if hindi_name in name:
            return "Muslim"

    parts = name.split()
    if not parts:
        return "Unknown"

    first_name = parts[0]

    # English Roman Muslim name set (from your list)
    roman_muslim_first_names = set([
        "khadija", "aisha", "zoya", "zahra", "inaya", "safa", "bushra", "arwa", "huda", "amina", "yasmin",
        "naima", "lubna", "hiba", "afreen", "farah", "zohra", "samira", "hana", "iman", "ayat", "mahira",
        "meher", "aleena", "rania", "hafsa", "muhammad", "ibrahim", "hasan", "omar", "abdullah", "zaid",
        "ayaan", "bilal", "rehan", "hamza", "saif", "farhan", "idris", "malik", "junaid", "faheem", "kareem",
        "zubair", "tariq", "rayyan", "rayan", "adeel", "faris", "mahir", "hassan", "ismail", "ayesha",
        "fatima", "zainab", "sana", "laila", "hina", "mariam", "rabia", "iqra", "shaista", "ahmed", "ahmad",
        "ali", "imran", "khalid", "salman", "yusuf", "zeeshan", "aamir", "faizan", "irfan", "noor", "aman",
        "sami", "isa", "iqbal", "abdul", "mohammed", "mohammad", "khan", "akbar", "amir", "arshad", "asif",
        "azhar", "aziz", "faisal", "farid", "firoz", "habib", "haider", "hakim", "hamid", "haroon", "husain",
        "hussein", "jafar", "javed", "kabir", "kamal", "mahmood", "mahmud", "mansoor", "mehboob", "mohamad",
        "mohamed", "moin", "mujtaba", "mukhtar", "murtaza", "mushtaq", "mustafa", "nadeem", "najeeb", "nasir",
        "nawaz", "nazir", "omer", "osama", "osman", "qasim", "rafiq", "rahim", "rahman", "rashid", "rehman",
        "riaz", "saeed", "salim", "samir", "shahid", "shakir", "shamshad", "shariq", "shoaib", "sikandar",
        "subhan", "sufyan", "sultan", "ubaid", "umar", "usman", "wahab", "yasin", "younus", "zafar", "zahid", "zakir"
    ])

    if first_name in roman_muslim_first_names:
        return "Muslim"

    # Handle special Patel rule
    if "patel" in name and first_name in ["mohammed", "abdul"]:
        return "Muslim"

    # Fuzzy fallback matching
    for mname in roman_muslim_first_names:
        if fuzz.partial_ratio(first_name, mname) > 90:
            return "Muslim"

    return "Hindu"
