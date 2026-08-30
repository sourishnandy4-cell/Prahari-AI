import React, { useState } from 'react';
import { 
  Brain, 
  Plus, 
  MessageSquare, 
  Trash2, 
  Edit2, 
  Check, 
  X, 
  Search, 
  PanelLeftClose, 
  Upload, 
  RotateCcw,
  Sparkles,
  ShieldCheck
} from 'lucide-react';

export default function Sidebar({ 
  onNewChat, 
  sessions = [], 
  activeSessionId, 
  onSelectSession, 
  onDeleteSession, 
  onRenameSession,
  onOpenUploadModal, 
  onReplayIntro,
  isOpen = true,
  onToggleSidebar
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [editingSessionId, setEditingSessionId] = useState(null);
  const [editTitle, setEditTitle] = useState('');

  const filteredSessions = sessions.filter(s => 
    s.title?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Group sessions by date like ChatGPT & Gemini
  const groupSessions = (list) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    const last7Days = new Date(today);
    last7Days.setDate(last7Days.getDate() - 7);

    const groups = {
      Today: [],
      Yesterday: [],
      'Previous 7 Days': [],
      Older: []
    };

    list.forEach(sess => {
      const sessDate = new Date(sess.updated_at || sess.created_at || Date.now());
      if (sessDate >= today) {
        groups.Today.push(sess);
      } else if (sessDate >= yesterday) {
        groups.Yesterday.push(sess);
      } else if (sessDate >= last7Days) {
        groups['Previous 7 Days'].push(sess);
      } else {
        groups.Older.push(sess);
      }
    });

    return groups;
  };

  const grouped = groupSessions(filteredSessions);

  const startEditing = (e, session) => {
    e.stopPropagation();
    setEditingSessionId(session.id);
    setEditTitle(session.title);
  };

  const saveEditing = (e, sessionId) => {
    e.stopPropagation();
    if (editTitle.trim()) {
      onRenameSession?.(sessionId, editTitle.trim());
    }
    setEditingSessionId(null);
  };

  const cancelEditing = (e) => {
    e.stopPropagation();
    setEditingSessionId(null);
  };

  const formatSessionTitle = (title) => {
    if (!title || title === 'New chat' || title === 'New Session') return 'New chat';
    return title;
  };

  return (
    <aside 
      className={`h-screen bg-zinc-950/95 border-r border-zinc-800/80 flex flex-col justify-between p-3.5 z-30 shrink-0 select-none transition-all duration-300 ${
        isOpen ? 'w-72 md:w-80' : 'w-0 p-0 border-r-0 overflow-hidden'
      }`}
    >
      <div className="flex flex-col gap-3 overflow-hidden flex-1">
        
        {/* Brand Header with Brain Logo */}
        <div className="flex items-center justify-between px-1.5 pt-1 pb-1">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-500/20 via-sky-500/10 to-zinc-900 border border-cyan-500/30 flex items-center justify-center text-cyan-400 shadow-md shadow-cyan-950/30">
              <Brain className="w-4 h-4 text-cyan-400" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="text-sm font-bold tracking-tight text-white font-sans">
                  PRAHARI
                </span>
                <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-zinc-900 text-cyan-400 border border-zinc-800">
                  AI 3.2
                </span>
              </div>
              <p className="text-[10px] text-zinc-400 font-sans tracking-wide">
                Sovereign Safety Assistant
              </p>
            </div>
          </div>

          <button
            onClick={onToggleSidebar}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-900 transition-colors cursor-pointer"
            title="Collapse sidebar"
          >
            <PanelLeftClose className="w-4 h-4" />
          </button>
        </div>

        {/* New Chat Button (Modern AI Pill Style) */}
        <button
          onClick={onNewChat}
          className="w-full flex items-center justify-between py-2.5 px-3.5 rounded-xl bg-zinc-900 hover:bg-zinc-800/90 border border-zinc-800 hover:border-zinc-700 text-white font-medium text-xs shadow-sm transition-all group cursor-pointer"
        >
          <div className="flex items-center gap-2.5">
            <div className="w-5 h-5 rounded-lg bg-white text-zinc-950 flex items-center justify-center font-bold">
              <Plus className="w-3.5 h-3.5" />
            </div>
            <span className="font-semibold tracking-wide">New chat</span>
          </div>
          <span className="text-[10px] font-mono text-zinc-400 bg-zinc-800/80 px-1.5 py-0.5 rounded border border-zinc-700/50 group-hover:text-zinc-300">
            Ctrl+K
          </span>
        </button>

        {/* Search Bar for History */}
        {sessions.length > 2 && (
          <div className="relative px-0.5">
            <Search className="w-3.5 h-3.5 text-zinc-500 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search previous questions..."
              className="w-full bg-zinc-900/70 border border-zinc-800/80 rounded-lg pl-8 pr-3 py-1.5 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-zinc-600 font-sans"
            />
          </div>
        )}

        {/* Previous Questions & Chat History (Gemini / ChatGPT Style) */}
        <div className="flex-1 overflow-y-auto pr-1 space-y-4 pt-1">
          {sessions.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-48 text-center px-4 text-zinc-500">
              <MessageSquare className="w-7 h-7 text-zinc-700 mb-2 stroke-[1.5]" />
              <p className="text-xs font-medium text-zinc-400">No questions asked yet</p>
              <p className="text-[11px] text-zinc-500 mt-1 leading-relaxed">
                Ask a safety protocol or SOP question to start your history.
              </p>
            </div>
          ) : (
            Object.entries(grouped).map(([groupName, groupItems]) => {
              if (groupItems.length === 0) return null;
              return (
                <div key={groupName} className="space-y-1">
                  <span className="text-[10px] font-semibold text-zinc-500 uppercase tracking-wider px-2 block font-mono">
                    {groupName}
                  </span>
                  <div className="space-y-0.5">
                    {groupItems.map((session) => {
                      const isActive = session.id === activeSessionId;
                      const isEditing = session.id === editingSessionId;
                      const displayTitle = formatSessionTitle(session.title);

                      return (
                        <div
                          key={session.id}
                          onClick={() => onSelectSession?.(session.id)}
                          className={`group relative flex items-center justify-between px-2.5 py-2 rounded-xl text-xs transition-all cursor-pointer ${
                            isActive
                              ? 'bg-zinc-800 text-white font-medium shadow-sm border border-zinc-700/70'
                              : 'text-zinc-300 hover:bg-zinc-900 hover:text-zinc-100'
                          }`}
                        >
                          <div className="flex items-center gap-2.5 min-w-0 flex-1">
                            <MessageSquare className={`w-3.5 h-3.5 shrink-0 ${
                              isActive ? 'text-cyan-400' : 'text-zinc-500 group-hover:text-zinc-400'
                            }`} />
                            
                            {isEditing ? (
                              <input
                                type="text"
                                value={editTitle}
                                onChange={(e) => setEditTitle(e.target.value)}
                                onClick={(e) => e.stopPropagation()}
                                onKeyDown={(e) => {
                                  if (e.key === 'Enter') saveEditing(e, session.id);
                                  if (e.key === 'Escape') cancelEditing(e);
                                }}
                                autoFocus
                                className="w-full bg-zinc-950 px-1.5 py-0.5 rounded border border-cyan-500 text-xs text-white focus:outline-none"
                              />
                            ) : (
                              <span className="truncate text-xs tracking-tight" title={displayTitle}>
                                {displayTitle}
                              </span>
                            )}
                          </div>

                          {/* Action Buttons on Hover */}
                          <div className="flex items-center gap-1 shrink-0 ml-1.5">
                            {isEditing ? (
                              <>
                                <button
                                  onClick={(e) => saveEditing(e, session.id)}
                                  className="p-1 text-emerald-400 hover:text-emerald-300 hover:bg-zinc-700/60 rounded transition-colors"
                                  title="Save title"
                                >
                                  <Check className="w-3 h-3" />
                                </button>
                                <button
                                  onClick={cancelEditing}
                                  className="p-1 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-700/60 rounded transition-colors"
                                  title="Cancel"
                                >
                                  <X className="w-3 h-3" />
                                </button>
                              </>
                            ) : (
                              <div className="opacity-0 group-hover:opacity-100 flex items-center gap-0.5 transition-opacity">
                                <button
                                  onClick={(e) => startEditing(e, session)}
                                  className="p-1 text-zinc-400 hover:text-white hover:bg-zinc-700/50 rounded transition-colors"
                                  title="Rename question"
                                >
                                  <Edit2 className="w-3 h-3" />
                                </button>
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    if (window.confirm('Delete this conversation?')) {
                                      onDeleteSession?.(session.id);
                                    }
                                  }}
                                  className="p-1 text-zinc-400 hover:text-rose-400 hover:bg-zinc-700/50 rounded transition-colors"
                                  title="Delete question"
                                >
                                  <Trash2 className="w-3 h-3" />
                                </button>
                              </div>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Sleek Bottom Actions & Sovereign Status */}
      <div className="pt-3 border-t border-zinc-800/80 space-y-2">
        {/* Upload Knowledge Base Manual Shortcut */}
        <button
          onClick={onOpenUploadModal}
          className="w-full flex items-center justify-between px-3 py-2 rounded-xl bg-zinc-900/60 hover:bg-zinc-800/80 border border-zinc-800/70 text-xs text-zinc-300 transition-all cursor-pointer group"
          title="Upload safety manuals and SOPs to vector database"
        >
          <div className="flex items-center gap-2">
            <Upload className="w-3.5 h-3.5 text-zinc-400 group-hover:text-cyan-400" />
            <span className="font-medium">Ingest SOP Manual</span>
          </div>
          <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-zinc-800 text-zinc-400 border border-zinc-700/50">
            PDF/RAG
          </span>
        </button>

        {/* Offline Security Status Pill */}
        <div className="flex items-center justify-between px-3 py-2 rounded-xl bg-zinc-900/40 border border-zinc-800/50 text-[11px] font-mono text-zinc-400">
          <div className="flex items-center gap-1.5">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="text-zinc-300 font-sans text-xs">Offline Sovereign</span>
          </div>
          <span className="text-[10px] text-zinc-400">Llama 3.2</span>
        </div>

        {/* Replay Intro Link */}
        <div className="flex items-center justify-between px-2 pt-0.5">
          <button
            onClick={onReplayIntro}
            className="flex items-center gap-1.5 text-[11px] text-zinc-400 hover:text-zinc-200 transition-colors font-sans py-0.5"
            title="Replay intro animation"
          >
            <RotateCcw className="w-3 h-3" />
            <span>Replay Intro</span>
          </button>
          <span className="text-[10px] text-zinc-500 font-mono">
            MRPL v2.0
          </span>
        </div>
      </div>
    </aside>
  );
}
