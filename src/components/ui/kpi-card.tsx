import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string | number;
  change?: {
    value: string;
    type: 'positive' | 'negative' | 'neutral';
  };
  icon?: React.ReactNode;
  className?: string;
  children?: React.ReactNode;
  unit?: string;
}

export function KPICard({ 
  title, 
  value, 
  change, 
  icon, 
  className,
  children,
  unit 
}: KPICardProps) {
  const getTrendIcon = () => {
    if (!change) return null;
    switch (change.type) {
      case 'positive':
        return <TrendingUp className="w-4 h-4" />;
      case 'negative':
        return <TrendingDown className="w-4 h-4" />;
      default:
        return <Minus className="w-4 h-4" />;
    }
  };

  return (
    <Card className={cn("h-full hover:shadow-xl transition-all relative overflow-visible", className)}>
      <div className="absolute top-0 right-0 w-24 h-24 sm:w-32 sm:h-32 bg-gradient-to-br from-primary/5 to-transparent rounded-full blur-3xl"></div>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 sm:pb-3 pt-0 px-4 sm:px-6 relative z-10">
        <CardTitle className="text-[10px] sm:text-xs font-bold text-muted-foreground uppercase tracking-widest">
          {title}
        </CardTitle>
        {icon && (
          <div className="flex h-8 w-8 sm:h-10 sm:w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-primary/80 text-white shadow-lg flex-shrink-0">
            {icon}
          </div>
        )}
      </CardHeader>
      <CardContent className="flex flex-col px-4 sm:px-6 pt-0 pb-0 relative z-10 overflow-visible">
        <div className="flex items-baseline gap-1 sm:gap-2 mb-4 sm:mb-6 overflow-visible">
          <div className="text-2xl sm:text-3xl md:text-4xl font-black metric-value" style={{ lineHeight: '1.4' }}>
            {value}
          </div>
          {unit && <span className="text-sm sm:text-base text-muted-foreground font-bold">{unit}</span>}
        </div>
        {change && (
          <div className={cn(
            "flex items-center gap-1 sm:gap-1.5 text-[10px] sm:text-xs font-bold px-2 sm:px-3 py-2 sm:py-2.5 rounded-full w-fit shadow-md mb-3 sm:mb-4 overflow-visible",
            change.type === 'positive' && "bg-gradient-to-r from-emerald-500 to-teal-500 text-white",
            change.type === 'negative' && "bg-gradient-to-r from-red-500 to-rose-500 text-white",
            change.type === 'neutral' && "bg-gradient-to-r from-gray-400 to-gray-500 text-white"
          )}>
            {getTrendIcon()}
            <span style={{ lineHeight: '1.6' }}>{change.value}</span>
          </div>
        )}
        {children && <div className="mt-3 sm:mt-4 flex-1 overflow-visible">{children}</div>}
      </CardContent>
    </Card>
  );
}

