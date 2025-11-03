"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

interface SliderProps {
  className?: string
  defaultValue?: number[] | number
  value?: number[] | number
  onValueChange?: (value: number[]) => void
  min?: number
  max?: number
  step?: number
  disabled?: boolean
}

function Slider({
  className,
  defaultValue,
  value,
  onValueChange,
  min = 0,
  max = 100,
  step = 1,
  disabled = false,
}: SliderProps) {
  // Normalize value
  const currentValue = React.useMemo(() => {
    const val = value ?? defaultValue ?? min
    return Array.isArray(val) ? val[0] : val
  }, [value, defaultValue, min])

  // Calculate fill percentage
  const fillPercentage = ((currentValue - min) / (max - min)) * 100

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = parseFloat(e.target.value)
    if (onValueChange) {
      onValueChange([newValue])
    }
  }

  return (
    <div className={cn("relative w-full", className)}>
      <style jsx>{`
        input[type="range"] {
          -webkit-appearance: none;
          appearance: none;
          width: 100%;
          height: 10px;
          border-radius: 5px;
          background: linear-gradient(
            to right,
            hsl(var(--primary)) 0%,
            hsl(var(--primary)) ${fillPercentage}%,
            rgb(229, 231, 235) ${fillPercentage}%,
            rgb(229, 231, 235) 100%
          );
          outline: none;
          cursor: pointer;
        }

        input[type="range"]::-webkit-slider-thumb {
          -webkit-appearance: none;
          appearance: none;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: white;
          border: 2px solid hsl(var(--primary));
          box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
          cursor: pointer;
          transition: transform 0.2s;
        }

        input[type="range"]::-webkit-slider-thumb:hover {
          transform: scale(1.1);
        }

        input[type="range"]::-moz-range-thumb {
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: white;
          border: 2px solid hsl(var(--primary));
          box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
          cursor: pointer;
          transition: transform 0.2s;
        }

        input[type="range"]::-moz-range-thumb:hover {
          transform: scale(1.1);
        }

        .dark input[type="range"] {
          background: linear-gradient(
            to right,
            hsl(var(--primary)) 0%,
            hsl(var(--primary)) ${fillPercentage}%,
            rgb(55, 65, 81) ${fillPercentage}%,
            rgb(55, 65, 81) 100%
          );
        }
      `}</style>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={currentValue}
        onChange={handleChange}
        disabled={disabled}
        className={cn(disabled && "opacity-50 cursor-not-allowed")}
      />
    </div>
  )
}

export { Slider }
