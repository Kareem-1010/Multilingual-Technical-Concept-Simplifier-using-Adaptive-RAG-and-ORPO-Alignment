import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Activity, BookOpen, Hash, AlertTriangle } from 'lucide-react';

const MetricsDisplay = ({ metrics, faithfulness }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  if (!metrics || !faithfulness) return null;
  
  const isFaithful = faithfulness.is_faithful;
  const faithfulnessScore = Math.round((faithfulness.score || 0) * 100);
  const readabilityScore = Math.round(metrics.readability_score || 0);
  
  // Flesch Reading Ease: 0-100 (higher is easier)
  const getReadabilityLabel = (score) => {
    if (score >= 80) return "Very Easy";
    if (score >= 60) return "Standard";
    if (score >= 30) return "Difficult";
    return "Very Difficult";
  };
  
  return (
    <div className="mt-6 border border-border rounded-xl bg-[#0D0F14] overflow-hidden">
      <button 
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between p-4 bg-surface hover:bg-surface/80 transition-colors"
      >
        <div className="flex items-center gap-2 text-slate-300 font-medium">
          <Activity size={18} className="text-primary" />
          <span>Evaluation Metrics</span>
        </div>
        {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </button>
      
      {isExpanded && (
        <div className="p-4 flex flex-col gap-4">
          {!isFaithful && (
            <div className="flex items-start gap-3 bg-warning/10 border border-warning/30 p-3 rounded-lg text-warning text-sm">
              <AlertTriangle size={18} className="shrink-0 mt-0.5" />
              <p>
                <span className="font-semibold">Low Faithfulness Warning:</span> Output may not be fully grounded in retrieved sources. Score: {faithfulnessScore}%
              </p>
            </div>
          )}
          
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-surface p-3 rounded-lg border border-border">
              <div className="flex items-center gap-2 text-xs text-slate-400 mb-2 uppercase font-semibold">
                <BookOpen size={14} />
                Readability
              </div>
              <div className="flex items-end gap-2">
                <span className="text-2xl font-bold">{readabilityScore}</span>
                <span className="text-sm text-slate-500 mb-1">{getReadabilityLabel(readabilityScore)}</span>
              </div>
              <div className="w-full bg-border h-1.5 rounded-full mt-3 overflow-hidden">
                <div 
                  className={`h-full ${readabilityScore >= 60 ? 'bg-success' : readabilityScore >= 30 ? 'bg-warning' : 'bg-red-500'}`} 
                  style={{ width: `${Math.min(100, Math.max(0, readabilityScore))}%` }}
                />
              </div>
            </div>
            
            <div className="bg-surface p-3 rounded-lg border border-border">
              <div className="flex items-center gap-2 text-xs text-slate-400 mb-2 uppercase font-semibold">
                <Activity size={14} />
                Faithfulness
              </div>
              <div className="flex items-end gap-2">
                <span className="text-2xl font-bold">{faithfulnessScore}%</span>
                <span className="text-sm text-slate-500 mb-1">{faithfulness.label}</span>
              </div>
              <div className="w-full bg-border h-1.5 rounded-full mt-3 overflow-hidden">
                <div 
                  className={`h-full ${isFaithful ? 'bg-success' : 'bg-warning'}`} 
                  style={{ width: `${Math.min(100, Math.max(0, faithfulnessScore))}%` }}
                />
              </div>
            </div>
            
            <div className="bg-surface p-3 rounded-lg border border-border">
              <div className="flex items-center gap-2 text-xs text-slate-400 mb-2 uppercase font-semibold">
                <Hash size={14} />
                Token Count
              </div>
              <div className="flex items-end gap-2">
                <span className="text-2xl font-bold">{metrics.token_count || 0}</span>
                <span className="text-sm text-slate-500 mb-1">words</span>
              </div>
            </div>

            {metrics.bleu !== undefined && (
              <div className="bg-surface p-3 rounded-lg border border-border">
                <div className="flex items-center gap-2 text-xs text-slate-400 mb-2 uppercase font-semibold">
                  <Activity size={14} />
                  BLEU Score
                </div>
                <div className="flex items-end gap-2">
                  <span className="text-2xl font-bold">{metrics.bleu.toFixed(2)}</span>
                </div>
              </div>
            )}

            {metrics.rouge_l !== undefined && (
              <div className="bg-surface p-3 rounded-lg border border-border">
                <div className="flex items-center gap-2 text-xs text-slate-400 mb-2 uppercase font-semibold">
                  <Activity size={14} />
                  ROUGE-L
                </div>
                <div className="flex items-end gap-2">
                  <span className="text-2xl font-bold">{(metrics.rouge_l * 100).toFixed(1)}%</span>
                </div>
              </div>
            )}

            {metrics.sari !== undefined && (
              <div className="bg-surface p-3 rounded-lg border border-border">
                <div className="flex items-center gap-2 text-xs text-slate-400 mb-2 uppercase font-semibold">
                  <Activity size={14} />
                  SARI
                </div>
                <div className="flex items-end gap-2">
                  <span className="text-2xl font-bold">{metrics.sari.toFixed(1)}</span>
                </div>
              </div>
            )}

            {metrics.bertscore !== undefined && (
              <div className="bg-surface p-3 rounded-lg border border-border">
                <div className="flex items-center gap-2 text-xs text-slate-400 mb-2 uppercase font-semibold">
                  <Activity size={14} />
                  BERTScore
                </div>
                <div className="flex items-end gap-2">
                  <span className="text-2xl font-bold">{(metrics.bertscore * 100).toFixed(1)}%</span>
                </div>
              </div>
            )}

            {metrics.answer_relevance !== undefined && (
              <div className="bg-surface p-3 rounded-lg border border-border">
                <div className="flex items-center gap-2 text-xs text-slate-400 mb-2 uppercase font-semibold">
                  <Activity size={14} />
                  Relevance
                </div>
                <div className="flex items-end gap-2">
                  <span className="text-2xl font-bold">{(metrics.answer_relevance * 100).toFixed(1)}%</span>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default MetricsDisplay;
