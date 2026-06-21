import { useState } from 'react';
import { simplifyText } from '../services/api';
import toast from 'react-hot-toast';

const useSimplify = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [progressStage, setProgressStage] = useState(-1);

  const simplify = async (payload) => {
    setLoading(true);
    setError(null);
    setProgressStage(0);
    
    // Fake progress simulation
    const stages = setInterval(() => {
      setProgressStage(prev => {
        if (prev >= 3) {
          clearInterval(stages);
          return 3;
        }
        return prev + 1;
      });
    }, 600);

    try {
      const data = await simplifyText(payload);
      clearInterval(stages);
      setResult(data);
    } catch (err) {
      clearInterval(stages);
      setError(err.message);
      toast.error(err.message);
    } finally {
      setLoading(false);
      setProgressStage(-1);
    }
  };

  return { simplify, result, loading, error, progressStage };
};

export default useSimplify;
