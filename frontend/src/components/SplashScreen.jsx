import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

export default function SplashScreen({ onComplete }) {
  const finishedRef = useRef(false);
  const videoRef = useRef(null);

  const handleFinish = () => {
    if (finishedRef.current) return;
    finishedRef.current = true;
    onComplete?.();
  };

  // Keyboard shortcut listener for instant skip (Esc, Space, Enter)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' || e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        handleFinish();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Set optimal playback rate
  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.playbackRate = 1.0;
    }
  }, []);

  // Safety timer matching video duration
  useEffect(() => {
    const timer = setTimeout(() => {
      handleFinish();
    }, 9800);

    return () => clearTimeout(timer);
  }, []);

  return (
    <motion.div
      key="splash-screen"
      className="fixed inset-0 z-[9999] w-screen h-screen bg-black text-zinc-100 overflow-hidden select-none cursor-pointer flex flex-col items-center justify-between py-6 sm:py-8 px-4 sm:px-8"
      onClick={handleFinish}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{
        opacity: 0,
        scale: 1.04,
        filter: 'blur(12px)',
        transition: { duration: 0.75, ease: [0.16, 1, 0.3, 1] },
      }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
    >
      {/* ── 1. Deep Space Black Canvas with Dynamic Ambient Neural Auras ── */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden bg-black">
        {/* Core Pulsing Cyan Hologram Aura */}
        <motion.div
          animate={{
            scale: [1, 1.18, 1],
            opacity: [0.25, 0.45, 0.25],
          }}
          transition={{
            duration: 4.5,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] bg-gradient-to-tr from-cyan-600/30 via-sky-500/20 to-blue-900/10 rounded-full blur-[160px] pointer-events-none"
        />

        {/* Ambient Outer Halo */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1000px] h-[1000px] bg-sky-950/20 rounded-full blur-[220px] pointer-events-none" />

        {/* Fine Cyber Grid Overlay (Blends the full screen seamlessly) */}
        <div
          className="absolute inset-0 opacity-[0.03] pointer-events-none"
          style={{
            backgroundImage: `radial-gradient(rgba(255,255,255,0.4) 1px, transparent 1px)`,
            backgroundSize: '32px 32px',
          }}
        />
      </div>

      {/* ── 2. Top Header Bar ── */}
      <div className="w-full max-w-7xl flex items-center justify-between z-30 pointer-events-auto">
        <div className="flex items-center gap-2.5 opacity-80 hover:opacity-100 transition-opacity text-[11px] font-mono tracking-widest text-zinc-300 uppercase">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_10px_rgba(34,211,238,0.9)]" />
          <span>Prahari Sovereign Intelligence</span>
        </div>

        <div className="text-[10px] font-mono tracking-wider text-zinc-400 hover:text-zinc-200 transition-colors uppercase border border-zinc-800/90 px-3 py-1 rounded-full bg-zinc-900/80 backdrop-blur-md shadow-sm">
          Press [ESC] to Skip
        </div>
      </div>

      {/* ── 3. Central Holographic Core (No Video Borders, 100% Organic Blend) ── */}
      <div className="relative w-full h-full flex items-center justify-center pointer-events-none overflow-hidden z-10">
        
        {/* Holographic Cyber HUD Rings (Framing the entity naturally) */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          {/* Outer Slow-Rotating Dashed Orbit */}
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 32, repeat: Infinity, ease: 'linear' }}
            className="w-[520px] h-[520px] sm:w-[620px] h-[620px] rounded-full border border-cyan-500/10 border-dashed pointer-events-none"
          />

          {/* Middle Counter-Rotating Coordinate Ring */}
          <motion.div
            animate={{ rotate: -360 }}
            transition={{ duration: 24, repeat: Infinity, ease: 'linear' }}
            className="w-[420px] h-[420px] sm:w-[500px] h-[500px] rounded-full border border-sky-400/15 border-t-transparent border-b-transparent pointer-events-none"
          />

          {/* Inner Glowing Reticle */}
          <motion.div
            animate={{ scale: [0.98, 1.02, 0.98], opacity: [0.3, 0.6, 0.3] }}
            transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
            className="w-[340px] h-[340px] sm:w-[400px] h-[400px] rounded-full border border-cyan-400/20 pointer-events-none"
          />
        </div>

        {/* ── The Holographic Video Projection ── */}
        <div
          className="relative w-full h-full flex items-center justify-center pointer-events-none"
          style={{
            // Multi-stop progressive gradient mask that completely dissolves outer frame
            maskImage: 'radial-gradient(ellipse 52% 48% at 50% 50%, rgba(0,0,0,1) 25%, rgba(0,0,0,0.85) 45%, rgba(0,0,0,0.3) 68%, rgba(0,0,0,0) 88%)',
            WebkitMaskImage: 'radial-gradient(ellipse 52% 48% at 50% 50%, rgba(0,0,0,1) 25%, rgba(0,0,0,0.85) 45%, rgba(0,0,0,0.3) 68%, rgba(0,0,0,0) 88%)',
          }}
        >
          <video
            ref={videoRef}
            autoPlay
            muted
            playsInline
            preload="auto"
            onEnded={handleFinish}
            className="w-full h-full max-w-4xl max-h-[78vh] object-contain pointer-events-none transform-gpu"
            style={{
              // Deep black crushing filter: forces any dark boundary artifacts to absolute #000000
              filter: 'contrast(1.24) brightness(0.98) saturate(1.2)',
              imageRendering: 'auto',
              WebkitBackfaceVisibility: 'hidden',
              transform: 'translateZ(0)',
            }}
          >
            <source src="/intro_video.webm" type="video/webm" />
            <source src="/intro_video.mp4" type="video/mp4" />
          </video>
        </div>

        {/* ── Seamless Full-Screen Vignette Falloff ── */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            background: 'radial-gradient(ellipse 70% 65% at 50% 50%, transparent 35%, rgba(0,0,0,0.6) 65%, #000000 92%)',
          }}
        />
      </div>

      {/* ── 4. Bottom Telemetry & Status ── */}
      <div className="w-full max-w-7xl flex items-center justify-between z-30 pointer-events-none text-[10px] font-mono text-zinc-500 tracking-widest uppercase">
        <span>LOC: MRPL REFINERY NETWORK</span>
        <span className="flex items-center gap-1.5 text-zinc-400">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
          INITIALIZING NEURAL GRAPH...
        </span>
        <span>STATUS: SOVEREIGN 100% AIR-GAPPED</span>
      </div>
    </motion.div>
  );
}
