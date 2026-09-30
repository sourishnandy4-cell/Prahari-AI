import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Sparkles, 
  ExternalLink, 
  Clipboard, 
  Check, 
  AlertCircle, 
  X, 
  Cpu, 
  Globe, 
  ShieldCheck, 
  Key, 
  CheckCircle2, 
  Loader2,
  Zap,
  Info,
  Wifi,
  WifiOff
} from 'lucide-react';

export default function AIModelSettingsModal({ 
  isOpen, 
  onClose, 
  apiUrl,
  currentModel,
  onModelChanged
}) {
  const [activeModel, setActiveModel] = useState(currentModel || 'llama3.2-web');
  const [apiKey, setApiKey] = useState('');
  const [maskedKey, setMaskedKey] = useState(null);
  const [isConfigured, setIsConfigured] = useState(false);
  const [isOnline, setIsOnline] = useState(true);
  const [ollamaReady, setOllamaReady] = useState(true);
  const [verifying, setVerifying] = useState(false);
  const [verifyResult, setVerifyResult] = useState(null);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [copyFeedback, setCopyFeedback] = useState(false);
  const [modelsList, setModelsList] = useState([]);

  // Fetch current config on open
  useEffect(() => {
    if (!isOpen) return;

    const fetchConfig = async () => {
      try {
        const targetUrl = apiUrl ? apiUrl('/api/settings/ai-config') : '/api/settings/ai-config';
        const res = await fetch(targetUrl);
        if (res.ok) {
          const data = await res.json();
          setActiveModel(data.active_model || 'llama3.2-web');
          setIsConfigured(Boolean(data.gemini_configured));
          setMaskedKey(data.gemini_masked_key || null);
          setIsOnline(Boolean(data.is_online));
          setOllamaReady(Boolean(data.ollama_ready));
          if (data.available_models) {
            setModelsList(data.available_models);
          }
        }
      } catch (err) {
        console.warn('Failed to load AI config:', err);
      }
    };

    fetchConfig();
    setVerifyResult(null);
    setSaveSuccess(false);
  }, [isOpen, apiUrl]);

  if (!isOpen) return null;

  // Handle paste from clipboard
  const handlePasteFromClipboard = async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (text && text.trim()) {
        const cleaned = text.trim();
        setApiKey(cleaned);
        setCopyFeedback(true);
        setTimeout(() => setCopyFeedback(false), 2000);
        // Clear any previous error
        setVerifyResult(null);
      }
    } catch (err) {
      alert('Please grant clipboard permission or paste manually into the input box.');
    }
  };

  // Test / Verify Gemini Key
  const handleVerifyKey = async () => {
    const keyToTest = apiKey.trim();
    if (!keyToTest) {
      setVerifyResult({ valid: false, error: 'Please paste or enter your Gemini API Key first.' });
      return;
    }

    setVerifying(true);
    setVerifyResult(null);

    try {
      const targetUrl = apiUrl ? apiUrl('/api/settings/verify-gemini-token') : '/api/settings/verify-gemini-token';
      const res = await fetch(targetUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ gemini_api_key: keyToTest }),
      });
      const data = await res.json();
      setVerifyResult(data);
      if (data.valid) {
        setIsConfigured(true);
      }
    } catch (err) {
      setVerifyResult({
        valid: false,
        error: 'Unable to reach backend verification service. Check internet connection.'
      });
    } finally {
      setVerifying(false);
    }
  };

  // Save Config & Model
  const handleSave = async () => {
    setSaving(true);
    setSaveSuccess(false);

    try {
      const targetUrl = apiUrl ? apiUrl('/api/settings/ai-config') : '/api/settings/ai-config';
      const payload = {
        model: activeModel,
      };
      if (apiKey.trim()) {
        payload.gemini_api_key = apiKey.trim();
      }

      const res = await fetch(targetUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        const data = await res.json();
        setSaveSuccess(true);
        if (onModelChanged) {
          onModelChanged(data.active_model);
        }
        setTimeout(() => {
          onClose();
        }, 1200);
      }
    } catch (err) {
      console.error('Failed to save AI config:', err);
    } finally {
      setSaving(false);
    }
  };

  const openGeminiPortal = () => {
    window.open('https://aistudio.google.com/app/apikey', '_blank', 'noopener,noreferrer');
  };

  return (
    <AnimatePresence>
      <div 
        className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/80 backdrop-blur-md select-none overflow-y-auto"
        onClick={onClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 15 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 15 }}
          className="relative w-full max-w-2xl bg-zinc-900 border border-zinc-700/80 p-5 sm:p-7 rounded-3xl shadow-2xl overflow-hidden my-auto max-h-[92vh] flex flex-col"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-center justify-between pb-4 border-b border-zinc-800 shrink-0">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 shadow-inner">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-base sm:text-lg font-bold text-zinc-100 flex items-center gap-2">
                  AI Model & Token Settings
                </h2>
                <p className="text-xs text-zinc-400 mt-0.5">
                  Choose between Google Gemini Cloud AI and Sovereign Offline LLaMA 3.2
                </p>
              </div>
            </div>

            <button
              onClick={onClose}
              className="p-2 rounded-xl text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 transition-colors cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Scrollable Content Body */}
          <div className="flex-1 overflow-y-auto py-4 space-y-5 pr-1 no-scrollbar">
            
            {/* Real-time Connectivity Bar */}
            <div className="flex flex-wrap items-center justify-between gap-2 p-3 rounded-2xl bg-zinc-950/80 border border-zinc-800 text-xs">
              <div className="flex items-center gap-2">
                {isOnline ? (
                  <span className="flex items-center gap-1.5 text-emerald-400 font-medium">
                    <Wifi className="w-4 h-4 text-emerald-400" />
                    Internet Connected (Online Mode Ready)
                  </span>
                ) : (
                  <span className="flex items-center gap-1.5 text-amber-400 font-medium">
                    <WifiOff className="w-4 h-4 text-amber-400" />
                    Device Offline (Automatic Offline Engine Active)
                  </span>
                )}
              </div>

              <div className="flex items-center gap-1.5 text-zinc-400 font-mono text-[11px]">
                <Cpu className="w-3.5 h-3.5 text-cyan-400" />
                <span>Local Neural: {ollamaReady ? '🟢 LLaMA 3.2 Ready' : '🟡 Sovereign Engine'}</span>
              </div>
            </div>

            {/* ── 1. GOOGLE GEMINI FREE TOKEN FETCHER SECTION ── */}
            <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-br from-cyan-950/40 via-zinc-900 to-blue-950/30 border border-cyan-500/30 space-y-4 shadow-lg">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-xl bg-cyan-500/20 border border-cyan-400/30 flex items-center justify-center text-cyan-300 shrink-0 mt-0.5">
                    <Key className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-sm font-bold text-zinc-100">
                        Google Gemini API Token (100% Free)
                      </h3>
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                        15 RPM / 1,500 req/day
                      </span>
                    </div>
                    <p className="text-xs text-zinc-400 mt-1 leading-relaxed">
                      Google provides free API tokens for Gemini with no credit card required. Click the link to generate your key, then click Paste.
                    </p>
                  </div>
                </div>

                {/* 1-Click Link Button */}
                <button
                  type="button"
                  onClick={openGeminiPortal}
                  className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-zinc-950 text-xs font-bold transition-all shadow-md hover:shadow-cyan-500/25 shrink-0 cursor-pointer active:scale-95"
                >
                  <span>1. Get Free Key ↗</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </button>
              </div>

              {/* Paste & Input Field */}
              <div className="space-y-2">
                <label className="text-[11px] font-medium text-zinc-300 flex items-center justify-between">
                  <span>Enter or Paste Gemini Key (starts with <code className="text-cyan-300">AIzaSy...</code>)</span>
                  {maskedKey && (
                    <span className="text-[10px] text-emerald-400 font-mono">
                      Current Key: {maskedKey}
                    </span>
                  )}
                </label>

                <div className="flex flex-col sm:flex-row gap-2">
                  <div className="relative flex-1">
                    <input
                      type="password"
                      value={apiKey}
                      onChange={(e) => {
                        setApiKey(e.target.value);
                        setVerifyResult(null);
                      }}
                      placeholder={maskedKey ? "Leave blank to keep current key, or paste new key" : "Paste your Google Gemini API key here"}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-zinc-950 border border-zinc-700/80 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-cyan-500 transition-colors font-mono"
                    />
                  </div>

                  {/* 1-Click Paste from Clipboard Button */}
                  <button
                    type="button"
                    onClick={handlePasteFromClipboard}
                    className={`flex items-center justify-center gap-1.5 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all cursor-pointer shrink-0 border ${
                      copyFeedback
                        ? 'bg-emerald-600 text-white border-emerald-500'
                        : 'bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border-zinc-700'
                    }`}
                    title="Paste directly from your clipboard"
                  >
                    {copyFeedback ? <Check className="w-3.5 h-3.5" /> : <Clipboard className="w-3.5 h-3.5 text-cyan-400" />}
                    <span>{copyFeedback ? 'Pasted!' : '2. Paste Key'}</span>
                  </button>

                  {/* Test & Verify Button */}
                  <button
                    type="button"
                    onClick={handleVerifyKey}
                    disabled={verifying || (!apiKey.trim() && !maskedKey)}
                    className="flex items-center justify-center gap-1.5 px-3.5 py-2.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 text-xs font-semibold text-zinc-200 disabled:opacity-40 disabled:cursor-not-allowed transition-all cursor-pointer shrink-0"
                  >
                    {verifying ? (
                      <>
                        <Loader2 className="w-3.5 h-3.5 animate-spin text-cyan-400" />
                        <span>Testing...</span>
                      </>
                    ) : (
                      <>
                        <Zap className="w-3.5 h-3.5 text-amber-400" />
                        <span>3. Test Key</span>
                      </>
                    )}
                  </button>
                </div>

                {/* Verification Result Feedback */}
                {verifyResult && (
                  <motion.div
                    initial={{ opacity: 0, y: -5 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`p-3 rounded-xl border text-xs flex items-start gap-2.5 ${
                      verifyResult.valid
                        ? 'bg-emerald-950/40 border-emerald-500/40 text-emerald-300'
                        : 'bg-rose-950/40 border-rose-500/40 text-rose-300'
                    }`}
                  >
                    {verifyResult.valid ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                    ) : (
                      <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                    )}
                    <div className="flex-1">
                      <p className="font-semibold">
                        {verifyResult.valid ? verifyResult.message : 'Verification Failed'}
                      </p>
                      {verifyResult.error && (
                        <p className="text-[11px] opacity-90 mt-0.5 font-sans">
                          {verifyResult.error}
                        </p>
                      )}
                      {verifyResult.free_tier_limits && (
                        <p className="text-[10px] text-emerald-400 font-mono mt-1">
                          Free Quota: {verifyResult.free_tier_limits}
                        </p>
                      )}
                    </div>
                  </motion.div>
                )}
              </div>
            </div>

            {/* ── 2. MODEL SELECTION CARDS ── */}
            <div className="space-y-3">
              <label className="text-xs font-semibold text-zinc-200 uppercase tracking-wider flex items-center gap-1.5">
                <span>Select Active AI Model</span>
                <Info className="w-3 h-3 text-zinc-400" />
              </label>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {/* Option 1: Gemini 1.5 Flash */}
                <div
                  onClick={() => setActiveModel('gemini-1.5-flash')}
                  className={`p-4 rounded-2xl border transition-all cursor-pointer relative flex flex-col justify-between ${
                    activeModel === 'gemini-1.5-flash'
                      ? 'bg-cyan-500/10 border-cyan-500 shadow-md shadow-cyan-500/10 ring-1 ring-cyan-500/40'
                      : 'bg-zinc-950/60 border-zinc-800 hover:border-zinc-700'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                        ⚡ Ultra-Fast Cloud
                      </span>
                      {activeModel === 'gemini-1.5-flash' && (
                        <div className="w-4 h-4 rounded-full bg-cyan-500 text-zinc-950 flex items-center justify-center">
                          <Check className="w-3 h-3 stroke-[3]" />
                        </div>
                      )}
                    </div>
                    <h4 className="text-sm font-bold text-zinc-100">Google Gemini 1.5 Flash</h4>
                    <p className="text-xs text-zinc-400 mt-1 leading-relaxed">
                      Google's fast multimodal model with 1M context. Ideal for real-time online queries.
                    </p>
                  </div>
                  <div className="mt-3 pt-2.5 border-t border-zinc-800/80 flex items-center justify-between text-[11px] text-zinc-500">
                    <span>Key: {isConfigured || apiKey ? '✅ Configured' : '⚠️ Free Key Needed'}</span>
                    <span className="text-cyan-400 font-mono text-[10px]">1,500 req/day</span>
                  </div>
                </div>

                {/* Option 2: Gemini 1.5 Pro */}
                <div
                  onClick={() => setActiveModel('gemini-1.5-pro')}
                  className={`p-4 rounded-2xl border transition-all cursor-pointer relative flex flex-col justify-between ${
                    activeModel === 'gemini-1.5-pro'
                      ? 'bg-purple-500/10 border-purple-500 shadow-md shadow-purple-500/10 ring-1 ring-purple-500/40'
                      : 'bg-zinc-950/60 border-zinc-800 hover:border-zinc-700'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30">
                        🧠 Deep Reasoning
                      </span>
                      {activeModel === 'gemini-1.5-pro' && (
                        <div className="w-4 h-4 rounded-full bg-purple-500 text-zinc-950 flex items-center justify-center">
                          <Check className="w-3 h-3 stroke-[3]" />
                        </div>
                      )}
                    </div>
                    <h4 className="text-sm font-bold text-zinc-100">Google Gemini 1.5 Pro</h4>
                    <p className="text-xs text-zinc-400 mt-1 leading-relaxed">
                      Highest reasoning quality for comparing multiple IS standards and complex QCO mandates.
                    </p>
                  </div>
                  <div className="mt-3 pt-2.5 border-t border-zinc-800/80 flex items-center justify-between text-[11px] text-zinc-500">
                    <span>Key: {isConfigured || apiKey ? '✅ Configured' : '⚠️ Free Key Needed'}</span>
                    <span className="text-purple-400 font-mono text-[10px]">Cloud AI</span>
                  </div>
                </div>

                {/* Option 3: Web-Augmented LLaMA 3.2 */}
                <div
                  onClick={() => setActiveModel('llama3.2-web')}
                  className={`p-4 rounded-2xl border transition-all cursor-pointer relative flex flex-col justify-between ${
                    activeModel === 'llama3.2-web'
                      ? 'bg-emerald-500/10 border-emerald-500 shadow-md shadow-emerald-500/10 ring-1 ring-emerald-500/40'
                      : 'bg-zinc-950/60 border-zinc-800 hover:border-zinc-700'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                        🌐 Live Web + Neural
                      </span>
                      {activeModel === 'llama3.2-web' && (
                        <div className="w-4 h-4 rounded-full bg-emerald-500 text-zinc-950 flex items-center justify-center">
                          <Check className="w-3 h-3 stroke-[3]" />
                        </div>
                      )}
                    </div>
                    <h4 className="text-sm font-bold text-zinc-100">Web-Augmented LLaMA 3.2</h4>
                    <p className="text-xs text-zinc-400 mt-1 leading-relaxed">
                      Fetches live web news on BIS and feeds context to local LLaMA 3.2. 100% Free, no key required.
                    </p>
                  </div>
                  <div className="mt-3 pt-2.5 border-t border-zinc-800/80 flex items-center justify-between text-[11px] text-zinc-500">
                    <span className="text-emerald-400 font-medium">No Key Needed</span>
                    <span className="font-mono text-[10px]">Hybrid Search</span>
                  </div>
                </div>

                {/* Option 4: Offline LLaMA 3.2 */}
                <div
                  onClick={() => setActiveModel('llama3.2-offline')}
                  className={`p-4 rounded-2xl border transition-all cursor-pointer relative flex flex-col justify-between ${
                    activeModel === 'llama3.2-offline'
                      ? 'bg-amber-500/10 border-amber-500 shadow-md shadow-amber-500/10 ring-1 ring-amber-500/40'
                      : 'bg-zinc-950/60 border-zinc-800 hover:border-zinc-700'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">
                        🔒 100% Air-Gapped
                      </span>
                      {activeModel === 'llama3.2-offline' && (
                        <div className="w-4 h-4 rounded-full bg-amber-500 text-zinc-950 flex items-center justify-center">
                          <Check className="w-3 h-3 stroke-[3]" />
                        </div>
                      )}
                    </div>
                    <h4 className="text-sm font-bold text-zinc-100">Offline LLaMA 3.2</h4>
                    <p className="text-xs text-zinc-400 mt-1 leading-relaxed">
                      Runs 100% locally on your CPU/GPU with local ChromaDB. Completely private and works with zero internet.
                    </p>
                  </div>
                  <div className="mt-3 pt-2.5 border-t border-zinc-800/80 flex items-center justify-between text-[11px] text-zinc-500">
                    <span className="text-amber-400 font-medium">Zero Internet Needed</span>
                    <span className="font-mono text-[10px]">Sovereign Local</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Note on Automatic Fallback */}
            <div className="p-3.5 rounded-2xl bg-zinc-950/60 border border-zinc-800 text-[11px] text-zinc-400 flex items-start gap-2.5">
              <ShieldCheck className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
              <p>
                <strong className="text-zinc-200">Resilient Dual-Engine Guarantee:</strong> If the device loses internet connection or Gemini API reaches quota, PRAHARI AI automatically and silently falls back to the offline local LLaMA 3.2 engine without interrupting your workflow.
              </p>
            </div>

          </div>

          {/* Footer Controls */}
          <div className="flex items-center justify-between pt-4 border-t border-zinc-800 shrink-0">
            <div className="text-xs text-zinc-400 font-mono">
              Active: <span className="text-cyan-400 font-bold">{activeModel}</span>
            </div>

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-xs font-semibold text-zinc-300 transition-colors cursor-pointer"
              >
                Cancel
              </button>

              <button
                type="button"
                onClick={handleSave}
                disabled={saving}
                className="flex items-center gap-1.5 px-5 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-zinc-950 text-xs font-bold transition-all shadow-md hover:shadow-cyan-500/25 cursor-pointer disabled:opacity-50"
              >
                {saving ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>Saving...</span>
                  </>
                ) : saveSuccess ? (
                  <>
                    <Check className="w-3.5 h-3.5 stroke-[3]" />
                    <span>Saved & Applied!</span>
                  </>
                ) : (
                  <span>Save & Apply</span>
                )}
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
