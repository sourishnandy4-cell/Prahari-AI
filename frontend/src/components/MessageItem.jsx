import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Brain, 
  User, 
  FileText, 
  ChevronDown, 
  ChevronUp, 
  Copy, 
  Check, 
  Sparkles, 
  GitBranch, 
  Clock, 
  File,
  Eye,
  Download
} from 'lucide-react';

export default function MessageItem({ message }) {
  const isUser = message.sender === 'user';
  const [showCitations, setShowCitations] = useState(false);
  const [copied, setCopied] = useState(false);
  const [previewImage, setPreviewImage] = useState(null);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const meta = message.metadata;
  const attachments = message.attachments || [];

  return (
    <motion.div
      initial={{ opacity: 0, y: 12, scale: 0.99 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.2, ease: 'easeOut' }}
      className={`flex w-full mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div className={`flex max-w-3xl gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar with Brain for AI */}
        <div className={`flex items-center justify-center w-8 h-8 rounded-xl shrink-0 ${
          isUser
            ? 'bg-zinc-100 text-zinc-950 font-bold shadow-sm'
            : 'bg-gradient-to-br from-cyan-500/20 via-sky-500/10 to-zinc-900 border border-cyan-500/30 text-cyan-400 shadow-md shadow-cyan-950/20'
        }`}>
          {isUser ? <User className="w-4 h-4" /> : <Brain className="w-4 h-4 text-cyan-400" />}
        </div>

        {/* Message Bubble Container */}
        <div className="flex flex-col min-w-0 max-w-[85vw] sm:max-w-xl md:max-w-2xl">
          <div className={`relative px-4 py-3.5 rounded-2xl ${
            isUser
              ? 'bg-zinc-800 text-white rounded-tr-sm border border-zinc-700/60 shadow-sm'
              : 'bg-zinc-900/90 text-zinc-100 rounded-tl-sm border border-zinc-800/90 shadow-md'
          }`}>

            {/* AI Header */}
            {!isUser && (
              <div className="flex items-center justify-between pb-2 mb-2 border-b border-zinc-800/80 text-xs text-zinc-400 font-medium">
                <span className="flex items-center gap-1.5 text-zinc-200 font-semibold">
                  <span className="text-cyan-400 font-sans">PRAHARI AI</span>
                  {message.streaming && (
                    <span className="inline-flex items-center gap-1 text-cyan-400 text-[10px] font-mono ml-1">
                      <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping" />
                      synthesizing...
                    </span>
                  )}
                </span>
                <button
                  onClick={handleCopy}
                  className="hover:text-white transition-colors p-1 rounded-md hover:bg-zinc-800 text-zinc-400"
                  title="Copy response"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                </button>
              </div>
            )}

            {/* Attachments inside message bubble */}
            {attachments.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-3">
                {attachments.map((att, idx) => (
                  <div key={idx} className="relative group">
                    {att.type?.startsWith('image/') || att.previewUrl ? (
                      <div className="relative rounded-xl overflow-hidden border border-zinc-700 max-w-[220px] max-h-[150px] bg-zinc-950 shadow-md">
                        <img 
                          src={att.previewUrl || att.data} 
                          alt={att.name || 'attachment'} 
                          className="w-full h-full object-cover cursor-pointer hover:opacity-90 transition-opacity"
                          onClick={() => setPreviewImage(att.previewUrl || att.data)}
                        />
                        <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity pointer-events-none">
                          <Eye className="w-4 h-4 text-white" />
                        </div>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-zinc-950 border border-zinc-700/80 text-xs text-zinc-200 shadow-sm">
                        <FileText className="w-4 h-4 text-cyan-400 shrink-0" />
                        <div className="flex flex-col min-w-0">
                          <span className="truncate max-w-[140px] text-[11px] font-medium text-white">{att.name}</span>
                          {att.size && (
                            <span className="text-[9px] font-mono text-zinc-400">
                              {(att.size / 1024).toFixed(0)} KB
                            </span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Metadata badges (mode, latency, hops) */}
            {!isUser && meta && !message.streaming && (
              <div className="flex flex-wrap gap-1.5 mb-2.5">
                {meta.mode && (
                  <span className="text-[9px] px-2 py-0.5 rounded-full bg-zinc-800/80 border border-zinc-700/60 text-cyan-300 font-mono">
                    {meta.mode}
                  </span>
                )}
                {meta.hops != null && meta.hops > 1 && (
                  <span className="text-[9px] px-2 py-0.5 rounded-full bg-zinc-800/80 border border-zinc-700/60 text-zinc-300 font-mono flex items-center gap-1">
                    <GitBranch className="w-2.5 h-2.5" />{meta.hops} hops
                  </span>
                )}
                {meta.latency_ms != null && (
                  <span className="text-[9px] px-2 py-0.5 rounded-full bg-zinc-800/80 border border-zinc-700/60 text-zinc-400 font-mono flex items-center gap-1">
                    <Clock className="w-2.5 h-2.5" />{meta.latency_ms}ms
                  </span>
                )}
              </div>
            )}

            {/* Main Text */}
            <div className="text-sm leading-relaxed font-sans space-y-2 select-text">
              {message.text ? (
                message.text.split('\n').map((line, idx) => {
                  if (!line.trim()) return <div key={idx} className="h-1" />;

                  const renderInline = (text) =>
                    text.split(/(\*\*.*?\*\*)/g).map((part, pIdx) =>
                      part.startsWith('**') && part.endsWith('**')
                        ? <strong key={pIdx} className="font-semibold text-white">{part.slice(2, -2)}</strong>
                        : part
                    );

                  if (line.trim().startsWith('•') || line.trim().startsWith('*') || line.trim().startsWith('-')) {
                    return (
                      <div key={idx} className="flex items-start gap-2 pl-1.5">
                        <span className="text-cyan-400 font-bold shrink-0 mt-0.5">•</span>
                        <div>{renderInline(line.replace(/^[•*-]\s*/, ''))}</div>
                      </div>
                    );
                  }

                  const numMatch = line.match(/^(\d+\.)\s+(.*)/);
                  if (numMatch) {
                    return (
                      <div key={idx} className="flex items-start gap-2 pl-1.5">
                        <span className="text-cyan-400 font-mono font-bold text-xs px-1.5 py-0.2 rounded bg-zinc-800/80 border border-zinc-700/70 shrink-0 mt-0.5">{numMatch[1]}</span>
                        <div>{renderInline(numMatch[2])}</div>
                      </div>
                    );
                  }

                  return <p key={idx}>{renderInline(line)}</p>;
                })
              ) : message.streaming ? (
                <span className="inline-flex gap-1.5 items-center text-zinc-400 py-1">
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce" style={{ animationDelay: '300ms' }} />
                </span>
              ) : null}
            </div>

            {/* Citations */}
            {!isUser && message.citations && message.citations.length > 0 && !message.streaming && (
              <div className="mt-3.5 pt-2.5 border-t border-zinc-800">
                <button
                  onClick={() => setShowCitations(!showCitations)}
                  className="flex items-center justify-between w-full text-xs text-zinc-300 hover:text-white transition-colors py-1.5 px-2.5 rounded-lg bg-zinc-950/70 border border-zinc-800 hover:border-zinc-700 cursor-pointer"
                >
                  <span className="flex items-center gap-1.5 font-medium">
                    <FileText className="w-3.5 h-3.5 text-cyan-400" />
                    Verified Citations ({message.citations.length})
                  </span>
                  {showCitations ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                </button>

                {showCitations && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    className="mt-2 space-y-1.5"
                  >
                    {message.citations.map((cite, idx) => (
                      <div key={idx} className="p-2.5 rounded-lg bg-zinc-950 border border-zinc-800/90 text-xs">
                        <div className="flex items-center justify-between text-zinc-200 font-medium mb-1">
                          <span className="truncate pr-2 font-mono text-[11px]">📄 {cite.source}</span>
                          <span className="px-1.5 py-0.2 rounded bg-zinc-800 text-[10px] text-cyan-400 font-mono shrink-0">Page {cite.page}</span>
                        </div>
                        <p className="text-zinc-400 italic text-[11px] leading-relaxed">
                          "{cite.snippet}"
                        </p>
                      </div>
                    ))}
                  </motion.div>
                )}
              </div>
            )}
          </div>

          <span className="text-[10px] text-zinc-500 mt-1 px-1 font-mono">
            {message.timestamp}
          </span>
        </div>
      </div>

      {/* Image Modal Lightbox */}
      {previewImage && (
        <div 
          onClick={() => setPreviewImage(null)}
          className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4 cursor-pointer"
        >
          <div className="relative max-w-4xl max-h-[85vh] rounded-xl overflow-hidden border border-zinc-700 bg-zinc-950 shadow-2xl">
            <img src={previewImage} alt="Expanded preview" className="w-full h-full object-contain" />
          </div>
        </div>
      )}
    </motion.div>
  );
}
