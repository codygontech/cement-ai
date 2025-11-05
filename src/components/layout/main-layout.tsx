'use client';

import React, { useState } from 'react';
import { Header } from './header';
import { Sidebar } from './sidebar';
import { useActiveModule } from '@/hooks/use-active-module';
import { ExecutiveDashboard } from '@/components/modules/executive-dashboard';
import { RawMaterialsModule } from '@/components/modules/raw-materials';
import { KilnOperationsModule } from '@/components/modules/kiln-operations';
import { QualityControlModule } from '@/components/modules/quality-control';
import { FuelOptimizationModule } from '@/components/modules/fuel-optimization';
import { CrossProcessModule } from '@/components/modules/cross-process';
import { UtilitiesModule } from '@/components/modules/utilities';
import { AIInsightsModule } from '@/components/modules/ai-insights';
import { AIChatModule } from '@/components/modules/ai-chat';
import { PlantLocations } from '@/components/modules/plant-locations';

export function MainLayout() {
  const { activeModule, switchModule } = useActiveModule();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const renderActiveModule = () => {
    switch (activeModule) {
      case 'executive':
        return <ExecutiveDashboard />;
      case 'rawmaterials':
        return <RawMaterialsModule />;
      case 'kiln':
        return <KilnOperationsModule />;
      case 'quality':
        return <QualityControlModule />;
      case 'fuel':
        return <FuelOptimizationModule />;
      case 'integration':
        return <CrossProcessModule />;
      case 'utilities':
        return <UtilitiesModule />;
      case 'insights':
        return <AIInsightsModule />;
      case 'chat':
        return <AIChatModule />;
      case 'locations':
        return <PlantLocations />;
      default:
        return <ExecutiveDashboard />;
    }
  };

  return (
    <div className="h-screen w-full bg-gradient-to-br from-background via-muted/30 to-background">
      <Header onMenuToggle={() => setIsSidebarOpen(!isSidebarOpen)} />
      
      <div className="flex h-[calc(100vh-4rem)]">
        <Sidebar 
          activeModule={activeModule} 
          onModuleChange={switchModule}
          isOpen={isSidebarOpen}
          onClose={() => setIsSidebarOpen(false)}
        />
        
        <main className="flex-1 lg:ml-72 overflow-y-auto h-full">
          <div className="p-4 md:p-6 lg:p-8 pb-20 md:pb-24">
            {renderActiveModule()}
          </div>
          
          {/* Fixed Footer */}
          <footer className="fixed bottom-0 left-0 lg:left-72 right-0 bg-white dark:bg-gray-950 py-3 px-4 md:px-8 z-20 border-t border-border">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-muted-foreground">
              <p className="text-center sm:text-left">© {new Date().getFullYear()} Codygon Technologies Private Limited. All rights reserved.</p>
              <p className="text-center sm:text-right">Cement AI - Intelligent Plant Management System</p>
            </div>
          </footer>
        </main>
      </div>
    </div>
  );
}
