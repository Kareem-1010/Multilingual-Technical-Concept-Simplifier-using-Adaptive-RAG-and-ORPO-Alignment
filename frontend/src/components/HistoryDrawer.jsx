import React, { useState, useEffect } from 'react';
import { getHistory } from '../services/api';
import { X, Search, Clock, Star } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const HistoryDrawer = ({ isOpen, onClose, onSelect }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetchHistory();
    }
  }, [isOpen]);

  const fetchHistory = async () => {
    setLoading(true);
    const data = await getHistory();
    setHistory(data);
    setLoading(false);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 z-40 backdrop-blur-sm"
          />
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed inset-y-0 right-0 w-full sm:w-96 bg-surface border-l border-border z-50 flex flex-col shadow-2xl"
          >
            <div className="p-4 border-b border-border flex justify-between items-center bg-[#0D0F14]">
              <div className="flex items-center gap-2 font-semibold text-slate-200">
                <Clock size={18} className="text-primary" />
                Recent Queries
              </div>
              <button 
                onClick={onClose}
                className="p-1.5 rounded-md hover:bg-border text-slate-400 hover:text-slate-200 transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
              {loading ? (
                <div className="flex justify-center py-10">
                  <span className="animate-pulse text-slate-500 text-sm">Loading history...</span>
                </div>
              ) : history.length === 0 ? (
                <div className="text-center py-10 text-slate-500 text-sm">
                  <Search size={32} className="mx-auto mb-3 opacity-20" />
                  No history found
                </div>
              ) : (
                <div className="flex flex-col gap-3">
                  {history.map((item) => (
                    <div 
                      key={item.id}
                      onClick={() => {
                        onSelect(item);
                        onClose();
                      }}
                      className="bg-[#0D0F14] border border-border p-3 rounded-lg hover:border-primary/50 cursor-pointer transition-colors group"
                    >
                      <div className="flex justify-between items-start mb-2">
                        <span className="text-xs text-slate-500">{formatDate(item.timestamp)}</span>
                        {item.rating && (
                          <div className="flex items-center gap-1 bg-warning/10 text-warning px-1.5 py-0.5 rounded text-xs">
                            <Star size={10} className="fill-warning" />
                            {item.rating}
                          </div>
                        )}
                      </div>
                      <p className="text-sm font-medium text-slate-200 mb-2 line-clamp-2 group-hover:text-primary transition-colors">
                        {item.query}
                      </p>
                      <div className="flex gap-2">
                        <span className="px-1.5 py-0.5 rounded bg-surface border border-border text-[10px] text-slate-400 uppercase">
                          {item.domain?.replace('_', ' ')}
                        </span>
                        <span className="px-1.5 py-0.5 rounded bg-surface border border-border text-[10px] text-slate-400 uppercase">
                          {item.language}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default HistoryDrawer;
