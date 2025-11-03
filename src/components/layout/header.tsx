'use client';

import React from 'react';
import { Badge } from '@/components/ui/badge';
import { Activity } from 'lucide-react';

export function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-xl shadow-md">
      <div className="container flex h-16 items-center justify-between px-6">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl industrial-gradient shadow-lg transform hover:scale-110 transition-transform">
              <span className="text-2xl font-black text-white">JK</span>
            </div>
            <div className="flex flex-col">
              <h1 className="text-xl font-black leading-none text-foreground">
                CementAI by Codygon{' '}
                <span className="text-sm text-muted-foreground font-normal">
                  (for JK Cement - Google Cloud - Hack2skill Hackathon)
                </span>
              </h1>
              <span className="text-xs text-muted-foreground font-bold">
                AI-Powered Plant Operations
              </span>
            </div>
          </div>

        </div>
        
        <div className="flex items-center gap-3">
                    <div className="hidden md:flex items-center gap-2 pl-4">
            <span className="status-indicator active"></span>
            <span className="text-sm font-bold text-foreground">Live Monitoring</span>
          </div>
          <Badge 
            variant="outline"
          >
            <Activity className="w-3.5 h-3.5" />
            Real-time
          </Badge>
        </div>
      </div>
    </header>
  );
}

