from typing import List, Optional, Tuple, Dict, Any
from .models import (
    IntentClassification,
    StrictClassificationResponse,
    DetailedClassificationResponse,
    Turn,
    SpeakerRole,
)
from .parser import TranscriptParser
from .lexicon import IntentLexicon


class IntentClassifier:
    """
    Two-Class Customer Intent Classifier for AI-powered sales & support calls.
    Determines whether a customer shows enough intent/curiosity/engagement/willingness
    to be placed into the company's positive-lead list (INTERESTED vs NOT_INTERESTED).
    
    Implements:
    - Multilingual intent recognition (English, Hindi, Marathi, Hinglish, code-switching)
    - Industry-agnostic reasoning
    - High-recall lead preservation
    - Agent vs Customer statement separation
    - 7-tier priority hierarchy and temporal override tracking
    """

    def __init__(self):
        self.parser = TranscriptParser
        self.lexicon = IntentLexicon

    def classify_strict(self, transcript: str) -> Dict[str, str]:
        """
        Returns strictly the JSON required by Section 20 of specification:
        {
          "classification": "INTERESTED"
        }
        or
        {
          "classification": "NOT_INTERESTED"
        }
        """
        detailed = self.classify_detailed(transcript)
        return {"classification": detailed.classification.value}

    def classify(self, transcript: str, explain: bool = False) -> Dict[str, Any]:
        """Classifies transcript, returning strict JSON or detailed schema based on `explain`."""
        if not explain:
            return self.classify_strict(transcript)
        return self.classify_detailed(transcript).model_dump()

    def classify_detailed(self, transcript: str) -> DetailedClassificationResponse:
        """
        Evaluates the transcript through the 9-step decision algorithm
        and returns a complete diagnostic response.
        """
        raw_text = transcript.strip() if transcript else ""
        if not raw_text:
            return DetailedClassificationResponse(
                classification=IntentClassification.NOT_INTERESTED,
                confidence=1.0,
                reason="Empty transcript: No evidence of customer intent.",
                priority_level=2,
                rule_applied="Empty transcript fallback",
                languages_detected=[],
                customer_turns_count=0,
                total_turns_count=0,
                signals_detected=[],
                is_ambiguous_rescued=False,
                turns=[]
            )

        turns = self.parser.parse(raw_text)
        languages = self.lexicon.detect_languages(raw_text)

        customer_turns: List[Turn] = []
        all_detected_signals = set()

        for turn in turns:
            signals = self.lexicon.extract_signals_from_text(turn.text)
            turn.signals = signals
            if turn.role == SpeakerRole.CUSTOMER:
                customer_turns.append(turn)
                all_detected_signals.update(signals)

        # In case all lines were from unknown speakers, evaluate those turns
        if not customer_turns:
            for turn in turns:
                if turn.role != SpeakerRole.AGENT:
                    customer_turns.append(turn)
                    all_detected_signals.update(turn.signals)

        # -------------------------------------------------------------
        # STEP 1: Check for Empty / Non-Conversational Disconnects
        # (Example 8: Only "Hello?", "Hello?", [call disconnected])
        # -------------------------------------------------------------
        is_empty_or_greeting_only = True
        for ct in customer_turns:
            cleaned_text = ct.text.strip().lower()
            # Strip punctuation
            import re
            cleaned_text_simple = re.sub(r"[^\w\s]", "", cleaned_text).strip()
            # If customer said anything beyond greeting / disconnect markers
            if not self.lexicon.match_any(cleaned_text, self.lexicon.EMPTY_OR_GREETING_PATTERNS) and cleaned_text_simple not in ["hello", "hi", "hey", "haan", "ha", "boliye", "bolo", "kaun"]:
                is_empty_or_greeting_only = False
                break

        if is_empty_or_greeting_only and not any(s in all_detected_signals for s in ["STRONG_INTEREST", "QUESTION_INQUIRY", "CONDITIONAL_FUTURE", "SKEPTICISM"]):
            return DetailedClassificationResponse(
                classification=IntentClassification.NOT_INTERESTED,
                confidence=0.95,
                reason="Call disconnected or contained only greetings without any product discussion or customer interest signal.",
                priority_level=2,
                rule_applied="Section 12 & Example 8: No meaningful transcript and no evidence of interest",
                languages_detected=languages,
                customer_turns_count=len(customer_turns),
                total_turns_count=len(turns),
                signals_detected=list(all_detected_signals),
                is_ambiguous_rescued=False,
                turns=turns
            )

        # -------------------------------------------------------------
        # STEP 2: Check for Hard Opt-Out / Do-Not-Contact (Priority 1)
        # Even if customer showed interest earlier, an explicit opt-out MUST result in NOT_INTERESTED.
        # -------------------------------------------------------------
        for ct in customer_turns:
            if "OPT_OUT" in ct.signals:
                return DetailedClassificationResponse(
                    classification=IntentClassification.NOT_INTERESTED,
                    confidence=0.99,
                    reason=f"Customer explicitly requested do-not-contact: '{ct.text}'",
                    priority_level=1,
                    rule_applied="Priority 1: Explicit customer opt-out / DNC overrides all positive signals",
                    languages_detected=languages,
                    customer_turns_count=len(customer_turns),
                    total_turns_count=len(turns),
                    signals_detected=list(all_detected_signals),
                    is_ambiguous_rescued=False,
                    turns=turns
                )

        # -------------------------------------------------------------
        # STEP 3: Check for Wrong Person / Irrelevant Customer (Priority 1.5)
        # -------------------------------------------------------------
        for ct in customer_turns:
            if "WRONG_PERSON" in ct.signals:
                return DetailedClassificationResponse(
                    classification=IntentClassification.NOT_INTERESTED,
                    confidence=0.95,
                    reason=f"Customer indicated wrong person or completely irrelevant requirement: '{ct.text}'",
                    priority_level=1,
                    rule_applied="Section 11: Wrong Person / Irrelevant Customer",
                    languages_detected=languages,
                    customer_turns_count=len(customer_turns),
                    total_turns_count=len(turns),
                    signals_detected=list(all_detected_signals),
                    is_ambiguous_rescued=False,
                    turns=turns
                )

        # -------------------------------------------------------------
        # STEP 4: Temporal & Final Turn Analysis
        # Determine customer's latest meaningful position:
        # Does a later positive signal override an earlier rejection? (Section 8)
        # Or did customer reject at the end? (Section 9)
        # -------------------------------------------------------------
        latest_rejection_idx = -1
        latest_positive_idx = -1
        is_explicit_rejection_at_end = False

        positive_signal_types = {"STRONG_INTEREST", "QUESTION_INQUIRY", "CONDITIONAL_FUTURE", "SKEPTICISM"}
        hard_rejection_patterns = [
            re.compile(r"\b(?:not\s+interested|no\s+need|don'?t\s+want|nahi\s+chahiye|chahiye\s+nahi|nako|mat\s+(?:de|do|karo|bhejo)|galat\s+number|wrong\s+number|nahi\s+janna|nahi\s+lena|nahi|nahin|no|nope|na)\b", re.IGNORECASE),
            re.compile(r"(?:नहीं\s+चाहिए|नहीं\s+जानना|नहीं\s+लेना|नहीं\s+सुनना|ज़रूरत\s+नहीं|जरूरत\s+नहीं|नको|मत\s+दे|मत\s+दो|गलत\s+नंबर|नाही\s+पाहिजे|नाही|नहीं|ना|रहने\s+दो|बस|छोड़ो)"),
        ]

        for idx, ct in enumerate(customer_turns):
            if "REJECTION" in ct.signals:
                latest_rejection_idx = idx
            if any(sig in positive_signal_types for sig in ct.signals):
                latest_positive_idx = idx

        # If customer showed positive signal AFTER rejection (Section 8 Example 7)
        if latest_positive_idx > latest_rejection_idx and latest_positive_idx != -1:
            matching_turn = customer_turns[latest_positive_idx]
            return DetailedClassificationResponse(
                classification=IntentClassification.INTERESTED,
                confidence=0.92,
                reason=f"Customer demonstrated positive interest signal ('{matching_turn.text}') which overrides earlier hesitation.",
                priority_level=3,
                rule_applied="Section 8: Meaningful positive signal overrides earlier hesitation",
                languages_detected=languages,
                customer_turns_count=len(customer_turns),
                total_turns_count=len(turns),
                signals_detected=list(all_detected_signals),
                is_ambiguous_rescued=False,
                turns=turns
            )

        # If customer ended with a rejection
        if latest_rejection_idx != -1 and latest_rejection_idx >= latest_positive_idx:
            rejection_turn = customer_turns[latest_rejection_idx]
            
            # Section 16: If the turn contains an active inquiry alongside frustration/sentiment
            # ("faltu baat band karo pehle price batao"), the inquiry takes precedence -> INTERESTED
            if any(sig in positive_signal_types for sig in rejection_turn.signals):
                return DetailedClassificationResponse(
                    classification=IntentClassification.INTERESTED,
                    confidence=0.88,
                    reason=f"Customer expressed frustration alongside an active inquiry ('{rejection_turn.text}'). Intent overrides sentiment.",
                    priority_level=4,
                    rule_applied="Section 16: Active inquiry overrides angry or skeptical sentiment",
                    languages_detected=languages,
                    customer_turns_count=len(customer_turns),
                    total_turns_count=len(turns),
                    signals_detected=list(all_detected_signals),
                    is_ambiguous_rescued=False,
                    turns=turns
                )
            
            polite_signoff_pattern = re.compile(
                r"^\s*(?:(?:ok|theek\s+hai|chalo|accha)\s*,?\s*)?(?:bye|bye\s+bye|alvida|tata|टाटा|बाय|thank\s+you|dhanyawad|shukriya)[\s\.,!]*$",
                re.IGNORECASE
            )
            is_pure_signoff = bool(polite_signoff_pattern.match(rejection_turn.text.strip()))
            
            # If customer had a genuine positive inquiry earlier and only said a polite sign-off like 'bye' at the end:
            if latest_positive_idx != -1 and is_pure_signoff:
                matching_turn = customer_turns[latest_positive_idx]
                return DetailedClassificationResponse(
                    classification=IntentClassification.INTERESTED,
                    confidence=0.90,
                    reason=f"Customer engaged with positive inquiry ('{matching_turn.text}') before polite sign-off.",
                    priority_level=3,
                    rule_applied="Inquiry Preservation: Customer questions and discovery treated as INTERESTED despite polite call sign-off",
                    languages_detected=languages,
                    customer_turns_count=len(customer_turns),
                    total_turns_count=len(turns),
                    signals_detected=list(all_detected_signals),
                    is_ambiguous_rescued=False,
                    turns=turns
                )

            return DetailedClassificationResponse(
                classification=IntentClassification.NOT_INTERESTED,
                confidence=0.95,
                reason=f"Customer made clear final rejection: '{rejection_turn.text}'",
                priority_level=2,
                rule_applied="Priority 2 / Section 9: Explicit final rejection",
                languages_detected=languages,
                customer_turns_count=len(customer_turns),
                total_turns_count=len(turns),
                signals_detected=list(all_detected_signals),
                is_ambiguous_rescued=False,
                turns=turns
            )

        # -------------------------------------------------------------
        # STEP 5: Clear Positive Intent (Priority 3)
        # -------------------------------------------------------------
        if "STRONG_INTEREST" in all_detected_signals:
            return DetailedClassificationResponse(
                classification=IntentClassification.INTERESTED,
                confidence=0.95,
                reason="Customer showed clear positive buying or engagement signal (e.g. asking for WhatsApp/details, demo, registration).",
                priority_level=3,
                rule_applied="Priority 3: Clear positive intent",
                languages_detected=languages,
                customer_turns_count=len(customer_turns),
                total_turns_count=len(turns),
                signals_detected=list(all_detected_signals),
                is_ambiguous_rescued=False,
                turns=turns
            )

        # -------------------------------------------------------------
        # STEP 6: Questions / Inquiries / Pricing / How it works (Priority 4)
        # Multiple or single questions about service/price/benefits = strong evidence of interest.
        # -------------------------------------------------------------
        if "QUESTION_INQUIRY" in all_detected_signals:
            return DetailedClassificationResponse(
                classification=IntentClassification.INTERESTED,
                confidence=0.90,
                reason="Customer asked exploratory questions regarding pricing, features, duration, or service workings.",
                priority_level=4,
                rule_applied="Priority 4: Questions and exploration demonstrate customer intent",
                languages_detected=languages,
                customer_turns_count=len(customer_turns),
                total_turns_count=len(turns),
                signals_detected=list(all_detected_signals),
                is_ambiguous_rescued=False,
                turns=turns
            )

        # -------------------------------------------------------------
        # STEP 7: Conditional or Future Interest (Priority 5)
        # -------------------------------------------------------------
        if "CONDITIONAL_FUTURE" in all_detected_signals:
            return DetailedClassificationResponse(
                classification=IntentClassification.INTERESTED,
                confidence=0.88,
                reason="Customer expressed conditional willingness or requested future contact/thinking time.",
                priority_level=5,
                rule_applied="Priority 5: Conditional or future interest preserved as lead",
                languages_detected=languages,
                customer_turns_count=len(customer_turns),
                total_turns_count=len(turns),
                signals_detected=list(all_detected_signals),
                is_ambiguous_rescued=False,
                turns=turns
            )

        # -------------------------------------------------------------
        # STEP 8: Skepticism with Continued Engagement (Priority 6)
        # -------------------------------------------------------------
        if "SKEPTICISM" in all_detected_signals:
            return DetailedClassificationResponse(
                classification=IntentClassification.INTERESTED,
                confidence=0.85,
                reason="Customer expressed skepticism or cost concerns while remaining engaged in the dialogue.",
                priority_level=6,
                rule_applied="Priority 6: Skepticism + continued engagement indicates intent",
                languages_detected=languages,
                customer_turns_count=len(customer_turns),
                total_turns_count=len(turns),
                signals_detected=list(all_detected_signals),
                is_ambiguous_rescued=False,
                turns=turns
            )

        # -------------------------------------------------------------
        # STEP 9: Negative Sentiment & Disinterest Check Before Multi-Turn
        # If customer showed ANY negative signals or dismissive words
        # and has NO positive buying/inquiry signals, it MUST be NOT_INTERESTED!
        # -------------------------------------------------------------
        has_positive_signals = any(
            sig in {"STRONG_INTEREST", "QUESTION_INQUIRY", "CONDITIONAL_FUTURE", "SKEPTICISM"}
            for sig in all_detected_signals
        )

        has_negative_signals = any(
            sig in {"REJECTION", "OPT_OUT", "WRONG_PERSON"}
            for sig in all_detected_signals
        )

        # Check for negative dismissal patterns across all customer turns
        customer_full_text = " ".join(ct.text for ct in customer_turns).strip()
        negative_markers_found = []
        for pat in self.lexicon.REJECTION_PATTERNS:
            if pat.search(customer_full_text):
                m = pat.search(customer_full_text)
                if m:
                    negative_markers_found.append(m.group(0))

        if (has_negative_signals or negative_markers_found) and not has_positive_signals:
            markers_str = ", ".join(f"'{m}'" for m in negative_markers_found[:3])
            return DetailedClassificationResponse(
                classification=IntentClassification.NOT_INTERESTED,
                confidence=0.88,
                reason=f"Customer expressed negative sentiment or dismissal ({markers_str or 'negative refusal'}) with no interest in the product/service.",
                priority_level=2,
                rule_applied="Negative Signal Priority: Customer disinterest and dismissive words override conversation length -> NOT_INTERESTED",
                languages_detected=languages,
                customer_turns_count=len(customer_turns),
                total_turns_count=len(turns),
                signals_detected=list(all_detected_signals) or ["REJECTION"],
                is_ambiguous_rescued=False,
                turns=turns
            )

        # -------------------------------------------------------------
        # STEP 10: Multi-Turn Engagement (Only when genuinely engaged without negative words)
        # -------------------------------------------------------------
        word_count = len(customer_full_text.split())

        if has_positive_signals:
            return DetailedClassificationResponse(
                classification=IntentClassification.INTERESTED,
                confidence=0.85,
                reason="Customer engaged in conversation with positive signals or inquiry.",
                priority_level=6,
                rule_applied="Section 7: Customer showed positive conversational engagement",
                languages_detected=languages,
                customer_turns_count=len(customer_turns),
                total_turns_count=len(turns),
                signals_detected=list(all_detected_signals),
                is_ambiguous_rescued=False,
                turns=turns
            )

        # If customer had multiple turns without any negative rejection (Sections 13 & 14)
        if (len(customer_turns) >= 2 or len(turns) >= 4) and not has_negative_signals:
            return DetailedClassificationResponse(
                classification=IntentClassification.INTERESTED,
                confidence=0.75,
                reason="Multi-turn conversation without rejection preserved as lead.",
                priority_level=7,
                rule_applied="Section 13 & 14: Unclear or ambiguous dialogue without rejection rescued as lead",
                languages_detected=languages,
                customer_turns_count=len(customer_turns),
                total_turns_count=len(turns),
                signals_detected=list(all_detected_signals),
                is_ambiguous_rescued=True,
                turns=turns
            )

        # No positive buying signals and no product interest demonstrated
        return DetailedClassificationResponse(
            classification=IntentClassification.NOT_INTERESTED,
            confidence=0.85,
            reason="Customer showed no interest, no inquiry about service, or dismissed the conversation.",
            priority_level=2,
            rule_applied="Section 14: No customer buying signals or product interest -> NOT_INTERESTED",
            languages_detected=languages,
            customer_turns_count=len(customer_turns),
            total_turns_count=len(turns),
            signals_detected=list(all_detected_signals),
            is_ambiguous_rescued=False,
            turns=turns
        )
