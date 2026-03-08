"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "outline";
}

export const Badge = React.forwardRef<HTMLDivElement, BadgeProps>(
  ({ className, variant = "default", ...props }, ref) => {
    const base =
      "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium";
    const variants: Record<NonNullable<BadgeProps["variant"]>, string> = {
      default: "border-sky-100 bg-sky-50 text-sky-700",
      outline: "border-slate-300 text-slate-700",
    };

    return (
      <div
        ref={ref}
        className={cn(base, variants[variant], className)}
        {...props}
      />
    );
  },
);

Badge.displayName = "Badge";

