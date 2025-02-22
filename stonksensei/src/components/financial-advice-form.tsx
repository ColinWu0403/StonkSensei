"use client"

import type React from "react"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

export default function FinancialAdviceForm() {
  const [amount, setAmount] = useState("")
  const [riskLevel, setRiskLevel] = useState("medium")
  const [timeline, setTimeline] = useState("medium")
  const [prompt, setPrompt] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would typically send the data to an API or process it
    console.log({ amount, riskLevel, timeline, prompt })
  }

  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <CardTitle>Enter Your Financial Details</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="amount">Amount to Invest (USD)</Label>
            <Input
              id="amount"
              type="number"
              placeholder="Enter amount in USD"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <Label>Risk Level</Label>
            <RadioGroup value={riskLevel} onValueChange={setRiskLevel} className="flex space-x-4">
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="low" id="risk-low" />
                <Label htmlFor="risk-low">Low</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="medium" id="risk-medium" />
                <Label htmlFor="risk-medium">Medium</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="high" id="risk-high" />
                <Label htmlFor="risk-high">High</Label>
              </div>
            </RadioGroup>
          </div>

          <div className="space-y-2">
            <Label>Investment Timeline</Label>
            <RadioGroup value={timeline} onValueChange={setTimeline} className="flex space-x-4">
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="short" id="timeline-short" />
                <Label htmlFor="timeline-short">Short</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="medium" id="timeline-medium" />
                <Label htmlFor="timeline-medium">Medium</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="long" id="timeline-long" />
                <Label htmlFor="timeline-long">Long</Label>
              </div>
            </RadioGroup>
          </div>

          <div className="space-y-2">
            <Label htmlFor="prompt">Additional Information or Questions</Label>
            <Textarea
              id="prompt"
              placeholder="Enter any additional details or specific questions..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="min-h-[100px]"
            />
          </div>
        </form>
      </CardContent>
      <CardFooter>
        <Button type="submit" className="w-full">
          Generate Advice
        </Button>
      </CardFooter>
    </Card>
  )
}

