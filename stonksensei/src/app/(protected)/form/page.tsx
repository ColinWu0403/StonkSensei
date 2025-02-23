"use client";

import { useState, useEffect } from "react";
import FinancialAdviceForm from "@/components/financial-advice-form";

import LoadingScreen from "@/components/LoadingScreen";

export default function FormPage() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate a loading delay (like an API call)
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 3000);

    // Cleanup the timer if the component unmounts
    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    // While loading, return the LoadingScreen component
    <div className="overflow-y-hidden min-h-[90vh] bg-neutral">
      <LoadingScreen />
    </div>
  }

  // Once loading is complete, render the content below
  return (
    <div className="overflow-y-hidden min-h-[90vh] bg-neutral">
      <FinancialAdviceForm />
    </div>
  );
}
