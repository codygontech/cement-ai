'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Sparkles, ChevronDown } from 'lucide-react';

interface InsightItem {
  id: string;
  title: string;
  description: string;
  priority?: 'high' | 'medium' | 'low';
  impact?: string;
  timeframe?: string;
  detailedInfo?: string;
}

export function AIInsightsModule() {
  const [expandedItem, setExpandedItem] = useState<string | null>(null);

  const immediateActions: InsightItem[] = [
    {
      id: '1',
      title: 'Reduce kiln temperature by 5°C',
      description: 'Optimize fuel consumption',
      priority: 'high',
      impact: '8% fuel savings',
      detailedInfo: 'Current kiln temperature is running 5-7°C higher than optimal range. Analysis shows that reducing temperature to 1,445°C will maintain clinker quality while reducing coal consumption by approximately 8%. Recommended implementation: Gradual reduction over 2 hours with continuous monitoring of free lime content and clinker strength.'
    },
    {
      id: '2',
      title: 'Increase limestone feed rate by 8 tons/hour',
      description: 'Better raw mix consistency',
      priority: 'medium',
      impact: 'Improved quality',
      detailedInfo: 'Raw mix LSF (Lime Saturation Factor) is currently trending below target at 92.5%. Increasing limestone feed from 142 to 150 tons/hour will bring LSF to optimal 94-95% range, improving clinker quality and reducing kiln refractory wear. Monitor silica modulus to ensure it stays within 2.4-2.6 range.'
    },
    {
      id: '3',
      title: 'Switch to 22% alternative fuel mix',
      description: 'Cost optimization opportunity',
      priority: 'high',
      impact: '₹45K/day savings',
      detailedInfo: 'Current AFR (Alternative Fuel Rate) is at 18%. Market analysis shows biomass and RDF prices are favorable this month. Increasing to 22% AFR with optimized blend (60% biomass, 40% RDF) will save ₹45,000 daily while maintaining thermal stability. Ensure proper feeding system calibration and monitor for any NOx emissions increase.'
    },
    {
      id: '4',
      title: 'Adjust grinding mill speed to 15.2 RPM',
      description: 'Efficiency improvement',
      priority: 'medium',
      impact: '5% energy reduction',
      detailedInfo: 'Grinding mill is currently operating at 16.1 RPM with suboptimal particle size distribution. Analysis indicates that reducing speed to 15.2 RPM with increased grinding media charge will improve Blaine fineness from 3,200 to target 3,400 cm²/g while reducing specific power consumption by 5%. Estimated energy savings: 180 kWh/hour.'
    }
  ];

  const predictiveAlerts: InsightItem[] = [
    {
      id: '5',
      title: 'Raw mill bearing temperature trending high',
      description: 'Maintenance recommended in 72 hours',
      priority: 'high',
      timeframe: '3 days',
      detailedInfo: 'Bearing temperature has increased from normal 65°C to current 78°C over the past 48 hours. Predictive model indicates probable lubricant degradation and suggests scheduling maintenance within 72 hours to avoid unplanned shutdown. Recommended actions: Check lubrication system, inspect for contamination, and prepare for bearing replacement if needed. Estimated downtime: 4-6 hours.'
    },
    {
      id: '6',
      title: 'Quality deviation predicted',
      description: 'Due to clay moisture content - expected in 6 hours',
      priority: 'high',
      timeframe: '6 hours',
      detailedInfo: 'Clay stockpile moisture has risen to 8.2% due to recent rainfall. AI model predicts this will affect raw mix homogeneity in approximately 6 hours, potentially causing compressive strength deviation of 3-5 MPa. Recommended: Adjust raw mix proportions by increasing clay temperature in pre-dryer to 180°C or reduce clay feed rate by 12% and compensate with alternative clay source.'
    },
    {
      id: '7',
      title: 'Energy cost spike expected tomorrow',
      description: 'Switch to biomass fuel recommended',
      priority: 'medium',
      timeframe: '1 day',
      detailedInfo: 'Grid energy pricing model predicts 22% cost increase during tomorrow\'s peak hours (2 PM - 8 PM). Recommendation: Increase biomass fuel usage from current 18% to 28% during peak hours, shift power-intensive grinding operations to off-peak hours (10 PM - 6 AM), and reduce HVAC loads in non-critical areas. Estimated savings: ₹1.2 lakh.'
    },
    {
      id: '8',
      title: 'Clinker cooler efficiency declining',
      description: 'Inspect grate plates for wear',
      priority: 'medium',
      timeframe: '1 week',
      detailedInfo: 'Cooler efficiency has dropped from 72% to 68% over the past month. Thermal imaging shows uneven cooling patterns indicating grate plate wear in zones 2 and 3. If left unchecked, efficiency may drop below 65% causing clinker quality issues and increased fuel consumption. Schedule inspection during next planned maintenance window. Replacement parts lead time: 5-7 days.'
    }
  ];

  const optimizationOpportunities: InsightItem[] = [
    {
      id: '9',
      title: 'Implement waste heat recovery',
      description: 'Potential 12% energy savings',
      impact: '₹8.5 Cr annual savings',
      detailedInfo: 'Current waste heat from preheater exhaust (320°C) and clinker cooler (280°C) represents significant energy loss. Installing WHR (Waste Heat Recovery) system with organic rankine cycle can generate 4.5 MW electricity, reducing grid dependency by 12%. Capital investment: ₹28 crores, ROI: 3.2 years. Additional benefits: 8,500 tons CO2 reduction annually, potential carbon credits worth ₹42 lakhs.'
    },
    {
      id: '10',
      title: 'Optimize preheater cyclone efficiency',
      description: '3% production increase possible',
      impact: '₹4.2 Cr annual value',
      detailedInfo: 'Cyclone separation efficiency analysis reveals 15% material bypass due to worn vortex finder in cyclone stage 3. Upgrading to ceramic-lined vortex finder and optimizing inlet geometry will improve separation efficiency from 82% to 95%, increasing preheating effectiveness and allowing 3% production increase. Investment: ₹18 lakhs, implementation time: 3 days during scheduled shutdown.'
    },
    {
      id: '11',
      title: 'Alternative fuel blend optimization',
      description: 'Advanced fuel mix strategy',
      impact: '₹2.3 Cr annual savings',
      detailedInfo: 'AI-powered fuel optimization algorithm can dynamically adjust fuel blend based on real-time factors: calorific value, cost, kiln temperature, and quality parameters. Implementation includes automated feeding system with load cells and advanced control logic. Optimal blend varies hourly based on 47 parameters. Expected outcomes: 8% fuel cost reduction, more stable kiln operation, reduced emissions. Software + hardware investment: ₹45 lakhs.'
    },
    {
      id: '12',
      title: 'Preventive maintenance scheduling',
      description: '15% downtime reduction opportunity',
      impact: '₹6.8 Cr annual savings',
      detailedInfo: 'Implementing AI-driven predictive maintenance system with IoT sensors (vibration, temperature, pressure at 250+ points) will enable condition-based maintenance instead of time-based. Analysis of 18 months data shows potential to reduce unplanned downtime from current 8.2% to 5.5%. System includes: sensor network, edge computing, ML models, maintenance workflow integration. Investment: ₹1.2 crores, payback: 18 months.'
    }
  ];

  const getPriorityColor = (priority?: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
      case 'low':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
    }
  };

  const toggleExpand = (id: string) => {
    setExpandedItem(expandedItem === id ? null : id);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Sparkles className="h-8 w-8 text-primary" />
          <div>
            <h2 className="text-3xl font-bold tracking-tight">AI Insights Dashboard</h2>
            <p className="text-sm text-muted-foreground">AI-Powered Recommendations & Predictions</p>
          </div>
        </div>
        <Badge variant="secondary" className="text-sm">
          🟢 AI Active
        </Badge>
      </div>

      {/* AI Insights Summary - Moved to Top */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">🎯 Total Recommendations</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">
              {immediateActions.length + predictiveAlerts.length + optimizationOpportunities.length}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Active insights across all categories
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">💰 Potential Savings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-600">₹21.8 Cr</div>
            <p className="text-xs text-muted-foreground mt-1">
              Annual savings from optimization opportunities
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">⚡ High Priority Items</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-red-600">
              {[...immediateActions, ...predictiveAlerts].filter(item => item.priority === 'high').length}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Require immediate attention
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Three Sections Side by Side */}
      <div className="grid gap-6 md:grid-cols-3">
        {/* Immediate Actions */}
        <Card className="border-0 shadow-none bg-transparent">
          <CardHeader className="px-0">
            <div className="flex items-center justify-between">
              <CardTitle className="text-xl">🔴 Immediate Actions</CardTitle>
              <Badge variant="destructive">{immediateActions.length}</Badge>
            </div>
          </CardHeader>
          <CardContent className="px-0">
            <div className="space-y-2">
              {immediateActions.map((action) => (
                <div key={action.id}>
                  <div
                    className="flex items-start gap-3 p-3 rounded-lg bg-card/50 hover:bg-accent/50 transition-colors cursor-pointer"
                    onClick={() => toggleExpand(action.id)}
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-0.5">
                        <h4 className="font-semibold text-xs">{action.title}</h4>
                        {action.priority && (
                          <Badge className={getPriorityColor(action.priority)} variant="secondary">
                            {action.priority}
                          </Badge>
                        )}
                        <ChevronDown 
                          className={`h-3 w-3 ml-auto transition-transform duration-300 ${
                            expandedItem === action.id ? 'rotate-180' : 'rotate-0'
                          }`}
                        />
                      </div>
                      <p className="text-xs text-muted-foreground">{action.description}</p>
                      {action.impact && (
                        <p className="text-xs text-primary font-medium mt-0.5">💰 {action.impact}</p>
                      )}
                    </div>
                  </div>
                  <div 
                    className={`overflow-hidden transition-all duration-300 ease-in-out ${
                      expandedItem === action.id ? 'max-h-96 opacity-100 mt-2' : 'max-h-0 opacity-0'
                    }`}
                  >
                    {action.detailedInfo && (
                      <div className="p-3 rounded-lg bg-muted/50 text-xs">
                        <p className="text-muted-foreground leading-relaxed">{action.detailedInfo}</p>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Predictive Alerts */}
        <Card className="border-0 shadow-none bg-transparent">
          <CardHeader className="px-0">
            <div className="flex items-center justify-between">
              <CardTitle className="text-xl">⚠️ Predictive Alerts</CardTitle>
              <Badge variant="outline" className="bg-yellow-50 text-yellow-800 border-yellow-200">
                {predictiveAlerts.length}
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="px-0">
            <div className="space-y-2">
              {predictiveAlerts.map((alert) => (
                <div key={alert.id}>
                  <div
                    className="flex items-start gap-3 p-3 rounded-lg bg-card/50 hover:bg-accent/50 transition-colors cursor-pointer"
                    onClick={() => toggleExpand(alert.id)}
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-0.5">
                        <h4 className="font-semibold text-xs">{alert.title}</h4>
                        {alert.priority && (
                          <Badge className={getPriorityColor(alert.priority)} variant="secondary">
                            {alert.priority}
                          </Badge>
                        )}
                        <ChevronDown 
                          className={`h-3 w-3 ml-auto transition-transform duration-300 ${
                            expandedItem === alert.id ? 'rotate-180' : 'rotate-0'
                          }`}
                        />
                      </div>
                      <p className="text-xs text-muted-foreground">{alert.description}</p>
                      {alert.timeframe && (
                        <p className="text-xs text-orange-600 font-medium mt-0.5">⏱️ {alert.timeframe}</p>
                      )}
                    </div>
                  </div>
                  <div 
                    className={`overflow-hidden transition-all duration-300 ease-in-out ${
                      expandedItem === alert.id ? 'max-h-96 opacity-100 mt-2' : 'max-h-0 opacity-0'
                    }`}
                  >
                    {alert.detailedInfo && (
                      <div className="p-3 rounded-lg bg-muted/50 text-xs">
                        <p className="text-muted-foreground leading-relaxed">{alert.detailedInfo}</p>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Optimization Opportunities */}
        <Card className="border-0 shadow-none bg-transparent">
          <CardHeader className="px-0">
            <div className="flex items-center justify-between">
              <CardTitle className="text-xl">💡 Optimization Opportunities</CardTitle>
              <Badge variant="outline" className="bg-green-50 text-green-800 border-green-200">
                {optimizationOpportunities.length}
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="px-0">
            <div className="space-y-2">
              {optimizationOpportunities.map((opportunity) => (
                <div key={opportunity.id}>
                  <div
                    className="flex items-start gap-3 p-3 rounded-lg bg-card/50 hover:bg-accent/50 transition-colors cursor-pointer"
                    onClick={() => toggleExpand(opportunity.id)}
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-0.5">
                        <h4 className="font-semibold text-xs">{opportunity.title}</h4>
                        <ChevronDown 
                          className={`h-3 w-3 ml-auto transition-transform duration-300 ${
                            expandedItem === opportunity.id ? 'rotate-180' : 'rotate-0'
                          }`}
                        />
                      </div>
                      <p className="text-xs text-muted-foreground">{opportunity.description}</p>
                      {opportunity.impact && (
                        <p className="text-xs text-green-600 font-medium mt-0.5">💰 {opportunity.impact}</p>
                      )}
                    </div>
                  </div>
                  <div 
                    className={`overflow-hidden transition-all duration-300 ease-in-out ${
                      expandedItem === opportunity.id ? 'max-h-96 opacity-100 mt-2' : 'max-h-0 opacity-0'
                    }`}
                  >
                    {opportunity.detailedInfo && (
                      <div className="p-3 rounded-lg bg-muted/50 text-xs">
                        <p className="text-muted-foreground leading-relaxed">{opportunity.detailedInfo}</p>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
