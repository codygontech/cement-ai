'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import telemetry from '@/lib/telemetry';

/**
 * Telemetry Provider Component
 * Initializes telemetry on app load and tracks page views
 */
export function TelemetryProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  
  // Initialize telemetry on mount
  useEffect(() => {
    telemetry.initialize().catch(console.error);
  }, []);
  
  // Track page views on route change
  useEffect(() => {
    if (pathname) {
      telemetry.trackPageView(pathname).catch(console.error);
    }
  }, [pathname]);
  
  // Track global errors
  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      telemetry.trackError(event.error || event.message, 'global_error_handler');
    };
    
    const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
      telemetry.trackError(
        event.reason instanceof Error ? event.reason : String(event.reason),
        'unhandled_promise_rejection'
      );
    };
    
    window.addEventListener('error', handleError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);
    
    return () => {
      window.removeEventListener('error', handleError);
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
    };
  }, []);
  
  // Track performance metrics
  useEffect(() => {
    // Track page load performance
    if (typeof window !== 'undefined' && 'performance' in window) {
      const trackPerformance = () => {
        const perfData = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
        
        if (perfData) {
          // DNS lookup time
          telemetry.trackPerformance('dns_lookup', perfData.domainLookupEnd - perfData.domainLookupStart);
          
          // Connection time
          telemetry.trackPerformance('connection_time', perfData.connectEnd - perfData.connectStart);
          
          // Server response time
          telemetry.trackPerformance('server_response', perfData.responseStart - perfData.requestStart);
          
          // DOM load time
          telemetry.trackPerformance('dom_load', perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart);
          
          // Total page load time
          telemetry.trackPerformance('page_load', perfData.loadEventEnd - perfData.fetchStart);
        }
        
        // Track Largest Contentful Paint (LCP)
        if ('PerformanceObserver' in window) {
          try {
            const lcpObserver = new PerformanceObserver((list) => {
              const entries = list.getEntries();
              const lastEntry = entries[entries.length - 1] as PerformanceEntry & { startTime: number };
              if (lastEntry?.startTime) {
                telemetry.trackPerformance('lcp', lastEntry.startTime);
              }
            });
            lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
          } catch {
            // LCP not supported, skip
          }
        }
      };
      
      // Wait for page to fully load
      if (document.readyState === 'complete') {
        trackPerformance();
      } else {
        window.addEventListener('load', trackPerformance);
        return () => window.removeEventListener('load', trackPerformance);
      }
    }
  }, []);
  
  return <>{children}</>;
}
