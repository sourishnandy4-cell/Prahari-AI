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

  // Safety timer matching cinematic 0.72x video duration (11.0 seconds)
  useEffect(() => {
    const timer = setTimeout(() => {
      handleFinish();
    }, 11400);

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
      transition={{ duration: 0.5, ease: 'easeOut' }}
    >
      {/* ── Background Ambient Radial Lighting (Pure Camouflage Black) ── */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden bg-black">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-white/[0.02] rounded-full blur-[180px] pointer-events-none" />
      </div>

      {/* ── Top Header Bar (Clean Minimal Logo) ── */}
      <div className="w-full max-w-7xl flex items-center justify-between z-30 pointer-events-auto">
        <div className="flex items-center gap-2.5 opacity-60 hover:opacity-100 transition-opacity text-[11px] font-mono tracking-widest text-zinc-400 uppercase">
          <span className="w-2 h-2 rounded-full bg-white animate-pulse shadow-[0_0_8px_rgba(255,255,255,0.9)]" />
          <span>Prahari Sovereign Intelligence</span>
        </div>
      </div>

      {/* ── Fullscreen Video Presentation (Fits Entire Screen Edge-to-Edge) ── */}
      <div className="absolute inset-0 w-full h-full flex items-center justify-center pointer-events-none overflow-hidden z-10">
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          preload="auto"
          onEnded={handleFinish}
          className="w-full h-full object-cover pointer-events-none mix-blend-screen transform-gpu"
        >
          <source src="/intro_video.mp4" type="video/mp4" />
          <source src="/intro_video.webm" type="video/webm" />
        </video>
      </div>

      {/* ── Bottom Spacing ── */}
      <div className="w-full max-w-7xl h-4 pointer-events-none z-30" />
    </motion.div>
  );
}
