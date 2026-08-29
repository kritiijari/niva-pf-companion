import { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  ArrowRight,
  Check,
  ChevronLeft,
  FileText,
  Globe2,
  Landmark,
  Send,
  Sparkles,
  WalletCards,
  RotateCcw,
  ShieldCheck,
  Upload,
  X,
} from 'lucide-react';
import './styles.css';

type TimelineStep = {
  key: string;
  label: string;
  state: 'complete' | 'current' | 'upcoming';
};

type Source = {
  title: string;
  url: string;
  section: string;
  excerpt: string;
};

type Analysis = {
  title: string;
  what_happened: string;
  what_to_do: string[];
  why: string;
  source?: Source | null;
  timeline: TimelineStep[];
  reasonCode?: string;
};

type Extraction = {
  mentioned_issue?: string | null;
  scenario_hint?: string | null;
  rejection_reason?: string | null;
  claim_type?: string | null;
  mode?: string;
};

type ClaimType = 'withdrawal' | 'transfer';
type Journey = 'general' | ClaimType;

type ResolutionPlan = {
  title: string;
  summary: string;
  steps: string[];
  guidanceLabel: string;
};

const translations: Record<string, Record<string, string>> = {
  EN: {},
  HI: {
    'Demo mode': 'डेमो मोड', 'Prototype — uses synthetic data. Not an official EPFO service.': 'प्रोटोटाइप — केवल कृत्रिम डेटा का उपयोग करता है। यह आधिकारिक EPFO सेवा नहीं है।',
    'Your PF journey,': 'आपकी PF यात्रा,', 'explained.': 'आसान भाषा में।', 'Understand what went wrong, why it happened, and what to do next.': 'जानें क्या गलत हुआ, क्यों हुआ और आगे क्या करना है।',
    'Your issue': 'आपकी समस्या', 'Workflow check': 'वर्कफ़्लो जाँच', 'Official guidance': 'आधिकारिक मार्गदर्शन', 'Resolution plan': 'समाधान योजना',
    'NIVA ANALYSIS': 'NIVA विश्लेषण', 'Tell NIVA what happened': 'NIVA को बताएं क्या हुआ', 'Describe your PF issue in your own words. NIVA will identify what may be blocking your journey and show the next practical step.': 'अपनी PF समस्या अपने शब्दों में बताएं। NIVA संभावित रुकावट पहचानकर अगला व्यावहारिक कदम बताएगा।', 'Start with my issue': 'मेरी समस्या से शुरू करें',
    'PF WITHDRAWAL': 'PF निकासी', 'I want to withdraw my PF': 'मैं अपना PF निकालना चाहता/चाहती हूँ', 'Explore withdrawal': 'निकासी देखें', 'PF TRANSFER': 'PF स्थानांतरण', 'I want to transfer my PF': 'मैं अपना PF स्थानांतरित करना चाहता/चाहती हूँ', 'Explore transfer': 'स्थानांतरण देखें', 'Built for clarity. No real personal data needed.': 'स्पष्टता के लिए बनाया गया। वास्तविक व्यक्तिगत डेटा की आवश्यकता नहीं।',
    'Back': 'वापस', 'STEP 1 OF 2': 'चरण 1 / 2', 'NIVA will identify the relevant PF workflow': 'NIVA संबंधित PF वर्कफ़्लो पहचानेगा', 'Tell NIVA what\nhappened.': 'NIVA को बताएं\nक्या हुआ।', 'What needs\nattention?': 'किस पर\nध्यान चाहिए?', 'What happened?': 'क्या हुआ?', 'Describe the issue in your own words': 'समस्या अपने शब्दों में बताएं', 'Add a synthetic notice': 'कृत्रिम सूचना जोड़ें', 'Ready to analyse': 'विश्लेषण के लिए तैयार', 'Text-based PDF · synthetic data only': 'टेक्स्ट आधारित PDF · केवल कृत्रिम डेटा', 'Let NIVA analyse this': 'NIVA से इसका विश्लेषण कराएं', 'Analyse my withdrawal request': 'मेरी निकासी अनुरोध का विश्लेषण करें', 'Analyse my transfer request': 'मेरे स्थानांतरण अनुरोध का विश्लेषण करें', 'Start over': 'फिर से शुरू करें', 'Try another demo': 'दूसरा डेमो आज़माएं',
    'ANALYSING SYNTHETIC DOCUMENT': 'कृत्रिम दस्तावेज़ का विश्लेषण', 'ANALYSING SYNTHETIC INFORMATION': 'कृत्रिम जानकारी का विश्लेषण', 'Understanding\nyour claim…': 'आपके दावे को\nसमझ रहे हैं…', 'We’re checking the information you provided.': 'हम आपकी दी गई जानकारी जाँच रहे हैं।',
    'ANALYSIS COMPLETE': 'विश्लेषण पूरा', 'WHAT NIVA FOUND': 'NIVA ने क्या पाया', 'WHAT HAPPENED?': 'क्या हुआ?', 'WHAT DO I DO?': 'मुझे क्या करना चाहिए?', 'OFFICIAL GUIDANCE': 'आधिकारिक मार्गदर्शन', 'View official guidance': 'आधिकारिक मार्गदर्शन देखें', 'YOUR JOURNEY': 'आपकी यात्रा', 'YOU ARE HERE': 'आप यहाँ हैं',
    'I understand my next step': 'मैं अपना अगला कदम समझता/समझती हूँ', 'Back to analysis': 'विश्लेषण पर वापस', 'YOUR RESOLUTION PLAN': 'आपकी समाधान योजना', 'NIVA RECOMMENDS': 'NIVA की सिफारिश', 'WHAT TO DO NEXT': 'आगे क्या करें', 'YOUR ACTION PLAN': 'आपकी कार्य योजना', 'Analyze another issue': 'दूसरी समस्या का विश्लेषण करें',
    'How NIVA works': 'NIVA कैसे काम करता है', 'Go to NIVA home': 'NIVA होम पर जाएँ', 'Language': 'भाषा', 'Exploring a PF withdrawal request': 'PF निकासी अनुरोध की जाँच', 'Exploring a PF transfer request': 'PF स्थानांतरण अनुरोध की जाँच',
    'Describe the issue or add a synthetic notice. NIVA will analyse the information, run a workflow check, and show the next practical step.': 'समस्या बताएं या कृत्रिम सूचना जोड़ें। NIVA जानकारी का विश्लेषण करेगा, वर्कफ़्लो जाँच करेगा और अगला व्यावहारिक कदम बताएगा।', 'Select a demo situation below, then add any context in your own words. You can also add a synthetic PDF notice.': 'नीचे एक डेमो स्थिति चुनें, फिर अपने शब्दों में संदर्भ जोड़ें। आप कृत्रिम PDF सूचना भी जोड़ सकते हैं।', 'Optional — helps NIVA explain it clearly': 'वैकल्पिक — NIVA को इसे स्पष्ट रूप से समझाने में मदद करता है',
    'Understand a blocked claim, verification issue, or the next step to submit.': 'रुके हुए दावे, सत्यापन समस्या या जमा करने के अगले कदम को समझें।', 'Check previous-employment details and move your PF account with confidence.': 'पिछले रोजगार का विवरण जाँचें और अपना PF खाता भरोसे से स्थानांतरित करें।', 'Please do not upload Aadhaar, PAN, UAN, bank details, OTPs, or any real personal data.': 'कृपया आधार, PAN, UAN, बैंक विवरण, OTP या कोई वास्तविक व्यक्तिगत डेटा अपलोड न करें।', 'Remove file': 'फ़ाइल हटाएँ',
    'Document received': 'दस्तावेज़ प्राप्त हुआ', 'Information analyzed': 'जानकारी का विश्लेषण किया गया', 'NIVA checks the case': 'NIVA मामले की जाँच करता है', 'Problem identified': 'समस्या पहचानी गई', 'Looking up official guidance': 'आधिकारिक मार्गदर्शन खोज रहे हैं', 'Official guidance found': 'आधिकारिक मार्गदर्शन मिला',
    'Retry': 'फिर से प्रयास करें', 'Return home': 'होम पर लौटें', 'NIVA analysis path': 'NIVA विश्लेषण पथ', 'YOUR REQUEST IS CLEAR TO CONTINUE': 'आपका अनुरोध आगे बढ़ने के लिए तैयार है', 'INFORMATION NIVA ANALYSED': 'NIVA द्वारा विश्लेषित जानकारी', 'WHY NIVA REACHED THIS RESULT': 'NIVA इस नतीजे पर क्यों पहुँचा', 'NIVA decision': 'NIVA निर्णय', 'Supporting information': 'सहायक जानकारी', 'SUPPORTING GUIDANCE': 'सहायक मार्गदर्शन', 'No matching source in the local knowledge base for this issue.': 'इस समस्या के लिए स्थानीय ज्ञान आधार में कोई मिलान स्रोत नहीं है।', 'NIVA interprets the information → deterministic rules decide the outcome → official guidance supports the next step.': 'NIVA जानकारी की व्याख्या करता है → निर्धारित नियम नतीजा तय करते हैं → आधिकारिक मार्गदर्शन अगले कदम में सहायता करता है।', 'Our local knowledge base does not contain sufficient source guidance for this issue.': 'हमारे स्थानीय ज्ञान आधार में इस समस्या के लिए पर्याप्त स्रोत मार्गदर्शन नहीं है।', 'Claim type': 'दावे का प्रकार', 'Issue mentioned': 'उल्लेखित समस्या', 'Information used': 'उपयोग की गई जानकारी', 'Issue identified': 'पहचानी गई समस्या',
    'NIVA found no blocking issue in the available information. The latest status on the official EPFO portal remains authoritative.': 'NIVA को उपलब्ध जानकारी में कोई रुकावट नहीं मिली। आधिकारिक EPFO पोर्टल पर नवीनतम स्थिति ही मान्य रहेगी।', 'Official guidance remains available on the analysis screen when a relevant source is retrieved.': 'संबंधित स्रोत मिलने पर आधिकारिक मार्गदर्शन विश्लेषण स्क्रीन पर उपलब्ध रहता है।', 'View official EPFO guidance': 'आधिकारिक EPFO मार्गदर्शन देखें', 'View official transfer guidance': 'आधिकारिक स्थानांतरण मार्गदर्शन देखें',
    'KYC verification': 'KYC सत्यापन', 'Bank verification': 'बैंक सत्यापन', 'Missing service info': 'सेवा जानकारी अनुपलब्ध', 'Information conflict': 'जानकारी में विरोध', 'No blocking issue': 'कोई रुकावट नहीं', 'Missing previous-employment info': 'पिछले रोजगार की जानकारी अनुपलब्ध', 'Transfer information mismatch': 'स्थानांतरण जानकारी में अंतर', 'Transfer ready to proceed': 'स्थानांतरण आगे बढ़ने के लिए तैयार',
    'Example: My PF claim was rejected because my bank details could not be verified.': 'उदाहरण: मेरा PF दावा अस्वीकार हो गया क्योंकि मेरे बैंक विवरण सत्यापित नहीं हो सके।', 'Example: My previous employer service details are missing for my PF transfer.': 'उदाहरण: मेरे PF स्थानांतरण के लिए मेरे पिछले नियोक्ता के सेवा विवरण अनुपलब्ध हैं।', 'Example: My withdrawal claim was rejected because KYC is incomplete.': 'उदाहरण: मेरा निकासी दावा अस्वीकार हो गया क्योंकि KYC अधूरा है।', 'WITHDRAWAL REQUEST': 'निकासी अनुरोध', 'TRANSFER REQUEST': 'स्थानांतरण अनुरोध',
  },
  KN: {
    'Demo mode': 'ಡೆಮೊ ಮೋಡ್', 'Prototype — uses synthetic data. Not an official EPFO service.': 'ಮಾದರಿ — ಕೃತಕ ಡೇಟಾವನ್ನು ಮಾತ್ರ ಬಳಸುತ್ತದೆ. ಇದು ಅಧಿಕೃತ EPFO ಸೇವೆಯಲ್ಲ.',
    'Your PF journey,': 'ನಿಮ್ಮ PF ಪಯಣ,', 'explained.': 'ಸರಳವಾಗಿ ವಿವರಿಸಲಾಗಿದೆ.', 'Understand what went wrong, why it happened, and what to do next.': 'ಏನು ತಪ್ಪಾಯಿತು, ಏಕೆ ಆಯಿತು ಮತ್ತು ಮುಂದೆ ಏನು ಮಾಡಬೇಕು ಎಂಬುದನ್ನು ತಿಳಿಯಿರಿ.',
    'Your issue': 'ನಿಮ್ಮ ಸಮಸ್ಯೆ', 'Workflow check': 'ಕಾರ್ಯಹರಿವು ಪರಿಶೀಲನೆ', 'Official guidance': 'ಅಧಿಕೃತ ಮಾರ್ಗದರ್ಶನ', 'Resolution plan': 'ಪರಿಹಾರ ಯೋಜನೆ',
    'NIVA ANALYSIS': 'NIVA ವಿಶ್ಲೇಷಣೆ', 'Tell NIVA what happened': 'NIVA ಗೆ ಏನಾಯಿತು ಎಂದು ತಿಳಿಸಿ', 'Describe your PF issue in your own words. NIVA will identify what may be blocking your journey and show the next practical step.': 'ನಿಮ್ಮ PF ಸಮಸ್ಯೆಯನ್ನು ನಿಮ್ಮ ಮಾತುಗಳಲ್ಲಿ ವಿವರಿಸಿ. NIVA ಅಡ್ಡಿಯಾಗಿರುವುದನ್ನು ಗುರುತಿಸಿ ಮುಂದಿನ ಪ್ರಾಯೋಗಿಕ ಹಂತವನ್ನು ತೋರಿಸುತ್ತದೆ.', 'Start with my issue': 'ನನ್ನ ಸಮಸ್ಯೆಯಿಂದ ಆರಂಭಿಸಿ',
    'PF WITHDRAWAL': 'PF ಹಿಂಪಡೆಯುವಿಕೆ', 'I want to withdraw my PF': 'ನನ್ನ PF ಹಿಂಪಡೆಯಲು ಬಯಸುತ್ತೇನೆ', 'Explore withdrawal': 'ಹಿಂಪಡೆಯುವಿಕೆ ನೋಡಿ', 'PF TRANSFER': 'PF ವರ್ಗಾವಣೆ', 'I want to transfer my PF': 'ನನ್ನ PF ವರ್ಗಾಯಿಸಲು ಬಯಸುತ್ತೇನೆ', 'Explore transfer': 'ವರ್ಗಾವಣೆ ನೋಡಿ', 'Built for clarity. No real personal data needed.': 'ಸ್ಪಷ್ಟತೆಗಾಗಿ ನಿರ್ಮಿಸಲಾಗಿದೆ. ನಿಜವಾದ ವೈಯಕ್ತಿಕ ಡೇಟಾ ಅಗತ್ಯವಿಲ್ಲ.',
    'Back': 'ಹಿಂದೆ', 'STEP 1 OF 2': 'ಹಂತ 1 / 2', 'NIVA will identify the relevant PF workflow': 'NIVA ಸಂಬಂಧಿತ PF ಕಾರ್ಯಹರಿವನ್ನು ಗುರುತಿಸುತ್ತದೆ', 'What happened?': 'ಏನಾಯಿತು?', 'Describe the issue in your own words': 'ಸಮಸ್ಯೆಯನ್ನು ನಿಮ್ಮ ಮಾತುಗಳಲ್ಲಿ ವಿವರಿಸಿ', 'Add a synthetic notice': 'ಕೃತಕ ಸೂಚನೆ ಸೇರಿಸಿ', 'Ready to analyse': 'ವಿಶ್ಲೇಷಣೆಗೆ ಸಿದ್ಧ', 'Text-based PDF · synthetic data only': 'ಪಠ್ಯ ಆಧಾರಿತ PDF · ಕೃತಕ ಡೇಟಾ ಮಾತ್ರ', 'Let NIVA analyse this': 'NIVA ಗೆ ಇದನ್ನು ವಿಶ್ಲೇಷಿಸಲು ಬಿಡಿ', 'Analyse my withdrawal request': 'ನನ್ನ ಹಿಂಪಡೆಯುವಿಕೆ ವಿನಂತಿಯನ್ನು ವಿಶ್ಲೇಷಿಸಿ', 'Analyse my transfer request': 'ನನ್ನ ವರ್ಗಾವಣೆ ವಿನಂತಿಯನ್ನು ವಿಶ್ಲೇಷಿಸಿ', 'Start over': 'ಮತ್ತೆ ಆರಂಭಿಸಿ', 'Try another demo': 'ಇನ್ನೊಂದು ಡೆಮೊ ಪ್ರಯತ್ನಿಸಿ',
    'ANALYSING SYNTHETIC DOCUMENT': 'ಕೃತಕ ದಾಖಲೆ ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ', 'ANALYSING SYNTHETIC INFORMATION': 'ಕೃತಕ ಮಾಹಿತಿ ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ', 'We’re checking the information you provided.': 'ನೀವು ನೀಡಿದ ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸುತ್ತಿದ್ದೇವೆ.',
    'ANALYSIS COMPLETE': 'ವಿಶ್ಲೇಷಣೆ ಪೂರ್ಣ', 'WHAT NIVA FOUND': 'NIVA ಕಂಡುಹಿಡಿದದ್ದು', 'WHAT HAPPENED?': 'ಏನಾಯಿತು?', 'WHAT DO I DO?': 'ನಾನು ಏನು ಮಾಡಬೇಕು?', 'OFFICIAL GUIDANCE': 'ಅಧಿಕೃತ ಮಾರ್ಗದರ್ಶನ', 'View official guidance': 'ಅಧಿಕೃತ ಮಾರ್ಗದರ್ಶನ ನೋಡಿ', 'YOUR JOURNEY': 'ನಿಮ್ಮ ಪಯಣ', 'YOU ARE HERE': 'ನೀವು ಇಲ್ಲಿದ್ದೀರಿ',
    'I understand my next step': 'ನನ್ನ ಮುಂದಿನ ಹಂತ ಅರ್ಥವಾಗಿದೆ', 'Back to analysis': 'ವಿಶ್ಲೇಷಣೆಗೆ ಹಿಂದಿರುಗಿ', 'YOUR RESOLUTION PLAN': 'ನಿಮ್ಮ ಪರಿಹಾರ ಯೋಜನೆ', 'NIVA RECOMMENDS': 'NIVA ಶಿಫಾರಸು', 'WHAT TO DO NEXT': 'ಮುಂದೆ ಏನು ಮಾಡಬೇಕು', 'YOUR ACTION PLAN': 'ನಿಮ್ಮ ಕಾರ್ಯ ಯೋಜನೆ', 'Analyze another issue': 'ಇನ್ನೊಂದು ಸಮಸ್ಯೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಿ',
    'How NIVA works': 'NIVA ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ', 'Go to NIVA home': 'NIVA ಮುಖಪುಟಕ್ಕೆ ಹೋಗಿ', 'Language': 'ಭಾಷೆ', 'Exploring a PF withdrawal request': 'PF ಹಿಂಪಡೆಯುವಿಕೆ ವಿನಂತಿಯನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ', 'Exploring a PF transfer request': 'PF ವರ್ಗಾವಣೆ ವಿನಂತಿಯನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ',
    'Tell NIVA what\nhappened.': 'NIVA ಗೆ ಏನಾಯಿತು ಎಂದು\nತಿಳಿಸಿ.', 'What needs\nattention?': 'ಯಾವುದಕ್ಕೆ\nಗಮನ ಬೇಕು?', 'Describe the issue or add a synthetic notice. NIVA will analyse the information, run a workflow check, and show the next practical step.': 'ಸಮಸ್ಯೆಯನ್ನು ವಿವರಿಸಿ ಅಥವಾ ಕೃತಕ ಸೂಚನೆಯನ್ನು ಸೇರಿಸಿ. NIVA ಮಾಹಿತಿಯನ್ನು ವಿಶ್ಲೇಷಿಸಿ, ಕಾರ್ಯಹರಿವು ಪರಿಶೀಲಿಸಿ ಮುಂದಿನ ಪ್ರಾಯೋಗಿಕ ಹಂತವನ್ನು ತೋರಿಸುತ್ತದೆ.', 'Select a demo situation below, then add any context in your own words. You can also add a synthetic PDF notice.': 'ಕೆಳಗೆ ಡೆಮೊ ಪರಿಸ್ಥಿತಿಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ, ನಂತರ ನಿಮ್ಮ ಮಾತುಗಳಲ್ಲಿ ಸಂದರ್ಭವನ್ನು ಸೇರಿಸಿ. ನೀವು ಕೃತಕ PDF ಸೂಚನೆಯನ್ನು ಕೂಡ ಸೇರಿಸಬಹುದು.', 'Optional — helps NIVA explain it clearly': 'ಐಚ್ಛಿಕ — ಇದನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ವಿವರಿಸಲು NIVA ಗೆ ಸಹಾಯ ಮಾಡುತ್ತದೆ',
    'Understand a blocked claim, verification issue, or the next step to submit.': 'ನಿರ್ಬಂಧಿತ ಕ್ಲೈಮ್, ಪರಿಶೀಲನೆ ಸಮಸ್ಯೆ ಅಥವಾ ಸಲ್ಲಿಸಲು ಮುಂದಿನ ಹಂತವನ್ನು ತಿಳಿಯಿರಿ.', 'Check previous-employment details and move your PF account with confidence.': 'ಹಿಂದಿನ ಉದ್ಯೋಗದ ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ನಿಮ್ಮ PF ಖಾತೆಯನ್ನು ವಿಶ್ವಾಸದಿಂದ ವರ್ಗಾಯಿಸಿ.', 'Please do not upload Aadhaar, PAN, UAN, bank details, OTPs, or any real personal data.': 'ದಯವಿಟ್ಟು ಆಧಾರ್, PAN, UAN, ಬ್ಯಾಂಕ್ ವಿವರಗಳು, OTP ಅಥವಾ ಯಾವುದೇ ನಿಜವಾದ ವೈಯಕ್ತಿಕ ಡೇಟಾವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಬೇಡಿ.', 'Remove file': 'ಫೈಲ್ ತೆಗೆದುಹಾಕಿ',
    'Understanding\nyour claim…': 'ನಿಮ್ಮ ಕ್ಲೈಮ್ ಅನ್ನು\nಅರ್ಥಮಾಡಿಕೊಳ್ಳಲಾಗುತ್ತಿದೆ…', 'Document received': 'ದಾಖಲೆ ಸ್ವೀಕರಿಸಲಾಗಿದೆ', 'Information analyzed': 'ಮಾಹಿತಿ ವಿಶ್ಲೇಷಿಸಲಾಗಿದೆ', 'NIVA checks the case': 'NIVA ಪ್ರಕರಣವನ್ನು ಪರಿಶೀಲಿಸುತ್ತದೆ', 'Problem identified': 'ಸಮಸ್ಯೆ ಗುರುತಿಸಲಾಗಿದೆ', 'Looking up official guidance': 'ಅಧಿಕೃತ ಮಾರ್ಗದರ್ಶನ ಹುಡುಕಲಾಗುತ್ತಿದೆ', 'Official guidance found': 'ಅಧಿಕೃತ ಮಾರ್ಗದರ್ಶನ ಕಂಡುಬಂದಿದೆ',
    'Retry': 'ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ', 'Return home': 'ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ', 'NIVA analysis path': 'NIVA ವಿಶ್ಲೇಷಣೆಯ ಮಾರ್ಗ', 'YOUR REQUEST IS CLEAR TO CONTINUE': 'ನಿಮ್ಮ ವಿನಂತಿ ಮುಂದುವರಿಯಲು ಸಿದ್ಧವಾಗಿದೆ', 'INFORMATION NIVA ANALYSED': 'NIVA ವಿಶ್ಲೇಷಿಸಿದ ಮಾಹಿತಿ', 'WHY NIVA REACHED THIS RESULT': 'NIVA ಈ ಫಲಿತಾಂಶಕ್ಕೆ ಏಕೆ ತಲುಪಿತು', 'NIVA decision': 'NIVA ನಿರ್ಧಾರ', 'Supporting information': 'ಪೋಷಕ ಮಾಹಿತಿ', 'SUPPORTING GUIDANCE': 'ಪೋಷಕ ಮಾರ್ಗದರ್ಶನ', 'No matching source in the local knowledge base for this issue.': 'ಈ ಸಮಸ್ಯೆಗೆ ಸ್ಥಳೀಯ ಜ್ಞಾನಕೋಶದಲ್ಲಿ ಹೊಂದಾಣಿಕೆಯ ಮೂಲವಿಲ್ಲ.', 'NIVA interprets the information → deterministic rules decide the outcome → official guidance supports the next step.': 'NIVA ಮಾಹಿತಿಯನ್ನು ಅರ್ಥೈಸುತ್ತದೆ → ನಿಗದಿತ ನಿಯಮಗಳು ಫಲಿತಾಂಶವನ್ನು ನಿರ್ಧರಿಸುತ್ತವೆ → ಅಧಿಕೃತ ಮಾರ್ಗದರ್ಶನ ಮುಂದಿನ ಹಂತಕ್ಕೆ ಬೆಂಬಲ ನೀಡುತ್ತದೆ.', 'Our local knowledge base does not contain sufficient source guidance for this issue.': 'ಈ ಸಮಸ್ಯೆಗೆ ನಮ್ಮ ಸ್ಥಳೀಯ ಜ್ಞಾನಕೋಶದಲ್ಲಿ ಸಾಕಷ್ಟು ಮೂಲ ಮಾರ್ಗದರ್ಶನವಿಲ್ಲ.', 'Claim type': 'ಕ್ಲೈಮ್ ಪ್ರಕಾರ', 'Issue mentioned': 'ಉಲ್ಲೇಖಿಸಿದ ಸಮಸ್ಯೆ', 'Information used': 'ಬಳಸಿದ ಮಾಹಿತಿ', 'Issue identified': 'ಗುರುತಿಸಿದ ಸಮಸ್ಯೆ',
    'NIVA found no blocking issue in the available information. The latest status on the official EPFO portal remains authoritative.': 'ಲಭ್ಯವಿರುವ ಮಾಹಿತಿಯಲ್ಲಿ NIVA ಗೆ ಯಾವುದೇ ತಡೆಯುವ ಸಮಸ್ಯೆ ಕಂಡುಬಂದಿಲ್ಲ. ಅಧಿಕೃತ EPFO ಪೋರ್ಟಲ್‌ನ ಇತ್ತೀಚಿನ ಸ್ಥಿತಿಯೇ ಮಾನ್ಯವಾಗಿರುತ್ತದೆ.', 'Official guidance remains available on the analysis screen when a relevant source is retrieved.': 'ಸಂಬಂಧಿತ ಮೂಲ ಸಿಕ್ಕಾಗ ಅಧಿಕೃತ ಮಾರ್ಗದರ್ಶನವು ವಿಶ್ಲೇಷಣೆ ಪರದೆಯಲ್ಲಿ ಲಭ್ಯವಿರುತ್ತದೆ.', 'View official EPFO guidance': 'ಅಧಿಕೃತ EPFO ಮಾರ್ಗದರ್ಶನ ನೋಡಿ', 'View official transfer guidance': 'ಅಧಿಕೃತ ವರ್ಗಾವಣೆ ಮಾರ್ಗದರ್ಶನ ನೋಡಿ',
    'KYC verification': 'KYC ಪರಿಶೀಲನೆ', 'Bank verification': 'ಬ್ಯಾಂಕ್ ಪರಿಶೀಲನೆ', 'Missing service info': 'ಸೇವಾ ಮಾಹಿತಿ ಕಾಣೆಯಾಗಿದೆ', 'Information conflict': 'ಮಾಹಿತಿ ಭಿನ್ನತೆ', 'No blocking issue': 'ತಡೆಯುವ ಸಮಸ್ಯೆ ಇಲ್ಲ', 'Missing previous-employment info': 'ಹಿಂದಿನ ಉದ್ಯೋಗದ ಮಾಹಿತಿ ಕಾಣೆಯಾಗಿದೆ', 'Transfer information mismatch': 'ವರ್ಗಾವಣೆ ಮಾಹಿತಿ ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ', 'Transfer ready to proceed': 'ವರ್ಗಾವಣೆ ಮುಂದುವರಿಯಲು ಸಿದ್ಧವಾಗಿದೆ',
    'Example: My PF claim was rejected because my bank details could not be verified.': 'ಉದಾಹರಣೆ: ನನ್ನ PF ಕ್ಲೈಮ್ ತಿರಸ್ಕರಿಸಲ್ಪಟ್ಟಿದೆ ಏಕೆಂದರೆ ನನ್ನ ಬ್ಯಾಂಕ್ ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.', 'Example: My previous employer service details are missing for my PF transfer.': 'ಉದಾಹರಣೆ: ನನ್ನ PF ವರ್ಗಾವಣೆಗಾಗಿ ಹಿಂದಿನ ಉದ್ಯೋಗದಾತರ ಸೇವಾ ವಿವರಗಳು ಕಾಣೆಯಾಗಿವೆ.', 'Example: My withdrawal claim was rejected because KYC is incomplete.': 'ಉದಾಹರಣೆ: KYC ಅಪೂರ್ಣವಾಗಿರುವುದರಿಂದ ನನ್ನ ಹಿಂಪಡೆಯುವಿಕೆ ಕ್ಲೈಮ್ ತಿರಸ್ಕರಿಸಲ್ಪಟ್ಟಿದೆ.', 'WITHDRAWAL REQUEST': 'ಹಿಂಪಡೆಯುವಿಕೆ ವಿನಂತಿ', 'TRANSFER REQUEST': 'ವರ್ಗಾವಣೆ ವಿನಂತಿ',
  },
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';

const issuesByClaimType: Record<ClaimType, [string, string][]> = {
  withdrawal: [
    ['kyc', 'KYC verification'],
    ['bank', 'Bank verification'],
    ['service', 'Missing service info'],
    ['conflict', 'Information conflict'],
    ['ready', 'No blocking issue'],
  ],
  transfer: [
    ['transfer_service', 'Missing previous-employment info'],
    ['transfer_conflict', 'Transfer information mismatch'],
    ['transfer_ready', 'Transfer ready to proceed'],
  ],
};

const local: Record<string, Omit<Analysis, 'timeline'>> = {
  kyc: {
    title: 'KYC verification needs attention',
    what_happened:
      'Your claim cannot move forward because required verification information is incomplete.',
    what_to_do: [
      'Review your KYC information, complete any missing verification, then return to continue your claim.',
    ],
    why: "NIVA's deterministic workflow check found that KYC verification is incomplete.",
    source: {
      title: 'EPFO Member e-Sewa',
      url: 'https://unifiedportal-mem.epfindia.gov.in/memberinterface/',
      section: 'KYC',
      excerpt:
        'KYC details should be completed and approved before a member continues their claim workflow.',
    },
  },

  bank: {
    title: 'Bank verification needs attention',
    what_happened:
      'Your claim is paused because the bank verification did not complete.',
    what_to_do: [
      'Review the bank details and verification status, correct what is needed, then continue your claim.',
    ],
    why: "NIVA's deterministic workflow check found a bank verification issue.",
    source: {
      title: 'EPFO Member e-Sewa',
      url: 'https://unifiedportal-mem.epfindia.gov.in/memberinterface/',
      section: 'Bank details',
      excerpt:
        'Review the bank details and their verification status in the member portal.',
    },
  },

  service: {
    title: 'Service information is missing',
    what_happened:
      'Your employment service information is incomplete, so the claim cannot be checked yet.',
    what_to_do: [
      'Ask your previous employer to review the missing service information, then return to your claim.',
    ],
    why: "NIVA's deterministic workflow check found missing service information.",
    source: null,
  },

  conflict: {
    title: 'Some information does not match',
    what_happened:
      'Your claim details and service record contain conflicting information.',
    what_to_do: [
      'Review the conflicting information with your employer and correct it before continuing.',
    ],
    why: "NIVA's deterministic workflow check found conflicting information.",
    source: null,
  },

  ready: {
    title: "You're ready to continue",
    what_happened:
      'We did not find a blocking issue in this synthetic case.',
    what_to_do: ['Continue to submit your claim and track its processing.'],
    why: "NIVA's deterministic workflow check found no blocking issue.",
    source: null,
  },
};

const defaultTimeline = (key: string): TimelineStep[] => {
  const labels = [
    'Understand claim',
    'Check eligibility',
    'Resolve KYC',
    'Verify bank',
    'Submit claim',
    'Track processing',
    'Payment',
  ];

  const currentIndex =
    key === 'kyc'
      ? 2
      : key === 'bank'
        ? 3
        : key === 'service'
          ? 1
          : key === 'conflict'
            ? 1
            : key === 'ready'
              ? 4
              : 2;

  return labels.map((label, index): TimelineStep => {
    let state: TimelineStep['state'];

    if (index < currentIndex) {
      state = 'complete';
    } else if (index === currentIndex) {
      state = 'current';
    } else {
      state = 'upcoming';
    }

    return {
      key: label,
      label,
      state,
    };
  });
};

function infer(text: string) {
  const t = text.toLowerCase();

  if (t.includes('transfer') || t.includes('previous employer') || t.includes('old employer')) {
    if (t.includes('mismatch') || t.includes('conflict') || t.includes('does not match')) {
      return 'transfer_conflict';
    }
    if (t.includes('ready') || t.includes('complete')) {
      return 'transfer_ready';
    }
    return 'transfer_service';
  }

  if (t.includes('bank')) {
    return 'bank';
  }

  if (t.includes('service') || t.includes('employment')) {
    return 'service';
  }

  if (t.includes('conflict') || t.includes('mismatch')) {
    return 'conflict';
  }

  if (t.includes('ready')) {
    return 'ready';
  }

  return 'kyc';
}

function titleFor(reasonCode?: string) {
  const titles: Record<string, string> = {
    KYC_INCOMPLETE: 'KYC verification needs attention',
    BANK_VERIFICATION_FAILED: 'Bank verification needs attention',
    SERVICE_INFORMATION_MISSING: 'Service information is missing',
    INFORMATION_CONFLICT: 'Information does not match',
    READY_TO_CONTINUE: 'Claim appears ready',
    TRANSFER_SERVICE_MISSING: 'Transfer service information is unavailable',
    TRANSFER_INFORMATION_CONFLICT: 'Transfer details do not match',
    TRANSFER_READY: 'Transfer appears ready',
  };

  return titles[reasonCode || ''] || 'PF request needs attention';
}

function resolutionPlan(analysis: Analysis): ResolutionPlan {
  const plans: Record<string, ResolutionPlan> = {
    KYC_INCOMPLETE: {
      title: 'Resolve your KYC issue',
      summary: 'NIVA found that KYC verification is the current blocker.',
      steps: ['Review which KYC information needs verification.', 'Complete or correct the required details through the appropriate EPFO process.', 'Return to NIVA and check the claim again.'],
      guidanceLabel: 'View official EPFO guidance',
    },
    BANK_VERIFICATION_FAILED: {
      title: 'Resolve bank verification',
      summary: 'NIVA found that bank verification needs attention before the claim can continue.',
      steps: ['Review the bank account details linked to the PF account.', 'Correct or update the details if required.', 'Verify the updated information before continuing with the claim.'],
      guidanceLabel: 'View official EPFO guidance',
    },
    SERVICE_INFORMATION_MISSING: {
      title: 'Resolve missing service information',
      summary: 'NIVA found that employment or service information is incomplete.',
      steps: ['Review employment and service details.', 'Identify the missing or incorrect information.', 'Complete the correction through the appropriate employer or EPFO process.', 'Return and analyze the claim again.'],
      guidanceLabel: 'View official EPFO guidance',
    },
    INFORMATION_CONFLICT: {
      title: 'Resolve the information mismatch',
      summary: 'NIVA found information that does not match the available records.',
      steps: ['Review the information that may not match.', 'Check personal, employment, and PF account details.', 'Correct the mismatch before continuing.', 'Return to NIVA and re-check the issue.'],
      guidanceLabel: 'View official EPFO guidance',
    },
    TRANSFER_SERVICE_MISSING: {
      title: 'Resolve missing transfer information',
      summary: 'NIVA found missing details related to previous employment.',
      steps: ['Review previous employment information.', 'Check the relevant previous and current PF account details.', 'Correct or complete missing information.', 'Re-check the transfer.'],
      guidanceLabel: 'View official transfer guidance',
    },
    TRANSFER_INFORMATION_CONFLICT: {
      title: 'Resolve the transfer information mismatch',
      summary: 'NIVA found a difference between previous and current employment records.',
      steps: ['Compare previous and current employment details.', 'Check PF account information for inconsistencies.', 'Correct the conflicting information before submitting the transfer again.'],
      guidanceLabel: 'View official transfer guidance',
    },
    TRANSFER_READY: {
      title: 'Your transfer appears ready to proceed',
      summary: 'NIVA found no blocking issue in the available transfer information.',
      steps: ['Review the transfer details once more.', 'Continue only with the latest status shown on the official EPFO portal.', 'Return to NIVA if a new issue appears.'],
      guidanceLabel: 'View official transfer guidance',
    },
    READY_TO_CONTINUE: {
      title: 'Your claim appears ready to continue',
      summary: 'NIVA found no blocking issue in the available claim information.',
      steps: ['Review the claim details once more.', 'Continue with the latest status shown on the official EPFO portal.', 'Return to NIVA if a new issue appears.'],
      guidanceLabel: 'View official EPFO guidance',
    },
  };

  return plans[analysis.reasonCode ?? ''] ?? {
    title: analysis.title,
    summary: analysis.what_happened,
    steps: analysis.what_to_do,
    guidanceLabel: 'View official guidance',
  };
}

function pipelineStages(hasDocument: boolean, hasGuidance: boolean, inFlight = false) {
  const stages = [
    ...(hasDocument ? [{ key: 'document', label: 'Document received' }] : []),
    { key: 'analyzed', label: 'Information analyzed' },
    { key: 'check', label: 'NIVA checks the case' },
    { key: 'problem', label: 'Problem identified' },
    ...(inFlight || hasGuidance
      ? [{ key: 'guidance', label: inFlight ? 'Looking up official guidance' : 'Official guidance found' }]
      : []),
    { key: 'plan', label: 'Resolution plan' },
  ];

  return stages;
}

function extractedFacts(extraction: Extraction | null) {
  if (!extraction) {
    return [];
  }

  const facts: [string, string][] = [];

  if (extraction.claim_type) {
    facts.push(['Claim type', extraction.claim_type]);
  }

  if (extraction.rejection_reason) {
    facts.push(['Issue mentioned', extraction.rejection_reason]);
  }

  if (extraction.mentioned_issue) {
    const text = extraction.mentioned_issue;
    facts.push([
      'Information used',
      text.length > 280 ? `${text.slice(0, 280)}…` : text,
    ]);
  }

  if (extraction.scenario_hint) {
    facts.push(['Issue identified', extraction.scenario_hint.replace(/_/g, ' ')]);
  }

  return facts;
}

async function readApiError(response: Response, fallback: string) {
  try {
    const body = await response.json();
    const message = body?.error?.message;

    if (typeof message === 'string' && message.trim()) {
      return message;
    }
  } catch {
    // Keep the fallback when the API does not return JSON.
  }

  return fallback;
}

function App() {
  const [screen, setScreen] = useState<
    'landing' | 'describe' | 'processing' | 'result' | 'resolution'
  >('landing');

  const [claimType, setClaimType] = useState<ClaimType>('withdrawal');
  const [journey, setJourney] = useState<Journey>('general');
  const [issue, setIssue] = useState('');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [extraction, setExtraction] = useState<Extraction | null>(null);
  const [usedDocument, setUsedDocument] = useState(false);
  const [error, setError] = useState('');
  const [locale, setLocale] = useState('EN');
  const t = (value: string) => translations[locale][value] ?? value;

  useEffect(() => {
    document.documentElement.lang = locale.toLowerCase();
  }, [locale]);

  const begin = (nextJourney: Journey) => {
    const isGeneral = nextJourney === 'general';
    const nextClaimType = isGeneral ? 'withdrawal' : nextJourney;

    setJourney(nextJourney);
    setClaimType(nextClaimType);
    setIssue(isGeneral ? '' : nextClaimType === 'transfer' ? 'transfer_service' : 'kyc');
    setDescription('');
    setFile(null);
    setExtraction(null);
    setUsedDocument(false);
    setError('');
    setScreen('describe');
  };

  async function analyze() {
    setError('');
    setScreen('processing');

    const scenario = issue || infer(description);
    const hadDocument = Boolean(file);
    setUsedDocument(hadDocument);
    setExtraction(null);

    try {
      const created = await fetch(`${API_BASE_URL}/cases`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          scenario,
          claim_type: claimType,
          language: locale.toLowerCase(),
        }),
      });

      if (!created.ok) {
        setError(await readApiError(created, 'Could not start this case. Please try again.'));
        setScreen('describe');
        return;
      }

      const { case_id } = await created.json();
      let documentExtraction: Extraction | null = null;

      if (file) {
        const form = new FormData();
        form.append('file', file);

        const upload = await fetch(
          `${API_BASE_URL}/cases/${case_id}/documents`,
          {
            method: 'POST',
            body: form,
          }
        );

        if (!upload.ok) {
          setError(await readApiError(upload, 'Could not read this synthetic notice. Try another PDF or describe the issue instead.'));
          setScreen('describe');
          return;
        }

        documentExtraction = await upload.json();
      }

      const res = await fetch(
        `${API_BASE_URL}/cases/${case_id}/analyze`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            description,
          }),
        }
      );

      if (!res.ok) {
        setError(await readApiError(res, 'Could not analyse this case. Please try again.'));
        setScreen('describe');
        return;
      }

      const body = await res.json();

      /*
       * Normalize source information from the backend.
       *
       * Depending on the API response schema, retrieved source metadata
       * may appear as:
       *   explanation.source
       *   explanation.source_references[0]
       *   body.source
       *   body.source_references[0]
       *
       * NIVA's frontend uses a single `source` field.
       */
      const explanation = body.explanation ?? {};

      const source: Source | null =
        explanation.source ??
        explanation.source_references?.[0] ??
        body.source ??
        body.source_references?.[0] ??
        null;

      setExtraction(documentExtraction ?? body.extraction ?? null);
      setAnalysis({
        ...explanation,
        title: explanation.title || titleFor(body.result?.reason_code),
        source,
        timeline: body.timeline ?? [],
        reasonCode: body.result?.reason_code,
      });
    } catch {
      const chosen = local[scenario] || local.kyc;

      setAnalysis({
        ...chosen,
        timeline: defaultTimeline(scenario),
      });

      setError(
        'The analysis service is unavailable. This result is a local synthetic preview only. You can retry when the service is running.'
      );
    }

    setTimeout(() => setScreen('result'), 650);
  }

  const back = () => {
    setScreen(screen === 'describe' ? 'landing' : 'describe');
  };

  const startOver = () => {
    setIssue(journey === 'general' ? '' : claimType === 'transfer' ? 'transfer_service' : 'kyc');
    setDescription('');
    setFile(null);
    setError('');
    setAnalysis(null);
    setExtraction(null);
    setUsedDocument(false);
    setScreen('describe');
  };

  const tryAnotherDemo = () => {
    setJourney('general');
    setClaimType('withdrawal');
    setIssue('');
    setDescription('');
    setFile(null);
    setError('');
    setAnalysis(null);
    setExtraction(null);
    setUsedDocument(false);
    setScreen('landing');
  };

  return (
    <main>
      <header>
        <button
          className="brand"
          onClick={() => setScreen('landing')}
          aria-label={t('Go to NIVA home')}
        >
          <span>N</span>
          <b>NIVA</b>
        </button>

        <div className="header-actions">
          <label className="text-button">
            <Globe2 size={17} />

            <select
              value={locale}
              onChange={(e) => setLocale(e.target.value)}
              aria-label={t('Language')}
            >
              <option value="EN">EN</option>
              <option value="HI">हिंदी</option>
              <option value="KN">ಕನ್ನಡ</option>
            </select>
          </label>

          <p className="demo" role="status">
            <span />
            {t('Demo mode')}
          </p>
        </div>
      </header>

      <div className="notice">
        <ShieldCheck size={15} />
        {t('Prototype — uses synthetic data. Not an official EPFO service.')}
      </div>

      {screen === 'landing' && (
        <section className="landing">
          <div className="landing-copy">
            <p className="eyebrow"><Sparkles size={14} /> NIVA</p>

          <h1>
            {t('Your PF journey,')}
            <br />
            <i>{t('explained.')}</i>
          </h1>

          <p className="lead">
            {t('Understand what went wrong, why it happened, and what to do next.')}
          </p>

          <ol className="product-pipeline" aria-label={t('How NIVA works')}>
            <li>{t('Your issue')}</li>
            <li>{t('Workflow check')}</li>
            <li>{t('Official guidance')}</li>
            <li>{t('Resolution plan')}</li>
          </ol>
          </div>

          <div className="journey-choices">
            <button className="niva-card" onClick={() => begin('general')}>
              <span className="journey-icon"><Sparkles size={22} /></span>
              <span className="journey-kicker">{t('NIVA ANALYSIS')}</span>
              <b>{t('Tell NIVA what happened')}</b>
              <small>{t('Describe your PF issue in your own words. NIVA will identify what may be blocking your journey and show the next practical step.')}</small>
              <span className="journey-cta">{t('Start with my issue')} <ArrowRight size={17} /></span>
            </button>

            <div className="guided-choices">
            <button className="journey-card withdrawal" onClick={() => begin('withdrawal')}>
              <span className="journey-icon"><WalletCards size={22} /></span>
              <span className="journey-kicker">{t('PF WITHDRAWAL')}</span>
              <b>{t('I want to withdraw my PF')}</b>
              <small>{t('Understand a blocked claim, verification issue, or the next step to submit.')}</small>
              <span className="journey-cta">{t('Explore withdrawal')} <ArrowRight size={17} /></span>
            </button>

            <button className="journey-card transfer" onClick={() => begin('transfer')}>
              <span className="journey-icon"><Landmark size={22} /></span>
              <span className="journey-kicker">{t('PF TRANSFER')}</span>
              <b>{t('I want to transfer my PF')}</b>
              <small>{t('Check previous-employment details and move your PF account with confidence.')}</small>
              <span className="journey-cta">{t('Explore transfer')} <ArrowRight size={17} /></span>
            </button>
            </div>
          </div>

          <p className="trust">
            <ShieldCheck size={16} />
            {t('Built for clarity. No real personal data needed.')}
          </p>
        </section>
      )}

      {screen === 'describe' && (
        <section className="flow">
          <button className="back" onClick={back}>
            <ChevronLeft size={18} />
            {t('Back')}
          </button>

          <p className="step">{t('STEP 1 OF 2')}</p>

          {journey === 'general' ? (
            <div className="workflow-badge general">
              <Sparkles size={18} />
              <span>{t('NIVA will identify the relevant PF workflow')}</span>
            </div>
          ) : (
            <div className={`workflow-badge ${claimType}`}>
              {claimType === 'withdrawal' ? <WalletCards size={18} /> : <Landmark size={18} />}
              <span>{t(`Exploring a PF ${claimType} request`)}</span>
            </div>
          )}

          <h1>
            {journey === 'general' ? <>{t('Tell NIVA what\nhappened.').split('\n').map((line, index) => <span key={line}>{index > 0 && <br />}{line}</span>)}</> : <>{t('What needs\nattention?').split('\n').map((line, index) => <span key={line}>{index > 0 && <br />}{line}</span>)}</>}
          </h1>

          <p className="sub">
            {journey === 'general'
              ? t('Describe the issue or add a synthetic notice. NIVA will analyse the information, run a workflow check, and show the next practical step.')
              : t('Select a demo situation below, then add any context in your own words. You can also add a synthetic PDF notice.')}
          </p>

          {error && (
            <p className="demo-error" role="alert">
              {error}
            </p>
          )}

          {journey !== 'general' && <div className="issues">
            {issuesByClaimType[claimType].map(([key, label]) => (
              <button
                key={key}
                className={issue === key ? 'selected' : ''}
                onClick={() => setIssue(key)}
              >
                <span className="radio" />
                {t(label)}
              </button>
            ))}
          </div>}

          <label htmlFor="description">
            {t('What happened?')} <em>{journey === 'general' ? t('Describe the issue in your own words') : t('Optional — helps NIVA explain it clearly')}</em>
          </label>

          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder={t(journey === 'general' ? 'Example: My PF claim was rejected because my bank details could not be verified.' : claimType === 'transfer' ? 'Example: My previous employer service details are missing for my PF transfer.' : 'Example: My withdrawal claim was rejected because KYC is incomplete.')}
            maxLength={3000}
          />

          <div className="upload">
            <input
              id="file"
              type="file"
              accept="application/pdf,.pdf"
              onChange={(e) => {
                setFile(e.target.files?.[0] || null);
              }}
            />

            <label htmlFor="file">
              <Upload size={19} />

              <span>
                {file ? file.name : t('Add a synthetic notice')}

                <small>
                  {file
                  ? t('Ready to analyse')
                    : t('Text-based PDF · synthetic data only')}
                </small>
              </span>
            </label>

            {file && (
              <button
                onClick={() => setFile(null)}
                aria-label={t('Remove file')}
              >
                <X size={17} />
              </button>
            )}
          </div>

          <button className="primary continue" onClick={analyze}>
            {journey === 'general' ? t('Let NIVA analyse this') : t(claimType === 'transfer' ? 'Analyse my transfer request' : 'Analyse my withdrawal request')}
            <Send size={17} />
          </button>

          <p className="privacy">
            {t('Please do not upload Aadhaar, PAN, UAN, bank details, OTPs, or any real personal data.')}
          </p>
        </section>
      )}

      {screen === 'processing' && (
        <section className="processing" aria-live="polite">
          <div className="pulse">
            <FileText size={32} />
          </div>

          <p className="eyebrow">
            {t(usedDocument ? 'ANALYSING SYNTHETIC DOCUMENT' : 'ANALYSING SYNTHETIC INFORMATION')}
          </p>

          <h1>
            {t('Understanding\nyour claim…').split('\n').map((line, index) => <span key={line}>{index > 0 && <br />}{line}</span>)}
          </h1>

          <p>{t('We’re checking the information you provided.')}</p>

          <ol className="process-stages">
            {pipelineStages(usedDocument, true, true).map((stage) => (
              <li key={stage.key}>{t(stage.label)}</li>
            ))}
          </ol>

          <div className="processing-line">
            <span />
          </div>
        </section>
      )}

      {screen === 'result' && analysis && (
        <section className="result">
          <button className="back" onClick={startOver}>
            <ChevronLeft size={18} />
            {t('Start over')}
          </button>

          {error && (
            <div className="demo-error" role="alert">
              <p>{error}</p>
              <div className="error-actions">
                <button type="button" onClick={() => setScreen('describe')}>{t('Retry')}</button>
                <button type="button" onClick={tryAnotherDemo}>{t('Return home')}</button>
              </div>
            </div>
          )}

          <p className="eyebrow">{t('ANALYSIS COMPLETE')}{journey === 'general' ? '' : ` · ${t(claimType === 'transfer' ? 'TRANSFER REQUEST' : 'WITHDRAWAL REQUEST')}`}</p>

          <ol className="result-pipeline" aria-label={t('NIVA analysis path')}>
            {pipelineStages(usedDocument, Boolean(analysis.source)).map((stage) => (
              <li key={stage.key}>{t(stage.label)}</li>
            ))}
          </ol>

          <div className="result-head">
            <div className="success-mark">
              <Check size={24} />
            </div>

            <div>
              <span>{analysis.reasonCode?.includes('READY') ? t('YOUR REQUEST IS CLEAR TO CONTINUE') : t('WHAT NIVA FOUND')}</span>
              <h1>{analysis.title}</h1>
            </div>
          </div>

          <article>
            <p className="article-label">{t('WHAT HAPPENED?')}</p>
            <p>{analysis.what_happened}</p>
          </article>

          {extractedFacts(extraction).length > 0 && (
            <article className="extracted">
              <p className="article-label">{t('INFORMATION NIVA ANALYSED')}</p>
              <dl>
                {extractedFacts(extraction).map(([label, value]) => (
                  <div key={label}>
                    <dt>{t(label)}</dt>
                    <dd>{value}</dd>
                  </div>
                ))}
              </dl>
            </article>
          )}

          <article className="explain">
            <p className="article-label">{t('WHY NIVA REACHED THIS RESULT')}</p>

            <div className="explain-grid">
              <div>
                <span>{t('NIVA decision')}</span>
                <strong>{analysis.reasonCode || 'WORKFLOW CHECK'}</strong>
              </div>
              <div>
                <span>{t('What NIVA found')}</span>
                <p>{analysis.why}</p>
              </div>
              <div>
                <span>{t('Supporting information')}</span>
                <p>
                  {analysis.source
                    ? analysis.source.title
                    : t('No matching source in the local knowledge base for this issue.')}
                </p>
              </div>
            </div>

            <p className="explain-path">
              {t('NIVA interprets the information → deterministic rules decide the outcome → official guidance supports the next step.')}
            </p>
          </article>

          <article className="action">
            <p className="article-label">{t('WHAT DO I DO?')}</p>
            <ol>
              {analysis.what_to_do.map((action) => <li key={action}>{action}</li>)}
            </ol>

            <button className="action-button" onClick={() => setScreen('resolution')}>
              {t('I understand my next step')}
              <ArrowRight size={18} />
            </button>
          </article>

          <article>
            <p className="article-label">{t('OFFICIAL GUIDANCE')}</p>

            {analysis.source ? (
              <div className="source-card">
                <div className="source-card-header">
                  <div>
                    <p className="source-label">{t('SUPPORTING GUIDANCE')}</p>

                    <h3>{analysis.source.title}</h3>

                    <span className="source-section">
                      {analysis.source.section}
                    </span>
                  </div>
                </div>

                {analysis.source.excerpt && (
                  <p className="source-excerpt">
                    {analysis.source.excerpt}
                  </p>
                )}

                <a
                  href={analysis.source.url}
                  target="_blank"
                  rel="noreferrer"
                >
                  {t('View official guidance')}
                  <ArrowRight size={14} />
                </a>
              </div>
            ) : (
              <small>
                {t('Our local knowledge base does not contain sufficient source guidance for this issue.')}
              </small>
            )}
          </article>

          <div className="journey">
            <p className="article-label">{t('YOUR JOURNEY')}</p>

            {analysis.timeline.map((step) => (
              <div
                className={`timeline ${step.state}`}
                key={step.key}
              >
                <span>
                  {step.state === 'complete' ? (
                    <Check size={14} />
                  ) : step.state === 'current' ? (
                    '•'
                  ) : (
                    '○'
                  )}
                </span>

                <b>{step.label}</b>

                {step.state === 'current' && (
                  <em>{t('YOU ARE HERE')}</em>
                )}
              </div>
            ))}
          </div>

          <button
            className="outline"
            onClick={tryAnotherDemo}
          >
            <RotateCcw size={17} />
            {t('Try another demo')}
          </button>
        </section>
      )}

      {screen === 'resolution' && analysis && (() => {
        const plan = resolutionPlan(analysis);

        return (
          <section className="resolution">
            <button className="back" onClick={() => setScreen('result')}>
              <ChevronLeft size={18} />
              {t('Back to analysis')}
            </button>

            <p className="eyebrow">{t('YOUR RESOLUTION PLAN')}</p>

            <div className="resolution-head">
              <div className="success-mark"><Check size={24} /></div>
              <div>
                <span>{t('NIVA RECOMMENDS')}</span>
                <h1>{plan.title}</h1>
              </div>
            </div>

            <article>
              <p className="article-label">{t('WHAT TO DO NEXT')}</p>
              <p>{plan.summary}</p>
              {(analysis.reasonCode === 'TRANSFER_READY' || analysis.reasonCode === 'READY_TO_CONTINUE') && (
                <p className="resolution-authority">
                  {t('NIVA found no blocking issue in the available information. The latest status on the official EPFO portal remains authoritative.')}
                </p>
              )}
            </article>

            <article className="resolution-steps">
              <p className="article-label">{t('YOUR ACTION PLAN')}</p>
              <ol>
                {plan.steps.map((step) => <li key={step}>{step}</li>)}
              </ol>
            </article>

            {analysis.source ? (
              <a className="primary resolution-guidance" href={analysis.source.url} target="_blank" rel="noreferrer">
                {t(plan.guidanceLabel)}
                <ArrowRight size={18} />
              </a>
            ) : (
              <p className="resolution-note">{t('Official guidance remains available on the analysis screen when a relevant source is retrieved.')}</p>
            )}

            <button className="outline" onClick={tryAnotherDemo}>
              <RotateCcw size={17} />
              {t('Analyze another issue')}
            </button>
          </section>
        );
      })()}
    </main>
  );
}

createRoot(document.getElementById('root')!).render(<App />);
