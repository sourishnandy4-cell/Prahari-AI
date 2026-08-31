import React, { useState, useEffect, useRef } from 'react';
import { AnimatePresence } from 'framer-motion';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import FileUploadModal from './components/FileUploadModal';
import SplashScreen from './components/SplashScreen';
import GetStartedScreen from './components/GetStartedScreen';
import { useIsMobile } from './hooks/useMediaQuery';
import { useSwipeGesture } from './hooks/useSwipeGesture';

// ── API base URL: auto-detects Electron file:// protocol, mobile LAN, and web proxy
const API_BASE = (
  import.meta.env.VITE_API_BASE_URL ||
  (typeof window !== 'undefined' && (window.location.protocol === 'file:' || !window.location.host)
    ? 'http://127.0.0.1:8000'
    : '')
).replace(/\/$/, '');

/** Build API url: works seamlessly across Electron (file://), mobile APK, and Vite proxy */
function apiUrl(path) {
  return `${API_BASE}${path}`;
}

export default function App() {
  const [sessions, setSessions] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [selectedQuery, setSelectedQuery] = useState('');
  const [indexedFiles, setIndexedFiles] = useState([]);
  const abortRef = useRef(null);

  // ── Responsive: default sidebar closed on mobile ─────────────────────────
  const isMobile = useIsMobile();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  // Close sidebar by default when screen shrinks to mobile
  useEffect(() => {
    if (isMobile) setIsSidebarOpen(false);
    else setIsSidebarOpen(true);
  }, [isMobile]);

  // ── Swipe gesture: right-edge swipe opens sidebar on mobile ──────────────
  useSwipeGesture({
    onSwipeRight: () => { if (isMobile) setIsSidebarOpen(true); },
    onSwipeLeft:  () => { if (isMobile) setIsSidebarOpen(false); },
  });

  // App stage state machine: 'splash' -> 'get_started' -> 'app'
  const [stage, setStage] = useState(() => {
    if (!sessionStorage.getItem('aegis_splash_shown')) return 'splash';
    if (!sessionStorage.getItem('aegis_onboarded')) return 'get_started';
    return 'app';
  });

  const handleSplashComplete = () => {
    sessionStorage.setItem('aegis_splash_shown', '1');
    setStage('get_started');
  };

  const handleGetStartedClick = () => {
    sessionStorage.setItem('aegis_onboarded', '1');
    setStage('app');
  };

  const handleReplayIntro = () => {
    sessionStorage.removeItem('aegis_splash_shown');
    sessionStorage.removeItem('aegis_onboarded');
    setStage('splash');
  };

  // ── Fetch all chat sessions ───────────────────────────────────────────────
  const fetchSessions = async () => {
    try {
      const res = await fetch(apiUrl('/api/sessions'));
      if (res.ok) {
        const data = await res.json();
        const list = Array.isArray(data) ? data : (data.sessions || []);
        setSessions(list);
        return list;
      }
    } catch {
      // Offline fallback
    }
    return [];
  };

  // ── Create a new chat session ────────────────────────────────────────────
  const handleNewChat = async () => {
    if (abortRef.current) {
      abortRef.current.close();
    }
    setMessages([]);
    setLoading(false);
    setIsStreaming(false);
    // Close sidebar on mobile after starting new chat
    if (isMobile) setIsSidebarOpen(false);

    try {
      const res = await fetch(apiUrl('/api/sessions'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: 'New chat' }),
      });
      if (res.ok) {
        const newSess = await res.json();
        setSessionId(newSess.id);
        setSessions((prev) => [newSess, ...prev.filter((s) => s.id !== newSess.id)]);
        return newSess.id;
      }
    } catch {
      const localId = Date.now().toString();
      setSessionId(localId);
      setSessions((prev) => [{ id: localId, title: 'New chat', created_at: new Date().toISOString() }, ...prev]);
      return localId;
    }
  };

  // ── Select and load a previous session ───────────────────────────────────
  const handleSelectSession = async (id) => {
    if (abortRef.current) {
      abortRef.current.close();
    }
    setSessionId(id);
    setLoading(false);
    setIsStreaming(false);
    // Close sidebar on mobile after selecting session
    if (isMobile) setIsSidebarOpen(false);

    try {
      const res = await fetch(apiUrl(`/api/sessions/${id}/messages`));
      if (res.ok) {
        const data = await res.json();
        const rawMsgs = data.messages || [];
        const formatted = rawMsgs.map((m) => ({
          id: m.id,
          sender: m.role === 'user' ? 'user' : 'bot',
          text: m.content,
          citations: m.citations || [],
          metadata: m.metadata || null,
          timestamp: new Date(m.created_at || Date.now()).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        }));
        setMessages(formatted);
      } else {
        setMessages([]);
      }
    } catch {
      setMessages([]);
    }
  };

  // ── Delete a session ──────────────────────────────────────────────────────
  const handleDeleteSession = async (id) => {
    try {
      await fetch(apiUrl(`/api/sessions/${id}`), { method: 'DELETE' });
    } catch {}

    setSessions((prev) => prev.filter((s) => s.id !== id));
    if (sessionId === id) {
      handleNewChat();
    }
  };

  // ── Rename a session ──────────────────────────────────────────────────────
  const handleRenameSession = async (id, newTitle) => {
    try {
      await fetch(apiUrl(`/api/sessions/${id}`), {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTitle }),
      });
    } catch {}

    setSessions((prev) =>
      prev.map((s) => (s.id === id ? { ...s, title: newTitle } : s))
    );
  };

  // ── On mount: Initialize sessions and documents ───────────────────────────
  useEffect(() => {
    const init = async () => {
      const existingSessions = await fetchSessions();
      if (existingSessions.length > 0) {
        handleSelectSession(existingSessions[0].id);
      } else {
        handleNewChat();
      }

      try {
        const docRes = await fetch(apiUrl('/api/documents'));
        if (docRes.ok) {
          const data = await docRes.json();
          const docs = Array.isArray(data) ? data : (data.documents || []);
          setIndexedFiles(docs);
        }
      } catch {}
    };
    init();
  }, []);

  // ── Global Keyboard Shortcut: Ctrl+K / Cmd+K for New Chat ─────────────────
  useEffect(() => {
    const handleGlobalKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        handleNewChat();
      }
    };
    window.addEventListener('keydown', handleGlobalKeyDown);
    return () => window.removeEventListener('keydown', handleGlobalKeyDown);
  }, []);

  const refreshDocuments = async () => {
    try {
      const res = await fetch(apiUrl('/api/documents'));
      if (res.ok) {
        const data = await res.json();
        const docs = Array.isArray(data) ? data : (data.documents || []);
        setIndexedFiles(docs);
      }
    } catch (e) {
      console.error('Error refreshing documents', e);
    }
  };

  // ── Handle sending message ───────────────────────────────────────────────
  const handleSendMessage = async (query, useStream = true, attachments = []) => {
    let currentSessionId = sessionId;
    if (!currentSessionId) {
      currentSessionId = await handleNewChat();
    }

    const userMsgId = Date.now().toString();
    const botMsgId = (Date.now() + 1).toString();

    // Auto-rename session to the user's question if session is default/untitled
    const currentSess = sessions.find((s) => s.id === currentSessionId);
    if (!currentSess || currentSess.title === 'New chat' || currentSess.title.startsWith('Session ')) {
      const autoTitle = (query || (attachments[0]?.name ? `File: ${attachments[0].name}` : 'Safety Analysis')).slice(0, 42);
      handleRenameSession(currentSessionId, autoTitle);
    }

    // Process file attachments (e.g. upload documents to ChromaDB)
    if (attachments.length > 0) {
      for (const att of attachments) {
        if (att.file && (att.name.endsWith('.pdf') || att.name.endsWith('.txt') || att.name.endsWith('.md'))) {
          try {
            const formData = new FormData();
            formData.append('file', att.file);
            fetch(apiUrl('/api/upload'), { method: 'POST', body: formData }).then(() => refreshDocuments());
          } catch (e) {
            console.error('Error auto-uploading attached doc', e);
          }
        }
      }
    }

    const userMessage = {
      id: userMsgId,
      sender: 'user',
      text: query,
      attachments: attachments.map((a) => ({
        name: a.name,
        size: a.size,
        type: a.type,
        previewUrl: a.previewUrl,
        data: a.data,
      })),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    // Build context query if attachments exist
    let augmentedQuery = query;
    if (attachments.length > 0) {
      const attNames = attachments.map((a) => a.name).join(', ');
      augmentedQuery = query ? `${query}\n\n[Context: User attached ${attNames}]` : `Please analyze the attached file: ${attNames}`;
    }

    if (useStream) {
      setIsStreaming(true);

      const initialBotMessage = {
        id: botMsgId,
        sender: 'bot',
        text: '',
        citations: [],
        metadata: null,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        streaming: true,
      };
      setMessages((prev) => [...prev, initialBotMessage]);

      try {
        const url = apiUrl(`/api/stream?query=${encodeURIComponent(augmentedQuery)}${currentSessionId ? `&session_id=${currentSessionId}` : ''}`);
        const eventSource = new EventSource(url);
        abortRef.current = eventSource;

        let accumulatedText = '';
        let citations = [];
        let meta = null;

        eventSource.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);

            if (data.type === 'token') {
              const textChunk = data.text !== undefined ? data.text : (data.token !== undefined ? data.token : '');
              accumulatedText += textChunk;
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === botMsgId
                    ? { ...msg, text: accumulatedText, streaming: true }
                    : msg
                )
              );
            } else if (data.type === 'citation' || data.type === 'citations') {
              const cites = data.citations || (data.citation ? [data.citation] : [data]);
              citations.push(...cites);
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === botMsgId
                    ? { ...msg, citations: [...citations] }
                    : msg
                )
              );
            } else if (data.type === 'meta') {
              meta = data;
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === botMsgId
                    ? { ...msg, metadata: meta }
                    : msg
                )
              );
            } else if (data.type === 'done') {
              eventSource.close();
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === botMsgId
                    ? { ...msg, streaming: false, text: accumulatedText }
                    : msg
                )
              );
              setLoading(false);
              setIsStreaming(false);
              fetchSessions();
            } else if (data.type === 'error') {
              eventSource.close();
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === botMsgId
                    ? {
                        ...msg,
                        streaming: false,
                        text: data.error || 'An error occurred during generation.',
                      }
                    : msg
                )
              );
              setLoading(false);
              setIsStreaming(false);
            }
          } catch (err) {
            console.error('Error parsing SSE event', err);
          }
        };

        eventSource.onerror = (err) => {
          console.error('EventSource error', err);
          eventSource.close();
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === botMsgId
                ? {
                    ...msg,
                    streaming: false,
                    text:
                      accumulatedText ||
                      'Stream disconnected. Please ensure the local Ollama and FastAPI backend are running.',
                  }
                : msg
            )
          );
          setLoading(false);
          setIsStreaming(false);
        };
      } catch (err) {
        console.error('Streaming setup error', err);
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === botMsgId
              ? {
                  ...msg,
                  streaming: false,
                  text: 'Failed to initialize SSE stream. Ensure FastAPI backend is online.',
                }
              : msg
          )
        );
        setLoading(false);
        setIsStreaming(false);
      }
    } else {
      try {
        const res = await fetch(apiUrl('/api/chat'), {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query: augmentedQuery,
            session_id: currentSessionId,
            use_agentic: true,
          }),
        });

        if (res.ok) {
          const data = await res.json();
          const botMessage = {
            id: botMsgId,
            sender: 'bot',
            text: data.answer,
            citations: data.citations || [],
            metadata: {
              mode: data.mode,
              rewritten_query: data.rewritten_query,
              hops: data.hops,
              latency_ms: data.latency_ms,
              execution_trace: data.execution_trace,
            },
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          };
          setMessages((prev) => [...prev, botMessage]);
          fetchSessions();
        } else {
          const errData = await res.json().catch(() => ({}));
          const errorMessage = {
            id: botMsgId,
            sender: 'bot',
            text: `Agent Error: ${errData.detail || 'Failed to retrieve grounded answer from local LLM.'}`,
            citations: [],
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          };
          setMessages((prev) => [...prev, errorMessage]);
        }
      } catch (err) {
        const errorMessage = {
          id: botMsgId,
          sender: 'bot',
          text: 'Network Error: Cannot connect to Aegis AI backend. Please verify FastAPI is running.',
          citations: [],
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setLoading(false);
      }
    }
  };

  const handleClearChat = async () => {
    if (sessionId) {
      try {
        await fetch(apiUrl(`/api/sessions/${sessionId}/messages`), { method: 'DELETE' });
      } catch {}
    }
    setMessages([]);
  };

  const handleIngestSuccess = async () => {
    await refreshDocuments();
  };

  return (
    <>
      <AnimatePresence mode="wait">
        {/* 1. Splash Screen */}
        {stage === 'splash' && (
          <SplashScreen key="splash-view" onComplete={handleSplashComplete} />
        )}

        {/* 2. Get Started Page */}
        {stage === 'get_started' && (
          <GetStartedScreen key="get-started-view" onGetStarted={handleGetStartedClick} />
        )}
      </AnimatePresence>

      {/* 3. Main Dashboard */}
      <div className={`flex h-screen w-screen bg-zinc-950 text-zinc-100 overflow-hidden font-sans transition-opacity duration-300 ${
        stage !== 'app' ? 'opacity-0 pointer-events-none fixed inset-0' : 'opacity-100'
      }`}>
        {/* Mobile sidebar backdrop overlay — tap to close */}
        {isMobile && isSidebarOpen && (
          <div
            className="sidebar-backdrop"
            onClick={() => setIsSidebarOpen(false)}
            aria-label="Close sidebar"
          />
        )}

        <Sidebar
          isOpen={isSidebarOpen}
          isMobile={isMobile}
          onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
          onNewChat={handleNewChat}
          sessions={sessions}
          activeSessionId={sessionId}
          onSelectSession={handleSelectSession}
          onDeleteSession={handleDeleteSession}
          onRenameSession={handleRenameSession}
          onOpenUploadModal={() => setIsUploadModalOpen(true)}
          onReplayIntro={handleReplayIntro}
        />

        <ChatWindow
          messages={messages}
          onSendMessage={handleSendMessage}
          loading={loading}
          isStreaming={isStreaming}
          onClearChat={handleClearChat}
          selectedQuery={selectedQuery}
          sessionId={sessionId}
          isSidebarOpen={isSidebarOpen}
          isMobile={isMobile}
          onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
          onNewChat={handleNewChat}
        />

        <FileUploadModal
          isOpen={isUploadModalOpen}
          onClose={() => setIsUploadModalOpen(false)}
          onIngestSuccess={handleIngestSuccess}
          indexedFiles={indexedFiles}
          apiUrl={apiUrl}
        />
      </div>
    </>
  );
}
