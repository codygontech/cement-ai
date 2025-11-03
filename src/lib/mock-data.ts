/**
 * Mock Data for Frontend Fallback
 * Used when backend is unavailable or returns empty data
 */

// Helper to generate timestamps
const generateTimestamps = (count: number, hoursAgo: number = 24) => {
  const now = new Date();
  return Array.from({ length: count }, (_, i) => {
    const timestamp = new Date(now.getTime() - (hoursAgo / count) * i * 60 * 60 * 1000);
    return timestamp.toISOString();
  }).reverse();
};

// Kiln Operations Mock Data
export const mockKilnOperations = Array.from({ length: 20 }, (_, i) => {
  const timestamps = generateTimestamps(20);
  return {
    id: i + 1,
    timestamp: timestamps[i],
    kiln_id: `KILN-${(i % 3) + 1}`,
    temperature: 1400 + Math.random() * 50,
    feed_rate: 180 + Math.random() * 20,
    rotation_speed: 3.2 + Math.random() * 0.3,
    pressure: 25 + Math.random() * 5,
    fuel_consumption: 45 + Math.random() * 5,
    thermal_efficiency: 78 + Math.random() * 8,
    production_rate: 250 + Math.random() * 30,
    status: Math.random() > 0.2 ? 'Normal' : 'Warning',
    location: ['Nimbahera', 'Mangrol', 'Gotan'][i % 3],
    created_at: timestamps[i],
  };
});

// Alternative Fuels Mock Data
export const mockAlternativeFuels = Array.from({ length: 15 }, (_, i) => {
  const timestamps = generateTimestamps(15);
  const fuelTypes = ['Biomass', 'RDF', 'Plastic Waste', 'Municipal Waste', 'Agricultural Waste'];
  return {
    id: i + 1,
    timestamp: timestamps[i],
    fuel_type: fuelTypes[i % fuelTypes.length],
    quantity_used: 50 + Math.random() * 100,
    substitution_rate: 20 + Math.random() * 15,
    cost_savings: 50000 + Math.random() * 100000,
    emissions_reduced: 100 + Math.random() * 200,
    energy_content: 15 + Math.random() * 10,
    kiln_id: `KILN-${(i % 3) + 1}`,
    location: ['Nimbahera', 'Mangrol', 'Gotan'][i % 3],
    created_at: timestamps[i],
  };
});

// Optimization Results Mock Data
export const mockOptimizationResults = Array.from({ length: 12 }, (_, i) => {
  const timestamps = generateTimestamps(12);
  const types = ['Energy', 'Fuel', 'Production', 'Quality', 'Maintenance'];
  return {
    id: i + 1,
    timestamp: timestamps[i],
    optimization_type: types[i % types.length],
    description: `Optimization recommendation ${i + 1}`,
    current_value: 100 + Math.random() * 50,
    optimized_value: 120 + Math.random() * 60,
    savings: 25000 + Math.random() * 75000,
    status: Math.random() > 0.3 ? 'Implemented' : 'Pending',
    location: ['Nimbahera', 'Mangrol', 'Gotan'][i % 3],
    created_at: timestamps[i],
  };
});

// Utilities Monitoring Mock Data
export const mockUtilitiesMonitoring = Array.from({ length: 18 }, (_, i) => {
  const timestamps = generateTimestamps(18);
  const utilityTypes = ['Electricity', 'Water', 'Compressed Air', 'Steam'];
  return {
    id: i + 1,
    timestamp: timestamps[i],
    utility_type: utilityTypes[i % utilityTypes.length],
    consumption: 500 + Math.random() * 500,
    cost: 10000 + Math.random() * 50000,
    unit: utilityTypes[i % utilityTypes.length] === 'Electricity' ? 'kWh' : 
          utilityTypes[i % utilityTypes.length] === 'Water' ? 'm³' : 
          utilityTypes[i % utilityTypes.length] === 'Compressed Air' ? 'm³' : 'kg',
    efficiency: 75 + Math.random() * 20,
    location: ['Nimbahera', 'Mangrol', 'Gotan'][i % 3],
    created_at: timestamps[i],
  };
});

// Raw Material Feed Mock Data
export const mockRawMaterialFeed = Array.from({ length: 16 }, (_, i) => {
  const timestamps = generateTimestamps(16);
  const materials = ['Limestone', 'Clay', 'Iron Ore', 'Gypsum', 'Fly Ash'];
  return {
    id: i + 1,
    timestamp: timestamps[i],
    material_type: materials[i % materials.length],
    quantity: 500 + Math.random() * 1000,
    source: ['Quarry A', 'Quarry B', 'Supplier 1', 'Supplier 2'][i % 4],
    quality_grade: ['A', 'B', 'A+'][Math.floor(Math.random() * 3)],
    cost_per_ton: 800 + Math.random() * 400,
    location: ['Nimbahera', 'Mangrol', 'Gotan'][i % 3],
    created_at: timestamps[i],
  };
});

