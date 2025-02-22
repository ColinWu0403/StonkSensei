"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"
import { motion } from "framer-motion"
import { Input } from "@/components/ui/input"
import { DollarSign } from "lucide-react"

// TODO: implement color changes based on risk level

export default function FinancialAdviceForm() {
  const [formData, setFormData] = useState({
    investmentAmount: 10000,
    riskLevel: "mid",
    investmentTimeline: "medium",
    yoloFactor: 50,
  })

  const handleChange = (name: string, value: string | number) => {
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }))
  }

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    console.log(formData)
    // Here you would typically send the data to your backend
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-12">
      <div className="space-y-4">
        <Label htmlFor="investmentAmount" className="text-lg font-medium text-white">
          Investment Amount
        </Label>
        <div className="relative flex justify-center">
          <div className="relative inline-block">
            <DollarSign className="absolute left-4 top-1/2 transform -translate-y-1/2 text-positive text-2xl" />
            <Input
              id="investmentAmount"
              type="text"
              inputMode="numeric"
              pattern="[0-9]*"
              value={formatCurrency(formData.investmentAmount).replace("$", "")}
              onChange={(e) => {
                const value = e.target.value.replace(/,/g, "")
                handleChange("investmentAmount", Number.parseInt(value) || 0)
              }}
              className="py-8 text-4xl font-bold bg-gray-800 text-white border-2 border-positive focus:ring-positive text-center"
            />
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <Label className="text-lg font-medium text-white">Risk Level</Label>
        <div className="flex justify-between">
          {["low", "mid", "high"].map((level) => (
            <motion.button
              key={level}
              type="button"
              onClick={() => handleChange("riskLevel", level)}
              className={`px-4 py-2 rounded-full ${
                formData.riskLevel === level ? "bg-positive text-black" : "bg-gray-700 text-white"
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {level}
            </motion.button>
          ))}
        </div>
      </div>

      <div className="space-y-4">
        <Label className="text-lg font-medium text-white">Investment Timeline</Label>
        <div className="flex justify-between">
          {["short", "medium", "long"].map((timeline) => (
            <motion.button
              key={timeline}
              type="button"
              onClick={() => handleChange("investmentTimeline", timeline)}
              className={`px-4 py-2 rounded-full ${
                formData.investmentTimeline === timeline ? "bg-positive text-black" : "bg-gray-700 text-white"
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {timeline}
            </motion.button>
          ))}
        </div>
      </div>

      <div className="space-y-4">
        <Label htmlFor="yoloFactor" className="text-lg font-medium text-white">
          YOLO Factor
        </Label>
        <div className="relative pt-1">
          <Slider
            id="yoloFactor"
            min={0}
            max={100}
            step={1}
            value={[formData.yoloFactor]}
            onValueChange={(value) => handleChange("yoloFactor", value[0])}
            className="w-full"
          />
          <div className="flex justify-between text-white mt-2">
            <span>Play it safe</span>
            <span className="absolute left-1/2 top-1/2 transform -translate-x-1/2 translate-y-2 text-white px-2 py-1 text-sm font-bold">
              YOLO: {formData.yoloFactor}%
            </span>
            <span>To the moon! 🚀</span>
          </div>
        </div>
      </div>

      <Button type="submit" className="w-full bg-positive hover:bg-positive/90 text-black font-semibold py-3 rounded-full">
        Get Investment Advice
      </Button>
    </form>
  )
}

