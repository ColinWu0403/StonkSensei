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

export default function InvestmentForm() {
  const [riskLevel, setRiskLevel] = useState<string>("");
  const [timeline, setTimeline] = useState<string>("");

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
              defaultValue={[5]}
              max={10}
              min={1}
              step={0.5}
              className="w-full"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="preferences">Other Preferences</Label>
            <Textarea
              id="preferences"
              placeholder="Enter any other preferences"
              className="bg-neutral outline-none bg-none focus:border-white"
            />
          </div>
        </CardContent>
        <CardFooter>
          <Button className="w-full text-black bg-positive">Invest</Button>
        </CardFooter>
      </Card>
      <FloatingPaths position={-1}/>
    </div>
  );
}