// Grinding Operations Mock Data
export const mockGrindingOperations = Array.from({ length: 14 }, (_, i) => {
  const timestamps = generateTimestamps(14);
  return {
    id: i + 1,
    timestamp: timestamps[i],
    mill_id: `MILL-${(i % 2) + 1}`,
    feed_rate: 120 + Math.random() * 30,
    fineness: 3200 + Math.random() * 400,
    power_consumption: 180 + Math.random() * 40,
    production_rate: 100 + Math.random() * 30,
    product_type: ['OPC 43', 'OPC 53', 'PPC'][i % 3],
    location: ['Nimbahera', 'Mangrol', 'Gotan'][i % 3],
    created_at: timestamps[i],
  };
});

// Quality Control Mock Data
export const mockQualityControl = Array.from({ length: 10 }, (_, i) => {
  const timestamps = generateTimestamps(10, 48);
  return {
    id: i + 1,
    timestamp: timestamps[i],
    sample_id: `QC-${1000 + i}`,
    product_type: ['OPC 43', 'OPC 53', 'PPC'][i % 3],
    strength_3day: 18 + Math.random() * 4,
    strength_7day: 28 + Math.random() * 5,
    strength_28day: 45 + Math.random() * 8,
    fineness: 3200 + Math.random() * 400,
    cao: 62 + Math.random() * 3,
    sio2: 20 + Math.random() * 2,
    al2o3: 5 + Math.random() * 1,
    fe2o3: 3 + Math.random() * 0.5,
    loi: 2 + Math.random() * 1,
    status: Math.random() > 0.15 ? 'Pass' : 'Review',
    location: ['Nimbahera', 'Mangrol', 'Gotan'][i % 3],
    created_at: timestamps[i],
  };
});

// AI Recommendations Mock Data
export const mockAIRecommendations = [
  {
    id: 1,
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    category: 'Energy Efficiency',
    priority: 'High',
    title: 'Optimize Kiln Feed Rate',
    description: 'Reduce kiln feed rate by 5% during off-peak hours to improve thermal efficiency and reduce energy costs.',
    expected_impact: 'Expected savings: ₹2.5L per month, 8% reduction in fuel consumption',
    status: 'Pending',
    location: 'Nimbahera',
    created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 2,
    timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
    category: 'Alternative Fuels',
    priority: 'High',
    title: 'Increase RDF Substitution',
    description: 'Increase RDF usage from 20% to 30% thermal substitution rate. Quality tests show no impact on clinker quality.',
    expected_impact: 'Expected savings: ₹4L per month, 15% reduction in CO₂ emissions',
    status: 'Implemented',
    location: 'Mangrol',
    created_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 3,
    timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(),
    category: 'Maintenance',
    priority: 'Medium',
    title: 'Schedule Mill Liner Replacement',
    description: 'Mill-2 showing 12% efficiency drop. Recommend liner inspection and replacement within 2 weeks.',
    expected_impact: 'Prevent 20% further efficiency loss, maintain production targets',
    status: 'Pending',
    location: 'Gotan',
    created_at: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 4,
    timestamp: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
    category: 'Quality Control',
    priority: 'Low',
    title: 'Adjust Limestone Proportion',
    description: 'Recent quality tests suggest increasing limestone proportion by 2% to improve CaO content consistency.',
    expected_impact: 'Improved quality consistency, reduce rejection rate by 3%',
    status: 'Under Review',
    location: 'Nimbahera',
    created_at: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 5,
    timestamp: new Date(Date.now() - 18 * 60 * 60 * 1000).toISOString(),
    category: 'Production',
    priority: 'High',
    title: 'Optimize Grinding Circuit',
    description: 'Adjust separator speed to reduce circulating load and improve mill throughput by 8%.',
    expected_impact: 'Increase production by 800 TPD, reduce specific power consumption',
    status: 'Implemented',
    location: 'Mangrol',
    created_at: new Date(Date.now() - 18 * 60 * 60 * 1000).toISOString(),
  },
];

