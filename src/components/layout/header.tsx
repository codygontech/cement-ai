'use client';

import React from 'react';
import { Badge } from '@/components/ui/badge';
import { Activity, Menu } from 'lucide-react';

interface HeaderProps {
  onMenuToggle?: () => void;
}

export function Header({ onMenuToggle }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-xl shadow-md">
      <div className="container flex h-16 items-center justify-between px-4 md:px-6">
        <div className="flex items-center gap-3 md:gap-6 flex-1 min-w-0">
          {/* Mobile menu button */}
          <button
            onClick={onMenuToggle}
            className="lg:hidden flex items-center justify-center h-10 w-10 rounded-lg hover:bg-muted transition-colors flex-shrink-0"
            aria-label="Toggle menu"
          >
            <Menu className="h-6 w-6" />
          </button>

          <div className="flex items-center gap-2 md:gap-3 min-w-0">
            <div className="flex h-10 w-10 md:h-12 md:w-12 items-center justify-center rounded-2xl industrial-gradient shadow-lg transform hover:scale-110 transition-transform flex-shrink-0">
              <span className="text-lg md:text-2xl font-black text-white">JK</span>
            </div>
            <div className="flex flex-col min-w-0">
              <h1 className="text-sm md:text-xl font-black leading-none text-foreground truncate">
                CementAI by Codygon{' '}
                <span className="hidden xl:inline text-sm text-muted-foreground font-normal">
                  (for JK Cement - Google Cloud - Hack2skill Hackathon)
                </span>
              </h1>
              <span className="text-[10px] md:text-xs text-muted-foreground font-bold">
                AI-Powered Plant Operations
              </span>
            </div>
          </div>
        </div>
        
        <div className="flex items-center gap-2 md:gap-3 flex-shrink-0">
          <div className="hidden md:flex items-center gap-2 pl-4">
            <span className="status-indicator active"></span>
            <span className="text-sm font-bold text-foreground">Live Monitoring</span>
          </div>
          <Badge 
            variant="outline"
            className="hidden sm:flex"
          >
            <Activity className="w-3.5 h-3.5" />
            Real-time
          </Badge>
          <Badge 
            variant="outline"
            className="sm:hidden"
          >
            <Activity className="w-3.5 h-3.5" />
          </Badge>
        </div>
      </div>
    </header>
  );
}

