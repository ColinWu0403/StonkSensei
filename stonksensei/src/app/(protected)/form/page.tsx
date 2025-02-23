"use client";

import { useEffect, useState } from "react";
import FinancialAdviceForm from "@/components/financial-advice-form";
import LoadingScreen from "@/components/LoadingScreen";
import Advice from "@/components/advice";

interface userData {
  amount: number;
  riskLevel: string;
  timeline: string;
  yolo: number;
  preferences: string;
}

export default function FormPage() {
  const [userData, setUserData] = useState<userData>();
  const [isLoading, setIsLoading] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [results, setResults] = useState<any>();

  // Updated initializePipeline to accept userData and perform a POST request.
  const initializePipeline = async (data: userData) => {
    console.log("Initializing ML pipeline...");
    const response = await fetch(
      `http://localhost:8000/advice/fakeadvice?investment_amount=${data.amount}&risk=${data.riskLevel}&timeline=${data.timeline}&yolo=${data.yolo}&preferences=${data.preferences}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (!response.ok) {
      throw new Error("Request failed");
    }
    return response.json();
  };

  const handleSubmit = async (data: userData) => {
    setIsLoading(true);
    setUserData(data);

    try {
      const adviceData = await initializePipeline(data);
      setResults(adviceData);
    } catch (error) {
      console.error("Error fetching advice:", error);
    } finally {
      setIsLoading(false);
      setIsComplete(true);
    }
  };

  useEffect(() => {
    if (isComplete) {
      console.log("Pipeline complete!");
      console.log(results);
    }
  }, [isComplete]);

  return (
    <div>
      {isLoading && <LoadingScreen />}
      {!isLoading && !isComplete && (
        <div
          className="overflow-y-hidden min-h-[90vh] bg-neutral"
          style={{ height: "90vh" }}
        >
          <FinancialAdviceForm onSubmit={handleSubmit} />
        </div>
      )}
      {isComplete && (
        <div
          className="flex flex-col justify-center items-center bg-neutral relative"
          style={{ height: "90vh" }}
        >
          <Advice advice={results} userData={userData!} />
        </div>
      )}
    </div>
  );
}
