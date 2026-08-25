from typing import Optional

from .domain import (
    Explanation,
    ExtractionResult,
    Language,
    RuleResult,
    SourceReference,
    WorkflowState,
)


# ============================================================
# COPY / TRANSLATIONS
# ============================================================

COPY = {
    # -----------------------------
    # KYC
    # -----------------------------
    "KYC_INCOMPLETE": (
        "KYC verification needs attention",
        "Your PF claim cannot move forward because the required KYC verification is incomplete.",
        "Review your KYC information and complete any missing verification.",
        "After the KYC details are completed or corrected, continue with the claim.",
    ),

    # -----------------------------
    # BANK
    # -----------------------------
    "BANK_VERIFICATION_FAILED": (
        "Bank verification needs attention",
        "Your PF claim may be affected because the bank verification has not been completed successfully.",
        "Check the bank account details linked to your PF account and verify the status.",
        "Correct the bank details if required, then continue with the claim.",
    ),

    # -----------------------------
    # SERVICE
    # -----------------------------
    "SERVICE_INFORMATION_MISSING": (
        "Service information is missing",
        "Your PF claim cannot be checked completely because required employment or service information is missing.",
        "Review the employment and service details associated with your PF account.",
        "Complete or correct the missing service information before continuing.",
    ),

    # -----------------------------
    # INFORMATION CONFLICT
    # -----------------------------
    "INFORMATION_CONFLICT": (
        "Information does not match",
        "Some information required for your PF claim does not match the available records.",
        "Review your personal, employment, and PF account information.",
        "Correct the mismatch before submitting or continuing the claim.",
    ),

    # -----------------------------
    # READY
    # -----------------------------
    "READY_TO_CONTINUE": (
        "Claim appears ready",
        "The available information does not indicate a blocking issue with the claim.",
        "Review the claim details once before proceeding.",
        "If EPFO shows a different status, follow the latest status shown on the official portal.",
    ),

    # -----------------------------
    # INVALID CLAIM
    # -----------------------------
    "INVALID_CLAIM_TYPE": (
        "Claim type needs attention",
        "The available information does not identify a supported PF claim type.",
        "Confirm whether this is a PF withdrawal or PF transfer request.",
        "Select the correct claim type and try again.",
    ),

    # -----------------------------
    # RESOLVED
    # -----------------------------
    "CLAIM_RESOLVED": (
        "Claim issue appears resolved",
        "The available case information indicates that this PF issue has been resolved.",
        "Review the latest case status and any remaining instructions.",
        "If the official EPFO portal shows a different status, follow the latest official status.",
    ),

    # -----------------------------
    # PF TRANSFER
    # -----------------------------
    "TRANSFER_SERVICE_MISSING": (
        "Transfer service information is unavailable",
        "Your PF transfer request needs additional information about your previous employment before it can proceed.",
        "Check the transfer service details associated with your previous and current employment.",
        "If the details are correct but the issue continues, contact EPFO support.",
    ),

    "TRANSFER_INFORMATION_CONFLICT": (
        "Transfer details do not match",
        "Some details in the transfer request do not match the information available in the PF records.",
        "Review your previous and current employment and PF account details.",
        "Correct the mismatch before submitting the transfer request again.",
    ),

    "TRANSFER_READY": (
        "Transfer appears ready",
        "The available transfer information does not show a blocking issue.",
        "Review the transfer details once before proceeding.",
        "If EPFO shows a different status, use the latest status shown on the official portal.",
    ),
}


