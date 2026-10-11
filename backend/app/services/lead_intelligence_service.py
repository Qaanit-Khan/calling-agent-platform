import os
import sys
import logging
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# Ensure the model package is importable
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "model"))
if MODEL_DIR not in sys.path and os.path.exists(MODEL_DIR):
    sys.path.insert(0, MODEL_DIR)

try:
    from classifier.engine import IntentClassifier
    from classifier.models import IntentClassification, DetailedClassificationResponse
    from classifier.followup_detector import followup_detector, FollowupDetectionResult, FOLLOWUP_CATEGORIES
    _classifier_available = True
except Exception as e:
    logging.getLogger(__name__).warning(f"Could not import IntentClassifier or FollowupDetector from model dir: {e}")
    _classifier_available = False
    followup_detector = None
    FOLLOWUP_CATEGORIES = {}

from app.models.call import Call, Transcript, TranscriptSegment
from app.models.lead import Lead, Followup

logger = logging.getLogger(__name__)


class LeadIntelligenceService:
    """
    Service wrapper for the Two-Class AI Call Transcript Intent Classifier.
    Evaluates real customer conversation transcripts across English, Hindi, Hinglish, and Marathi
    to classify intent into INTERESTED or NOT_INTERESTED with full diagnostic reasoning.
    """

    def __init__(self):
        if _classifier_available:
            self.classifier = IntentClassifier()
        else:
            self.classifier = None

    def build_transcript_text(self, call: Call) -> str:
        """
        Extracts formatted multi-turn conversation text from call transcript segments.
        """
        if not call.transcript or not call.transcript.segments:
            return ""

        lines = []
        for seg in sorted(call.transcript.segments, key=lambda s: s.sequence if s.sequence is not None else 0):
            role_prefix = "Agent" if seg.speaker in ("agent", "bot", "assistant") else "Customer"
            lines.append(f"{role_prefix}: {seg.text}")

        return "\n".join(lines).strip()

    async def analyze_call(self, session: AsyncSession, call: Call) -> Dict[str, Any]:
        """
        Analyzes a call's full transcript using the IntentClassifier engine
        and updates the call disposition and lead records accordingly.
        """
        transcript_text = self.build_transcript_text(call)

        # Handle empty/unrecorded calls
        if not transcript_text:
            return {
                "analysis_id": f"intel_{call.id}",
                "call_id": call.id,
                "agent_id": call.agent_id,
                "contact_id": call.contact_id,
                "status": "uncertain",
                "confidence_score": 0.0,
                "confidence": 0.0,
                "classification": "UNCERTAIN",
                "reasoning": "No transcript turns available to evaluate customer intent.",
                "rule_applied": "No conversational data",
                "signals": [],
                "languages": [],
                "keywords": [],
                "created_at": datetime.now(UTC).isoformat(),
            }

        if self.classifier:
            try:
                diag: DetailedClassificationResponse = self.classifier.classify_detailed(transcript_text)
                is_interested = (diag.classification == IntentClassification.INTERESTED)
                status = "interested" if is_interested else "not_interested"
                confidence = float(diag.confidence)

                # Persist intelligence disposition on call
                call.disposition = status
                session.add(call)

                # Auto-create or update Lead record if interested
                if is_interested:
                    lead_stmt = select(Lead).where(Lead.call_id == call.id)
                    lead_res = await session.execute(lead_stmt)
                    lead = lead_res.scalar_one_or_none()
                    if not lead:
                        lead = Lead(
                            tenant_id=call.tenant_id,
                            agent_id=call.agent_id,
                            contact_id=call.contact_id,
                            call_id=call.id,
                            phone_number=call.phone_number,
                            score=confidence,
                            reason=diag.reason,
                            status="interested",
                        )
                        session.add(lead)
                    else:
                        lead.score = confidence
                        lead.reason = diag.reason
                        lead.status = "interested"

                keywords = list(diag.signals_detected) if diag.signals_detected else []
                if diag.languages_detected:
                    keywords.extend([f"Lang: {l}" for l in diag.languages_detected if l not in keywords])

                # Check follow-up condition
                followup_info = None
                if followup_detector:
                    f_res = followup_detector.detect_followup_detailed(transcript_text)
                    if f_res.category_id is not None:
                        followup_info = {
                            "category_id": f_res.category_id,
                            "name": f_res.name,
                            "description": f_res.description,
                            "requires_followup": f_res.requires_followup,
                            "action": f_res.action,
                            "suggested_scheduled_at": f_res.suggested_scheduled_at,
                            "matched_utterance": f_res.matched_utterance,
                        }

                return {
                    "analysis_id": f"intel_{call.id}",
                    "call_id": call.id,
                    "agent_id": call.agent_id,
                    "contact_id": call.contact_id,
                    "status": status,
                    "confidence_score": confidence,
                    "confidence": confidence,
                    "classification": diag.classification.value,
                    "reasoning": diag.reason,
                    "rule_applied": diag.rule_applied,
                    "signals": diag.signals_detected,
                    "languages": diag.languages_detected,
                    "keywords": keywords,
                    "followup": followup_info,
                    "raw_model_output": diag.model_dump(),
                    "created_at": datetime.now(UTC).isoformat(),
                }
            except Exception as e:
                logger.error(f"IntentClassifier failed on call {call.id}: {e}", exc_info=True)

        # Fallback if engine unavailable
        return {
            "analysis_id": f"intel_{call.id}",
            "call_id": call.id,
            "agent_id": call.agent_id,
            "contact_id": call.contact_id,
            "status": "uncertain",
            "confidence_score": 0.5,
            "confidence": 0.5,
            "classification": "UNCERTAIN",
            "reasoning": "Model classifier engine could not be executed.",
            "rule_applied": "Fallback",
            "signals": [],
            "languages": [],
            "keywords": [],
            "followup": None,
            "created_at": datetime.now(UTC).isoformat(),
        }

    async def analyze_followup(self, session: AsyncSession, call: Call) -> Dict[str, Any]:
        """
        Evaluates the transcript using the 25-category Follow-Up Detection Engine.
        If a follow-up condition is detected, optionally records or updates the Followup table.
        """
        transcript_text = self.build_transcript_text(call)
        if not followup_detector:
            return {
                "call_id": call.id,
                "category_id": None,
                "name": None,
                "requires_followup": False,
                "message": "Followup detector engine unavailable"
            }

        res: FollowupDetectionResult = followup_detector.detect_followup_detailed(transcript_text)
        scheduled_dt = None
        if res.suggested_scheduled_at:
            try:
                scheduled_dt = datetime.fromisoformat(res.suggested_scheduled_at.replace("Z", "+00:00"))
            except Exception:
                pass

        followup_record_id = None
        # Auto-create or update Followup record if category requires follow-up
        call_phone = call.phone_number or call.caller_number
        if res.requires_followup and call_phone:
            stmt = select(Followup).where(Followup.call_id == call.id)
            db_res = await session.execute(stmt)
            followup = db_res.scalar_one_or_none()
            notes_str = f"Category {res.category_id}: {res.name}. Action: {res.action}. (Matched: '{res.matched_utterance or 'N/A'}')"

            if not followup:
                followup = Followup(
                    tenant_id=call.tenant_id,
                    contact_id=call.contact_id,
                    agent_id=call.agent_id,
                    call_id=call.id,
                    phone_number=call_phone,
                    scheduled_at=scheduled_dt,
                    status="pending",
                    notes=notes_str,
                )
                session.add(followup)
            else:
                followup.scheduled_at = scheduled_dt or followup.scheduled_at
                followup.notes = notes_str
                followup.status = "pending"

            await session.flush()
            followup_record_id = followup.id

        return {
            "call_id": call.id,
            "agent_id": call.agent_id,
            "category_id": res.category_id,
            "name": res.name,
            "description": res.description,
            "requires_followup": res.requires_followup,
            "action": res.action,
            "suggested_scheduled_at": res.suggested_scheduled_at,
            "matched_utterance": res.matched_utterance,
            "priority_level": res.priority_level,
            "followup_id": followup_record_id,
        }


lead_intelligence_service = LeadIntelligenceService()

