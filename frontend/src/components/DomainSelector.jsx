import React from 'react';
import { Cpu, Dna, Atom, Calculator, Zap } from 'lucide-react';

const DOMAINS = [
  { id: 'auto', name: 'Auto-detect', icon: Zap },
  { id: 'computer_science', name: 'CS', icon: Cpu },
  { id: 'biology', name: 'Biology', icon: Dna },
  { id: 'physics', name: 'Physics', icon: Atom },
  { id: 'mathematics', name: 'Math', icon: Calculator },
];

const DomainSelector = ({ value, onChange, disabled }) => {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Domain Hint</label>
      <div className="flex flex-wrap gap-2">
        {DOMAINS.map(domain => {
          const Icon = domain.icon;
          const isSelected = value === domain.id;
          return (
            <button
              key={domain.id}
              onClick={() => onChange(domain.id)}
              disabled={disabled}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                isSelected 
                  ? 'bg-primary/20 text-primary border border-primary/50' 
                  : 'bg-surface border border-border text-slate-400 hover:text-slate-200 hover:border-slate-600'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              <Icon size={14} />
              {domain.name}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default DomainSelector;
