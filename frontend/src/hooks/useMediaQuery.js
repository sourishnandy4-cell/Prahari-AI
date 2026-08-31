import { useState, useEffect } from 'react';

/**
 * useMediaQuery — Reactive breakpoint detection hook
 * Returns true if the media query matches the current viewport.
 */
export function useMediaQuery(query) {
  const [matches, setMatches] = useState(() => {
    if (typeof window === 'undefined') return false;
    return window.matchMedia(query).matches;
  });

  useEffect(() => {
    const mq = window.matchMedia(query);
    const handler = (e) => setMatches(e.matches);
    mq.addEventListener('change', handler);
    setMatches(mq.matches);
    return () => mq.removeEventListener('change', handler);
  }, [query]);

  return matches;
}

/** Convenience hook: true when viewport is mobile (< 768px) */
export function useIsMobile() {
  return useMediaQuery('(max-width: 767px)');
}

/** Convenience hook: true when viewport is tablet (768px – 1023px) */
export function useIsTablet() {
  return useMediaQuery('(min-width: 768px) and (max-width: 1023px)');
}

/** Convenience hook: true when viewport is desktop (≥ 1024px) */
export function useIsDesktop() {
  return useMediaQuery('(min-width: 1024px)');
}
