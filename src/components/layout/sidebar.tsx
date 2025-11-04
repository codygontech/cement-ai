'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { NAVIGATION_ITEMS } from '@/constants';
import { ModuleId } from '@/types/plant-data';
import { X } from 'lucide-react';

interface SidebarProps {
  activeModule: ModuleId;
  onModuleChange: (moduleId: ModuleId) => void;
  isOpen?: boolean;
  onClose?: () => void;
}

export function Sidebar({ activeModule, onModuleChange, isOpen = true, onClose }: SidebarProps) {
  const handleModuleChange = (moduleId: ModuleId) => {
    onModuleChange(moduleId);
    // Close sidebar on mobile after selection
    if (onClose && window.innerWidth < 1024) {
      onClose();
    }
  };

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden backdrop-blur-sm"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside className={cn(
        "fixed left-0 top-16 z-50 h-[calc(100vh-4rem)] w-72 transition-transform duration-300 ease-in-out shadow-2xl",
        "bg-white text-foreground lg:bg-sidebar lg:text-sidebar-foreground",
        "lg:translate-x-0 lg:z-30 lg:shadow-none",
        isOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex flex-col h-full">
          {/* Mobile close button */}
          <div className="lg:hidden flex items-center justify-between px-6 py-4 border-b border-border">
            <h2 className="text-sm font-semibold text-foreground uppercase tracking-wider">
              Menu
            </h2>
            <button
              onClick={onClose}
              className="flex items-center justify-center h-8 w-8 rounded-lg hover:bg-sidebar-accent/50 transition-colors"
              aria-label="Close menu"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Navigation Header - Hidden on mobile */}
          <div className="hidden lg:block px-6 py-5">
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
                      : "text-foreground hover:bg-muted lg:text-sidebar-foreground/80 lg:hover:bg-sidebar-accent/50 lg:hover:text-sidebar-foreground"
                  )}
                  onClick={() => handleModuleChange(item.id)}
                >
                  <span className="text-xl flex-shrink-0">{item.icon}</span>
                  <span className="text-sm font-semibold truncate">{item.label}</span>
                </Button>
              );
            })}
          </nav>
          
          {/* Footer Info */}
          <div className="p-5 bg-muted lg:bg-sidebar-accent/30">
            <div className="text-xs text-muted-foreground lg:text-sidebar-foreground/60">
              <p className="font-medium mb-1">System Status</p>
              <div className="flex items-center gap-2">
                <span className="status-indicator active"></span>
                <span>All systems operational</span>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}

