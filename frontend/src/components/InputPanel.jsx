import React, { useState } from 'react';
import LanguageSelector from './LanguageSelector';
import DomainSelector from './DomainSelector';
import LoadingAnimation from './LoadingAnimation';
import { Send } from 'lucide-react';

const InputPanel = ({ onSubmit, loading, progressStage }) => {
  const [query, setQuery] = useState('');
  const [targetLanguage, setTargetLanguage] = useState('en');
  const [domainHint, setDomainHint] = useState('auto');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim().length >= 3 && !loading) {
      onSubmit(query, targetLanguage, domainHint);
    }
  };

  return (
    <div className="bg-surface border border-border rounded-xl p-5 flex flex-col h-full shadow-lg">
      <h2 className="text-lg font-semibold mb-4 text-slate-100">Input Concept</h2>
      
      <form onSubmit={handleSubmit} className="flex flex-col flex-1 gap-6">
        <div className="relative flex-1 flex flex-col">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
            placeholder="Enter a technical concept, term, or paragraph..."
            className="w-full flex-1 min-h-[150px] bg-[#0D0F14] border border-border rounded-lg p-4 text-slate-200 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none transition-shadow disabled:opacity-50"
          />
          <div className="absolute bottom-3 right-3 text-xs text-slate-500 bg-[#0D0F14] px-1">
            {query.length} chars
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <LanguageSelector 
            value={targetLanguage} 
            onChange={setTargetLanguage} 
            disabled={loading}
          />
          <DomainSelector 
            value={domainHint} 
            onChange={setDomainHint} 
            disabled={loading}
          />
        </div>

        <div className="mt-auto pt-4">
          <button
            type="submit"
            disabled={loading || query.trim().length < 3}
            className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-primary to-indigo-500 hover:from-indigo-500 hover:to-primary text-white font-medium py-3 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
          >
            {loading ? (
              <span className="animate-pulse">Processing...</span>
            ) : (
              <>
                <Send size={18} />
                Simplify Concept
              </>
            )}
          </button>
        </div>
      </form>

      {loading && progressStage >= 0 && (
        <LoadingAnimation stage={progressStage} />
      )}
    </div>
  );
};

export default InputPanel;
