'use client';

import { useCallback } from 'react';
import telemetry from '@/lib/telemetry';

/**
 * Hook for tracking user interactions
 * Usage: const trackClick = useTelemetry();
 *        trackClick('button', 'save_settings', { setting: 'value' });
 */
export function useTelemetry() {
  const trackInteraction = useCallback(
    (type: string, target: string, data?: Record<string, unknown>) => {
      telemetry.trackInteraction(type, target, data).catch(console.error);
    },
    []
  );
  
  const trackError = useCallback(
    (error: Error | string, context?: string) => {
      telemetry.trackError(error, context).catch(console.error);
    },
    []
  );
  
  const trackPerformance = useCallback(
    (metric: string, value: number, data?: Record<string, unknown>) => {
      telemetry.trackPerformance(metric, value, data).catch(console.error);
    },
    []
  );
  
  return {
    trackInteraction,
    trackError,
    trackPerformance,
  };
}

/**
 * Hook for tracking API calls
 * Automatically tracks API response times and errors
 */
export function useApiTelemetry() {
  const { trackPerformance, trackError } = useTelemetry();
  
  const trackApiCall = useCallback(
    async <T,>(
      endpoint: string,
      apiCall: () => Promise<T>
    ): Promise<T> => {
      const startTime = performance.now();
      
      try {
        const result = await apiCall();
        const duration = performance.now() - startTime;
        
        trackPerformance('api_call', duration, {
          endpoint,
          status: 'success',
        });
        
        return result;
      } catch (error) {
        const duration = performance.now() - startTime;
        
        trackPerformance('api_call', duration, {
          endpoint,
          status: 'error',
        });
        
        trackError(
          error instanceof Error ? error : String(error),
          `api_call_${endpoint}`
        );
        
        throw error;
      }
    },
    [trackPerformance, trackError]
  );
  
  return { trackApiCall };
}
