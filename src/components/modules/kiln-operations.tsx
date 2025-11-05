'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { KPICard } from '@/components/ui/kpi-card';
import { Slider } from '@/components/ui/slider';
import { Timestamp } from '@/components/timestamp';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { CHART_COLORS } from '@/constants';

const temperatureData = [
  { zone: 'Preheater Top', temp: 352.4 },
  { zone: 'Preheater Bottom', temp: 897.6 },
  { zone: 'Calciner', temp: 901.3 },
  { zone: 'Kiln Inlet', temp: 1067.2 },
  { zone: 'Burning Zone', temp: 1467.8 },
  { zone: 'Cooler Inlet', temp: 1243.5 },
];

export function KilnOperationsModule() {
  const [coalRate, setCoalRate] = React.useState([90]);
  const [altFuelRate, setAltFuelRate] = React.useState([20]);
  const [aiOptimizationEnabled, setAiOptimizationEnabled] = React.useState(true);

  // AI-optimized values (based on optimal thermal efficiency)
  const aiOptimizedRates = {
    coal: 85,      // Optimized coal consumption (reduced from 90)
    altFuel: 25    // Optimized alternative fuel rate (increased from 20%)
  };

  // Current/manual rates
  const manualRates = {
    coal: 90,
    altFuel: 20
  };

  // Handle AI optimization toggle
  const handleAiToggle = (enabled: boolean) => {
    setAiOptimizationEnabled(enabled);
    if (enabled) {
      // Apply AI-optimized rates
      setCoalRate([aiOptimizedRates.coal]);
      setAltFuelRate([aiOptimizedRates.altFuel]);
    } else {
      // Revert to manual rates
      setCoalRate([manualRates.coal]);
      setAltFuelRate([manualRates.altFuel]);
    }
  };

  return (
    <div className="h-full w-full flex flex-col space-y-6">
      {/* Header Section */}
      <div className="flex items-center justify-between pb-2 border-b border-border">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-foreground">Kiln Operations</h2>
          <p className="text-sm text-muted-foreground mt-1">Real-time kiln performance and control</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center space-x-2">
            <input 
              type="checkbox" 
              id="kilnAI" 
              checked={aiOptimizationEnabled}
              onChange={(e) => handleAiToggle(e.target.checked)}
              className="h-4 w-4 cursor-pointer" 
            />
            <label htmlFor="kilnAI" className="text-sm font-medium cursor-pointer">
              AI Optimization {aiOptimizationEnabled && <span className="text-green-600">✓</span>}
            </label>
          </div>
          <div className="text-sm text-muted-foreground flex items-center gap-2">
            <span className="status-indicator active"></span>
            Live<Timestamp />
          </div>
        </div>
      </div>

      {/* AI Optimization Status */}
      {aiOptimizationEnabled && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <p className="text-green-800 text-sm">
            ✨ AI Optimization Active - Fuel rates automatically adjusted for optimal thermal efficiency (93.2%) and reduced CO₂ emissions (-18.4%)
          </p>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <KPICard
          title="Kiln Efficiency"
          value="86.3"
          unit="%"
          change={{ value: "+2.1% from target", type: "positive" }}
        />

        <KPICard
          title="Burning Zone Temp"
          value="1462.3"
          unit="°C"
          change={{ value: "Optimal range", type: "positive" }}
        />

        <KPICard
          title="Production Rate"
          value="188.2"
          unit="t/h"
          change={{ value: "+5.7% vs target", type: "positive" }}
        />

        <KPICard
          title="Energy Savings"
          value="9.7"
          unit="%"
          change={{ value: "vs baseline", type: "positive" }}
        />
      </div>

      {/* Temperature Zones and Controls */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card className="py-5">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg font-semibold">Temperature Zones</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="w-full" style={{ height: '300px', minHeight: '250px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={temperatureData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis 
                    dataKey="zone" 
                    angle={-45} 
                    textAnchor="end" 
                    height={100} 
                    fontSize={9}
                    interval={0}
                  />
                  <YAxis fontSize={10} />
                  <Tooltip 
                    contentStyle={{ 
                      borderRadius: '8px', 
                      border: '1px solid #e5e7eb',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                    }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="temp" 
                    stroke={CHART_COLORS.error} 
                    strokeWidth={3}
                    dot={{ fill: CHART_COLORS.error, r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className={`py-5 ${aiOptimizationEnabled ? 'border-green-400 shadow-green-100' : ''}`}>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg font-semibold">Fuel Controls</CardTitle>
              {aiOptimizationEnabled && <span className="text-xs text-green-600 font-medium">AI</span>}
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-semibold text-foreground">Coal Consumption</label>
                {aiOptimizationEnabled && <span className="text-xs text-green-600">(Optimized)</span>}
              </div>
              <div className="mt-2">
                <Slider
                  value={coalRate}
                  onValueChange={aiOptimizationEnabled ? undefined : setCoalRate}
                  max={120}
                  min={60}
                  step={1}
                  className="w-full"
                  disabled={aiOptimizationEnabled}
                />
                <div className="flex justify-between text-xs text-muted-foreground mt-1">
                  <span>60 t/h</span>
                  <span className="font-medium">{coalRate[0]} t/h</span>
                  <span>120 t/h</span>
                </div>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-semibold text-foreground">Alternative Fuel Rate</label>
                {aiOptimizationEnabled && <span className="text-xs text-green-600">(Optimized)</span>}
              </div>
              <div className="mt-2">
                <Slider
                  value={altFuelRate}
                  onValueChange={aiOptimizationEnabled ? undefined : setAltFuelRate}
                  max={40}
                  min={10}
                  step={0.5}
                  className="w-full"
                  disabled={aiOptimizationEnabled}
                />
                <div className="flex justify-between text-xs text-muted-foreground mt-1">
                  <span>10%</span>
                  <span className="font-semibold text-foreground">{altFuelRate[0]}%</span>
                  <span>40%</span>
                </div>
              </div>
            </div>

            {/* Status Summary */}
            <div className="mt-6 pt-4 border-t border-border">
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div>
                  <span className="text-muted-foreground">Thermal Efficiency</span>
                  <p className="text-base font-bold text-foreground mt-1">93.2%</p>
                </div>
                <div>
                  <span className="text-muted-foreground">CO₂ Reduction</span>
                  <p className="text-base font-bold text-emerald-600 mt-1">-18.4%</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
