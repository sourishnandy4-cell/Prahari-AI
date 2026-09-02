import React from 'react';
import { motion } from 'framer-motion';
import { Shield } from 'lucide-react';

export default function LottieLoader({ text = "Synthesizing response from local vector vault..." }) {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.98 }}
      className="flex flex-col items-center justify-center p-6 bg-zinc-900/80 border border-zinc-800 rounded-xl my-4 max-w-md mx-auto shadow-lg select-none"
    >
      <div className="relative flex items-center justify-center w-14 h-14 mb-3">
        {/* Rotating subtle spinner */}
        <motion.div 
          animate={{ rotate: 360 }}
          transition={{ duration: 1.6, repeat: Infinity, ease: "linear" }}
          className="absolute inset-0 rounded-full border border-t-white border-r-zinc-700 border-b-zinc-800 border-l-transparent"
        />
        {/* Center Icon */}
        <div className="z-10 text-white flex flex-col items-center">
          <Shield className="w-4 h-4 text-zinc-300" />
        </div>
      </div>

      <motion.p 
        animate={{ opacity: [0.6, 1, 0.6] }}
        transition={{ duration: 1.8, repeat: Infinity }}
        className="text-xs font-medium text-zinc-300 tracking-wide text-center"
      >
        {text}
      </motion.p>
      
      <div className="flex items-center space-x-2 mt-2.5 text-[10px] text-zinc-500 font-mono">
        <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
        <span>Local ChromaDB &bull; Sovereign AI Engine</span>
      </div>
    </motion.div>
  );
}
