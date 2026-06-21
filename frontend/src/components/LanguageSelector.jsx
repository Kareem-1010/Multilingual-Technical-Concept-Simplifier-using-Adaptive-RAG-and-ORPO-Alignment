import React from 'react';

const SUPPORTED_LANGUAGES = {
  "en": { name: "English", flag: "🇬🇧" },
  "hi": { name: "Hindi", flag: "🇮🇳" },
  "fr": { name: "French", flag: "🇫🇷" },
  "de": { name: "German", flag: "🇩🇪" },
  "es": { name: "Spanish", flag: "🇪🇸" },
  "ar": { name: "Arabic", flag: "🇸🇦" },
  "zh-cn": { name: "Chinese (Simplified)", flag: "🇨🇳" },
  "ja": { name: "Japanese", flag: "🇯🇵" },
  "ko": { name: "Korean", flag: "🇰🇷" },
  "pt": { name: "Portuguese", flag: "🇵🇹" },
};

const LanguageSelector = ({ value, onChange, disabled }) => {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Target Language</label>
      <div className="relative">
        <select 
          value={value} 
          onChange={(e) => onChange(e.target.value)}
          disabled={disabled}
          className="w-full appearance-none bg-surface border border-border text-sm rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent disabled:opacity-50 transition-shadow"
        >
          {Object.entries(SUPPORTED_LANGUAGES).map(([code, {name, flag}]) => (
            <option key={code} value={code}>
              {flag} {name}
            </option>
          ))}
        </select>
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-slate-400">
          <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/>
          </svg>
        </div>
      </div>
    </div>
  );
};

export default LanguageSelector;
