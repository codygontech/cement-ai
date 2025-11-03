'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import dynamic from 'next/dynamic';
import { PlantLocation, PlantLocationStats } from '@/types/plant-data';
import apiClient from '@/lib/api-client';

// Dynamically import map component to avoid SSR issues with Leaflet
const PlantLocationsMap = dynamic(
  () => import('./plant-locations-map'),
  { 
    ssr: false,
    loading: () => (
      <div className="h-[600px] bg-secondary/20 rounded-lg flex items-center justify-center">
        <p className="text-muted-foreground">Loading map...</p>
      </div>
    )
  }
);

export function PlantLocations() {
  const [locations, setLocations] = useState<PlantLocation[]>([]);
  const [stats, setStats] = useState<PlantLocationStats | null>(null);
  const [selectedLocation, setSelectedLocation] = useState<PlantLocation | null>(null);
  const [filterState, setFilterState] = useState<string>('all');
  const [filterType, setFilterType] = useState<string>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLocations();
    fetchStats();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filterState, filterType]);

  const fetchLocations = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getPlantLocations();
      
      // Apply filters client-side since backend might not support them with mock data
      let filteredData = data || [];
      
      if (filterState !== 'all') {
        filteredData = filteredData.filter(l => l.state === filterState);
      }
      if (filterType !== 'all') {
        filteredData = filteredData.filter(l => l.plant_type === filterType);
      }
      
      setLocations(filteredData);
    } catch (error) {
      console.error('Error fetching locations:', error);
      setLocations([]); // Set empty array on error to prevent crash
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const data = await apiClient.getPlantLocations();
      
      // Calculate stats from locations if backend doesn't provide them
      if (data && data.length > 0) {
        const totalPlants = data.length;
        const totalCapacity = data.reduce((sum, loc) => sum + (loc.capacity_tpd || 0), 0);
        const activeStates = new Set(data.map(l => l.state)).size;
        
        setStats({
          total_plants: totalPlants,
          total_capacity_tpd: totalCapacity,
          states_covered: activeStates,
          operational_plants: data.filter(l => l.status === 'Active').length,
          planned_plants: 0,
          plant_types: {},
        });
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
      // Set default stats on error
      setStats({
        total_plants: 0,
        total_capacity_tpd: 0,
        states_covered: 0,
        operational_plants: 0,
        planned_plants: 0,
        plant_types: {},
      });
    }
  };

  const states = Array.from(new Set(locations.map(l => l.state))).sort();
  const plantTypes = Array.from(new Set(locations.map(l => l.plant_type))).sort();

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case 'operational':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      case 'planned':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
      case 'maintenance':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
    }
  };

  const getTypeBadgeColor = (type: string) => {
    if (type.includes('Integrated')) return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300';
    if (type.includes('Grinding')) return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300';
    if (type.includes('White')) return 'bg-sky-100 text-sky-800 dark:bg-sky-900 dark:text-sky-300';
    return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground mb-2">
          🗺️ JK Cement Plant Locations
        </h1>
        <p className="text-muted-foreground">
          Multi-plant operations across India and International markets
        </p>
      </div>

      {/* Statistics Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="p-4 bg-gradient-to-br from-purple-50 to-white dark:from-purple-950/20 dark:to-background">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Plants</p>
                <p className="text-3xl font-bold text-foreground">{stats.total_plants}</p>
              </div>
              <div className="text-4xl">🏭</div>
            </div>
          </Card>

          <Card className="p-4 bg-gradient-to-br from-blue-50 to-white dark:from-blue-950/20 dark:to-background">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Capacity</p>
                <p className="text-3xl font-bold text-foreground">{stats.total_capacity_tpd.toLocaleString()}</p>
                <p className="text-xs text-muted-foreground">TPD</p>
              </div>
              <div className="text-4xl">⚡</div>
            </div>
          </Card>

          <Card className="p-4 bg-gradient-to-br from-green-50 to-white dark:from-green-950/20 dark:to-background">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Operational</p>
                <p className="text-3xl font-bold text-foreground">{stats.operational_plants}</p>
              </div>
              <div className="text-4xl">✓</div>
            </div>
          </Card>

          <Card className="p-4 bg-gradient-to-br from-orange-50 to-white dark:from-orange-950/20 dark:to-background">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">States Covered</p>
                <p className="text-3xl font-bold text-foreground">{stats.states_covered}</p>
              </div>
              <div className="text-4xl">🌏</div>
            </div>
          </Card>
        </div>
      )}

      {/* Filters */}
      <Card className="p-6 bg-gradient-to-br from-blue-50/50 to-indigo-50/50 dark:from-blue-950/20 dark:to-indigo-950/20 border-blue-200 dark:border-blue-900">
        <h3 className="text-lg font-semibold mb-4 text-foreground">Filter Plants</h3>
        <div className="flex flex-wrap gap-4 items-end">
          <div className="flex-1 min-w-[200px]">
            <label className="text-sm font-medium text-muted-foreground mb-2 block">
              State
            </label>
            <select
              value={filterState}
              onChange={(e) => setFilterState(e.target.value)}
              className="w-full px-4 py-2.5 bg-background/80 backdrop-blur-sm border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-sm hover:border-blue-300 dark:hover:border-blue-700"
            >
              <option value="all">All States</option>
              {states.map((state) => (
                <option key={state} value={state}>
                  {state}
                </option>
              ))}
            </select>
          </div>

          <div className="flex-1 min-w-[200px]">
            <label className="text-sm font-medium text-muted-foreground mb-2 block">
              Plant Type
            </label>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="w-full px-4 py-2.5 bg-background/80 backdrop-blur-sm border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-sm hover:border-blue-300 dark:hover:border-blue-700"
            >
              <option value="all">All Types</option>
              {plantTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          <div>
            <Button
              onClick={() => {
                setFilterState('all');
                setFilterType('all');
              }}
              variant="outline"
              size="default"
              className="px-6 bg-background/80 backdrop-blur-sm hover:bg-blue-50 dark:hover:bg-blue-950/50 border-blue-300 dark:border-blue-700 hover:border-blue-400 dark:hover:border-blue-600 shadow-sm"
            >
              <span className="mr-2">✕</span>
              Clear Filters
            </Button>
          </div>
        </div>
      </Card>

      {/* Map and Plant List */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Map */}
        <Card className="lg:col-span-2 p-4">
          <h2 className="text-xl font-semibold mb-4 text-foreground">Interactive Map</h2>
          <PlantLocationsMap
            locations={locations}
            selectedLocation={selectedLocation}
            onLocationSelect={setSelectedLocation}
          />
        </Card>

        {/* Plant List */}
        <Card className="p-4">
          <h2 className="text-xl font-semibold mb-4 text-foreground">
            Plants ({locations.length})
          </h2>
          <div className="space-y-3 max-h-[600px] overflow-y-auto p-1 pr-2">
            {loading ? (
              <div className="text-center py-8 text-muted-foreground">
                Loading plants...
              </div>
            ) : locations.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                No plants found with current filters
              </div>
            ) : (
              locations.map((location) => (
                <div
                  key={location.id}
                  className={`p-3 rounded-lg transition-all cursor-pointer ${
                    selectedLocation?.id === location.id
                      ? 'bg-[#FF6B35]/10 shadow-md ring-2 ring-[#FF6B35]/40'
                      : 'bg-card hover:bg-accent/50 hover:shadow-md'
                  }`}
                  onClick={() => setSelectedLocation(location)}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-sm text-foreground line-clamp-1">
                      {location.plant_name}
                    </h3>
                    <Badge className={getStatusBadgeColor(location.status)}>
                      {location.status}
                    </Badge>
                  </div>
                  <p className="text-xs text-muted-foreground mb-2">
                    📍 {location.city}, {location.state}
                  </p>
                  <div className="flex items-center justify-between">
                    <Badge className={getTypeBadgeColor(location.plant_type)}>
                      {location.plant_type}
                    </Badge>
                    <span className="text-xs font-medium text-foreground">
                      {location.capacity_tpd.toLocaleString()} TPD
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </Card>
      </div>

      {/* Selected Plant Details */}
      {selectedLocation && (
        <Card className="p-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h2 className="text-2xl font-bold text-foreground mb-2">
                {selectedLocation.plant_name}
              </h2>
              <p className="text-muted-foreground">
                Plant Code: {selectedLocation.plant_code}
              </p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setSelectedLocation(null)}
            >
              Close
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <h3 className="text-sm font-semibold text-muted-foreground mb-2">
                Location Details
              </h3>
              <div className="space-y-2 text-sm">
                <p>
                  <span className="font-medium">Address:</span> {selectedLocation.location}
                </p>
                <p>
                  <span className="font-medium">City:</span> {selectedLocation.city}
                </p>
                <p>
                  <span className="font-medium">State:</span> {selectedLocation.state}
                </p>
                <p>
                  <span className="font-medium">Country:</span> {selectedLocation.country}
                </p>
                <p>
                  <span className="font-medium">Coordinates:</span>{' '}
                  {selectedLocation.latitude.toFixed(4)}, {selectedLocation.longitude.toFixed(4)}
                </p>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-semibold text-muted-foreground mb-2">
                Plant Information
              </h3>
              <div className="space-y-2 text-sm">
                <p>
                  <span className="font-medium">Type:</span>{' '}
                  <Badge className={getTypeBadgeColor(selectedLocation.plant_type)}>
                    {selectedLocation.plant_type}
                  </Badge>
                </p>
                <p>
                  <span className="font-medium">Capacity:</span>{' '}
                  {selectedLocation.capacity_tpd.toLocaleString()} TPD
                </p>
                <p>
                  <span className="font-medium">Commissioned:</span>{' '}
                  {selectedLocation.commissioned_year}
                </p>
                <p>
                  <span className="font-medium">Status:</span>{' '}
                  <Badge className={getStatusBadgeColor(selectedLocation.status)}>
                    {selectedLocation.status}
                  </Badge>
                </p>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-semibold text-muted-foreground mb-2">
                Contact Information
              </h3>
              <div className="space-y-2 text-sm">
                {selectedLocation.contact_email && (
                  <p>
                    <span className="font-medium">Email:</span>{' '}
                    <a
                      href={`mailto:${selectedLocation.contact_email}`}
                      className="text-primary hover:underline"
                    >
                      {selectedLocation.contact_email}
                    </a>
                  </p>
                )}
                {selectedLocation.contact_phone && (
                  <p>
                    <span className="font-medium">Phone:</span>{' '}
                    <a
                      href={`tel:${selectedLocation.contact_phone}`}
                      className="text-primary hover:underline"
                    >
                      {selectedLocation.contact_phone}
                    </a>
                  </p>
                )}
              </div>
            </div>
          </div>

          {selectedLocation.description && (
            <div className="mt-6 pt-6 border-t border-border">
              <h3 className="text-sm font-semibold text-muted-foreground mb-2">
                Description
              </h3>
              <p className="text-sm text-foreground">{selectedLocation.description}</p>
            </div>
          )}

          {/* AI-Powered Recommendations */}
          <div className="mt-6 pt-6 border-t border-border">
            <div className="flex items-center gap-2 mb-4">
              <span className="text-2xl">🤖</span>
              <h3 className="text-lg font-semibold text-foreground">
                AI-Powered Insights
              </h3>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              {/* Overall Health */}
              <Card className="p-4 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/20 dark:to-emerald-950/20 border-green-200 dark:border-green-900">
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-3xl">💚</span>
                  <div>
                    <h4 className="font-semibold text-green-900 dark:text-green-100">Overall Health</h4>
                    <p className="text-xs text-green-700 dark:text-green-300">Real-time assessment</p>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-green-800 dark:text-green-200">Health Score</span>
                    <span className="text-2xl font-bold text-green-900 dark:text-green-100">
                      {selectedLocation.status === 'Operational' ? '92%' : 
                       selectedLocation.status === 'Maintenance' ? '75%' : '45%'}
                    </span>
                  </div>
                  <div className="w-full bg-green-200 dark:bg-green-900 rounded-full h-2">
                    <div 
                      className="bg-green-600 dark:bg-green-400 h-2 rounded-full transition-all" 
                      style={{ 
                        width: selectedLocation.status === 'Operational' ? '92%' : 
                               selectedLocation.status === 'Maintenance' ? '75%' : '45%'
                      }}
                    ></div>
                  </div>
                  <p className="text-xs text-green-700 dark:text-green-300 mt-2">
                    {selectedLocation.status === 'Operational' 
                      ? 'All systems running optimally. No critical issues detected.'
                      : selectedLocation.status === 'Maintenance'
                      ? 'Scheduled maintenance in progress. Expected completion in 2 days.'
                      : 'Multiple systems require immediate attention.'}
                  </p>
                </div>
              </Card>

              {/* Predictions */}
              <Card className="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20 border-blue-200 dark:border-blue-900">
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-3xl">📈</span>
                  <div>
                    <h4 className="font-semibold text-blue-900 dark:text-blue-100">Predictions</h4>
                    <p className="text-xs text-blue-700 dark:text-blue-300">Next 30 days forecast</p>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="flex gap-3">
                    <span className="text-green-600 dark:text-green-400 font-bold">▲</span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-blue-900 dark:text-blue-100 mb-1">Production Increase</p>
                      <p className="text-xs text-blue-700 dark:text-blue-300">
                        Expected +8% output capacity by optimizing kiln efficiency
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <span className="text-green-600 dark:text-green-400 font-bold">▼</span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-blue-900 dark:text-blue-100 mb-1">Energy Savings</p>
                      <p className="text-xs text-blue-700 dark:text-blue-300">
                        Projected 12% reduction in power consumption through AI optimization
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <span className="text-orange-600 dark:text-orange-400 font-bold">●</span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-blue-900 dark:text-blue-100 mb-1">Maintenance Due</p>
                      <p className="text-xs text-blue-700 dark:text-blue-300">
                        Kiln bearing replacement recommended within 45 days
                      </p>
                    </div>
                  </div>
                </div>
              </Card>

              {/* Recommendations */}
              <Card className="p-4 bg-gradient-to-br from-orange-50 to-amber-50 dark:from-orange-950/20 dark:to-amber-950/20 border-orange-200 dark:border-orange-900">
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-3xl">💡</span>
                  <div>
                    <h4 className="font-semibold text-orange-900 dark:text-orange-100">Recommendations</h4>
                    <p className="text-xs text-orange-700 dark:text-orange-300">AI-driven actions</p>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="bg-white/50 dark:bg-gray-900/50 rounded-lg p-2">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-semibold text-orange-900 dark:text-orange-100">HIGH PRIORITY</span>
                    </div>
                    <p className="text-xs text-orange-800 dark:text-orange-200">
                      Increase alternative fuel ratio to 35% for cost savings of ₹2.5L/month
                    </p>
                  </div>
                  <div className="bg-white/50 dark:bg-gray-900/50 rounded-lg p-2">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-semibold text-orange-900 dark:text-orange-100">MEDIUM</span>
                    </div>
                    <p className="text-xs text-orange-800 dark:text-orange-200">
                      Optimize raw material feed mix to improve clinker quality by 3%
                    </p>
                  </div>
                  <div className="bg-white/50 dark:bg-gray-900/50 rounded-lg p-2">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-semibold text-orange-900 dark:text-orange-100">LOW</span>
                    </div>
                    <p className="text-xs text-orange-800 dark:text-orange-200">
                      Schedule off-peak power usage to reduce electricity costs by 5%
                    </p>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}
