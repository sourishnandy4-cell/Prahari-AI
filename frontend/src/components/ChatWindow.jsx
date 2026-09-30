import React, { useState, useRef, useEffect } from 'react';
import { 
  Brain, 
  Trash2, 
  Sparkles, 
  Radio, 
  ArrowUp, 
  Plus, 
  Paperclip, 
  Image as ImageIcon, 
  FileText, 
  X, 
  Mic, 
  MicOff, 
  PanelLeft, 
  Flame, 
  Wrench, 
  FileCheck,
  ChevronRight,
  Upload,
  Building2,
  Users,
  Languages,
  ShieldCheck,
  Scale,
  Award,
  HelpCircle,
  PhoneCall,
  Zap,
  Globe
} from 'lucide-react';
import MessageItem from './MessageItem';
import LottieLoader from './LottieLoader';
import NeuralBrainHero3D from './NeuralBrainHero3D';

// ── PROMPT CARDS (INDUSTRY vs CONSUMER / EN vs HI) ───────────────────────────
const INDUSTRY_CARDS_EN = [
  {
    icon: Building2,
    title: "Which IS Standard Applies?",
    desc: "Which Indian Standard and QCO order applies to manufacturing TMT steel rebars (Fe 500D)?",
    category: "Product Standard Finder",
    color: "text-amber-400 bg-amber-500/10 border-amber-500/20"
  },
  {
    icon: Wrench,
    title: "Mandatory Testing Requirements",
    desc: "What testing is needed and what in-house lab equipment is required for packaged drinking water (IS 14543)?",
    category: "Conformity & Lab Testing",
    color: "text-cyan-400 bg-cyan-500/10 border-cyan-500/20"
  },
  {
    icon: FileCheck,
    title: "Step-by-Step BIS Licence Guide",
    desc: "Provide the complete step-by-step procedure and document checklist to get a BIS licence on MANAK Online.",
    category: "Scheme-I Licensing",
    color: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20"
  },
  {
    icon: Scale,
    title: "Standards Comparison (IS X vs IS Y)",
    desc: "What is the difference between municipal drinking water IS 10500 and packaged water IS 14543?",
    category: "Standards Comparison",
    color: "text-purple-400 bg-purple-500/10 border-purple-500/20"
  },
  {
    icon: ShieldCheck,
    title: "Domestic Plugs & Sockets (IS 1293)",
    desc: "What are the safety shutter, insulation resistance, and 5000-cycle endurance rules under IS 1293:2019?",
    category: "Electrical Accessories QCO",
    color: "text-sky-400 bg-sky-500/10 border-sky-500/20"
  },
  {
    icon: Flame,
    title: "MRPL Refinery Safety SOP",
    desc: "What is the emergency shutdown procedure for the Crude Distillation Unit (CDU-3)?",
    category: "Operational Safety SOP",
    color: "text-rose-400 bg-rose-500/10 border-rose-500/20"
  }
];

const INDUSTRY_CARDS_HI = [
  {
    icon: Building2,
    title: "लागू भारतीय मानक (IS कोड)",
    desc: "टीएमटी सरिया (Fe 500D) के निर्माण पर कौन सा भारतीय मानक और क्यूसीओ आदेश लागू होता है?",
    category: "मानक खोजकर्ता (Standard Finder)",
    color: "text-amber-400 bg-amber-500/10 border-amber-500/20"
  },
  {
    icon: Wrench,
    title: "अनिवार्य प्रयोगशाला परीक्षण",
    desc: "पैकेज्ड पेयजल (IS 14543) के लिए कौन-कौन से रासायनिक एवं सूक्ष्मजैविक परीक्षण आवश्यक हैं?",
    category: "लैब एवं गुणवत्ता परीक्षण",
    color: "text-cyan-400 bg-cyan-500/10 border-cyan-500/20"
  },
  {
    icon: FileCheck,
    title: "बीआईएस लाइसेंस आवेदन प्रक्रिया",
    desc: "मानक ऑनलाइन पर बीआईएस आईएसआई लाइसेंस प्राप्त करने की चरण-दर-चरण प्रक्रिया और आवश्यक दस्तावेज बताएं।",
    category: "स्कीम-I लाइसेंसिंग",
    color: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20"
  },
  {
    icon: Scale,
    title: "मानकों की तुलना (IS X बनाम IS Y)",
    desc: "सामान्य पेयजल IS 10500 और पैकेज्ड पेयजल IS 14543 के बीच क्या मुख्य अंतर हैं?",
    category: "मानक तुलना (Comparison)",
    color: "text-purple-400 bg-purple-500/10 border-purple-500/20"
  },
  {
    icon: ShieldCheck,
    title: "प्लग और सॉकेट सुरक्षा (IS 1293)",
    desc: "घरेलू प्लग और सॉकेट के लिए शटर सुरक्षा और 5000 साइकिल इन्सर्शन परीक्षण के नियम क्या हैं?",
    category: "इलेक्ट्रिकल सुरक्षा मानक",
    color: "text-sky-400 bg-sky-500/10 border-sky-500/20"
  },
  {
    icon: Flame,
    title: "रिफाइनरी सुरक्षा एसओपी (MRPL)",
    desc: "क्रूड डिस्टिलेशन यूनिट (CDU-3) के लिए आपातकालीन शटडाउन प्रक्रिया क्या है?",
    category: "ऑपरेशनल सेफ्टी एसओपी",
    color: "text-rose-400 bg-rose-500/10 border-rose-500/20"
  }
];

