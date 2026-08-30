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

  // Set optimal playback rate and crisp rendering
  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.playbackRate = 1.0;
    }
  }, []);

  // Safety timer matching video duration (approx. 9.5 seconds)
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
        filter: 'blur(10px)',
        transition: { duration: 0.75, ease: [0.16, 1, 0.3, 1] },
      }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
    >
      {/* ── Background Deep Pitch-Black Radial Aura ── */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden bg-black">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[900px] h-[900px] bg-cyan-950/20 rounded-full blur-[200px] pointer-events-none" />
      </div>

      {/* ── Top Header Bar ── */}
      <div className="w-full max-w-7xl flex items-center justify-between z-30 pointer-events-auto">
        <div className="flex items-center gap-2.5 opacity-75 hover:opacity-100 transition-opacity text-[11px] font-mono tracking-widest text-zinc-300 uppercase">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_10px_rgba(34,211,238,0.9)]" />
          <span>Prahari Sovereign Intelligence</span>
        </div>

        <div className="text-[10px] font-mono tracking-wider text-zinc-500 hover:text-zinc-300 transition-colors uppercase border border-zinc-800/80 px-2.5 py-1 rounded-full bg-zinc-900/60 backdrop-blur-sm">
          Press [ESC] to Skip
        </div>
      </div>

      {/* ── High-Fidelity Neural Video Presentation (Crisp, Native Aspect Ratio, Feathered Aura) ── */}
      <div className="absolute inset-0 w-full h-full flex items-center justify-center pointer-events-none overflow-hidden z-10 p-4 sm:p-8">
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          preload="auto"
          onEnded={handleFinish}
          className="w-full h-full max-w-5xl max-h-[85vh] object-contain pointer-events-none transform-gpu"
          style={{
            filter: 'contrast(1.18) brightness(1.06) saturate(1.15)',
            maskImage: 'radial-gradient(circle at center, rgba(0,0,0,1) 68%, rgba(0,0,0,0) 98%)',
            WebkitMaskImage: 'radial-gradient(circle at center, rgba(0,0,0,1) 68%, rgba(0,0,0,0) 98%)',
            imageRendering: 'crisp-edges',
            WebkitBackfaceVisibility: 'hidden',
            transform: 'translateZ(0)',
          }}
        >
          {/* Prioritize high-bitrate WebM format for modern crisp rendering */}
          <source src="/intro_video.webm" type="video/webm" />
          <source src="/intro_video.mp4" type="video/mp4" />
        </video>
      </div>

      {/* ── Bottom Ambient Indicator ── */}
      <div className="w-full max-w-7xl flex items-center justify-center z-30 pointer-events-none">
        <span className="text-[10px] font-mono text-zinc-600 tracking-widest uppercase">
          AIR-GAPPED &bull; SOVEREIGN &bull; ON-PREMISE
        </span>
      </div>
    </motion.div>
  );
}
