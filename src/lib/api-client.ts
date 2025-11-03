/**
 * API Client for Backend Communication
 * Handles all data fetching from the FastAPI backend
 */

import {
  mockKilnOperations,
  mockAlternativeFuels,
  mockOptimizationResults,
  mockUtilitiesMonitoring,
  mockRawMaterialFeed,
  mockGrindingOperations,
  mockQualityControl,
  mockAIRecommendations,
  mockKPIs,
  mockOptimizationOpportunities,
  mockPlantLocations,
  mockChatResponse,
  mockChatHistory,
} from './mock-data';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const USE_MOCK_DATA = process.env.NEXT_PUBLIC_USE_MOCK_DATA === 'true';

interface FetchOptions extends RequestInit {
  params?: Record<string, string | number>;
}

/**
 * Generic API fetch function with error handling, timeout, retry logic, and mock data fallback
 */
async function apiFetch<T>(
  endpoint: string, 
  options: FetchOptions = {},
  mockData?: T
): Promise<T> {
  // Return mock data if explicitly enabled
  if (USE_MOCK_DATA && mockData) {
    console.log(`Using mock data for ${endpoint}`);
    return mockData;
  }

  const { params, ...fetchOptions } = options;

  // Build URL with query parameters
  const url = new URL(`${API_BASE_URL}${endpoint}`);
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      url.searchParams.append(key, String(value));
    });
  }

  const maxRetries = 2; // Reduced retries for faster fallback
  const retryDelay = 1000; // 1 second
  const timeout = 10000; // 10 seconds timeout (reduced for faster fallback)

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      // Create abort controller for timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(url.toString(), {
        ...fetchOptions,
        headers: {
          'Content-Type': 'application/json',
          ...fetchOptions.headers,
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      
      // If response is empty array or null, use mock data
      if (mockData && (data === null || (Array.isArray(data) && data.length === 0))) {
        console.log(`Backend returned empty data for ${endpoint}, using mock data`);
        return mockData;
      }

      return data;
    } catch (error) {
      const isLastAttempt = attempt === maxRetries;
      const isAbortError = error instanceof Error && error.name === 'AbortError';
      
      if (isLastAttempt) {
        console.error(`API fetch error for ${endpoint} after ${maxRetries + 1} attempts:`, error);
        
        // Return mock data as fallback on final failure
        if (mockData) {
          console.log(`Using mock data as fallback for ${endpoint}`);
          return mockData;
        }
        
        throw error;
      }

      // Retry on network errors or timeouts
      if (isAbortError || error instanceof TypeError) {
        console.warn(`API fetch attempt ${attempt + 1} failed for ${endpoint}, retrying...`);
        await new Promise(resolve => setTimeout(resolve, retryDelay * (attempt + 1)));
      } else {
        // For other errors, use mock data if available
        if (mockData) {
          console.log(`Using mock data as fallback for ${endpoint} due to error`);
          return mockData;
        }
        throw error;
      }
    }
  }

  // This should never be reached, but TypeScript needs it
  if (mockData) {
    return mockData;
  }
  throw new Error(`Failed to fetch ${endpoint}`);
}

/**
 * API Client Methods
 */
export const apiClient = {
  // Kiln Operations
  getKilnOperations: (limit = 50) =>
    apiFetch('/api/data/kiln-operations', { params: { limit } }, mockKilnOperations),

  getKilnOperationById: (id: string) =>
    apiFetch(`/api/data/kiln-operations/${id}`),

  // Alternative Fuels
  getAlternativeFuels: (limit = 50) =>
    apiFetch('/api/data/alternative-fuels', { params: { limit } }, mockAlternativeFuels),

  // Optimization Results
  getOptimizationResults: (limit = 50, type?: string) =>
    apiFetch('/api/data/optimization-results', {
      params: { limit, ...(type && { type }) },
    }, mockOptimizationResults),

  // Utilities Monitoring
  getUtilitiesMonitoring: (limit = 50) =>
    apiFetch('/api/data/utilities-monitoring', { params: { limit } }, mockUtilitiesMonitoring),

  // Raw Material Feed
  getRawMaterialFeed: (limit = 50) =>
    apiFetch('/api/data/raw-material-feed', { params: { limit } }, mockRawMaterialFeed),

  // Grinding Operations
  getGrindingOperations: (limit = 50) =>
    apiFetch('/api/data/grinding-operations', { params: { limit } }, mockGrindingOperations),

  // Quality Control
  getQualityControl: (limit = 50) =>
    apiFetch('/api/data/quality-control', { params: { limit } }, mockQualityControl),

  // AI Recommendations
  getAIRecommendations: (status?: string) =>
    apiFetch('/api/data/ai-recommendations', {
      params: { ...(status && { status }) },
    }, mockAIRecommendations),

  // Analytics
  getKPIs: () => apiFetch('/api/analytics/kpis', {}, mockKPIs),

  getOptimizationOpportunities: () =>
    apiFetch('/api/analytics/optimization-opportunities', {}, mockOptimizationOpportunities),

  // AI Chat
  sendChatMessage: (message: string) =>
    apiFetch('/api/ai-chat/chat', {
      method: 'POST',
      body: JSON.stringify({ message }),
    }, mockChatResponse),

  getChatHistory: (sessionId?: string) =>
    apiFetch('/api/ai-chat/history', {
      params: { ...(sessionId && { session_id: sessionId }) },
    }, mockChatHistory),

  // Plant Locations
  getPlantLocations: () => 
    apiFetch('/api/locations/locations', {}, mockPlantLocations),

  // Vision API
  analyzeImage: (formData: FormData) =>
    fetch(`${API_BASE_URL}/api/vision/analyze`, {
      method: 'POST',
      body: formData, // Don't set Content-Type for FormData
    }).then((res) => {
      if (!res.ok) throw new Error(`Vision API Error: ${res.status}`);
      return res.json();
    }),
};

export default apiClient;
