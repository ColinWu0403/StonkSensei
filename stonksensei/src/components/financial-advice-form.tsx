"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"
import { Textarea } from "@/components/ui/textarea"
import FloatingPaths from "./FloatingPaths"
import { useRouter } from "next/navigation"

export default function FinancialAdviceForm() {
  const [amount, setAmount] = useState<string>("")
  const [riskLevel, setRiskLevel] = useState<string>("Low")
  const [timeline, setTimeline] = useState<string>("Short")
  const [yoloFactor, setYoloFactor] = useState<number>(5)
  const [preferences, setPreferences] = useState<string>("")
  const router = useRouter()

  const handleInvest = async () => {
    console.log(amount, riskLevel, timeline, yoloFactor, preferences);
    try {
      const response = await fetch("localhost:8000/advice/llm_response/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          investment_amount: amount ? amount : 0,
          risk: riskLevel.toLowerCase(),
          timeline: timeline.toLowerCase(),
          yolo: yoloFactor.toString(),
          preferences: preferences,
        }),
      });
      

      if (!response.ok) {
        throw new Error("Failed to fetch advice")
      }

      const data = await response.json()

      // Store the advice data in localStorage
      localStorage.setItem("investmentAdvice", JSON.stringify(data))

      // Redirect to the advice output page
      router.push("/investment-advice")
    } catch (error) {
      console.error("Error fetching advice:", error)
      // Handle error, e.g., show an error message to the user
    }
  }

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
              onChange={(e) => setAmount(e.target.value)}
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
                  className={timeline === term ? "text-white outline outline-white" : ""}
                  onClick={() => setTimeline(term)}
                >
                  {term}
                </Button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>YOLO Factor: {yoloFactor}</Label>
            <Slider
              value={[yoloFactor]}
              onValueChange={(value) => setYoloFactor(value[0])}
              max={10}
              min={1}
              step={1}
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
          <Button className="w-full text-black bg-positive" onClick={handleInvest}>
            Invest
          </Button>
        </CardFooter>
      </Card>
      <FloatingPaths position={-1} />
    </div>
  )
}

