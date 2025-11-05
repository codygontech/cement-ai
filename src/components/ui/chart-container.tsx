'use client';

import React from 'react';

interface ChartContainerProps {
  children: React.ReactNode;
  className?: string;
  minHeight?: number;
  height?: number | string;
}

/**
 * Wrapper component for charts that ensures proper rendering on mobile devices
 * by guaranteeing the container has explicit dimensions
 */
export function ChartContainer({ 
  children, 
  className = '', 
  minHeight = 200,
  height = 300
}: ChartContainerProps) {
  const heightValue = typeof height === 'number' ? `${height}px` : height;

  return (
    <div
      className={className}
      style={{
        width: '100%',
        height: heightValue,
        minHeight: `${minHeight}px`,
        position: 'relative',
        display: 'block'
      }}
    >
      {children}
    </div>
  );
}
