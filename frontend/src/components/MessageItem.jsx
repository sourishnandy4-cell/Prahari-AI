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
  Download,
  ChevronRight,
  ShieldCheck,
  Tag
} from 'lucide-react';

function renderInline(text, keyPrefix = 'inl') {
  if (!text) return null;

  // Split by inline code first: `...`
  const codeParts = text.split(/(`[^`]+`)/g);

  return codeParts.map((part, cpIdx) => {
    if (part.startsWith('`') && part.endsWith('`') && part.length >= 2) {
      return (
        <code 
          key={`${keyPrefix}-c-${cpIdx}`} 
          className="px-1.5 py-0.5 mx-0.5 rounded bg-zinc-800 border border-zinc-700 font-mono text-cyan-300 text-[11px]"
        >
          {part.slice(1, -1)}
        </code>
      );
    }

    // Split by bold: **...**
    const boldParts = part.split(/(\*\*[^*]+\*\*)/g);
    return boldParts.map((bPart, bpIdx) => {
      if (bPart.startsWith('**') && bPart.endsWith('**') && bPart.length >= 4) {
        return (
          <strong key={`${keyPrefix}-b-${cpIdx}-${bpIdx}`} className="font-semibold text-white">
            {bPart.slice(2, -2)}
          </strong>
        );
      }

      // Split by italic: *...*
      const italicParts = bPart.split(/(\*[^*]+\*)/g);
      return italicParts.map((iPart, ipIdx) => {
        if (iPart.startsWith('*') && iPart.endsWith('*') && iPart.length >= 2) {
          return (
            <em key={`${keyPrefix}-i-${cpIdx}-${bpIdx}-${ipIdx}`} className="italic text-zinc-200">
              {iPart.slice(1, -1)}
            </em>
          );
        }
        return iPart;
      });
    });
  });
}

function MarkdownContent({ content }) {
  if (!content) return null;

  const lines = content.split('\n');
  const elements = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    // 1. Code Block (```...```)
    if (trimmed.startsWith('```')) {
      const lang = trimmed.slice(3).trim();
      const codeLines = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith('```')) {
        codeLines.push(lines[i]);
        i++;
      }
      i++; // skip closing ```
      const codeText = codeLines.join('\n');
      elements.push(
        <div key={`code-${elements.length}`} className="my-2.5 rounded-xl border border-zinc-700/80 bg-zinc-950 overflow-hidden font-mono text-xs shadow-md">
          {lang && (
            <div className="flex items-center justify-between px-3 py-1.5 bg-zinc-900 border-b border-zinc-800 text-[10px] text-zinc-400 uppercase tracking-wider font-semibold">
              <span>{lang}</span>
              <button 
                onClick={() => navigator.clipboard.writeText(codeText)} 
                className="hover:text-cyan-400 transition-colors flex items-center gap-1 cursor-pointer"
                title="Copy code"
              >
                <Copy className="w-3 h-3" />
                Copy
              </button>
            </div>
          )}
          <pre className="p-3 overflow-x-auto text-zinc-200 leading-relaxed font-mono">
            <code>{codeText}</code>
          </pre>
        </div>
      );
      continue;
    }

    // 2. Table (| Header | ... |)
    if (trimmed.startsWith('|') && trimmed.endsWith('|') && i + 1 < lines.length) {
      const nextTrimmed = lines[i + 1].trim();
      if (nextTrimmed.startsWith('|') && nextTrimmed.endsWith('|')) {
        const delimCells = nextTrimmed.slice(1, -1).split('|').map(c => c.trim());
        const isTable = delimCells.length > 0 && delimCells.every(c => /^:?-+:?$/.test(c));

        if (isTable) {
          const headers = trimmed.slice(1, -1).split('|').map(c => c.trim());
          const alignments = delimCells.map(c => {
            if (c.startsWith(':') && c.endsWith(':')) return 'text-center';
            if (c.endsWith(':')) return 'text-right';
            return 'text-left';
          });

          i += 2; // skip header and delimiter lines
          const rows = [];
          while (i < lines.length && lines[i].trim().startsWith('|') && lines[i].trim().endsWith('|')) {
            const rowCells = lines[i].trim().slice(1, -1).split('|').map(c => c.trim());
            rows.push(rowCells);
            i++;
          }

          elements.push(
            <div key={`table-${elements.length}`} className="my-3 overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-950/70 shadow-lg">
              <table className="w-full text-left border-collapse text-xs">
                <thead className="bg-zinc-800/80 border-b border-zinc-700 text-zinc-200">
                  <tr>
                    {headers.map((h, hIdx) => (
                      <th key={hIdx} className={`px-3.5 py-2 font-semibold ${alignments[hIdx] || 'text-left'}`}>
                        {renderInline(h, `th-${hIdx}`)}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800/60">
                  {rows.map((row, rIdx) => (
                    <tr key={rIdx} className="hover:bg-zinc-800/30 transition-colors odd:bg-zinc-900/30">
                      {row.map((cell, cIdx) => (
                        <td key={cIdx} className={`px-3.5 py-2 text-zinc-300 ${alignments[cIdx] || 'text-left'}`}>
                          {renderInline(cell, `td-${rIdx}-${cIdx}`)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
          continue;
        }
      }
    }

    // 3. Headings
    if (trimmed.startsWith('#### ')) {
      elements.push(
        <h4 key={`h4-${i}`} className="text-xs font-semibold text-zinc-300 uppercase tracking-wider mt-3 mb-1">
          {renderInline(trimmed.slice(5), `h4-${i}`)}
        </h4>
      );
      i++;
      continue;
    }
    if (trimmed.startsWith('### ')) {
      elements.push(
        <h3 key={`h3-${i}`} className="text-sm font-semibold text-cyan-300 mt-3 mb-1 flex items-center gap-1.5">
          {renderInline(trimmed.slice(4), `h3-${i}`)}
        </h3>
      );
      i++;
      continue;
    }
    if (trimmed.startsWith('## ')) {
      elements.push(
        <h2 key={`h2-${i}`} className="text-base font-bold text-white mt-3 mb-1 pb-1 border-b border-zinc-800/70">
          {renderInline(trimmed.slice(3), `h2-${i}`)}
        </h2>
      );
      i++;
      continue;
    }
    if (trimmed.startsWith('# ')) {
      elements.push(
        <h1 key={`h1-${i}`} className="text-lg font-bold text-white mt-3 mb-1.5 pb-1 border-b border-zinc-800">
          {renderInline(trimmed.slice(2), `h1-${i}`)}
        </h1>
      );
      i++;
      continue;
    }

    // 4. Horizontal Rule
    if (/^(\-{3,}|\*{3,}|_{3,})$/.test(trimmed)) {
      elements.push(
        <div key={`hr-${i}`} className="my-3 h-[1px] bg-gradient-to-r from-transparent via-zinc-700/80 to-transparent" />
      );
      i++;
      continue;
    }

    // 5. Blockquote
    if (trimmed.startsWith('>')) {
      const quoteText = trimmed.replace(/^>\s*/, '');
      elements.push(
        <blockquote key={`bq-${i}`} className="my-2 pl-3 py-1 border-l-2 border-cyan-500/70 bg-zinc-900/40 text-zinc-300 italic text-xs rounded-r">
          {renderInline(quoteText, `bq-${i}`)}
        </blockquote>
      );
      i++;
      continue;
    }

    // 6. Unordered List
    if (trimmed.startsWith('•') || trimmed.startsWith('*') || trimmed.startsWith('-')) {
      const listText = trimmed.replace(/^[•*-]\s*/, '');
      elements.push(
        <div key={`ul-${i}`} className="flex items-start gap-2 pl-1.5 my-1">
          <span className="text-cyan-400 font-bold shrink-0 mt-0.5">•</span>
          <div className="text-zinc-200">{renderInline(listText, `ul-${i}`)}</div>
        </div>
      );
      i++;
      continue;
    }

    // 7. Ordered List
    const numMatch = trimmed.match(/^(\d+\.)\s+(.*)/);
    if (numMatch) {
      elements.push(
        <div key={`ol-${i}`} className="flex items-start gap-2 pl-1.5 my-1">
          <span className="text-cyan-400 font-mono font-bold text-xs px-1.5 py-0.2 rounded bg-zinc-800/80 border border-zinc-700/70 shrink-0 mt-0.5">
            {numMatch[1]}
          </span>
          <div className="text-zinc-200">{renderInline(numMatch[2], `ol-${i}`)}</div>
        </div>
      );
      i++;
      continue;
    }

    // 8. Empty line
    if (!trimmed) {
      elements.push(<div key={`empty-${i}`} className="h-1.5" />);
      i++;
      continue;
    }

    // 9. Standard Paragraph
    elements.push(
      <p key={`p-${i}`} className="text-zinc-200">
        {renderInline(line, `p-${i}`)}
      </p>
    );
    i++;
  }

  return <>{elements}</>;
}

export default function MessageItem({ message, onSelectQuery }) {
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

            {/* Main Text with Rich Markdown Rendering */}
            <div className="text-sm leading-relaxed font-sans space-y-1.5 select-text">
              {message.text ? (
                <MarkdownContent content={message.text} />
              ) : message.streaming ? (
                <span className="inline-flex gap-1.5 items-center text-zinc-400 py-1">
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce" style={{ animationDelay: '300ms' }} />
                </span>
              ) : null}
            </div>

            {/* Interactive Follow-up Question Options (if vague query was detected) */}
            {!isUser && message.follow_up_options && message.follow_up_options.length > 0 && !message.streaming && (
              <div className="mt-3.5 pt-2.5 border-t border-zinc-800/80">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-cyan-300 mb-2">
                  <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Clarify your product category or specification:</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {message.follow_up_options.map((opt, oIdx) => (
                    <button
                      key={oIdx}
                      type="button"
                      onClick={() => onSelectQuery && onSelectQuery(opt)}
                      className="px-3 py-1.5 rounded-xl bg-cyan-950/60 hover:bg-cyan-900/90 border border-cyan-700/50 hover:border-cyan-400 text-xs text-cyan-200 transition-all cursor-pointer flex items-center gap-1.5 shadow-sm hover:scale-[1.02] active:scale-[0.98]"
                    >
                      <span>{opt}</span>
                      <ChevronRight className="w-3 h-3 text-cyan-400" />
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Citations with Standard Number and Clause Badges */}
            {!isUser && message.citations && message.citations.length > 0 && !message.streaming && (
              <div className="mt-3.5 pt-2.5 border-t border-zinc-800">
                <button
                  onClick={() => setShowCitations(!showCitations)}
                  className="flex items-center justify-between w-full text-xs text-zinc-300 hover:text-white transition-colors py-1.5 px-2.5 rounded-lg bg-zinc-950/70 border border-zinc-800 hover:border-zinc-700 cursor-pointer"
                >
                  <span className="flex items-center gap-1.5 font-medium">
                    <FileText className="w-3.5 h-3.5 text-cyan-400" />
                    Verified Standard Citations ({message.citations.length})
                  </span>
                  {showCitations ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                </button>

                {showCitations && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    className="mt-2 space-y-1.5"
                  >
                    {message.citations.map((cite, idx) => {
                      const docName = cite.source || cite.document || cite.filename || 'BIS Standard';
                      const pageNum = cite.page ?? cite.section ?? '-';
                      const stdCode = cite.standard;
                      const clauseCode = cite.clause;
                      const snippetText = cite.snippet || cite.text || cite.content || '';
                      return (
                        <div key={idx} className="p-2.5 rounded-lg bg-zinc-950 border border-zinc-800/90 text-xs">
                          <div className="flex flex-wrap items-center justify-between gap-1 text-zinc-200 font-medium mb-1">
                            <div className="flex items-center gap-1.5 flex-wrap">
                              {stdCode && (
                                <span className="px-2 py-0.5 rounded-md bg-amber-500/20 text-amber-300 font-bold border border-amber-500/30 text-[10px]">
                                  🏷️ {stdCode}
                                </span>
                              )}
                              {clauseCode && (
                                <span className="px-2 py-0.5 rounded-md bg-cyan-500/20 text-cyan-300 font-mono text-[10px] border border-cyan-500/30">
                                  📌 {clauseCode}
                                </span>
                              )}
                              <span className="truncate pr-2 font-mono text-[11px] text-zinc-300">📄 {docName}</span>
                            </div>
                            <span className="px-1.5 py-0.2 rounded bg-zinc-800 text-[10px] text-cyan-400 font-mono shrink-0">Page {pageNum}</span>
                          </div>
                          {snippetText && (
                            <p className="text-zinc-400 italic text-[11px] leading-relaxed mt-1">
                              "{snippetText}"
                            </p>
                          )}
                        </div>
                      );
                    })}
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
