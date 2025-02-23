"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Textarea } from "@/components/ui/textarea";
import FloatingPaths from "./FloatingPaths";
import LoadingScreen from "./LoadingScreen";

export default function FinancialAdviceForm({
  onSubmit,
}: {
  onSubmit: (data: {
    amount: number;
    riskLevel: string;
    timeline: string;
    yolo: number;
    preferences: string;
  }) => void;
}) {
  const [amount, setAmount] = useState<number>(0);
  const [riskLevel, setRiskLevel] = useState<string>("");
  const [timeline, setTimeline] = useState<string>("");
  const [yolo, setYolo] = useState<number>(5);
  const [preferences, setPreferences] = useState<string>("");

  const handleInvest = () => {
    onSubmit({ amount, riskLevel, timeline, yolo, preferences });
  };

  return (
    <div className="flex items-center justify-center my-16 p-4">
      <Card className="w-full max-w-md bg-neutral-light border-none z-10">
        <CardHeader>
          <CardTitle>Investment Form</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="amount">Investment Amount ($)</Label>
            <Input
              id="amount"
              type="number"
              min="0.01"
              step="0.01"
              placeholder="Enter amount"
              value={amount}
              onChange={(e) => setAmount(parseInt(e.target.value))}
            />
          </div>

          <div className="space-y-2">
            <Label>Risk Level</Label>
            <div className="flex space-x-2">
              {["Low", "Medium", "High"].map((level) => (
                <Button
                  key={level}
                  variant={riskLevel === level ? "default" : "outline"}
                  onClick={() => setRiskLevel(level)}
                  className={
                    riskLevel === level
                      ? level === "Low"
                        ? "bg-positive"
                        : level === "Medium"
                        ? "bg-mid"
                        : "bg-negative"
                      : ""
                  }
                >
                  {level}
                </Button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>Investment Timeline</Label>
            <div className="flex space-x-2">
              {["Short", "Medium", "Long"].map((term) => (
                <Button
                  key={term}
                  variant={timeline === term ? "default" : "outline"}
                  className={
                    timeline === term ? "text-white outline outline-white" : ""
                  }
                  onClick={() => setTimeline(term)}
                >
                  {term}
                </Button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>YOLO Factor</Label>
            <Slider
              max={10}
              min={1}
              step={1}
              value={[yolo]}
              onValueChange={(value) => setYolo(value[0])}
              className="w-full"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="preferences">Other Preferences</Label>
            <Textarea
              id="preferences"
              placeholder="Enter any other preferences"
              className="bg-neutral outline-none bg-none focus:border-white"
              value={preferences}
              onChange={(e) => setPreferences(e.target.value)}
            />
          </div>
        </CardContent>
        <CardFooter>
          <Button
            className="w-full text-black bg-positive"
            onClick={handleInvest}
          >
            Invest
          </Button>
        </CardFooter>
      </Card>
      <FloatingPaths position={-1} />
    </div>
  );
}
