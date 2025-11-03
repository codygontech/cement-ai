'use client';

import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import { PlantLocation } from '@/types/plant-data';

// Fix for default marker icons in Leaflet
// eslint-disable-next-line @typescript-eslint/no-explicit-any
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Custom icons for different plant types
const createCustomIcon = (type: string, status: string) => {
  let color = '#6B7280'; // gray default
  
  if (type.includes('Integrated')) color = '#9333EA'; // purple
  else if (type.includes('Grinding')) color = '#F97316'; // orange
  else if (type.includes('White')) color = '#0EA5E9'; // sky blue
  
  if (status !== 'operational') color = '#94A3B8'; // lighter gray for non-operational
  
  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div style="
        background-color: ${color};
        width: 30px;
        height: 30px;
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        border: 3px solid white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
      ">
        <span style="
          transform: rotate(45deg);
          font-size: 16px;
          color: white;
        ">🏭</span>
      </div>
    `,
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -30],
  });
};

interface MapUpdaterProps {
  locations: PlantLocation[];
  selectedLocation: PlantLocation | null;
}

function MapUpdater({ locations, selectedLocation }: MapUpdaterProps) {
  const map = useMap();

  useEffect(() => {
    // Ensure map is ready before operations
    if (!map) return;
    
    const timeoutId = setTimeout(() => {
      if (selectedLocation) {
        map.flyTo([selectedLocation.latitude, selectedLocation.longitude], 10, {
          duration: 1.5,
        });
      } else if (locations.length > 0) {
        // Fit bounds to show all locations
        const bounds = L.latLngBounds(
          locations.map((loc) => [loc.latitude, loc.longitude])
        );
        map.fitBounds(bounds, { padding: [50, 50] });
      }
    }, 100);
    
    return () => clearTimeout(timeoutId);
  }, [locations, selectedLocation, map]);

  return null;
}

interface PlantLocationsMapProps {
  locations: PlantLocation[];
  selectedLocation: PlantLocation | null;
  onLocationSelect: (location: PlantLocation) => void;
}

export default function PlantLocationsMap({
  locations,
  selectedLocation,
  onLocationSelect,
}: PlantLocationsMapProps) {
  const [isClient, setIsClient] = React.useState(false);
  const [mapKey, setMapKey] = React.useState(0);

  React.useEffect(() => {
    setIsClient(true);
    // Force remount of map component after client-side hydration
    const timer = setTimeout(() => setMapKey(1), 100);
    return () => clearTimeout(timer);
  }, []);

  // Default center on India
  const defaultCenter: [number, number] = [23.5937, 78.9629];
  const defaultZoom = 5;

  if (!isClient || mapKey === 0) {
    return (
      <div className="h-[600px] rounded-lg overflow-hidden border border-border bg-secondary/20 flex items-center justify-center">
        <p className="text-muted-foreground">Loading map...</p>
      </div>
    );
  }

  return (
    <div className="h-[600px] rounded-lg overflow-hidden border border-border">
      <MapContainer
        key={mapKey}
        center={defaultCenter}
        zoom={defaultZoom}
        style={{ height: '100%', width: '100%' }}
        className="z-0"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <MapUpdater locations={locations} selectedLocation={selectedLocation} />

        {locations.map((location) => (
          <Marker
            key={location.id}
            position={[location.latitude, location.longitude]}
            icon={createCustomIcon(location.plant_type, location.status)}
            eventHandlers={{
              click: () => onLocationSelect(location),
            }}
          >
            <Popup>
              <div className="p-2 min-w-[250px]">
                <h3 className="font-bold text-sm mb-2">{location.plant_name}</h3>
                <div className="space-y-1 text-xs">
                  <p>
                    <span className="font-semibold">Location:</span> {location.city}, {location.state}
                  </p>
                  <p>
                    <span className="font-semibold">Type:</span> {location.plant_type}
                  </p>
                  <p>
                    <span className="font-semibold">Capacity:</span>{' '}
                    {location.capacity_tpd.toLocaleString()} TPD
                  </p>
                  <p>
                    <span className="font-semibold">Status:</span>{' '}
                    <span
                      className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${
                        location.status === 'operational'
                          ? 'bg-green-100 text-green-800'
                          : location.status === 'planned'
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {location.status}
                    </span>
                  </p>
                  {location.contact_phone && (
                    <p>
                      <span className="font-semibold">Phone:</span> {location.contact_phone}
                    </p>
                  )}
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
