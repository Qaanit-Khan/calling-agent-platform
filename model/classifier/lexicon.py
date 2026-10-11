import re
from typing import List, Dict, Pattern

class IntentLexicon:
    """
    Multilingual intent vocabulary & regex patterns covering:
    - English
    - Hindi (Devanagari & Romanized/Hinglish)
    - Marathi (Devanagari & Romanized/Marathish)
    - Code-switching and typical ASR phonetic variations
    """

    # -------------------------------------------------------------
    # Priority 1: Hard Opt-Out / Do-Not-Contact (Hard Negative)
    # -------------------------------------------------------------
    OPT_OUT_PATTERNS: List[Pattern] = [
        re.compile(p, re.IGNORECASE) for p in [
            r"\b(?:don'?t|do\s+not|never)\s+(?:call|contact|reach|message|disturb)\s+(?:me|us)?\s*(?:again|anymore|ever)?\b",
            r"\b(?:stop|quit)\s+(?:calling|contacting|messaging|disturbing|bothering)\b",
            r"\b(?:remove|delete|erase)\s+(?:my|this)?\s*(?:number|contact|data|details)\b",
            r"\b(?:put\s+me\s+on\s+(?:the\s+)?(?:do\s+not\s+call|dnc))\b",
            r"\b(?:block\s+(?:my|this)?\s*number)\b",
            r"\bi\s+don'?t\s+want\s+(?:any\s+more|further)\s+calls\b",
            # Hindi / Hinglish
            r"\b(?:call|phone)\s+(?:mat\s+(?:karna|karo|kijiye|kariyega)|nahi\s+karna)\b",
            r"\b(?:dobara|phir\s*se|bar\s*bar|aage\s*se)\s+(?:call|phone)\s+mat\b",
            r"\b(?:number\s+(?:hata|delete|nikal|remove)\s+(?:do|karo|kijiye|kardo))\b",
            r"\b(?:disturb|pareshan|tang)\s+mat\s+karo\b",
            r"\b(?:bar\s*bar\s+phone\s+mat\s+karo)\b",
            # Marathi
            r"\b(?:punha|parat|aata)\s+(?:phone|call)\s+(?:karu\s+naka|nako\s+karu|karu\s+nakos)\b",
            r"\b(?:phone|call)\s+nako\s+karu\b",
            r"\b(?:number\s+(?:kadhun\s+taka|delete\s+kara))\b",
            r"\b(?:tras|pareshan)\s+deu\s+naka\b",
            # Devanagari
            r"(?:कॉल|फोन)\s+करू\s+नका",
            r"(?:कॉल|फोन)\s+नको\s+करू",
            r"(?:कॉल|फोन)\s+मत\s+(?:करो|करना|कीजिए)",
            r"दोबारा\s+(?:कॉल|फोन)\s+मत",
            r"नंबर\s+(?:हटा|डिलीट)\s+कर",
        ]
    ]

    # -------------------------------------------------------------
    # Priority 1.5: Wrong Person / Irrelevant Customer (Hard Negative)
    # -------------------------------------------------------------
    WRONG_PERSON_PATTERNS: List[Pattern] = [
        re.compile(p, re.IGNORECASE) for p in [
            r"\bwrong\s+number\b",
            r"\byou\s+have\s+(?:the\s+)?wrong\s+(?:person|number|contact)\b",
            r"\bi'?m\s+not\s+the\s+person\s+you'?re\s+looking\s+for\b",
            r"\bi\s+don'?t\s+(?:use|have|need)\s+this\s+type\s+of\s+service\b",
            r"\bi\s+(?:am\s+not|m\s+not)\s+involved\s+in\s+this\b",
            r"\bi\s+don'?t\s+have\s+this\s+requirement\b",
            r"\bnot\s+for\s+me\b",
            # Hindi / Hinglish
            r"\b(?:galat|wrong)\s+number\b",
            r"\bkisi\s+aur\s+ka\s+number\b",
            r"\bmain\s+(?:vo|woh|ye)\s+nahi\s+hoon\b",
            r"\bmera\s+(?:isse|ye)\s+koi\s+lena\s*dena\s+nahi\b",
            r"\bmain\s+use\s+nahi\s+karta\b",
            # Marathi
            r"\bchuki\s*cha\s+number\b",
            r"\bmajha\s+he\s+kaam\s+nahi\b",
            r"\bchukun\s+lagla\b",
            # Devanagari
            r"गलत\s+नंबर",
            r"चुकीचा\s+नंबर",
        ]
    ]

    # -------------------------------------------------------------
    # Priority 2: Explicit Final Rejection (Negative Signal)
    # -------------------------------------------------------------
    REJECTION_PATTERNS: List[Pattern] = [
        re.compile(p, re.IGNORECASE) for p in [
            r"\b(?:i\s+am\s+not|i'?m\s+not|not)\s+interested\b",
            r"\b(?:i\s+don'?t|do\s+not)\s+(?:need|want)\s+(?:it|this|your\s+service|the\s+service|anything)\b",
            r"\b(?:i\s+don'?t|do\s+not)\s+want\s+to\s+buy\b",
            r"\b(?:no|nope)\s+thanks\b",
            r"\bno\s+thank\s+you\b",
            r"\bi\s+already\s+have\s+(?:everything|another|all|one)\b",
            r"\bi\s+don'?t\s+want\s+to\s+change\s+providers?\b",
            r"\bnot\s+useful\s+for\s+me\b",
            r"\bnot\s+looking\s+for\s+this\b",
            r"\bdefinitely\s+not\b",
            r"\bnever\s+interested\b",
            r"\bkeep\s+your\s+service\b",
            r"\b(?:ok\s*,?\s*)?bye(?:\s+bye)?\b",
            r"\bleave\s+it\b",
            r"\bdrop\s+it\b",
            r"\bdon'?t\s+(?:give|send|call|bother)\b",
            r"\bno\s+need\b",
            # Hindi / Hinglish
            r"\b(?:nahi|na|nahin)\s*(?:,\s*|\s+)(?:mujhe\s+)?(?:iski|ye|yeh|is)\s+(?:zarurat|jarurat|jaroorat)\s+nahi\s+hai\b",
            r"\b(?:zarurat|jarurat|jaroorat)\s+nahi\s+hai\b",
            r"\b(?:nahi|na|nahin)\s+chahiye\b",
            r"\bchahiye\s+nahi\b",
            r"\binterest\s+nahi\s+hai\b",
            r"\bkoi\s+(?:interest|shauk|zarurat)\s+nahi\s+hai\b",
            r"\bbilkul\s+(?:bhi\s+)?nahi\b",
            r"\bnahi\s+lena\s+hai\b",
            r"\bnahi\s+lena\b",
            r"\bnahi\s+karna\s+hai\b",
            r"\bmera\s+koi\s+mood\s+nahi\s+hai\b",
            r"\bkaam\s+ka\s+nahi\s+hai\b",
            r"\b(?:kuch\s+)?mat\s+(?:de|do|bhejo|batao|karo|dijiye)\b",
            r"\bicon\s+mat\s+de\b",
            r"\bmat\s+de\b",
            r"\bmat\s+do\b",
            r"\brehne\s+do\b",
            r"\brahne\s+do\b",
            r"\bchhoro\b",
            r"\bchhod\s+do\b",
            r"\bphone\s+(?:rakh|rakho|kaat|kaato|band\s+karo)\b",
            r"\bkaat\s+do\b",
            r"\bbakwas\b",
            r"\bfaltu\b",
            r"\btime\s+waste\b",
            # Marathi
            r"\b(?:mala\s+)?nako\s+(?:ahe|ye)?\b",
            r"\bnako\s+re\s+baba\b",
            r"\bnakoy\b",
            r"\bnakos\b",
            r"\bgaraj\s+nahi\b",
            r"\bkahi\s+garaj\s+nahi\b",
            r"\binterest\s+nahi\s+mala\b",
            r"\bmala\s+interest\s+nahi\b",
            r"\bkahi\s+upayog\s+nahi\b",
            r"\bphone\s+theva\b",
            r"\bdeu\s+naka\b",
            r"\bpathvu\s+naka\b",
            r"\bvel\s+nahi\b",
            # Devanagari (Hindi & Marathi)
            r"गरज\s+नाही",
            r"नको\s+आहे",
            r"नकोय",
            r"नको",
            r"मला\s+नको",
            r"देऊ\s+नका",
            r"पाठवू\s+नका",
            r"फोन\s+ठेवा",
            r"जरुरत\s+नहीं",
            r"ज़रूरत\s+नहीं",
            r"नहीं\s+चाहिए",
            r"नहीं\s+जानना",
            r"नहीं\s+जाननी",
            r"नहीं\s+सुनना",
            r"मुझे\s+(?:नहीं\s+जानना|नहीं\s+चाहिए|कुछ\s+नहीं\s+चाहिए)",
            r"नाही\s+पाहिजे",
            r"नाही\s+नको",
            r"इन्टरेस्ट\s+नाही",
            r"मत\s+दे",
            r"मत\s+दो",
            r"मत\s+भेजो",
            r"मत\s+बताओ",
            r"रहने\s+दो",
            r"छोड़ो",
            r"काटो",
            r"फोन\s+रखो",
            r"बंद\s+करो",
            r"बस",
            r"कुछ\s+नहीं\s+चाहिए",
            r"नहीं\s+लेना",
            r"नहीं\s+करना",
            r"बाय",
            r"टाटा",
            # Common ASR phonetic variations for negative refusals
            r"(?:झाइ|झाही|रही\s+जनना|लगी\s+चाहिये|नहीं\s+जनना)",
            r"\b(?:nahi|na|nahin)\s+(?:janna|chahiye|lena|sunna|batao)\b",
            r"\b(?:mujhe\s+)?(?:nahi\s+janna|nahi\s+chahiye)\b",
            r"^(?:nahi|nahin|na|no|nope|नाही|ना|नहीं|नको)[\s\.,!]*$",
        ]
    ]

    # -------------------------------------------------------------
    # Priority 3: Strong Positive Intent (Positive Signal)
    # -------------------------------------------------------------
    STRONG_INTEREST_PATTERNS: List[Pattern] = [
        re.compile(p, re.IGNORECASE) for p in [
            r"\b(?:yes|yeah|yep|yup|haan|ha|ho|sure)\s*,?\s*(?:i\s+am|i'?m)?\s*interested\b",
            r"\bi\s+(?:am|m)\s+interested\b",
            r"\btell\s+me\s+more\b",
            r"\bcan\s+you\s+(?:explain|tell|send|clarify|elaborate)\b",
            r"\b(?:send|share|give)\s+(?:me\s+)?(?:the\s+)?(?:details|info|information|brochure|catalogue|pdf|document)\b",
            r"\b(?:send|whatsapp|share)\s+(?:it\s+)?(?:on|to|via)\s+(?:whatsapp|whats\s*app|mail|email|message|sms)\b",
            r"\b(?:whatsapp|whats\s*app|watsp|watsap|wapp)\s+pe\s+(?:bhej|send|share|dalo)\b",
            r"\b(?:watsp|watsap|wapp|whatsapp)\s+pe\s+(?:detils|details|jankari)\b",
            r"\b(?:detils|details)\s+(?:bhej|bhejo|send|share)\b",
            r"\bcan\s+you\s+call\s+me\s+(?:later|tomorrow|next\s+week|in\s+the\s+evening)\b",
            r"\bcall\s+me\s+(?:later|tomorrow|next\s+week|tonight|evening|morning)\b",
            r"\bi\s+want\s+to\s+(?:try|buy|purchase|test|enroll|register|join|take)\s+it\b",
            r"\bhow\s+can\s+i\s+(?:register|get\s+started|sign\s+up|join|buy|order|apply)\b",
            r"\bwhere\s+can\s+i\s+buy\b",
            r"\bcan\s+i\s+get\s+a\s+demo\b",
            r"\bcan\s+someone\s+(?:contact|call|visit|meet)\s+me\b",
            r"\bi\s+might\s+be\s+interested\b",
            r"\bwhat\s+happens\s+if\s+i\s+sign\s+up\b",
            # Hindi / Hinglish
            r"\b(?:haan|ha|haa|haji)\s*,?\s*(?:batao|bataiye|explain\s+karo|boliye|sunte\s+hain|sunao)\b",
            r"\b(?:sun\s+raha\s+hu|sun\s+rahe\s+hain)\s*,?\s*(?:batao|bataiye|boliye)\b",
            r"\b(?:details|detils|jankari|jaankari|mahiti)\s+(?:bhejo|bhej\s+do|bhej\s+sakte\s+ho|send\s+karo|share\s+karo|chahiye|do)\b",
            r"\b(?:jankari|jaankari|details|detils)\s+chahiye\b",
            r"\bwhatsapp\s+pe\s+details\b",
            r"\bmujhe\s+(?:chahiye|try\s+karna\s+hai|janana\s+hai|samajhna\s+hai|seekhna\s+hai|sikhna\s+hai)\b",
            r"\b(?:seekhna|sikhna|learn\s+karna)\s+(?:hai|chahta|chahti)\b",
            r"\b(?:course|training|classes?|coaching)\s+(?:chahiye|karna\s+hai|join\s+karna)\b",
            r"\bmain\s+(?:try|le|dekh|seekh)\s+(?:sakta|chahta)\s+hoon\b",
            r"\bkaise\s+(?:milega|le\s+sakte|register\s+karein|shuru\s+karein|join\s+karein)\b",
            r"\baap\s+kya\s+provide\s+karte\s+hain\b",
            r"\bdemo\s+(?:milega|dikha|do)\b",
            # Marathi
            r"\b(?:ho|haan|ha)\s*,?\s*(?:sanga|sang\s+na|mahiti\s+dya|samjun\s+sanga)\b",
            r"\b(?:mahiti|details)\s+(?:pathva|dya|whatsapp\s+var\s+pathva|pahije)\b",
            r"\bwhatsapp\s+var\s+pathva\b",
            r"\bkasa\s+milnar\b",
            r"\bkasa\s+suru\s+karaycha\b",
            r"\bghyayla\s+aavdel\b",
            r"\btry\s+karaycha\s+ahe\b",
            r"\bshikaycha\s+ahe\b",
            # Devanagari
            r"हाँ\s*,?\s*(?:बताओ|बताइए|समझाइए)",
            r"व्हाट्सएप\s+(?:पर|पे)\s+(?:भेज|भेजो|डालो)",
            r"माहिती\s+(?:पाठवा|द्या|पाहिजे)",
            r"हो\s*,?\s*(?:सांगा|माहिती\s+द्या)",
            r"डेमो\s+(?:दाखवा|मिळेल|दीजिए)",
            r"व्हाट्सअॅपवर\s+पाठवा",
            r"(?:जानकारी|सूचना|डिटेल्स)\s+(?:चाहिए|दीजिए|दे\s+दो|बताइए|लेना\s+है)",
            r"(?:सीखना|सिखना|सिखाओ)\s+(?:है|चाहता|चाहती|चाहिए)",
            r"मदद\s+(?:चाहिए|कर\s+सकते|करो)",
            r"एडमिशन\s+(?:लेना|चाहिए)",
            r"रजिस्टर\s+(?:करना|होना)",
        ]
    ]

    # -------------------------------------------------------------
    # Priority 4: Questions, Inquiries, Pricing, Mechanism (Positive Signal)
    # -------------------------------------------------------------
    QUESTION_INQUIRY_PATTERNS: List[Pattern] = [
        re.compile(p, re.IGNORECASE) for p in [
            # Pricing / Cost
            r"\bhow\s+much\s+(?:does\s+it\s+cost|is\s+it|do\s+you\s+charge|will\s+it\s+be)\b",
            r"\bwhat\s+is\s+the\s+(?:price|cost|fee|charge|rate|subscription)\b",
            r"\bwhat\s+plans?\s+do\s+you\s+have\b",
            r"\bwhat\s+are\s+the\s+charges\b",
            r"\bany\s+discount\b",
            r"\bfree\s+trial\b",
            # How it works / Process
            r"\bhow\s+does\s+it\s+work\b",
            r"\bwhat\s+are\s+the\s+benefits\b",
            r"\bhow\s+long\s+does\s+it\s+take\b",
            r"\bcan\s+i\s+try\s+it\s+(?:first|free)?\b",
            r"\bwhat\s+exactly\s+do\s+you\s+provide\b",
            r"\bhow\s+will\s+this\s+help\s+me\b",
            # Hindi / Hinglish
            r"\b(?:iska|inka|service\s+ka)?\s*(?:price|rate|cost|kharcha|charges|paisa|fees?)\s*(?:kya|kitna)\s+hai\b",
            r"\bkitne\s+(?:ka|ki|ke|rupaiye|paise)\s+hai\b",
            r"\bkitna\s+(?:kharcha|cost|paisa|charge|padega|lagega)\b",
            r"\bpehle\s+price\s+batao\b",
            r"\bprice\s+batao\b",
            r"\bkya\s+price\s+hai\b",
            r"\bkaise\s+(?:work|kaam)\s+karta\s+hai\b",
            r"\bkya\s+(?:benefit|fayda|fayada)\s+hoga\b",
            r"\bkitna\s+time\s+lagega\b",
            r"\bwoh\s+plan\s+kitne\s+ka\s+hai\b",
            r"\bkya\s+plans?\s+hain\b",
            r"\bfree\s+trial\s+hai\s+kya\b",
            r"\bpehle\s+dekh\s+sakte\s+hain\s+kya\b",
            r"\bkaise\s+chalta\s+hai\b",
            r"\b(?:kahan|kidhar)\s+se\s+(?:seekhun|sikhun|shuru\s+karun|milega)\b",
            r"\bkaise\s+(?:karun|hoga|join\s+karein|start\s+karein)\b",
            r"\b(?:question|sawaal|sawal|doubt)\s+(?:hai|puchna|poochna)\b",
            r"\bbaare\s+mein\s+(?:batao|bataiye|janana)\b",
            # Marathi
            r"\bkiti\s+(?:rupaye|paise|charges|padel|kharch\s+hoil|lagel)\b",
            r"\bkasa\s+chalto\b",
            r"\bkasa\s+work\s+karto\b",
            r"\bkay\s+(?:fayda|plans|offers?)\s+ahet?\b",
            r"\bto\s+plan\s+kiticha\s+ahe\b",
            r"\bkiti\s+divas\s+lagtil\b",
            r"\baadhi\s+try\s+karta\s+yeil\s+ka\b",
            r"\bkuthe\s+(?:shikaycha|milnar|samjel)\b",
            # Devanagari
            r"किंमत\s+किती\s+आहे",
            r"किती\s+पडेल",
            r"खर्च\s+किती",
            r"किस्का\s+प्राइस\s+क्या\s+है",
            r"कितने\s+का\s+है",
            r"कितना\s+(?:पड़ेगा|लगेगा)",
            r"कैसे\s+काम\s+करता\s+है",
            r"काय\s+फायदा\s+आहे",
            r"कहाँ\s+से\s+(?:सीखूँ|सिखू|मिलेगा|शुरू\s+करूँ)",
            r"कैसे\s+(?:होगा|करूँ|हो\s+जाऊँ|कर\s+सकते|होगा)",
            r"(?:सवाल|प्रश्न|questions?)\s+(?:है|पूछना|करना)",
            r"के\s+बारे\s+में\s+(?:बताओ|बताइए|जानना\s+है)",
        ]
    ]

    # -------------------------------------------------------------
    # Priority 5: Conditional / Future Interest (Positive Signal)
    # -------------------------------------------------------------
    CONDITIONAL_FUTURE_PATTERNS: List[Pattern] = [
        re.compile(p, re.IGNORECASE) for p in [
            r"\bif\s+the\s+price\s+is\s+(?:reasonable|low|cheap|good|okay|fine)\b",
            r"\blet\s+me\s+(?:check|ask|consult|think|discuss)\s+(?:with\s+my)?\b",
            r"\bi\s+(?:need\s+to|have\s+to|want\s+to)\s+think\s+about\s+it\b",
            r"\bmaybe\s+(?:i\s+can|next\s+month|later)\b",
            r"\bcall\s+me\s+(?:next\s+week|tomorrow|later|in\s+two\s+days)\b",
            r"\bcontact\s+me\s+(?:next\s+week|tomorrow|later)\b",
            r"\bi\s+am\s+busy\s+(?:right\s+now|currently|today),\s*(?:call|talk)\s+later\b",
            # Hindi / Hinglish
            r"\bsoch\s+ke\s+(?:batata|bataunga|bataungi|bolta)\b",
            r"\bthoda\s+time\s+(?:chahiye|do|dijiye)\b",
            r"\bkal\s+(?:call|phone)\s+(?:karo|karna|kijiye)\b",
            r"\bbaad\s+me\s+(?:call|phone|baat)\s+(?:karo|karna|karenge)\b",
            r"\bagle\s+hafte\s+(?:call|baat)\b",
            r"\bghar\s+(?:pe|par)\s+(?:puch|baat)\s+karke\b",
            r"\babhi\s+busy\s+hoon\s*,?\s*(?:baad\s+me|kal)\b",
            r"\babhi\s+sure\s+nahi\s+hoon\b",
            # Marathi
            r"\bvichar\s+karun\s+sangto\b",
            r"\budya\s+(?:phone|call)\s+kara\b",
            r"\bnantar\s+(?:phone|call|bolu)\s+kara\b",
            r"\bghari\s+vicharun\s+sangto\b",
            r"\baata\s+busy\s+ahe\s*,?\s*nantar\b",
            r"\bpudhchya\s+aathvadyat\b",
            # Devanagari
            r"सोच\s+के\s+बताता",
            r"सोचकर\s+बताऊंगा",
            r"बाद\s+में\s+कॉल\s+करना",
            r"कल\s+कॉल\s+करो",
            r"विचार\s+करून\s+सांगतो",
            r"उद्या\s+फोन\s+करा",
            r"नंतर\s+बोलू",
        ]
    ]

    # -------------------------------------------------------------
    # Priority 6: Skepticism / Resistance with Continued Engagement
    # -------------------------------------------------------------
    SKEPTICISM_PATTERNS: List[Pattern] = [
        re.compile(p, re.IGNORECASE) for p in [
            r"\bi'?m\s+not\s+sure\s+this\s+will\s+work\b",
            r"\bi\s+don'?t\s+completely\s+trust\b",
            r"\bi'?m\s+currently\s+using\s+another\s+(?:company|provider|service)\b",
            r"\bwhy\s+should\s+i\s+switch\b",
            r"\blooks?\s+(?:a\s+bit\s+)?expensive\b",
            r"\btoo\s+expensive\b",
            r"\bcostly\s+lag\s+raha\s+hai\b",
            # Hindi / Hinglish
            r"\bexpensive\s+lag\s+raha\s+hai\b",
            r"\bmehnga\s+(?:lag\s+raha|hai)\b",
            r"\bthoda\s+expensive\b",
            r"\btrust\s+nahi\s+ho\s+raha\b",
            r"\bhar\s+koi\s+yehi\s+bolta\s+hai\b",
            r"\bpehle\s+se\s+dusra\s+use\s+kar\s+raha\s+hoon\b",
            # Marathi
            r"\bmahag\s+vatatay\b",
            r"\bmahag\s+ahe\b",
            r"\bkhara\s+vatat\s+nahi\b",
            # Devanagari
            r"महंगा\s+लग\s+रहा\s+है",
            r"महाग\s+आहे",
            r"विश्वास\s+नाही\s+बसत",
        ]
    ]

    # -------------------------------------------------------------
    # Neutral / Acoustic / Immediate Hangup (No Intent Evidence)
    # -------------------------------------------------------------
    EMPTY_OR_GREETING_PATTERNS: List[Pattern] = [
        re.compile(p, re.IGNORECASE) for p in [
            r"^(?:hello|hi|hey|haan|ha|ji|bolo|boliye|aawaz\s+nahi\s+aa\s+rahi|hello\s*\?)+$",
            r"^\[?call\s+(?:disconnected|ended|dropped)\]?$",
            r"^(?:hello\s*\?\s*)+$",
            r"^(?:kaun\s*\?\s*)+$",
        ]
    ]

    @classmethod
    def match_any(cls, text: str, patterns: List[Pattern]) -> bool:
        """Checks if text matches any regex in the pattern list."""
        for pattern in patterns:
            if pattern.search(text):
                return True
        return False

    @classmethod
    def extract_signals_from_text(cls, text: str) -> List[str]:
        """Identifies all positive, negative, and conditional signals in a text."""
        signals = []
        if cls.match_any(text, cls.OPT_OUT_PATTERNS):
            signals.append("OPT_OUT")
        if cls.match_any(text, cls.WRONG_PERSON_PATTERNS):
            signals.append("WRONG_PERSON")
        if cls.match_any(text, cls.REJECTION_PATTERNS):
            signals.append("REJECTION")
        if cls.match_any(text, cls.STRONG_INTEREST_PATTERNS):
            signals.append("STRONG_INTEREST")
        if cls.match_any(text, cls.QUESTION_INQUIRY_PATTERNS):
            signals.append("QUESTION_INQUIRY")
        if cls.match_any(text, cls.CONDITIONAL_FUTURE_PATTERNS):
            signals.append("CONDITIONAL_FUTURE")
        if cls.match_any(text, cls.SKEPTICISM_PATTERNS):
            signals.append("SKEPTICISM")
        return signals

    @classmethod
    def detect_languages(cls, text: str) -> List[str]:
        """Detects whether transcript contains English, Hindi, Marathi, or mixed code-switching."""
        languages = set()
        
        # Devanagari detection
        if re.search(r"[\u0900-\u097F]", text):
            # Differentiate Marathi-specific characters/words if possible
            marathi_dev_keywords = ["आहे", "नाही", "नको", "करा", "पाठवा", "सांगा", "होय", "पाहिजे"]
            if any(k in text for k in marathi_dev_keywords):
                languages.add("Marathi")
            else:
                languages.add("Hindi")

        # Romanized keywords
        hindi_keywords = [
            "kya", "kaise", "hai", "nahi", "chahiye", "batao", "bhejo", "soch", 
            "zarurat", "hum", "aap", "aur", "pehle", "batana", "tha", "achha", "iska"
        ]
        marathi_keywords = [
            "ahe", "nako", "nakoy", "nakos", "sang", "sanga", "kasa", "kiti", 
            "pathva", "mahiti", "padel", "vichar", "nantar", "mahag", "majha"
        ]
        english_keywords = [
            "interested", "service", "explain", "price", "cost", "details", 
            "whatsapp", "tomorrow", "register", "company", "call", "product"
        ]

        text_lower = text.lower()
        words = set(re.findall(r"\b[a-z]+\b", text_lower))

        if any(w in words for w in hindi_keywords):
            languages.add("Hindi/Hinglish")
        if any(w in words for w in marathi_keywords):
            languages.add("Marathi")
        if any(w in words for w in english_keywords):
            languages.add("English")

        if not languages:
            languages.add("English")
            
        return sorted(list(languages))
