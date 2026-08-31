import { useEffect, useRef } from 'react';

/**
 * useSwipeGesture — Detects horizontal swipe gestures on touch devices.
 * 
 * @param {Object} options
 * @param {Function} options.onSwipeRight - Called when user swipes right (open sidebar)
 * @param {Function} options.onSwipeLeft  - Called when user swipes left (close sidebar)
 * @param {number}   options.threshold    - Minimum swipe distance in px (default: 60)
 * @param {number}   options.edgeZone    - Left edge zone in px to trigger swipe-right (default: 40)
 * @returns {Object} ref to attach to the target element
 */
export function useSwipeGesture({
  onSwipeRight,
  onSwipeLeft,
  threshold = 60,
  edgeZone = 40,
} = {}) {
  const touchStartX = useRef(null);
  const touchStartY = useRef(null);
  const isEdgeSwipe = useRef(false);
  const ref = useRef(null);

  useEffect(() => {
    const el = ref.current || window;

    const handleTouchStart = (e) => {
      const touch = e.touches[0];
      touchStartX.current = touch.clientX;
      touchStartY.current = touch.clientY;
      // Only track swipes that start from the left edge zone
      isEdgeSwipe.current = touch.clientX <= edgeZone;
    };

    const handleTouchEnd = (e) => {
      if (touchStartX.current === null) return;

      const touch = e.changedTouches[0];
      const deltaX = touch.clientX - touchStartX.current;
      const deltaY = touch.clientY - touchStartY.current;

      // Must be more horizontal than vertical (ratio > 1.5)
      if (Math.abs(deltaX) < threshold || Math.abs(deltaX) < Math.abs(deltaY) * 1.5) {
        touchStartX.current = null;
        return;
      }

      if (deltaX > 0 && isEdgeSwipe.current && onSwipeRight) {
        onSwipeRight();
      } else if (deltaX < 0 && onSwipeLeft) {
        onSwipeLeft();
      }

      touchStartX.current = null;
    };

    el.addEventListener('touchstart', handleTouchStart, { passive: true });
    el.addEventListener('touchend', handleTouchEnd, { passive: true });

    return () => {
      el.removeEventListener('touchstart', handleTouchStart);
      el.removeEventListener('touchend', handleTouchEnd);
    };
  }, [onSwipeRight, onSwipeLeft, threshold, edgeZone]);

  return ref;
}
