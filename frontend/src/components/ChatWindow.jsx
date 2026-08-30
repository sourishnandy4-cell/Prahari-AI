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
  ShieldAlert, 
  Flame, 
  Wrench, 
  FileCheck,
  ChevronRight,
  Upload
} from 'lucide-react';
import MessageItem from './MessageItem';
import LottieLoader from './LottieLoader';

const PROMPT_CARDS = [
  {
    icon: Flame,
    title: "Emergency Shutdown CDU",
    desc: "What is the emergency shutdown procedure for the Crude Distillation Unit (CDU-3)?",
    category: "Emergency SOP Directive",
    color: "text-rose-400 bg-rose-500/10 border-rose-500/20"
  },
  {
    icon: Wrench,
    title: "Asset History: PRV-401",
    desc: "Pull the maintenance history, pop-test tolerances, and recertification records for PRV-401.",
    category: "Asset Integrity Registry",
    color: "text-cyan-400 bg-cyan-500/10 border-cyan-500/20"
  },
  {
    icon: FileCheck,
    title: "P&ID Schematic Tracing",
    desc: "Analyze the CDU-3 P&ID schematic for block isolation valves EBV-101/102 and flare bypasses.",
    category: "Multimodal P&ID Vision",
    color: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20"
  },
  {
    icon: ShieldAlert,
    title: "Material Code Harmonization",
    desc: "Check if vendor submitted ASTM A105 flange meets MRPL PMS-300-SS sour service standards.",
    category: "MOP&NG Standards Agent",
    color: "text-purple-400 bg-purple-500/10 border-purple-500/20"
  },
  {
    icon: ShieldAlert,
    title: "Near-Miss Precursor NLP",
    desc: "Screen recent field unsafe-act logs to flag high-consequence injury and fatality precursors.",
    category: "NLP Precursor Detection",
    color: "text-amber-400 bg-amber-500/10 border-amber-500/20"
  },
  {
    icon: FileCheck,
    title: "H2S Exposure Limits & PPE",
    desc: "What are the permissible H2S gas exposure limits and mandatory SCBA protocols in Sector-2?",
    category: "Toxic Gas Safety",
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
  onToggleSidebar,
  onNewChat
}) {
  const [inputQuery, setInputQuery] = useState('');
  const [useStream, setUseStream] = useState(true);
  const [attachments, setAttachments] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

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

  // Handle Voice Input via Web Speech API
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

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
  }, []);

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
      const reader = new FileReader();
      const isImg = file.type.startsWith('image/');

      reader.onload = (event) => {
        setAttachments((prev) => [
          ...prev,
          {
            id: Date.now() + Math.random().toString(),
            file,
            name: file.name,
            size: file.size,
            type: file.type,
            previewUrl: isImg ? event.target.result : null,
            data: event.target.result,
          },
        ]);
      };

      if (isImg) {
        reader.readAsDataURL(file);
      } else {
        reader.readAsText(file);
      }
    });
  };

  const handleFileChange = (e) => {
    processFiles(e.target.files);
    e.target.value = '';
  };

  // Drag and Drop support
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

  // Paste image or files support
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

  return (
    <main 
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className="flex-1 h-screen flex flex-col justify-between bg-zinc-950 text-zinc-100 relative overflow-hidden select-none"
    >
      
      {/* Header (Clean & Modern like Gemini / ChatGPT) */}
      <header className="h-14 bg-zinc-950/80 backdrop-blur-md border-b border-zinc-800/80 px-4 md:px-6 flex items-center justify-between z-10 shrink-0">
        <div className="flex items-center gap-3">
          {/* Sidebar Toggle button if collapsed */}
          {!isSidebarOpen && (
            <button
              onClick={onToggleSidebar}
              className="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors cursor-pointer"
              title="Open sidebar"
            >
              <PanelLeft className="w-4 h-4" />
            </button>
          )}

          {/* Model Selector Pill with Brain Icon */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-zinc-900 border border-zinc-800 text-xs text-zinc-200 font-medium shadow-sm">
            <Brain className="w-3.5 h-3.5 text-cyan-400" />
            <span className="font-semibold text-white">PRAHARI AI</span>
            <span className="text-[10px] text-emerald-400 font-mono flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block" />
              100% Offline
            </span>
          </div>
        </div>

        {/* Right Action Controls */}
        <div className="flex items-center gap-2">
          {/* Streaming toggle */}
          <button
            onClick={() => setUseStream(!useStream)}
            title={useStream ? 'Streaming tokens active' : 'Batch mode active'}
            className={`flex items-center gap-1.5 text-xs px-3 py-1 rounded-full border transition-all cursor-pointer ${
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
            className="flex items-center gap-1 text-xs px-2.5 py-1.5 rounded-lg text-zinc-300 hover:text-white hover:bg-zinc-900 border border-zinc-800/80 transition-all cursor-pointer"
            title="Start fresh conversation"
          >
            <Plus className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">New</span>
          </button>

          {/* Clear messages */}
          <button
            onClick={onClearChat}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-900 transition-colors cursor-pointer"
            title="Clear Chat History"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </header>

      {/* Message Feed / Main Chat Area */}
      <div className="flex-1 overflow-y-auto px-4 md:px-8 py-6 z-10">
        {messages.length === 0 ? (
          /* Empty / Welcome State (ChatGPT & Gemini Hero with Brain Logo) */
          <div className="h-full flex flex-col items-center justify-center text-center max-w-2xl mx-auto px-2 select-text">
            
            {/* Glowing Brain Hero Logo */}
            <div className="relative mb-5 group">
              <div className="absolute -inset-3 bg-gradient-to-r from-cyan-500/25 via-sky-500/20 to-indigo-500/25 rounded-full blur-xl opacity-80 group-hover:opacity-100 transition duration-700 animate-pulse" />
              <div className="relative w-16 h-16 rounded-2xl bg-zinc-900 border border-cyan-500/40 flex items-center justify-center text-cyan-400 shadow-2xl shadow-cyan-950/40">
                <Brain className="w-9 h-9 text-cyan-400" />
              </div>
            </div>

            {/* Title & Subtitle */}
            <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight mb-2 font-sans">
              How can Prahari AI assist you today?
            </h2>
            <p className="text-zinc-400 text-xs sm:text-sm leading-relaxed mb-8 max-w-lg font-normal">
              Ask technical safety queries, audit emergency SOPs, or attach pictures, diagrams, and compliance documents for sovereign offline analysis.
            </p>

            {/* 4 Interactive Prompt Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full text-left">
              {PROMPT_CARDS.map((card, idx) => {
                const IconComponent = card.icon;
                return (
                  <button
                    key={idx}
                    onClick={() => {
                      setInputQuery('');
                      onSendMessage(card.desc, useStream, []);
                    }}
                    className="p-3.5 rounded-2xl bg-zinc-900/80 hover:bg-zinc-800/90 border border-zinc-800 hover:border-zinc-700 text-left transition-all duration-200 group flex flex-col justify-between gap-2 shadow-sm cursor-pointer"
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
                      <span>Analyze protocol</span>
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
              <MessageItem key={msg.id} message={msg} />
            ))}
          </div>
        )}

        {/* Loading state (non-streaming) */}
        {loading && !isStreaming && (
          <div className="max-w-3xl mx-auto">
            <LottieLoader text="Synthesizing response from local Sovereign LLM..." />
          </div>
        )}

        {/* Streaming indicator */}
        {isStreaming && messages.some(m => m.streaming) && (
          <div className="max-w-3xl mx-auto flex items-center gap-2 text-xs text-zinc-400 mt-2 pl-4 animate-pulse">
            <Radio className="w-3 h-3 text-cyan-400" />
            <span>Streaming tokens from local Llama 3.2...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Floating Bottom Input Bar (ChatGPT / Gemini Style with + Attachment Icon) */}
      <footer className="p-3 sm:p-5 z-10 shrink-0">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto">
          
          {/* Attachment Preview Tray above the input */}
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

          {/* Main Input Capsule (Modern Floating AI Bar) */}
          <div className={`relative flex items-center bg-zinc-900/95 hover:bg-zinc-900 rounded-2xl p-2 border transition-all shadow-2xl backdrop-blur-xl ${
            isDragging ? 'border-cyan-400 ring-2 ring-cyan-500/20' : 'border-zinc-800 focus-within:border-zinc-600 focus-within:ring-1 focus-within:ring-zinc-600'
          }`}>
            
            {/* (+) Plus Attachment Button for Photos, Docs, SOPs */}
            <div className="relative">
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="flex items-center justify-center w-8 h-8 rounded-xl text-zinc-400 hover:text-white hover:bg-zinc-800 transition-all cursor-pointer mr-1.5 shrink-0 group"
                title="Add pictures, documents or SOPs to analyze"
              >
                <Plus className="w-4 h-4 font-bold group-hover:scale-110 transition-transform" />
              </button>

              {/* Hidden file input supporting images, docs, pdfs */}
              <input
                ref={fileInputRef}
                type="file"
                multiple
                accept=".pdf,.png,.jpg,.jpeg,.webp,.txt,.docx,.md,.csv"
                onChange={handleFileChange}
                className="hidden"
              />
            </div>

            {/* Text Input */}
            <input
              ref={inputRef}
              type="text"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              onPaste={handlePaste}
              placeholder="Ask a safety question or attach pictures/docs to analyze..."
              disabled={isActive}
              className="w-full bg-transparent px-2 py-2 text-zinc-100 placeholder-zinc-500 text-sm focus:outline-none font-sans"
            />

            {/* Voice Input (Mic) Button */}
            <button
              type="button"
              onClick={toggleVoiceInput}
              disabled={isActive}
              className={`p-2 rounded-xl text-zinc-400 hover:text-white hover:bg-zinc-800 transition-all cursor-pointer shrink-0 mr-1.5 ${
                isRecording ? 'bg-rose-500/20 text-rose-400 animate-pulse' : ''
              }`}
              title={isRecording ? 'Listening... click to stop' : 'Voice input'}
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

          <p className="text-[10px] text-zinc-500 text-center mt-2 font-mono">
            PRAHARI AI &bull; 100% Sovereign Offline Intelligence &bull; MRPL Refinery
          </p>
        </form>
      </footer>
    </main>
  );
}
