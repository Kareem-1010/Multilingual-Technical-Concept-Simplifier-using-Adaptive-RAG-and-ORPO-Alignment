import React from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Key, Lightbulb, Zap, Clock } from 'lucide-react';
import MetricsDisplay from './MetricsDisplay';
import FeedbackWidget from './FeedbackWidget';

const OutputPanel = ({ result, loading, error, sessionId }) => {
  if (error) {
    return (
      <div className="h-full flex items-center justify-center bg-surface border border-border rounded-xl p-6">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-500/10 text-red-500 mb-4">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-slate-200 mb-2">Processing Error</h3>
          <p className="text-slate-400 max-w-sm mx-auto">{error}</p>
        </div>
      </div>
    );
  }

  if (!result && !loading) {
    return (
      <div className="h-full flex items-center justify-center bg-surface border border-border rounded-xl p-6 border-dashed">
        <div className="text-center text-slate-500 max-w-sm">
          <div className="mb-4 flex justify-center opacity-50">
            <Zap size={48} className="text-primary" />
          </div>
          <p>Submit a concept to see the simplified explanation, key terms, analogies, and metrics.</p>
        </div>
      </div>
    );
  }

  if (!result) return null; // Loading state is handled in InputPanel

  const { output, domain, target_language, processing_time_ms } = result;

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="flex flex-col h-full overflow-y-auto pr-2 custom-scrollbar">
      <div className="flex items-center justify-between mb-4 px-2">
        <div className="flex gap-2">
          <span className="px-2.5 py-1 rounded-md text-xs font-medium bg-primary/20 text-primary border border-primary/20 capitalize">
            {domain.replace('_', ' ')}
          </span>
          <span className="px-2.5 py-1 rounded-md text-xs font-medium bg-surface border border-border text-slate-300 uppercase">
            {target_language}
          </span>
        </div>
        <div className="flex items-center gap-1.5 text-xs text-slate-500">
          <Clock size={14} />
          Generated in {(processing_time_ms / 1000).toFixed(1)}s
        </div>
      </div>

      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="flex flex-col gap-4"
      >
        {/* 📘 Plain Explanation */}
        <motion.div variants={itemVariants} className="bg-surface border border-border rounded-xl p-5 shadow-md">
          <div className="flex items-center gap-2 text-primary mb-3 font-semibold">
            <BookOpen size={18} />
            <h2>Plain Explanation</h2>
          </div>
          <p className="text-slate-200 leading-relaxed text-[15px]">
            {output.explanation}
          </p>
        </motion.div>

        {/* 🔑 Key Terms */}
        {output.key_terms && output.key_terms.length > 0 && (
          <motion.div variants={itemVariants} className="bg-surface border border-border rounded-xl p-5 shadow-md">
            <div className="flex items-center gap-2 text-primary mb-4 font-semibold">
              <Key size={18} />
              <h2>Key Terms</h2>
            </div>
            <div className="flex flex-wrap gap-2">
              {output.key_terms.map((item, idx) => (
                <div key={idx} className="group relative">
                  <span className="inline-block px-3 py-1.5 bg-[#0D0F14] border border-border rounded-md text-sm font-mono text-slate-300 cursor-help transition-colors group-hover:border-primary/50 group-hover:text-primary">
                    {item.term}
                  </span>
                  {item.definition && (
                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 p-2 bg-slate-800 text-xs text-slate-200 rounded shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-10 text-center pointer-events-none">
                      {item.definition}
                      <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-slate-800"></div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {/* 💡 Analogy */}
        {output.analogy && (
          <motion.div variants={itemVariants} className="bg-warning/10 border border-warning/20 rounded-xl p-5 shadow-md">
            <div className="flex items-center gap-2 text-warning mb-3 font-semibold">
              <Lightbulb size={18} />
              <h2>Analogy</h2>
            </div>
            <p className="text-slate-200 leading-relaxed italic text-[15px]">
              "{output.analogy}"
            </p>
          </motion.div>
        )}

        {/* ⚡ TL;DR */}
        {output.summary && (
          <motion.div variants={itemVariants} className="bg-gradient-to-r from-primary/10 to-transparent border border-primary/20 rounded-xl p-5 shadow-md">
            <div className="flex items-center gap-2 text-primary mb-3 font-semibold">
              <Zap size={18} />
              <h2>TL;DR</h2>
            </div>
            <p className="text-slate-100 font-medium text-lg">
              {output.summary}
            </p>
          </motion.div>
        )}
      </motion.div>

      {/* 📚 RAG Retrieved Context */}
      {result.retrieved_passages && result.retrieved_passages.length > 0 && (
        <div className="mt-6 border border-border rounded-xl bg-[#0D0F14] overflow-hidden">
          <details className="group">
            <summary className="flex items-center justify-between p-4 bg-surface hover:bg-surface/80 transition-colors cursor-pointer list-none">
              <div className="flex items-center gap-2 text-slate-300 font-medium">
                <BookOpen size={18} className="text-primary" />
                <span>RAG Retrieval Context (Top-K)</span>
              </div>
              <div className="text-primary opacity-70 group-open:rotate-180 transition-transform">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </div>
            </summary>
            <div className="p-4 flex flex-col gap-3 border-t border-border">
              <p className="text-xs text-slate-500 mb-2">
                These are the top chunks retrieved by the FAISS Vector Store and Cross-Encoder Reranker, which were used to ground the explanation.
              </p>
              {result.retrieved_passages.map((passage, idx) => (
                <div key={idx} className="bg-surface p-3 rounded border border-border/50 text-sm text-slate-300 leading-relaxed italic">
                  <span className="font-bold text-primary mr-2">#{idx + 1}</span>
                  {passage}
                </div>
              ))}
            </div>
          </details>
        </div>
      )}

      <MetricsDisplay metrics={result.metrics} faithfulness={result.faithfulness} />
      <FeedbackWidget sessionId={sessionId} result={result} />
    </div>
  );
};

export default OutputPanel;
