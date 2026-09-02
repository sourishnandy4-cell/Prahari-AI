import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Brain } from 'lucide-react';
import FluidSmokeCanvas from './FluidSmokeCanvas';

export default function GetStartedScreen({ onGetStarted }) {
  const [isBursting, setIsBursting] = useState(false);

  const handleClick = () => {
    if (isBursting) return;
    setIsBursting(true);
    setTimeout(() => {
      onGetStarted?.();
    }, 1700);
  };

  return (
    <motion.div
      key="get-started-screen"
      className="fixed inset-0 z-[9990] flex flex-col items-center justify-between bg-zinc-950 text-zinc-100 overflow-hidden select-none p-4 sm:p-8"
      initial={{ opacity: 0, scale: 0.94, filter: 'blur(10px)' }}
      animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
      exit={{ opacity: 0, scale: 1.05, filter: 'blur(8px)' }}
      transition={{ duration: 1.0, ease: [0.16, 1, 0.3, 1] }}
    >
      {/* ── 1. Interactive Real-Time WebGL Monochrome Fluid Smoke ── */}
      <FluidSmokeCanvas isBursting={isBursting} />

      {/* ── 2. Top Header (Locked Position) ── */}
      <header
        className="w-full max-w-6xl mx-auto flex items-center justify-between z-10 transition-opacity duration-700 ease-out pt-2 sm:pt-0"
        style={{
          opacity: isBursting ? 0 : 1,
          transitionDelay: isBursting ? '250ms' : '0ms',
          pointerEvents: isBursting ? 'none' : 'auto'
        }}
      >
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-500/20 via-sky-500/10 to-zinc-900 border border-cyan-500/30 flex items-center justify-center text-cyan-400 font-bold shadow-sm">
            <Brain className="w-4 h-4 text-cyan-400" />
          </div>
          <span className="text-sm font-semibold tracking-tight text-white font-sans">
            PRAHARI
          </span>
        </div>

        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-900/80 border border-zinc-800 text-[10px] sm:text-[11px] font-mono text-zinc-400">
          <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
          <span>AIR-GAPPED SOVEREIGN RAG</span>
        </div>
      </header>

      {/* ── 3. Central Hero Presentation (Locked Position) ── */}
      <main
        className="relative flex flex-col items-center justify-center text-center max-w-3xl mx-auto z-10 my-auto transition-opacity duration-700 ease-out px-2"
        style={{
          opacity: isBursting ? 0 : 1,
          transitionDelay: isBursting ? '300ms' : '0ms',
          pointerEvents: isBursting ? 'none' : 'auto'
        }}
      >
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, ease: 'easeOut' }}
          className="space-y-4 sm:space-y-6"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-900/90 border border-zinc-800 text-[11px] sm:text-xs text-zinc-300 font-medium shadow-sm">
            <span>Mangalore Refinery & Petrochemicals (MRPL)</span>
          </div>

          <h1 className="text-3xl sm:text-5xl md:text-7xl font-bold tracking-tight text-white uppercase leading-tight">
            Sovereign Safety <br /> Intelligence
          </h1>

          <p className="text-sm sm:text-lg text-zinc-300 max-w-xl mx-auto tracking-wider font-light italic">
            “ Sovereign &bull; Intelligent &bull; Verifiable ”
          </p>

          {/* High-Contrast "GET STARTED" CTA Button */}
          <div className="pt-2 sm:pt-4 flex flex-col items-center gap-3">
            <motion.button
              id="btn-get-started"
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
              onClick={handleClick}
              disabled={isBursting}
              className={`group relative flex items-center justify-center gap-2.5 px-6 sm:px-8 py-3 sm:py-3.5 rounded-xl bg-white hover:bg-zinc-200 text-zinc-950 font-semibold text-xs sm:text-sm shadow-xl transition-all duration-200 cursor-pointer ${
                isBursting ? 'opacity-75 cursor-default' : ''
              }`}
            >
              <span>{isBursting ? 'INITIALIZING...' : 'GET STARTED'}</span>
              <ArrowRight className="w-4 h-4" />
            </motion.button>
          </div>
        </motion.div>
      </main>

      {/* ── 4. Minimalist Footer (Locked Position) ── */}
      <footer
        className="w-full max-w-6xl mx-auto flex items-center justify-between text-[11px] text-zinc-500 font-mono z-10 transition-opacity duration-700 ease-out"
        style={{
          opacity: isBursting ? 0 : 1,
          transitionDelay: isBursting ? '250ms' : '0ms',
          pointerEvents: isBursting ? 'none' : 'auto'
        }}
      >
        <span>Smart India Hackathon 2026</span>
        <span>Zero Cloud Connection &bull; Local ChromaDB &bull; Sovereign AI Engine</span>
      </footer>
    </motion.div>
  );
}
