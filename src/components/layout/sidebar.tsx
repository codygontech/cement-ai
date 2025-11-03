'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { NAVIGATION_ITEMS } from '@/constants';
import { ModuleId } from '@/types/plant-data';

interface SidebarProps {
  activeModule: ModuleId;
  onModuleChange: (moduleId: ModuleId) => void;
}

export function Sidebar({ activeModule, onModuleChange }: SidebarProps) {
  return (
    <aside className="fixed left-0 top-16 z-30 h-[calc(100vh-4rem)] w-72 bg-gradient-to-b from-sidebar to-sidebar/95 text-sidebar-foreground">
      <div className="flex flex-col h-full">
        {/* Navigation Header */}
        <div className="px-6 py-5">
          <h2 className="text-xs font-semibold text-sidebar-foreground/60 uppercase tracking-wider">
            Plant Modules
          </h2>
        </div>
        
        {/* Navigation Items */}
        <nav className="flex-1 space-y-1 p-3 overflow-y-auto">
          {NAVIGATION_ITEMS.map((item) => {
            const isActive = activeModule === item.id;
            return (
              <Button
                key={item.id}
                variant="ghost"
                className={cn(
                  "w-full justify-start gap-4 h-12 px-4 transition-all duration-200 ease-in-out rounded-lg",
                  isActive 
                    ? "bg-[#FF6B35] text-white font-bold hover:bg-[#FF6B35]/90 shadow-md" 
                    : "text-sidebar-foreground/80 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground"
                )}
                onClick={() => onModuleChange(item.id)}
              >
                <span className="text-xl flex-shrink-0">{item.icon}</span>
                <span className="text-sm font-semibold truncate">{item.label}</span>
              </Button>
            );
          })}
        </nav>
        
        {/* Footer Info */}
        <div className="p-5 bg-sidebar-accent/30">
          <div className="text-xs text-sidebar-foreground/60">
            <p className="font-medium mb-1">System Status</p>
            <div className="flex items-center gap-2">
              <span className="status-indicator active"></span>
              <span>All systems operational</span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}

