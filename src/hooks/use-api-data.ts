import { useEffect, useState } from 'react';
import apiClient from '../lib/api-client';

/**
 * Generic hook for fetching data from the backend API
 */
function useAPIData<T>(
  fetchFn: () => Promise<T>,
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  deps: any[] = []
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const result = await fetchFn();
      setData(result);
      setError(null);
    } catch (err) {
      console.error('API fetch error:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, deps); // eslint-disable-line react-hooks/exhaustive-deps

  return { data, loading, error, refetch: fetchData };
}

/**
 * Hook for fetching kiln operations data
 */
export function useKilnOperations(limit = 50) {
  return useAPIData(
    () => apiClient.getKilnOperations(limit),
    [limit]
  );
}

/**
 * Hook for fetching alternative fuels data
 */
export function useAlternativeFuels(limit = 50) {
  return useAPIData(
    () => apiClient.getAlternativeFuels(limit),
    [limit]
  );
}

/**
 * Hook for fetching optimization results
 */
export function useOptimizationResults(limitOrType?: number | string, type?: string) {
  // Handle overloaded parameters: useOptimizationResults(50) or useOptimizationResults('fuel')
  const limit = typeof limitOrType === 'number' ? limitOrType : 50;
  const filterType = typeof limitOrType === 'string' ? limitOrType : type;
  
  return useAPIData(
    () => apiClient.getOptimizationResults(limit, filterType),
    [limit, filterType]
  );
}

/**
 * Hook for fetching utilities monitoring data
 */
export function useUtilitiesMonitoring(limit = 50) {
  return useAPIData(
    () => apiClient.getUtilitiesMonitoring(limit),
    [limit]
  );
}

/**
 * Hook for fetching raw material feed data
 */
export function useRawMaterialFeed(limit = 50) {
  return useAPIData(
    () => apiClient.getRawMaterialFeed(limit),
    [limit]
  );
}

/**
 * Hook for fetching grinding operations data
 */
export function useGrindingOperations(limit = 50) {
  return useAPIData(
    () => apiClient.getGrindingOperations(limit),
    [limit]
  );
}

/**
 * Hook for fetching quality control data
 */
export function useQualityControl(limit = 50) {
  return useAPIData(
    () => apiClient.getQualityControl(limit),
    [limit]
  );
}

/**
 * Hook for fetching AI recommendations
 */
export function useAIRecommendations(status?: string) {
  return useAPIData(
    () => apiClient.getAIRecommendations(status),
    [status]
  );
}

/**
 * Hook for fetching KPIs
 */
export function useKPIs() {
  return useAPIData(() => apiClient.getKPIs());
}

/**
 * Hook for fetching optimization opportunities
 */
export function useOptimizationOpportunities() {
  return useAPIData(() => apiClient.getOptimizationOpportunities());
}

/**
 * Hook for fetching chat history
 */
export function useChatHistory(sessionId?: string) {
  return useAPIData(
    () => apiClient.getChatHistory(sessionId),
    [sessionId]
  );
}
