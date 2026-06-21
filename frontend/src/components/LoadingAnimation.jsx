import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, Loader2, Circle } from 'lucide-react';

const STAGES = [
  "Preprocessing text...",
  "Detecting language & domain...",
  "Generating hypothesis...",
  "Retrieving knowledge...",
  "Generating explanation..."
];

const LoadingAnimation = ({ stage }) => {
  return (
    <div className="mt-6 flex flex-col gap-3">
      <AnimatePresence>
        {STAGES.map((text, idx) => {
          if (idx > stage + 1) return null; // Don't show future stages unless they are next
          
          const isCompleted = idx < stage;
          const isCurrent = idx === stage;
          
          return (
            <motion.div 
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex items-center gap-3 text-sm ${
                isCompleted ? 'text-slate-400' : isCurrent ? 'text-primary' : 'text-slate-600'
              }`}
            >
              {isCompleted ? (
                <CheckCircle2 size={16} className="text-success" />
              ) : isCurrent ? (
                <Loader2 size={16} className="animate-spin" />
              ) : (
                <Circle size={16} />
              )}
              <span>{text}</span>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
};

export default LoadingAnimation;
