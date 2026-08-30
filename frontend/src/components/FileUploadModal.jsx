import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { UploadCloud, FileCheck, X, Loader2, AlertCircle, Database } from 'lucide-react';

export default function FileUploadModal({ isOpen, onClose, onIngestSuccess, indexedFiles }) {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [uploadSuccess, setUploadSuccess] = useState(null);
  const [uploadProgress, setUploadProgress] = useState('');

  if (!isOpen) return null;

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') setDragActive(true);
    else if (e.type === 'dragleave') setDragActive(false);
  };

  const processFile = async (file) => {
    if (!file.name.endsWith('.pdf')) {
      setErrorMsg('Only PDF refinery manuals are supported.');
      return;
    }

    setUploading(true);
    setErrorMsg('');
    setUploadSuccess(null);
    setUploadProgress('Uploading file...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploadProgress('Extracting text from PDF...');
      const response = await fetch('/api/upload', { method: 'POST', body: formData });
      const data = await response.json();

      if (response.ok && data.status === 'success') {
        setUploadProgress('');
        setUploadSuccess(data);
        await onIngestSuccess(data);
      } else {
        setErrorMsg(data.detail || 'Failed to ingest PDF manual.');
        setUploadProgress('');
      }
    } catch (err) {
      setErrorMsg('Network error. Verify local FastAPI backend is online (http://localhost:8000).');
      setUploadProgress('');
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files?.[0]) processFile(e.dataTransfer.files[0]);
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files?.[0]) processFile(e.target.files[0]);
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md select-none">
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 15 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 15 }}
          className="relative w-full max-w-lg bg-zinc-900 border border-zinc-800 p-6 rounded-2xl shadow-2xl overflow-hidden"
        >
          {/* Header */}
          <div className="flex items-center justify-between pb-4 border-b border-zinc-800">
            <div className="flex items-center gap-2.5">
              <Database className="w-4 h-4 text-white" />
              <h2 className="text-sm font-semibold text-white tracking-wide">Ingest Technical Document (PDF)</h2>
            </div>
            <button
              onClick={onClose}
              className="p-1 rounded-md hover:bg-zinc-800 text-zinc-400 hover:text-white transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Drop Zone */}
          <div className="mt-5">
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              className={`relative border-2 border-dashed rounded-xl p-7 text-center transition-all cursor-pointer ${
                dragActive
                  ? 'border-white bg-zinc-800/80 scale-[1.01]'
                  : 'border-zinc-700/80 hover:border-zinc-500 bg-zinc-950/40'
              }`}
            >
              <input
                type="file"
                accept=".pdf"
                onChange={handleChange}
                disabled={uploading}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
              />

              <div className="flex flex-col items-center justify-center gap-2 pointer-events-none">
                {uploading ? (
                  <Loader2 className="w-8 h-8 text-white animate-spin my-1" />
                ) : (
                  <UploadCloud className="w-8 h-8 text-zinc-400 my-1" />
                )}

                <p className="text-xs font-medium text-zinc-200">
                  {uploading ? uploadProgress : 'Drop SOP manual PDF here, or click to browse'}
                </p>
                <p className="text-[10px] text-zinc-500 font-mono">
                  Extracts text, builds ChromaDB vector embeddings
                </p>
              </div>
            </div>
          </div>

          {/* Error display */}
          {errorMsg && (
            <div className="mt-4 p-3 rounded-lg bg-zinc-950 border border-red-500/40 text-red-400 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Success summary */}
          {uploadSuccess && (
            <div className="mt-4 p-3.5 rounded-lg bg-zinc-950 border border-zinc-700 text-xs space-y-1">
              <div className="flex items-center gap-2 text-white font-medium">
                <FileCheck className="w-4 h-4 text-emerald-400" />
                <span>Successfully Indexed: {uploadSuccess.filename}</span>
              </div>
              <div className="flex gap-4 text-[10px] text-zinc-400 font-mono pt-1">
                <span>Chunks: <b className="text-white">{uploadSuccess.total_chunks}</b></span>
                <span>Size: <b className="text-white">{uploadSuccess.file_size_kb} KB</b></span>
              </div>
            </div>
          )}

          {/* Footer */}
          <div className="mt-6 flex justify-end gap-2.5">
            <button
              onClick={onClose}
              className="px-4 py-2 text-xs font-medium rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 transition-colors"
            >
              Close
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
