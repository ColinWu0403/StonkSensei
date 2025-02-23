"use client";

import FinancialAdviceForm from "@/components/financial-advice-form";
import { Suspense } from "react";

export default function FormPage() {
  return (
    <div className="overflow-y-hidden min-h-[90vh] bg-neutral">
      <FinancialAdviceForm />
    </div>
  );
}
