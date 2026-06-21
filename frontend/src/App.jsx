import React, { useState, useEffect, useContext } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { v4 as uuidv4 } from 'uuid';
import InputPanel from './components/InputPanel';
import OutputPanel from './components/OutputPanel';
import HistoryDrawer from './components/HistoryDrawer';
import { History, LogOut } from 'lucide-react';
import useSimplify from './hooks/useSimplify';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import { AuthContext } from './context/AuthContext';

const Dashboard = () => {
  const [sessionId, setSessionId] = useState('');
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const { simplify, result, loading, error, progressStage } = useSimplify();
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    let sid = localStorage.getItem('mtcs_session_id');
    if (!sid) {
      sid = uuidv4();
      localStorage.setItem('mtcs_session_id', sid);
    }
    setSessionId(sid);
  }, []);

  const handleSimplify = async (query, targetLanguage, domainHint) => {
    await simplify({
      query,
      target_language: targetLanguage,
      domain_hint: domainHint === 'auto' ? null : domainHint,
      session_id: sessionId
    });
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-900 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-gray-900 to-black text-slate-200 flex flex-col font-sans">
      <header className="border-b border-white/10 p-4 flex justify-between items-center bg-black/30 backdrop-blur-md">
        <div>
          <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
            MTCS Enterprise
          </h1>
          <p className="text-xs text-slate-400">Advanced NLP Concept Simplification</p>
        </div>
        <div className="flex items-center gap-4">
          <button 
            onClick={() => setIsHistoryOpen(true)}
            className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors flex items-center gap-2 border border-white/10"
          >
            <History size={18} className="text-blue-300" />
            <span className="hidden sm:inline text-sm font-medium">History</span>
          </button>
          <button 
            onClick={handleLogout}
            className="p-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 transition-colors flex items-center gap-2 border border-red-500/20"
          >
            <LogOut size={18} />
            <span className="hidden sm:inline text-sm font-medium">Logout</span>
          </button>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 grid grid-cols-1 md:grid-cols-12 gap-6 relative">
        <div className="md:col-span-5 h-full">
          <InputPanel 
            onSubmit={handleSimplify} 
            loading={loading}
            progressStage={progressStage}
          />
        </div>
        
        <div className="md:col-span-7 h-full">
          <OutputPanel 
            result={result} 
            loading={loading} 
            error={error} 
            sessionId={sessionId}
          />
        </div>
      </main>

      <HistoryDrawer 
        isOpen={isHistoryOpen} 
        onClose={() => setIsHistoryOpen(false)} 
        onSelect={() => {}}
      />
    </div>
  );
};

const ProtectedRoute = ({ children }) => {
  const { user } = useContext(AuthContext);
  if (!user) return <Navigate to="/login" replace />;
  return children;
};

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route 
        path="/*" 
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } 
      />
    </Routes>
  );
}

export default App;