TRANSLATIONS = {
    "en": COPY,

    "hi": {
        "KYC_INCOMPLETE": (
            "KYC सत्यापन पर ध्यान देना आवश्यक है",
            "आपका PF दावा आगे नहीं बढ़ सकता क्योंकि आवश्यक KYC सत्यापन पूरा नहीं हुआ है।",
            "अपनी KYC जानकारी की जाँच करें और आवश्यक सत्यापन पूरा करें।",
            "KYC जानकारी पूरी या सही करने के बाद दावे के साथ आगे बढ़ें।",
        ),

        "BANK_VERIFICATION_FAILED": (
            "बैंक सत्यापन पर ध्यान देना आवश्यक है",
            "आपके PF दावे में समस्या हो सकती है क्योंकि बैंक सत्यापन सफलतापूर्वक पूरा नहीं हुआ है।",
            "अपने PF खाते से जुड़े बैंक विवरण और सत्यापन स्थिति की जाँच करें।",
            "यदि आवश्यक हो तो बैंक विवरण सही करें और फिर दावे के साथ आगे बढ़ें।",
        ),

        "SERVICE_INFORMATION_MISSING": (
            "सेवा संबंधी जानकारी उपलब्ध नहीं है",
            "आपके PF दावे की पूरी जाँच नहीं हो सकती क्योंकि आवश्यक रोजगार या सेवा संबंधी जानकारी उपलब्ध नहीं है।",
            "अपने PF खाते से जुड़े रोजगार और सेवा विवरण की जाँच करें।",
            "आगे बढ़ने से पहले आवश्यक सेवा जानकारी पूरी या सही करें।",
        ),

        "INFORMATION_CONFLICT": (
            "जानकारी मेल नहीं खाती",
            "PF दावे के लिए आवश्यक कुछ जानकारी उपलब्ध रिकॉर्ड से मेल नहीं खाती।",
            "अपनी व्यक्तिगत, रोजगार और PF खाते की जानकारी की जाँच करें।",
            "दावा आगे बढ़ाने से पहले इस अंतर को ठीक करें।",
        ),

        "READY_TO_CONTINUE": (
            "दावा आगे बढ़ाने के लिए तैयार दिखाई देता है",
            "उपलब्ध जानकारी में दावे को रोकने वाली कोई स्पष्ट समस्या दिखाई नहीं दे रही है।",
            "आगे बढ़ने से पहले दावे के विवरण की एक बार जाँच करें।",
            "यदि EPFO पर अलग स्थिति दिखाई देती है, तो आधिकारिक पोर्टल की नवीनतम स्थिति का पालन करें।",
        ),

        "INVALID_CLAIM_TYPE": (
            "दावे के प्रकार पर ध्यान देना आवश्यक है",
            "उपलब्ध जानकारी से समर्थित PF दावे का प्रकार स्पष्ट नहीं है।",
            "पुष्टि करें कि यह PF withdrawal या PF transfer अनुरोध है।",
            "सही दावे का प्रकार चुनकर दोबारा प्रयास करें।",
        ),

        "CLAIM_RESOLVED": (
            "दावे की समस्या हल दिखाई देती है",
            "उपलब्ध केस जानकारी के अनुसार PF से संबंधित समस्या हल हो गई है।",
            "नवीनतम केस स्थिति और शेष निर्देशों की जाँच करें।",
            "यदि आधिकारिक EPFO पोर्टल पर अलग स्थिति दिखाई देती है, तो नवीनतम आधिकारिक स्थिति का पालन करें।",
        ),

        "TRANSFER_SERVICE_MISSING": (
            "ट्रांसफर सेवा की जानकारी उपलब्ध नहीं है",
            "आपके PF ट्रांसफर अनुरोध को आगे बढ़ाने के लिए पुराने रोजगार से संबंधित अतिरिक्त जानकारी आवश्यक है।",
            "अपने पुराने और वर्तमान रोजगार से जुड़ी PF ट्रांसफर जानकारी की जाँच करें।",
            "यदि जानकारी सही है लेकिन समस्या बनी रहती है, तो EPFO सहायता से संपर्क करें।",
        ),

        "TRANSFER_INFORMATION_CONFLICT": (
            "ट्रांसफर की जानकारी मेल नहीं खाती",
            "ट्रांसफर अनुरोध में कुछ जानकारी PF रिकॉर्ड में उपलब्ध जानकारी से मेल नहीं खाती।",
            "अपने पुराने और वर्तमान रोजगार तथा PF खाते की जानकारी की जाँच करें।",
            "ट्रांसफर अनुरोध दोबारा भेजने से पहले इस अंतर को ठीक करें।",
        ),

        "TRANSFER_READY": (
            "ट्रांसफर आगे बढ़ाने के लिए तैयार दिखाई देता है",
            "उपलब्ध ट्रांसफर जानकारी में कोई स्पष्ट रुकावट दिखाई नहीं दे रही है।",
            "आगे बढ़ने से पहले ट्रांसफर विवरण की एक बार जाँच करें।",
            "यदि EPFO पर अलग स्थिति दिखाई देती है, तो आधिकारिक पोर्टल की नवीनतम स्थिति देखें।",
        ),
    },

    "kn": {
        "KYC_INCOMPLETE": (
            "KYC ಪರಿಶೀಲನೆಗೆ ಗಮನ ಅಗತ್ಯವಿದೆ",
            "ಅಗತ್ಯ KYC ಪರಿಶೀಲನೆ ಪೂರ್ಣಗೊಂಡಿಲ್ಲದ ಕಾರಣ ನಿಮ್ಮ PF ಕ್ಲೈಮ್ ಮುಂದುವರಿಯಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ.",
            "ನಿಮ್ಮ KYC ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಅಗತ್ಯ ಪರಿಶೀಲನೆಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ.",
            "KYC ಮಾಹಿತಿಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿದ ಅಥವಾ ಸರಿಪಡಿಸಿದ ನಂತರ ಕ್ಲೈಮ್ ಮುಂದುವರಿಸಿ.",
        ),

        "BANK_VERIFICATION_FAILED": (
            "ಬ್ಯಾಂಕ್ ಪರಿಶೀಲನೆಗೆ ಗಮನ ಅಗತ್ಯವಿದೆ",
            "ಬ್ಯಾಂಕ್ ಪರಿಶೀಲನೆ ಯಶಸ್ವಿಯಾಗಿ ಪೂರ್ಣಗೊಂಡಿಲ್ಲದ ಕಾರಣ ನಿಮ್ಮ PF ಕ್ಲೈಮ್ ಮೇಲೆ ಪರಿಣಾಮ ಬೀರುವ ಸಾಧ್ಯತೆಯಿದೆ.",
            "ನಿಮ್ಮ PF ಖಾತೆಗೆ ಸಂಬಂಧಿಸಿದ ಬ್ಯಾಂಕ್ ವಿವರಗಳು ಮತ್ತು ಪರಿಶೀಲನಾ ಸ್ಥಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ.",
            "ಅಗತ್ಯವಿದ್ದರೆ ಬ್ಯಾಂಕ್ ವಿವರಗಳನ್ನು ಸರಿಪಡಿಸಿ ಮತ್ತು ನಂತರ ಕ್ಲೈಮ್ ಮುಂದುವರಿಸಿ.",
        ),

        "SERVICE_INFORMATION_MISSING": (
            "ಸೇವಾ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ",
            "ಅಗತ್ಯ ಉದ್ಯೋಗ ಅಥವಾ ಸೇವಾ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲದ ಕಾರಣ ನಿಮ್ಮ PF ಕ್ಲೈಮ್ ಅನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ಪರಿಶೀಲಿಸಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ.",
            "ನಿಮ್ಮ PF ಖಾತೆಗೆ ಸಂಬಂಧಿಸಿದ ಉದ್ಯೋಗ ಮತ್ತು ಸೇವಾ ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
            "ಮುಂದುವರಿಯುವ ಮೊದಲು ಅಗತ್ಯ ಸೇವಾ ಮಾಹಿತಿಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ ಅಥವಾ ಸರಿಪಡಿಸಿ.",
        ),

        "INFORMATION_CONFLICT": (
            "ಮಾಹಿತಿ ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ",
            "PF ಕ್ಲೈಮ್‌ಗೆ ಅಗತ್ಯವಿರುವ ಕೆಲವು ಮಾಹಿತಿ ಲಭ್ಯವಿರುವ ದಾಖಲೆಗಳಿಗೆ ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ.",
            "ನಿಮ್ಮ ವೈಯಕ್ತಿಕ, ಉದ್ಯೋಗ ಮತ್ತು PF ಖಾತೆಯ ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ.",
            "ಕ್ಲೈಮ್ ಮುಂದುವರಿಸುವ ಮೊದಲು ಈ ವ್ಯತ್ಯಾಸವನ್ನು ಸರಿಪಡಿಸಿ.",
        ),

        "READY_TO_CONTINUE": (
            "ಕ್ಲೈಮ್ ಮುಂದುವರಿಸಲು ಸಿದ್ಧವಾಗಿದೆ",
            "ಲಭ್ಯವಿರುವ ಮಾಹಿತಿಯಲ್ಲಿ ಕ್ಲೈಮ್ ಅನ್ನು ತಡೆಯುವ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಸಮಸ್ಯೆ ಕಾಣಿಸುತ್ತಿಲ್ಲ.",
            "ಮುಂದುವರಿಯುವ ಮೊದಲು ಕ್ಲೈಮ್ ವಿವರಗಳನ್ನು ಮತ್ತೊಮ್ಮೆ ಪರಿಶೀಲಿಸಿ.",
            "EPFO ನಲ್ಲಿ ಬೇರೆ ಸ್ಥಿತಿ ಕಂಡುಬಂದರೆ ಅಧಿಕೃತ ಪೋರ್ಟಲ್‌ನ ಇತ್ತೀಚಿನ ಸ್ಥಿತಿಯನ್ನು ಅನುಸರಿಸಿ.",
        ),

        "INVALID_CLAIM_TYPE": (
            "ಕ್ಲೈಮ್ ಪ್ರಕಾರಕ್ಕೆ ಗಮನ ಅಗತ್ಯವಿದೆ",
            "ಲಭ್ಯವಿರುವ ಮಾಹಿತಿಯಿಂದ ಬೆಂಬಲಿತ PF ಕ್ಲೈಮ್ ಪ್ರಕಾರವನ್ನು ಗುರುತಿಸಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ.",
            "ಇದು PF withdrawal ಅಥವಾ PF transfer ವಿನಂತಿಯೇ ಎಂದು ಖಚಿತಪಡಿಸಿ.",
            "ಸರಿಯಾದ ಕ್ಲೈಮ್ ಪ್ರಕಾರವನ್ನು ಆಯ್ಕೆ ಮಾಡಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        ),

        "CLAIM_RESOLVED": (
            "ಕ್ಲೈಮ್ ಸಮಸ್ಯೆ ಪರಿಹಾರಗೊಂಡಂತೆ ಕಾಣುತ್ತದೆ",
            "ಲಭ್ಯವಿರುವ ಪ್ರಕರಣದ ಮಾಹಿತಿಯ ಪ್ರಕಾರ PF ಸಮಸ್ಯೆ ಪರಿಹಾರಗೊಂಡಿದೆ.",
            "ಇತ್ತೀಚಿನ ಪ್ರಕರಣದ ಸ್ಥಿತಿ ಮತ್ತು ಉಳಿದ ಸೂಚನೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
            "ಅಧಿಕೃತ EPFO ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಬೇರೆ ಸ್ಥಿತಿ ಕಂಡುಬಂದರೆ ಇತ್ತೀಚಿನ ಅಧಿಕೃತ ಸ್ಥಿತಿಯನ್ನು ಅನುಸರಿಸಿ.",
        ),

        "TRANSFER_SERVICE_MISSING": (
            "ವರ್ಗಾವಣೆ ಸೇವೆಯ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ",
            "ನಿಮ್ಮ PF ವರ್ಗಾವಣೆ ವಿನಂತಿಯನ್ನು ಮುಂದುವರಿಸಲು ಹಿಂದಿನ ಉದ್ಯೋಗಕ್ಕೆ ಸಂಬಂಧಿಸಿದ ಹೆಚ್ಚುವರಿ ಮಾಹಿತಿ ಅಗತ್ಯವಿದೆ.",
            "ಹಿಂದಿನ ಮತ್ತು ಪ್ರಸ್ತುತ ಉದ್ಯೋಗಕ್ಕೆ ಸಂಬಂಧಿಸಿದ PF ವರ್ಗಾವಣೆ ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ.",
            "ಮಾಹಿತಿ ಸರಿಯಾಗಿದ್ದರೂ ಸಮಸ್ಯೆ ಮುಂದುವರಿದರೆ EPFO ಸಹಾಯವನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        ),

        "TRANSFER_INFORMATION_CONFLICT": (
            "ವರ್ಗಾವಣೆ ಮಾಹಿತಿ ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ",
            "ವರ್ಗಾವಣೆ ವಿನಂತಿಯಲ್ಲಿರುವ ಕೆಲವು ಮಾಹಿತಿ PF ದಾಖಲೆಗಳಲ್ಲಿರುವ ಮಾಹಿತಿಗೆ ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ.",
            "ಹಿಂದಿನ ಮತ್ತು ಪ್ರಸ್ತುತ ಉದ್ಯೋಗ ಹಾಗೂ PF ಖಾತೆಯ ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
            "ವರ್ಗಾವಣೆ ವಿನಂತಿಯನ್ನು ಮತ್ತೆ ಸಲ್ಲಿಸುವ ಮೊದಲು ವ್ಯತ್ಯಾಸವನ್ನು ಸರಿಪಡಿಸಿ.",
        ),

        "TRANSFER_READY": (
            "ವರ್ಗಾವಣೆ ಮುಂದುವರಿಸಲು ಸಿದ್ಧವಾಗಿದೆ",
            "ಲಭ್ಯವಿರುವ ವರ್ಗಾವಣೆ ಮಾಹಿತಿಯಲ್ಲಿ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಅಡ್ಡಿ ಕಾಣಿಸುತ್ತಿಲ್ಲ.",
            "ಮುಂದುವರಿಯುವ ಮೊದಲು ವರ್ಗಾವಣೆ ವಿವರಗಳನ್ನು ಮತ್ತೊಮ್ಮೆ ಪರಿಶೀಲಿಸಿ.",
            "EPFO ನಲ್ಲಿ ಬೇರೆ ಸ್ಥಿತಿ ಕಂಡುಬಂದರೆ ಅಧಿಕೃತ ಪೋರ್ಟಲ್‌ನ ಇತ್ತೀಚಿನ ಸ್ಥಿತಿಯನ್ನು ಅನುಸರಿಸಿ.",
        ),
    },
}


# ============================================================
# SCENARIO INFERENCE
# ============================================================

def infer_scenario(text: str) -> Optional[str]:
    """
    Infer the PF workflow scenario from user-provided text.

    Returns:
        "transfer"
        "withdrawal"
        None
    """

    t = (text or "").lower().strip()

    transfer_words = [
        "transfer",
        "pf transfer",
        "uan transfer",
        "previous employer",
        "old employer",
        "current employer",
        "transfer claim",
        "transfer request",
    ]

    withdrawal_words = [
        "withdraw",
        "withdrawal",
        "withdraw pf",
        "pf withdrawal",
        "claim",
        "settlement",
        "final settlement",
    ]

    # Transfer must be checked first because a transfer request
    # may also contain the word "claim".
    if any(word in t for word in transfer_words):
        return "transfer"

    if any(word in t for word in withdrawal_words):
        return "withdrawal"

    return None


# ============================================================
# ISSUE INFERENCE
# ============================================================

def infer_issue(text: str) -> Optional[str]:
    """
    Infer a normalized issue category from the text.

    Priority is deliberate:
        1. Transfer-specific issues
        2. Bank issues
        3. Service/employment issues
        4. Information conflicts
        5. KYC issues
        6. Ready
    """

    t = (text or "").lower().strip()

    # --------------------------------------------------------
    # TRANSFER
    # --------------------------------------------------------

    is_transfer = any(
        word in t
        for word in [
            "transfer",
            "previous employer",
            "old employer",
            "current employer",
        ]
    )

    if is_transfer:

        # Transfer conflict has highest priority.
        if any(
            phrase in t
            for phrase in [
                "conflict",
                "mismatch",
                "does not match",
                "do not match",
                "don't match",
                "doesn't match",
                "not matching",
                "different",
                "incorrect details",
                "incorrect information",
            ]
        ):
            return "transfer_conflict"

        # Missing/incomplete transfer service information.
        if any(
            phrase in t
            for phrase in [
                "missing",
                "incomplete",
                "not available",
                "not found",
                "unavailable",
                "missing service",
                "service information",
            ]
        ):
            return "transfer_service"

        # Explicitly ready/complete transfer.
        if any(
            phrase in t
            for phrase in [
                "ready",
                "ready to continue",
                "ready to proceed",
                "complete",
                "completed",
                "successfully completed",
            ]
        ):
            return "transfer_ready"

        return "transfer_service"

    # --------------------------------------------------------
    # BANK
    # --------------------------------------------------------

    if any(
        phrase in t
        for phrase in [
            "bank",
            "bank account",
            "bank details",
            "bank verification",
            "account number",
            "ifsc",
            "ifsc code",
        ]
    ):
        return "bank"

    # --------------------------------------------------------
    # SERVICE / EMPLOYMENT
    # --------------------------------------------------------

    if any(
        phrase in t
        for phrase in [
            "service information",
            "service details",
            "employment information",
            "employment details",
            "employment history",
            "service history",
            "missing service",
            "service missing",
            "employment missing",
            "employment record",
        ]
    ):
        return "service"

    # --------------------------------------------------------
    # INFORMATION CONFLICT
    # --------------------------------------------------------

    if any(
        phrase in t
        for phrase in [
            "conflict",
            "mismatch",
            "does not match",
            "do not match",
            "don't match",
            "doesn't match",
            "not matching",
            "different",
            "incorrect details",
            "incorrect information",
            "details do not match",
            "details don't match",
            "information does not match",
            "information doesn't match",
            "records do not match",
            "records don't match",
        ]
    ):
        return "conflict"

    # --------------------------------------------------------
    # KYC
    # --------------------------------------------------------
    #
    # IMPORTANT:
    # This block deliberately comes BEFORE "ready" / "complete".
    #
    # Example:
    # "KYC verification is incomplete"
    #
    # contains "complete", but it is NOT a ready case.
    # --------------------------------------------------------

    if "kyc" in t:

        if any(
            phrase in t
            for phrase in [
                "incomplete",
                "incomplete kyc",
                "kyc incomplete",
                "missing",
                "not verified",
                "not verified kyc",
                "verification failed",
                "verification is incomplete",
                "verification incomplete",
                "verify",
                "verification",
                "rejected",
                "rejection",
                "failed",
                "failure",
                "pending",
                "not complete",
                "not completed",
            ]
        ):
            return "kyc"

        # If KYC is explicitly mentioned without a positive
        # completion statement, treat it as a KYC issue.
        if not any(
            phrase in t
            for phrase in [
                "kyc complete",
                "kyc completed",
                "kyc verified",
                "kyc successfully verified",
            ]
        ):
            return "kyc"

    # --------------------------------------------------------
    # GENERIC VERIFICATION / REJECTION
    # --------------------------------------------------------

    if any(
        phrase in t
        for phrase in [
            "verification failed",
            "verification is incomplete",
            "verification incomplete",
            "not verified",
            "rejected",
            "rejection",
            "claim rejected",
            "claim was rejected",
        ]
    ):
        return "kyc"

    # --------------------------------------------------------
    # READY
    # --------------------------------------------------------
    #
    # This is intentionally near the end.
    # "incomplete" must NEVER reach this branch.
    # --------------------------------------------------------

    if any(
        phrase in t
        for phrase in [
            "ready to continue",
            "ready to proceed",
            "claim is ready",
            "claim appears ready",
            "ready",
        ]
    ):
        return "ready"

    return None


# ============================================================
# EXTRACTION
# ============================================================

def local_extraction(text: str) -> ExtractionResult:
    """
    Deterministic local extraction used by the demo/mock workflow.
    """

    cleaned = redact(text)

    return ExtractionResult(
        mentioned_issue=cleaned or None,
        scenario_hint=infer_issue(text) or infer_scenario(text),
        mode="demo_mock",
    )


# ============================================================
# REDACTION
# ============================================================

def redact(text: str) -> str:
    """
    Minimal deterministic redaction for obvious sensitive identifiers.

    This intentionally does not attempt to identify every possible
    piece of PII. It is only a demo-safe preprocessing layer.
    """

    if not text:
        return ""

    import re

    value = text

    # Aadhaar-like 12 digit number.
    value = re.sub(
        r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "[REDACTED-AADHAAR]",
        value,
    )

    # PAN-like identifier.
    value = re.sub(
        r"\b[A-Z]{5}\d{4}[A-Z]\b",
        "[REDACTED-PAN]",
        value,
        flags=re.IGNORECASE,
    )

    # UAN-like 12 digit number.
    value = re.sub(
        r"\b\d{12}\b",
        "[REDACTED-ID]",
        value,
    )

    return value


# ============================================================
# LOCAL EXPLANATION
# ============================================================

def local_explanation(
    result: RuleResult,
    sources: list[SourceReference],
    language: Language,
    mode: str = "demo_mock",
) -> Explanation:
    """
    Generate deterministic explanation text.

    This function returns the exact fields expected by
    domain.Explanation.
    """

    language_key = getattr(
        language,
        "value",
        str(language),
    )

    translations = TRANSLATIONS.get(
        language_key,
        TRANSLATIONS["en"],
    )

    reason_code = getattr(
        result.reason_code,
        "value",
        str(result.reason_code),
    )

    reason_code = reason_code.upper()

    copy = translations.get(reason_code)

    if copy is None:
        copy = COPY.get(reason_code)

    # Final safety fallback.
    if copy is None:
        copy = (
            "PF request needs attention",
            "The available information indicates that this PF request needs additional review.",
            "Review the details associated with the request and verify the relevant information.",
            "If the issue continues, check the latest EPFO guidance or contact EPFO support.",
        )

    title, happened, first, second = copy

    why = (
        "NIVA's deterministic workflow check found: "
        f"{reason_code.replace('_', ' ').lower()}."
    )

    if sources:
        why += " The listed official guidance is relevant to this next step."

    return Explanation(
        what_happened=happened,
        what_to_do=[
            first,
            second,
        ],
        why=why,
        source_references=sources,
        language=language,
        mode=mode,
    )


# ============================================================
# TIMELINE
# ============================================================

def timeline(current_step: WorkflowState) -> list[dict]:
    """
    Build deterministic workflow timeline.

    The API schema converts these dictionaries into TimelineItem
    objects automatically.
    """

    steps = [
        ("claim_preparation", "Claim preparation"),
        ("eligibility_check", "Eligibility check"),
        ("kyc_verification", "KYC verification"),
        ("bank_verification", "Bank verification"),
        ("claim_submission", "Claim submission"),
        ("processing", "Processing"),
        ("payment", "Payment"),
        ("resolved", "Resolved"),
    ]

    current_key = getattr(
        current_step,
        "value",
        str(current_step),
    )

    current_index = -1

    for index, (key, _) in enumerate(steps):
        if key == current_key:
            current_index = index
            break

    result = []

    for index, (key, label) in enumerate(steps):

        if current_index == -1:
            state = "upcoming"

        elif index < current_index:
            state = "complete"

        elif index == current_index:
            state = "current"

        else:
            state = "upcoming"

        result.append(
            {
                "key": key,
                "label": label,
                "state": state,
            }
        )

    return result
