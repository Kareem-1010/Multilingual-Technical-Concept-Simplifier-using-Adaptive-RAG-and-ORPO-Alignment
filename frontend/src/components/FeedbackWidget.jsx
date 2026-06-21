import React, { useState } from 'react';
import { Star } from 'lucide-react';
import { submitFeedback } from '../services/api';
import toast from 'react-hot-toast';

const FeedbackWidget = ({ sessionId, result }) => {
  const [rating, setRating] = useState(0);
  const [hoveredRating, setHoveredRating] = useState(0);
  const [comment, setComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  if (!result || isSubmitted) return null;

  const handleSubmit = async () => {
    if (rating === 0) {
      toast.error('Please select a rating first');
      return;
    }

    setIsSubmitting(true);
    try {
      await submitFeedback({
        session_id: sessionId,
        query: result.query,
        domain: result.domain,
        language: result.target_language,
        explanation: result.output.explanation,
        rating: rating,
        comment: comment,
        faithfulness_score: result.faithfulness?.score,
        readability_score: result.metrics?.readability_score
      });
      toast.success('Thanks! Your feedback helps improve the model 🙏');
      setIsSubmitted(true);
    } catch (error) {
      toast.error('Failed to submit feedback');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="mt-6 bg-surface border border-border rounded-xl p-5 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-300 mb-3">Rate this explanation</h3>
      
      <div className="flex gap-1 mb-4">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            type="button"
            className="focus:outline-none transition-transform hover:scale-110"
            onMouseEnter={() => setHoveredRating(star)}
            onMouseLeave={() => setHoveredRating(0)}
            onClick={() => setRating(star)}
          >
            <Star 
              size={24} 
              className={`${
                star <= (hoveredRating || rating) 
                  ? 'fill-warning text-warning' 
                  : 'text-slate-600'
              } transition-colors`}
            />
          </button>
        ))}
      </div>
      
      <textarea
        value={comment}
        onChange={(e) => setComment(e.target.value.slice(0, 200))}
        placeholder="Any suggestions? (Optional)"
        className="w-full bg-[#0D0F14] border border-border rounded-lg p-3 text-sm text-slate-200 placeholder:text-slate-500 focus:outline-none focus:border-primary resize-none mb-3"
        rows={2}
      />
      
      <div className="flex justify-between items-center">
        <span className="text-xs text-slate-500">{comment.length}/200</span>
        <button
          onClick={handleSubmit}
          disabled={isSubmitting || rating === 0}
          className="bg-primary hover:bg-indigo-600 text-white text-sm font-medium py-1.5 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isSubmitting ? 'Submitting...' : 'Submit Feedback'}
        </button>
      </div>
    </div>
  );
};

export default FeedbackWidget;
