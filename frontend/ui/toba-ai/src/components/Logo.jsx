export default function Logo({ size = 40, className = "" }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 120 120"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Background circle with gradient */}
      <defs>
        <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#27d6d3" />
          <stop offset="100%" stopColor="#1598af" />
        </linearGradient>
        <linearGradient id="logoGradientDark" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#2e9fa0" />
          <stop offset="100%" stopColor="#4f80f0" />
        </linearGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      
      {/* Main circle */}
      <circle cx="60" cy="60" r="54" fill="url(#logoGradient)" />
      
      {/* Inner decorative ring */}
      <circle cx="60" cy="60" r="48" stroke="rgba(255,255,255,0.2)" strokeWidth="1.5" fill="none" />
      
      {/* Mountain silhouette - representing Samosir/Danau Toba */}
      <path
        d="M20 78 L38 52 L48 62 L60 40 L75 58 L86 48 L100 78 Z"
        fill="rgba(255,255,255,0.95)"
      />
      
      {/* Water reflection/waves */}
      <path
        d="M22 82 Q35 78 48 82 Q60 86 72 82 Q85 78 98 82"
        stroke="rgba(255,255,255,0.6)"
        strokeWidth="2"
        strokeLinecap="round"
        fill="none"
      />
      <path
        d="M28 88 Q40 84 52 88 Q64 92 76 88 Q88 84 92 88"
        stroke="rgba(255,255,255,0.35)"
        strokeWidth="1.5"
        strokeLinecap="round"
        fill="none"
      />
      
      {/* Sun/moon dot */}
      <circle cx="72" cy="38" r="5" fill="rgba(255,255,255,0.85)" />
      
      {/* Star sparkle decorations */}
      <path d="M32 38 L34 34 L36 38 L34 42 Z" fill="rgba(255,255,255,0.5)" />
      <path d="M88 32 L89 29 L90 32 L89 35 Z" fill="rgba(255,255,255,0.4)" />
    </svg>
  );
}