const CONSUMER_CARDS_EN = [
  {
    icon: Award,
    title: "Verify Gold Hallmark (6-Digit HUID)",
    desc: "How do I check and verify the 6-digit HUID hallmark on gold jewellery via the BIS Care App?",
    category: "Gold Hallmark Verification",
    color: "text-amber-400 bg-amber-500/10 border-amber-500/20"
  },
  {
    icon: ShieldCheck,
    title: "Verify Authentic ISI Mark & CML",
    desc: "How can a consumer verify if an ISI mark and 7-digit CML number on a product are authentic?",
    category: "ISI Mark Authenticity",
    color: "text-cyan-400 bg-cyan-500/10 border-cyan-500/20"
  },
  {
    icon: Scale,
    title: "File a Consumer Complaint",
    desc: "How do I file an official complaint against substandard goods or fake ISI marks with BIS?",
    category: "Consumer Grievance Redressal",
    color: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20"
  },
  {
    icon: ShieldCheck,
    title: "Two-Wheeler Helmets (IS 4151)",
    desc: "Is an ISI mark mandatory for two-wheeler helmets, and what happens if a retailer sells non-ISI helmets?",
    category: "Road & Personal Safety",
    color: "text-rose-400 bg-rose-500/10 border-rose-500/20"
  },
  {
    icon: Users,
    title: "Toy Safety & Choking Hazards (IS 9873)",
    desc: "What are the mandatory child safety rules and heavy metal limits for toys in India?",
    category: "Child Safety Standards",
    color: "text-purple-400 bg-purple-500/10 border-purple-500/20"
  },
  {
    icon: PhoneCall,
    title: "BIS Toll-Free Helpline & Rights",
    desc: "What is the official BIS consumer helpline, and what compensation can I claim if gold purity fails?",
    category: "Helpline & Consumer Rights",
    color: "text-sky-400 bg-sky-500/10 border-sky-500/20"
  }
];

const CONSUMER_CARDS_HI = [
  {
    icon: Award,
    title: "सोने का हॉलमार्क (6-अंकीय HUID) जांचें",
    desc: "सोने के गहनों पर 6-अंकीय HUID कोड की जांच 'BIS Care App' पर कैसे करें?",
    category: "हॉलमार्क सत्यापन (Hallmark Check)",
    color: "text-amber-400 bg-amber-500/10 border-amber-500/20"
  },
  {
    icon: ShieldCheck,
    title: "असली आईएसआई (ISI) मार्क की पहचान",
    desc: "किसी उत्पाद पर मुद्रित आईएसआई मार्क और 7-अंकीय CML लाइसेंस नंबर असली है या नकली कैसे जांचें?",
    category: "आईएसआई मार्क जांच",
    color: "text-cyan-400 bg-cyan-500/10 border-cyan-500/20"
  },
  {
    icon: Scale,
    title: "घटिया उत्पाद या नकली ISI की शिकायत",
    desc: "घटिया गुणवत्ता वाले उत्पाद या नकली आईएसआई मार्क के खिलाफ बीआईएस में शिकायत कैसे दर्ज करें?",
    category: "उपभोक्ता शिकायत निवारण",
    color: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20"
  },
  {
    icon: ShieldCheck,
    title: "हेलमेट सुरक्षा नियम (IS 4151)",
    desc: "क्या दोपहिया हेलमेट पर आईएसआई मार्क अनिवार्य है और बिना आईएसआई हेलमेट बेचने पर क्या सजा है?",
    category: "सड़क सुरक्षा मानक",
    color: "text-rose-400 bg-rose-500/10 border-rose-500/20"
  },
  {
    icon: Users,
    title: "खिलौनों की सुरक्षा (IS 9873)",
    desc: "भारत में बच्चों के खिलौनों के लिए लेड, कैडमियम और चोकिंग हैज़र्ड की अनिवार्य सीमाएं क्या हैं?",
    category: "बाल सुरक्षा मानक",
    color: "text-purple-400 bg-purple-500/10 border-purple-500/20"
  },
  {
    icon: PhoneCall,
    title: "बीआईएस हेल्पलाइन एवं मुआवज़ा अधिकार",
    desc: "बीआईएस की टोल-फ्री हेल्पलाइन क्या है और हॉलमार्क शुद्धता फेल होने पर जौहरी से क्या मुआवज़ा मिलता है?",
    category: "हेल्पलाइन एवं उपभोक्ता अधिकार",
    color: "text-sky-400 bg-sky-500/10 border-sky-500/20"
  }
];

