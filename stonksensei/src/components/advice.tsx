"use client";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { MetricsCard } from "@/components/MetricsCard";
import { VaultTable } from "@/components/VaultTable";
import {
  BarChart3,
  ChevronDown,
  Globe,
  Home,
  LayoutDashboard,
  LifeBuoy,
  Settings,
  Wallet,
} from "lucide-react";
import FloatingPaths from "./FloatingPaths";

export default function Page() {
  return (
    <>
      <div className="bg-neutral-light rounded-lg flex z-10 drop-shadow-xl shadow-black">
        <main className="p-6">
          <div className="mb-6 flex items-center justify-between">
            <div className="space-y-1">
              <h1 className="text-2xl font-bold">Results</h1>
              <div className="text-sm text-muted-foreground">
                Query Date: {new Date().toLocaleDateString()}
              </div>
            </div>
            <Button variant="outline" className="gap-2">
              Dummy Data
            </Button>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            <MetricsCard title="Amount" value="$74,892" />
            <MetricsCard title="Risk" value="High" />
            <MetricsCard title="Timeline" value="Medium" />
          </div>
          <div className="mt-6">
            <VaultTable />
          </div>
        </main>
      </div>
      <FloatingPaths position={-1} />
    </>
  );
}
