import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center justify-center rounded-full px-3 py-1 text-xs font-bold w-fit whitespace-nowrap shrink-0 [&>svg]:size-3 gap-1.5 [&>svg]:pointer-events-none transition-all shadow-sm hover:shadow-md",
  {
    variants: {
      variant: {
        default:
          "bg-gradient-to-r from-primary to-primary/90 text-primary-foreground [a&]:hover:shadow-lg [a&]:hover:scale-105",
        secondary:
          "bg-gradient-to-r from-secondary to-secondary/80 text-secondary-foreground [a&]:hover:shadow-lg [a&]:hover:scale-105",
        destructive:
          "bg-gradient-to-r from-destructive to-destructive/90 text-white [a&]:hover:shadow-lg [a&]:hover:scale-105",
        outline:
          "border border-primary text-primary bg-primary/5 [a&]:hover:bg-primary/10 [a&]:hover:scale-105",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

function Badge({
  className,
  variant,
  asChild = false,
  ...props
}: React.ComponentProps<"span"> &
  VariantProps<typeof badgeVariants> & { asChild?: boolean }) {
  const Comp = asChild ? Slot : "span"

  return (
    <Comp
      data-slot="badge"
      className={cn(badgeVariants({ variant }), className)}
      {...props}
    />
  )
}

export { Badge, badgeVariants }