// KPIs Mock Data
export const mockKPIs = {
  production: {
    current: 2850,
    target: 3000,
    unit: 'TPD',
    trend: 'up',
    change: 5.2,
  },
  efficiency: {
    current: 82.6,
    target: 85,
    unit: '%',
    trend: 'up',
    change: 2.1,
  },
  thermal_substitution: {
    current: 25.5,
    target: 30,
    unit: '%',
    trend: 'up',
    change: 3.8,
  },
  energy_consumption: {
    current: 88.5,
    target: 85,
    unit: 'kWh/ton',
    trend: 'down',
    change: -2.3,
  },
  quality_compliance: {
    current: 98.2,
    target: 98,
    unit: '%',
    trend: 'stable',
    change: 0.1,
  },
  cost_savings: {
    current: 4.76,
    target: 5,
    unit: 'Cr/month',
    trend: 'up',
    change: 12.5,
  },
};

// Optimization Opportunities Mock Data
export const mockOptimizationOpportunities = [
  {
    category: 'Energy',
    title: 'Reduce Peak Hour Consumption',
    potential_savings: 180000,
    difficulty: 'Easy',
    impact: 'Medium',
  },
  {
    category: 'Fuel',
    title: 'Increase Alternative Fuel Usage',
    potential_savings: 450000,
    difficulty: 'Medium',
    impact: 'High',
  },
  {
    category: 'Production',
    title: 'Optimize Kiln Rotation Speed',
    potential_savings: 120000,
    difficulty: 'Easy',
    impact: 'Low',
  },
  {
    category: 'Maintenance',
    title: 'Predictive Maintenance Implementation',
    potential_savings: 300000,
    difficulty: 'Hard',
    impact: 'High',
  },
];

// Plant Locations Mock Data
export const mockPlantLocations = [
  {
    id: 1,
    plant_code: 'JK_NIMBAHERA',
    plant_name: 'JK Cement Nimbahera',
    location: 'Nimbahera, Rajasthan',
    city: 'Nimbahera',
    state: 'Rajasthan',
    country: 'India',
    latitude: 24.6219,
    longitude: 74.6869,
    capacity_tpd: 10000,
    plant_type: 'Integrated',
    commissioned_year: 1982,
    status: 'Active',
    contact_email: 'nimbahera@jkcement.com',
    contact_phone: '+91-1234567890',
    description: 'Integrated cement plant with state-of-the-art manufacturing facilities',
  },
  {
    id: 2,
    plant_code: 'JK_MANGROL',
    plant_name: 'JK Cement Mangrol',
    location: 'Mangrol, Rajasthan',
    city: 'Mangrol',
    state: 'Rajasthan',
    country: 'India',
    latitude: 25.3492,
    longitude: 76.5084,
    capacity_tpd: 8333,
    plant_type: 'Integrated',
    commissioned_year: 2008,
    status: 'Active',
    contact_email: 'mangrol@jkcement.com',
    contact_phone: '+91-1234567891',
    description: 'Modern integrated cement plant with advanced automation',
  },
  {
    id: 3,
    plant_code: 'JK_GOTAN',
    plant_name: 'JK Cement Gotan',
    location: 'Gotan, Rajasthan',
    city: 'Gotan',
    state: 'Rajasthan',
    country: 'India',
    latitude: 26.7929,
    longitude: 73.4413,
    capacity_tpd: 6667,
    plant_type: 'Grinding',
    commissioned_year: 2012,
    status: 'Active',
    contact_email: 'gotan@jkcement.com',
    contact_phone: '+91-1234567892',
    description: 'Grinding unit with efficient production capabilities',
  },
];

// AI Chat Mock Data
export const mockChatResponse = {
  message: "Based on current kiln operations data, I recommend optimizing the fuel mix to increase alternative fuel ratio from 15% to 20%. This could reduce coal consumption by approximately 50 kg/ton and lower CO2 emissions by 8%.",
  session_id: "mock_session_123",
  timestamp: new Date().toISOString(),
  recommendations: [
    "Increase alternative fuel ratio to 20%",
    "Reduce coal consumption by 50 kg/ton",
    "Monitor kiln temperature stability during transition",
  ],
};

export const mockChatHistory = [
  {
    role: "user",
    content: "What's the current status of kiln operations?",
    timestamp: new Date(Date.now() - 3600000).toISOString(),
  },
  {
    role: "assistant",
    content: "The kiln is operating at 95% efficiency with a temperature of 1420°C. Coal consumption is at 120 kg/ton with 15% alternative fuel ratio.",
    timestamp: new Date(Date.now() - 3500000).toISOString(),
  },
  {
    role: "user",
    content: "How can we improve fuel efficiency?",
    timestamp: new Date(Date.now() - 1800000).toISOString(),
  },
  {
    role: "assistant",
    content: "I recommend increasing the alternative fuel ratio to reduce coal dependency. Current data shows stable kiln conditions suitable for optimization.",
    timestamp: new Date(Date.now() - 1700000).toISOString(),
  },
];
