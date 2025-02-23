"use client";

import FinancialAdviceForm from "@/components/financial-advice-form";
import FloatingPaths from "@/components/FloatingPaths";
export default function FormPage() {
  return (
    <div className="overflow-y-hidden bg-neutral">
      <FinancialAdviceForm />
      {/* <FloatingPaths position={1} /> */}
    </div>
  );
}