export default function ChatWindow({ 
  messages, 
  onSendMessage, 
  loading, 
  isStreaming, 
  onClearChat, 
  selectedQuery, 
  sessionId,
  isSidebarOpen,
  isMobile = false,
  onToggleSidebar,
  onNewChat,
  currentModel,
  onOpenModelModal
}) {
  const [inputQuery, setInputQuery] = useState('');
  const [useStream, setUseStream] = useState(true);
  const [attachments, setAttachments] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  // Dual Entry Points: 'industry' | 'consumer'
  const [entryPoint, setEntryPoint] = useState('industry');
  // Bilingual Language: 'en' | 'hi'
  const [language, setLanguage] = useState('en');

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const fileInputRef = useRef(null);
  const recognitionRef = useRef(null);

  useEffect(() => {
    if (selectedQuery) {
      setInputQuery(selectedQuery);
      inputRef.current?.focus();
    }
  }, [selectedQuery]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Voice Input via Web Speech API (supports English and Hindi)
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = language === 'hi' ? 'hi-IN' : 'en-IN';

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputQuery((prev) => (prev ? `${prev} ${transcript}` : transcript));
        setIsRecording(false);
      };

      recognition.onerror = () => {
        setIsRecording(false);
      };

      recognition.onend = () => {
        setIsRecording(false);
      };

      recognitionRef.current = recognition;
    }
  }, [language]);

  const toggleVoiceInput = () => {
    if (!recognitionRef.current) {
      alert('Speech Recognition is not supported in this browser. Please use Chrome or Edge.');
      return;
    }

    if (isRecording) {
      recognitionRef.current.stop();
      setIsRecording(false);
    } else {
      try {
        recognitionRef.current.lang = language === 'hi' ? 'hi-IN' : 'en-IN';
        recognitionRef.current.start();
        setIsRecording(true);
      } catch (err) {
        setIsRecording(false);
      }
    }
  };

  const processFiles = (fileList) => {
    const files = Array.from(fileList || []);
    if (!files.length) return;

    files.forEach((file) => {
      const isImg = file.type.startsWith('image/');
      const isText = file.type.startsWith('text/') || /\.(txt|md|csv|json|py|js|html|css|xml|yaml|yml|log)$/i.test(file.name);

      if (isImg) {
        const reader = new FileReader();
        reader.onload = (event) => {
          setAttachments((prev) => [
            ...prev,
            {
              id: Date.now() + Math.random().toString(),
              file,
              name: file.name,
              size: file.size,
              type: file.type,
              previewUrl: event.target.result,
              data: event.target.result,
            },
          ]);
        };
        reader.readAsDataURL(file);
      } else if (isText) {
        const reader = new FileReader();
        reader.onload = (event) => {
          setAttachments((prev) => [
            ...prev,
            {
              id: Date.now() + Math.random().toString(),
              file,
              name: file.name,
              size: file.size,
              type: file.type,
              previewUrl: null,
              data: event.target.result,
            },
          ]);
        };
        reader.readAsText(file);
      } else {
        // Binary files (PDF, DOCX, etc.)
        setAttachments((prev) => [
          ...prev,
          {
            id: Date.now() + Math.random().toString(),
            file,
            name: file.name,
            size: file.size,
            type: file.type || 'application/octet-stream',
            previewUrl: null,
            data: null,
          },
        ]);
      }
    });
  };

  const handleFileChange = (e) => {
    processFiles(e.target.files);
    e.target.value = '';
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files) {
      processFiles(e.dataTransfer.files);
    }
  };

  const handlePaste = (e) => {
    if (e.clipboardData.files && e.clipboardData.files.length > 0) {
      processFiles(e.clipboardData.files);
    }
  };

  const removeAttachment = (id) => {
    setAttachments((prev) => prev.filter((a) => a.id !== id));
  };

  const handleSubmit = (e) => {
    e?.preventDefault();
    if ((!inputQuery.trim() && attachments.length === 0) || loading) return;

    onSendMessage(inputQuery, useStream, attachments);
    setInputQuery('');
    setAttachments([]);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const isActive = loading || isStreaming;

  // Active prompt cards based on Entry Point and Language
  const activePromptCards = entryPoint === 'industry'
    ? (language === 'hi' ? INDUSTRY_CARDS_HI : INDUSTRY_CARDS_EN)
    : (language === 'hi' ? CONSUMER_CARDS_HI : CONSUMER_CARDS_EN);

  return (
    <main 
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className="flex-1 h-screen flex flex-col justify-between bg-zinc-950 text-zinc-100 relative overflow-hidden select-none"
    >
      
      {/* ── TOP HEADER (Dual Entry Points & Bilingual Toggle) ───────────────── */}
      <header className="h-16 bg-zinc-950/90 backdrop-blur-md border-b border-zinc-800/80 px-4 md:px-6 flex items-center justify-between z-10 shrink-0 gap-2">
        <div className="flex items-center gap-3">
          {(isMobile || !isSidebarOpen) && (
            <button
              onClick={onToggleSidebar}
              className="p-2 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors cursor-pointer touch-target"
              title="Open sidebar"
            >
              <PanelLeft className="w-5 h-5" />
            </button>
          )}

          {/* Dual Entry Points Switcher (Industry vs Consumer) */}
          <div className="flex items-center p-1 rounded-xl bg-zinc-900 border border-zinc-800 text-xs font-semibold shadow-inner">
            <button
              type="button"
              onClick={() => setEntryPoint('industry')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
                entryPoint === 'industry'
                  ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40 shadow-sm'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <Building2 className="w-3.5 h-3.5 text-amber-400" />
              <span>{language === 'hi' ? '🏭 उद्योग पोर्टल' : '🏭 Industry Portal'}</span>
            </button>

            <button
              type="button"
              onClick={() => setEntryPoint('consumer')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
                entryPoint === 'consumer'
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <Users className="w-3.5 h-3.5 text-cyan-400" />
              <span>{language === 'hi' ? '👥 उपभोक्ता पोर्टल' : '👥 Consumer Portal'}</span>
            </button>
          </div>
        </div>

        {/* Right Controls: Model Switcher, Language Selector, Streaming Toggle, New Chat, Clear */}
        <div className="flex items-center gap-2">
          {/* Active Model Selector Button */}
          <button
            type="button"
            onClick={onOpenModelModal}
            className="flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 border border-zinc-700/80 text-zinc-200 font-medium transition-all cursor-pointer shadow-sm hover:border-cyan-500/80 group"
            title="Change AI Model or configure free Google Gemini Token"
          >
            {currentModel?.startsWith('gemini') ? (
              <>
                <Zap className="w-3.5 h-3.5 text-cyan-400 group-hover:scale-110 transition-transform shrink-0" />
                <span className="font-semibold text-cyan-300 hidden sm:inline">
                  {currentModel.includes('pro') ? 'Gemini 1.5 Pro' : 'Gemini Flash'}
                </span>
                <span className="font-semibold text-cyan-300 sm:hidden">Gemini</span>
              </>
            ) : currentModel === 'llama3.2-offline' ? (
              <>
                <ShieldCheck className="w-3.5 h-3.5 text-amber-400 group-hover:scale-110 transition-transform shrink-0" />
                <span className="font-semibold text-amber-300 hidden sm:inline">Offline LLaMA</span>
                <span className="font-semibold text-amber-300 sm:hidden">Offline</span>
              </>
            ) : (
              <>
                <Globe className="w-3.5 h-3.5 text-emerald-400 group-hover:scale-110 transition-transform shrink-0" />
                <span className="font-semibold text-emerald-300 hidden sm:inline">LLaMA + Web</span>
                <span className="font-semibold text-emerald-300 sm:hidden">LLaMA</span>
              </>
            )}
            <span className="text-[9px] text-zinc-500 group-hover:text-zinc-300 ml-0.5">▼</span>
          </button>

          {/* Bilingual English / Hindi Toggle */}
          <button
            type="button"
            onClick={() => setLanguage(l => l === 'en' ? 'hi' : 'en')}
            className="flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 border border-zinc-700/80 text-zinc-200 font-semibold transition-all cursor-pointer shadow-sm hover:border-cyan-500"
            title="Toggle Language (English / हिन्दी)"
          >
            <Languages className="w-3.5 h-3.5 text-cyan-400" />
            <span className="font-mono">{language === 'en' ? 'EN' : 'हिन्दी'}</span>
          </button>

          {/* Streaming toggle */}
          <button
            onClick={() => setUseStream(!useStream)}
            title={useStream ? 'Streaming tokens active' : 'Batch mode active'}
            className={`hidden sm:flex items-center gap-1 text-xs px-2.5 py-1.5 rounded-xl border transition-all cursor-pointer ${
              useStream
                ? 'bg-zinc-100 text-zinc-950 border-zinc-100 font-semibold shadow-sm'
                : 'bg-zinc-900 border-zinc-800 text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <Radio className="w-3 h-3" />
            <span>{useStream ? 'Stream' : 'Batch'}</span>
          </button>

          {/* New Chat Quick Button */}
          <button
            onClick={onNewChat}
            className="flex items-center gap-1 text-xs px-2.5 py-1.5 rounded-xl text-zinc-300 hover:text-white hover:bg-zinc-900 border border-zinc-800/80 transition-all cursor-pointer"
            title="Start fresh conversation"
          >
            <Plus className="w-3.5 h-3.5" />
            <span className="hidden md:inline">{language === 'hi' ? 'नया चैट' : 'New'}</span>
          </button>

          {/* Clear messages */}
          <button
            onClick={onClearChat}
            className="p-1.5 rounded-xl text-zinc-400 hover:text-white hover:bg-zinc-900 transition-colors cursor-pointer"
            title="Clear Chat History"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </header>

      {/* ── QUICK ACTION CHIPS TRAY (Industry & Consumer Shortcuts) ─────────── */}
      <div className="bg-zinc-950/60 border-b border-zinc-900 px-4 md:px-8 py-2 overflow-x-auto flex items-center gap-2 text-xs no-scrollbar shrink-0 z-10">
        <span className="text-[10px] uppercase font-mono tracking-wider text-zinc-500 font-semibold shrink-0">
          {language === 'hi' ? 'त्वरित प्रश्न:' : 'Quick Actions:'}
        </span>

        {entryPoint === 'industry' ? (
          <>
            <button
              onClick={() => onSendMessage(language === 'hi' ? "टीएमटी सरिया (Fe 500D) के लिए कौन सा IS मानक और परीक्षण आवश्यक है?" : "Which IS standard applies to TMT steel rebars (Fe 500D) and what testing is needed?", useStream, [])}
              className="px-2.5 py-1 rounded-full bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 shrink-0 cursor-pointer transition-colors"
            >
              🏷️ {language === 'hi' ? 'लागू IS कोड खोजें' : 'Which IS applies?'}
            </button>
            <button
              onClick={() => onSendMessage(language === 'hi' ? "पैकेज्ड पेयजल IS 14543 के लिए कौन से परीक्षण आवश्यक हैं?" : "What testing is needed for Packaged Drinking Water under IS 14543:2004?", useStream, [])}
              className="px-2.5 py-1 rounded-full bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 shrink-0 cursor-pointer transition-colors"
            >
              🧪 {language === 'hi' ? 'आवश्यक लैब परीक्षण' : 'What testing is needed?'}
            </button>
            <button
              onClick={() => onSendMessage(language === 'hi' ? "मानक ऑनलाइन पर बीआईएस लाइसेंस प्राप्त करने की चरण-दर-चरण प्रक्रिया और आवश्यक दस्तावेज बताएं।" : "Provide the step-by-step procedure and document checklist to get an ISI licence on MANAK Online.", useStream, [])}
              className="px-2.5 py-1 rounded-full bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 shrink-0 cursor-pointer transition-colors"
            >
              📜 {language === 'hi' ? 'लाइसेंस प्रक्रिया और दस्तावेज' : 'Step-by-step Licence Guide'}
            </button>
            <button
              onClick={() => onSendMessage(language === 'hi' ? "IS 10500 और IS 14543 में क्या अंतर है?" : "What is the difference between IS 10500 and IS 14543?", useStream, [])}
              className="px-2.5 py-1 rounded-full bg-purple-500/10 hover:bg-purple-500/20 text-purple-300 border border-purple-500/30 shrink-0 cursor-pointer transition-colors"
            >
              ⚖️ {language === 'hi' ? 'मानकों की तुलना (Compare)' : 'Compare IS 10500 vs 14543'}
            </button>
            <button
              onClick={() => onSendMessage(language === 'hi' ? "घरेलू प्लग और सॉकेट के लिए IS 1293:2019 के क्या नियम हैं?" : "What are the rules and tests for domestic plugs and sockets under IS 1293:2019?", useStream, [])}
              className="px-2.5 py-1 rounded-full bg-sky-500/10 hover:bg-sky-500/20 text-sky-300 border border-sky-500/30 shrink-0 cursor-pointer transition-colors"
            >
              🔌 {language === 'hi' ? 'प्लग एवं सॉकेट (IS 1293)' : 'Plugs & Sockets (IS 1293)'}
            </button>
          </>
        ) : (
          <>
            <button
              onClick={() => onSendMessage(language === 'hi' ? "सोने के गहनों पर 6-अंकीय HUID हॉलमार्क की जांच कैसे करें?" : "How do I check and verify the 6-digit HUID hallmark on gold jewellery via the BIS Care App?", useStream, [])}
              className="px-2.5 py-1 rounded-full bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 shrink-0 cursor-pointer transition-colors"
            >
              💎 {language === 'hi' ? 'सोना हॉलमार्क (HUID) जांचें' : 'Verify Gold Hallmark (HUID)'}
            </button>
            <button
              onClick={() => onSendMessage(language === 'hi' ? "असली आईएसआई मार्क और 7-अंकीय CML नंबर का सत्यापन कैसे करें?" : "How to verify genuine ISI mark and 7-digit CML number on BIS Care App?", useStream, [])}
              className="px-2.5 py-1 rounded-full bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 shrink-0 cursor-pointer transition-colors"
            >
              🛡️ {language === 'hi' ? 'आईएसआई मार्क व CML जांचें' : 'Check ISI Mark & CML'}
            </button>
            <button
              onClick={() => onSendMessage(language === 'hi' ? "घटिया उत्पाद या नकली आईएसआई की शिकायत बीआईएस में कैसे दर्ज करें?" : "How do I file an official consumer complaint against substandard goods or fake ISI marks?", useStream, [])}
              className="px-2.5 py-1 rounded-full bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 shrink-0 cursor-pointer transition-colors"
            >
              ⚖️ {language === 'hi' ? 'उपभोक्ता शिकायत दर्ज करें' : 'File Consumer Complaint'}
            </button>
            <button
              onClick={() => onSendMessage(language === 'hi' ? "दोपहिया वाहन हेलमेट के लिए क्या आईएसआई अनिवार्य है?" : "Is ISI mark mandatory for two wheeler helmets under IS 4151:2015?", useStream, [])}
              className="px-2.5 py-1 rounded-full bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/30 shrink-0 cursor-pointer transition-colors"
            >
              🪖 {language === 'hi' ? 'हेलमेट सुरक्षा (IS 4151)' : 'Helmets Safety (IS 4151)'}
            </button>
            <button
              onClick={() => onSendMessage(language === 'hi' ? "बीआईएस राष्ट्रीय टोल-फ्री हेल्पलाइन नंबर और सहायता पोर्टल क्या हैं?" : "What is the official BIS toll-free helpline number and portals?", useStream, [])}
              className="px-2.5 py-1 rounded-full bg-sky-500/10 hover:bg-sky-500/20 text-sky-300 border border-sky-500/30 shrink-0 cursor-pointer transition-colors"
            >
              📞 {language === 'hi' ? 'हेल्पलाइन: 1800-11-1255' : 'Helpline: 1800-11-1255'}
            </button>
          </>
        )}
      </div>

      {/* ── MAIN CHAT AREA / MESSAGE FEED ──────────────────────────────────── */}
      <div className="flex-1 overflow-y-auto px-4 md:px-8 py-6 z-10">
        {messages.length === 0 ? (
          /* Empty / Welcome State with 3D Neural Human Brain Hero */
          <div className="w-full flex flex-col items-center justify-start text-center max-w-3xl mx-auto px-2 select-text pt-2 pb-8">
            
            {/* 3D Anatomical Brain Hero Canvas */}
            <div className="relative w-full h-40 sm:h-48 md:h-52 mb-2 flex items-center justify-center pointer-events-auto">
              <div className="absolute inset-0 bg-gradient-to-t from-cyan-500/10 via-transparent to-transparent rounded-full blur-2xl pointer-events-none" />
              <NeuralBrainHero3D phase={0} className="w-full h-full" />
            </div>

            {/* Portal Badge & Heading */}
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-900 border border-zinc-800 text-xs text-zinc-300 font-mono mb-2">
              <span className={`w-2 h-2 rounded-full ${entryPoint === 'industry' ? 'bg-amber-400' : 'bg-cyan-400'} animate-pulse`} />
              <span>
                {entryPoint === 'industry' 
                  ? (language === 'hi' ? 'उद्योग व विनिर्माण सहायता मोड' : 'Industry & Manufacturing Mode') 
                  : (language === 'hi' ? 'नागरिक व उपभोक्ता अधिकार मोड' : 'Consumer Rights & Verification Mode')
                }
              </span>
            </div>

            <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-white tracking-tight mb-1.5 font-sans">
              {language === 'hi' 
                ? (entryPoint === 'industry' ? 'भारतीय मानक एवं बीआईएस प्रमाणन में आपकी क्या सहायता करूँ?' : 'आईएसआई मार्क एवं हॉलमार्क सत्यापन में आपका स्वागत है')
                : (entryPoint === 'industry' ? 'How can BIS Virtual Assistant assist your enterprise?' : 'BIS Consumer Protection & Standards Assistant')
              }
            </h2>

            <p className="text-zinc-400 text-xs sm:text-sm leading-relaxed mb-6 max-w-xl font-normal">
              {language === 'hi'
                ? 'भारतीय मानकों (IS Codes), अनिवार्य क्यूसीओ आदेशों, परीक्षण आवश्यकताओं, 6-अंकीय HUID हॉलमार्क और शिकायत निवारण हेतु संपूर्ण मार्गदर्शिका।'
                : 'Search Indian Standards (IS Codes), verify 6-digit HUID Hallmarks, inspect ISI Mark (CML numbers), audit mandatory QCOs, and navigate step-by-step certification.'
              }
            </p>

            {/* Prompt Cards Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 w-full text-left">
              {activePromptCards.map((card, idx) => {
                const IconComponent = card.icon;
                return (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => {
                      setInputQuery('');
                      onSendMessage(card.desc, useStream, []);
                    }}
                    className="p-3.5 rounded-2xl bg-zinc-900/80 hover:bg-zinc-800/90 border border-zinc-800 hover:border-zinc-700 text-left transition-all duration-200 group flex flex-col justify-between gap-2 shadow-sm cursor-pointer hover:scale-[1.01]"
                  >
                    <div className="flex items-center justify-between">
                      <div className={`p-1.5 rounded-xl border ${card.color}`}>
                        <IconComponent className="w-4 h-4" />
                      </div>
                      <span className="text-[10px] font-mono text-zinc-500">
                        {card.category}
                      </span>
                    </div>

                    <div>
                      <h3 className="text-xs font-semibold text-zinc-200 group-hover:text-white mb-0.5">
                        {card.title}
                      </h3>
                      <p className="text-[11px] text-zinc-400 line-clamp-2 leading-relaxed font-normal">
                        {card.desc}
                      </p>
                    </div>

                    <div className="flex items-center gap-1 text-[10px] text-zinc-500 group-hover:text-cyan-400 font-medium pt-1">
                      <span>{language === 'hi' ? 'उत्तर देखें' : 'View Standards'}</span>
                      <ChevronRight className="w-3 h-3 transition-transform group-hover:translate-x-1" />
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        ) : (
          <div className="max-w-3xl mx-auto">
            {messages.map((msg) => (
              <MessageItem 
                key={msg.id} 
                message={msg} 
                onSelectQuery={(q) => onSendMessage(q, useStream, [])}
              />
            ))}
          </div>
        )}

        {/* Loading state (non-streaming) */}
        {loading && !isStreaming && (
          <div className="max-w-3xl mx-auto">
            <LottieLoader text={language === 'hi' ? 'भारतीय मानक डेटाबेस से सटीक क्लॉज निकाले जा रहे हैं...' : 'Retrieving Indian Standards & verifying clauses...'} />
          </div>
        )}

        {/* Streaming indicator */}
        {isStreaming && messages.some(m => m.streaming) && (
          <div className="max-w-3xl mx-auto flex items-center gap-2 text-xs text-zinc-400 mt-2 pl-4 animate-pulse">
            <Radio className="w-3 h-3 text-cyan-400" />
            <span>{language === 'hi' ? 'मानक दस्तावेज़ से रीयल-टाइम उत्तर प्राप्त हो रहा है...' : 'Streaming response from Sovereign Standards Engine...'}</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* ── FLOATING BOTTOM INPUT BAR (Speech + Attachment + Send) ──────────── */}
      <footer className={`z-10 shrink-0 ${isMobile ? 'mobile-input-bar p-3 pt-3' : 'p-3 sm:p-5'}`}>
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto">
          
          {/* Attachment Preview Tray */}
          {attachments.length > 0 && (
            <div className="flex flex-wrap items-center gap-2 mb-2 p-2.5 rounded-2xl bg-zinc-900/95 border border-zinc-800 shadow-xl backdrop-blur-md">
              {attachments.map((att) => (
                <div 
                  key={att.id} 
                  className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-zinc-950 border border-zinc-700/80 text-xs text-zinc-200 relative group shadow-sm"
                >
                  {att.previewUrl ? (
                    <img src={att.previewUrl} alt={att.name} className="w-7 h-7 rounded-lg object-cover border border-zinc-800" />
                  ) : (
                    <FileText className="w-4 h-4 text-cyan-400 shrink-0" />
                  )}
                  <div className="flex flex-col min-w-0">
                    <span className="truncate max-w-[130px] text-[11px] font-medium text-white">{att.name}</span>
                    {att.size && (
                      <span className="text-[9px] text-zinc-400 font-mono">
                        {(att.size / 1024).toFixed(0)} KB
                      </span>
                    )}
                  </div>
                  <button
                    type="button"
                    onClick={() => removeAttachment(att.id)}
                    className="p-1 rounded-full hover:bg-zinc-800 text-zinc-400 hover:text-white transition-colors cursor-pointer ml-1"
                    title="Remove attachment"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              ))}
            </div>
          )}

          {/* Main Input Capsule */}
          <div className={`relative flex items-center bg-zinc-900/95 hover:bg-zinc-900 rounded-2xl p-2 border transition-all shadow-2xl backdrop-blur-xl ${
            isDragging ? 'border-cyan-400 ring-2 ring-cyan-500/20' : 'border-zinc-800 focus-within:border-zinc-600 focus-within:ring-1 focus-within:ring-zinc-600'
          }`}>
            
            {/* (+) Attachment Button for Standards & Manuals */}
            <div className="relative">
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="flex items-center justify-center w-8 h-8 rounded-xl text-zinc-400 hover:text-white hover:bg-zinc-800 transition-all cursor-pointer mr-1.5 shrink-0 group"
                title="Attach standard PDF, document or image"
              >
                <Plus className="w-4 h-4 font-bold group-hover:scale-110 transition-transform" />
              </button>

              <input
                ref={fileInputRef}
                type="file"
                multiple
                accept=".pdf,.png,.jpg,.jpeg,.webp,.txt,.docx,.md,.csv"
                onChange={handleFileChange}
                className="hidden"
              />
            </div>

            {/* Input Box */}
            {isMobile ? (
              <textarea
                ref={inputRef}
                value={inputQuery}
                onChange={(e) => setInputQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                onPaste={handlePaste}
                placeholder={language === 'hi' 
                  ? (entryPoint === 'industry' ? "उत्पाद मानक या परीक्षण नियम पूछें..." : "हॉलमार्क, आईएसआई या शिकायत प्रक्रिया पूछें...")
                  : (entryPoint === 'industry' ? "Ask: Which IS applies? What testing is needed?..." : "Ask: Verify gold hallmark, check ISI mark, file complaint...")
                }
                disabled={isActive}
                rows={1}
                style={{ resize: 'none', overflow: 'hidden' }}
                onInput={(e) => {
                  e.target.style.height = 'auto';
                  e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
                }}
                className="w-full bg-transparent px-2 py-2 text-zinc-100 placeholder-zinc-500 text-sm focus:outline-none font-sans leading-relaxed select-text cursor-text"
              />
            ) : (
              <input
                ref={inputRef}
                type="text"
                value={inputQuery}
                onChange={(e) => setInputQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                onPaste={handlePaste}
                placeholder={language === 'hi'
                  ? (entryPoint === 'industry' ? "पूछें: कौन सा IS मानक लागू होता है? क्या परीक्षण आवश्यक हैं? या PDF अटैच करें..." : "पूछें: सोने का हॉलमार्क कैसे चेक करें? नकली ISI की शिकायत कैसे करें?...")
                  : (entryPoint === 'industry' ? "Ask: 'Which IS standard applies to my product?', 'What testing is needed?', or upload PDF..." : "Ask: 'How to check gold hallmark HUID?', 'Verify ISI mark', 'Consumer complaint process'...")
                }
                disabled={isActive}
                className="w-full bg-transparent px-2 py-2 text-zinc-100 placeholder-zinc-500 text-sm focus:outline-none font-sans select-text cursor-text"
              />
            )}

            {/* Voice Input (Speech-to-Text) Button */}
            <button
              type="button"
              onClick={toggleVoiceInput}
              disabled={isActive}
              className={`p-2 rounded-xl text-zinc-400 hover:text-white hover:bg-zinc-800 transition-all cursor-pointer shrink-0 mr-1.5 ${
                isRecording ? 'bg-rose-500/20 text-rose-400 animate-pulse ring-2 ring-rose-500/40' : ''
              }`}
              title={isRecording 
                ? (language === 'hi' ? 'सुन रहा हूँ... रोकने के लिए क्लिक करें' : 'Listening... click to stop') 
                : (language === 'hi' ? 'आवाज़ द्वारा पूछें (Voice Input)' : `Voice input (${language === 'hi' ? 'Hindi' : 'English'})`)
              }
            >
              {isRecording ? <Mic className="w-4 h-4 text-rose-400" /> : <Mic className="w-4 h-4" />}
            </button>

            {/* Send Button */}
            <button
              type="submit"
              disabled={isActive || (!inputQuery.trim() && attachments.length === 0)}
              className="flex items-center justify-center w-8 h-8 rounded-xl bg-white hover:bg-zinc-200 text-zinc-950 shadow-md disabled:opacity-20 disabled:cursor-not-allowed transition-all shrink-0 cursor-pointer"
              title="Send question"
            >
              <ArrowUp className="w-4 h-4 font-bold stroke-[2.5]" />
            </button>
          </div>

          <p className="text-[10px] text-zinc-500 text-center mt-2 font-mono flex items-center justify-center gap-2">
            <span>PRAHARI AI &bull; SIH Topic 26107 &bull; Bureau of Indian Standards (BIS)</span>
            <span className="text-zinc-600">|</span>
            <span className="text-cyan-500/80">Helpline: 1800-11-1255</span>
          </p>
        </form>
      </footer>
    </main>
  );
}
