"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { ArrowRight, TrendingUp, DollarSign } from 'lucide-react'

export default function InvestmentAdvice() {
  const [advice, setAdvice] = useState({
    riskLevel: "mid",
    investmentAmount: 50000,
    yoloFactor: 50,
    timeline: "medium",
    portfolioAllocation: [
      { name: "Stocks", value: 60 },
      { name: "Bonds", value: 30 },
      { name: "Crypto", value: 10 },
    ],
    expectedReturn: 8.5,
  })

  // In a real application, you would fetch the advice from your backend based on the user's input
  useEffect(() => {
    // Simulating an API call
    setTimeout(() => {
      setAdvice({
        riskLevel: "mid",
        investmentAmount: 50000,
        yoloFactor: 50,
        timeline: "medium",
        portfolioAllocation: [
          { name: "Stocks", value: 60 },
          { name: "Bonds", value: 30 },
          { name: "Crypto", value: 10 },
        ],
        expectedReturn: 8.5,
      })
    }, 1000)
  }, [])

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  return (
    <div className="space-y-8">
      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-white">Investment Summary</h2>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-700 p-4 rounded-lg">
            <p className="text-sm text-gray-300">Investment Amount</p>
            <p className="text-2xl font-bold text-white">{formatCurrency(advice.investmentAmount)}</p>
          </div>
          <div className="bg-gray-700 p-4 rounded-lg">
            <p className="text-sm text-gray-300">Risk Level</p>
            <p className="text-2xl font-bold text-white capitalize">{advice.riskLevel}</p>
          </div>
          <div className="bg-gray-700 p-4 rounded-lg">
            <p className="text-sm text-gray-300">YOLO Factor</p>
            <p className="text-2xl font-bold text-white">{advice.yoloFactor}%</p>
          </div>
          <div className="bg-gray-700 p-4 rounded-lg">
            <p className="text-sm text-gray-300">Timeline</p>
            <p className="text-2xl font-bold text-white capitalize">{advice.timeline}</p>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-white">Portfolio Allocation</h2>
        <div className="bg-gray-700 p-4 rounded-lg">
          {advice.portfolioAllocation.map((item, index) => (
            <div key={index} className="flex justify-between items-center mb-2">
              <span className="text-white">{item.name}</span>
              <span className="text-white font-bold">{item.value}%</span>
            </div>
          ))}
        </div>
      </div>

      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-white">Expected Return</h2>
        <div className="flex items-center justify-center space-x-2 bg-gray-700 p-4 rounded-lg">
          <TrendingUp className="text-positive" size={24} />
          <p className="text-3xl font-bold text-positive">{advice.expectedReturn}%</p>
          <p className="text-gray-300">annual return</p>
        </div>
      </div>

      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-white">Next Steps</h2>
        <ul className="space-y-2 bg-gray-700 p-4 rounded-lg">
          <li className="flex items-center space-x-2 text-white">
            <ArrowRight className="text-positive" size={20} />
            <span>Open a brokerage account if you haven't already</span>
          </li>
          <li className="flex items-center space-x-2 text-white">
            <ArrowRight className="text-positive" size={20} />
            <span>Set up automatic monthly contributions</span>
          </li>
          <li className="flex items-center space-x-2 text-white">
            <ArrowRight className="text-positive" size={20} />
            <span>Diversify your portfolio according to the recommended allocation</span>
          </li>
        </ul>
      </div>

      <Button className="w-full bg-positive text-black font-semibold py-3 rounded-xl">Start Investing Now</Button>
    </div>
  )
}
