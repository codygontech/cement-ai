'use client';

import React from 'react';
import { Card } from '@/components/ui/card';
import { KPICard } from '@/components/ui/kpi-card';
import { useKilnOperations, useAlternativeFuels, useOptimizationResults } from '../../hooks/use-api-data';

// Mock data as fallback - using actual database field names
const mockKilnData = [
  { thermal_consumption: 3.85, feed_rate: 100, burning_zone_temp: 1450 }
];

const mockFuelData = [
  { fuel_type: 'Coal', tsr: 75, savings_amount: 2.3 },
  { fuel_type: 'Biomass', tsr: 10, savings_amount: 0.1 },
  { fuel_type: 'Pet Coke', tsr: 8, savings_amount: 3.1 },
  { fuel_type: 'RDF', tsr: 7, savings_amount: 0.8 }
];

const mockOptimizationData = [
  { optimization_type: 'fuel', confidence_score: 12.5, expected_savings: 125000 }
];

export function FuelOptimizationModule() {
  const { data: kilnDataRaw, loading: kilnLoading, error: kilnError } = useKilnOperations();
  const { data: fuelDataRaw, loading: fuelLoading, error: fuelError } = useAlternativeFuels();
  const { data: optimizationDataRaw, loading: optimizationLoading, error: optimizationError } = useOptimizationResults('fuel');

  // Add null safety
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const kilnData = (kilnDataRaw || []) as any[];
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const fuelData = (fuelDataRaw || []) as any[];
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const optimizationData = (optimizationDataRaw || []) as any[];

  console.log('🔥 Fuel Optimization Component Data:');
  console.log('Kiln data:', { data: kilnData, loading: kilnLoading, error: kilnError });
  console.log('Fuel data:', { data: fuelData, loading: fuelLoading, error: fuelError });
  console.log('Fuel data sample:', fuelData.slice(0, 3));
  console.log('Optimization data:', { data: optimizationData, loading: optimizationLoading, error: optimizationError });

  // Use real data if available, otherwise fallback to mock data
  const currentKilnData = kilnData.length > 0 ? kilnData : mockKilnData;
  const rawFuelData = fuelData.length > 0 ? fuelData : mockFuelData;
  const currentOptimizationData = optimizationData.length > 0 ? optimizationData : mockOptimizationData;

  // Aggregate fuel data by fuel type to avoid duplicates
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const fuelByType = rawFuelData.reduce((acc: any, fuel: any) => {
    const fuelType = fuel.fuel_type;
    if (!acc[fuelType]) {
      acc[fuelType] = { 
        fuel_type: fuelType, 
        tsr: [], 
        savings_amount: [] 
      };
    }
    acc[fuelType].tsr.push(fuel.tsr || fuel.thermal_substitution_pct || 0);
    acc[fuelType].savings_amount.push(fuel.savings_amount || fuel.co2_reduction_tph || 0);
    return acc;
  }, {});

  // Calculate averages for each fuel type
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const currentFuelData = Object.values(fuelByType).map((fuel: any) => ({
    fuel_type: fuel.fuel_type,
    tsr: fuel.tsr.reduce((a: number, b: number) => a + b, 0) / fuel.tsr.length,
    savings_amount: fuel.savings_amount.reduce((a: number, b: number) => a + b, 0) / fuel.savings_amount.length,
    count: fuel.tsr.length
  }));

  console.log('🔧 Aggregated fuel data:', currentFuelData);

  // Calculate KPIs from real or mock data
  // Map database fields: tsr = thermal substitution rate, thermal_consumption = heat consumption
  const avgThermalSubstitution = currentFuelData.reduce((sum, item) => sum + (item.tsr || 0), 0) / (currentFuelData.length || 1);
  const avgHeatConsumption = currentKilnData.reduce((sum, item) => sum + (item.thermal_consumption || item.specific_heat_consumption_mjkg || 0), 0) / (currentKilnData.length || 1);
  const totalCO2Reduction = currentFuelData.reduce((sum, item) => sum + (item.savings_amount || 0), 0);
  const avgEfficiencyImprovement = currentOptimizationData.reduce((sum, item) => sum + (item.confidence_score || item.improvement_pct || 0), 0) / (currentOptimizationData.length || 1);

  console.log('📊 Calculated KPIs:', {
    avgThermalSubstitution,
    avgHeatConsumption,
    totalCO2Reduction,
    avgEfficiencyImprovement
  });

  const isLoading = kilnLoading || fuelLoading || optimizationLoading;
  const hasError = kilnError || fuelError || optimizationError;

  if (hasError) {
    console.error('❌ Fuel Optimization Errors:', { kilnError, fuelError, optimizationError });
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Fuel Optimization</h1>
        <div className="text-sm text-gray-500">
          {isLoading ? 'Loading data...' : `${fuelData.length > 0 ? `${currentFuelData.length} fuel types (${fuelData.length} records)` : 'Using mock data'}`}
        </div>
      </div>

      {hasError && (
        <Card className="p-4 border-red-200 bg-red-50">
          <p className="text-red-600">
            Error loading data: {kilnError || fuelError || optimizationError}. Using fallback data.
          </p>
        </Card>
      )}

      {/* KPI Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard
          title="Thermal Substitution"
          value={isLoading ? "..." : `${avgThermalSubstitution.toFixed(1)}%`}
          change={isLoading ? undefined : { value: "+2.3%", type: "positive" }}
        />
        <KPICard
          title="Heat Consumption"
          value={isLoading ? "..." : `${avgHeatConsumption.toFixed(2)} MJ/kg`}
          change={isLoading ? undefined : { value: "-0.15 MJ/kg", type: "positive" }}
        />
        <KPICard
          title="CO₂ Reduction"
          value={isLoading ? "..." : `${totalCO2Reduction.toFixed(1)} tph`}
          change={isLoading ? undefined : { value: "+0.8 tph", type: "positive" }}
        />
        <KPICard
          title="Efficiency Gain"
          value={isLoading ? "..." : `${avgEfficiencyImprovement.toFixed(1)}%`}
          change={isLoading ? undefined : { value: "+1.2%", type: "positive" }}
        />
      </div>

      {/* Fuel Mix Chart */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Alternative Fuel Mix (Aggregated by Type)</h3>
        <div className="space-y-4">
          {currentFuelData.map((fuel, index) => {
            const tsrValue = fuel.tsr || 0;
            return (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="font-medium">{fuel.fuel_type}</span>
                  <span className="text-xs text-gray-500">({fuel.count} records)</span>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${Math.min(tsrValue, 100)}%` }}
                    />
                  </div>
                  <span className="text-sm text-gray-600 w-12">
                    {tsrValue.toFixed(1)}%
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </Card>

      {/* Optimization Results */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Optimization Results</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="text-sm font-medium text-gray-600 mb-2">Efficiency Improvement</h4>
            <p className="text-2xl font-bold text-green-600">
              {avgEfficiencyImprovement.toFixed(1)}%
            </p>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-600 mb-2">Cost Savings</h4>
            <p className="text-2xl font-bold text-green-600">
              ₹{(currentOptimizationData[0]?.expected_savings || currentOptimizationData[0]?.cost_saved_usd || 125000).toLocaleString('en-IN')}
            </p>
          </div>
        </div>
      </Card>

      {/* Data Source Info */}
      <Card className="p-4 bg-blue-50 border-blue-200">
        <h4 className="font-medium text-blue-900 mb-2">Data Source Information</h4>
        <div className="text-sm text-blue-700 space-y-1">
          <p>• Kiln Operations: {kilnData.length} records {kilnData.length > 0 ? '(Live Data)' : '(Mock Data)'}</p>
          <p>• Alternative Fuels: {fuelData.length} raw records → {currentFuelData.length} fuel types {fuelData.length > 0 ? '(Live Data - Aggregated)' : '(Mock Data)'}</p>
          <p>• Optimization Results: {optimizationData.length} records {optimizationData.length > 0 ? '(Live Data)' : '(Mock Data)'}</p>
          <p className="mt-2 font-medium">
            Status: {isLoading ? 'Loading...' : hasError ? 'Error - Using Fallback' : 'Connected to Backend API'}
          </p>
        </div>
      </Card>
    </div>
  );
}
