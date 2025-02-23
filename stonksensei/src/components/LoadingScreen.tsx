"use client"

"use client"

import { useEffect, useState } from "react"
import { TrendingUp, TrendingDown, BarChart2, Activity, MessageCircle, Zap, Rocket } from "lucide-react"

const investmentStages = [
  {
    name: "Collecting Fundamentals",
    icon: BarChart2,
    color: "text-blue-400",
    sentence: "Analyzing market fundamentals...",
  },
  { name: "Judging Volatility", icon: Activity, color: "text-yellow-400", sentence: "Assessing market volatility..." },
  { name: "Sentiment Analysis", icon: MessageCircle, color: "text-positive", sentence: "Gauging market sentiment..." },
  { name: "Hype Measurements", icon: Zap, color: "text-purple-400", sentence: "Measuring hype levels..." },
  { name: "YOLO Factor", icon: Rocket, color: "text-negative", sentence: "Optimizing YOLO factor..." },
]

export default function LoadingScreen() {
  const [currentStage, setCurrentStage] = useState(0)
  const [marketTrend, setMarketTrend] = useState<"up" | "down">("up")

  useEffect(() => {
    const stageInterval = setInterval(() => {
      setCurrentStage((prevStage) => (prevStage + 1) % investmentStages.length)
    }, 3000) // Change stage every 3 seconds

    const trendInterval = setInterval(() => {
      setMarketTrend((prev) => (Math.random() > 0.5 ? "up" : "down"))
    }, 2000) // Change trend randomly every 2 seconds

    return () => {
      clearInterval(stageInterval)
      clearInterval(trendInterval)
    }
  }, [])

  return (
    <div className="flex flex-col items-center justify-center min-h-[90vh] bg-neutral text-white p-4">
      <h1 className="text-3xl font-bold mb-12">Optimizing Your Investment</h1>
      <div className="mb-12 relative">
        <svg className="w-48 h-48 animate-spin" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="45" fill="none" stroke="#1d1d1d" strokeWidth="8" />
          <path d="M50 5 A45 45 0 0 1 95 50" fill="none" stroke="#B2E911" strokeWidth="8" strokeLinecap="round" />
        </svg>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 flex items-center justify-center">
          {marketTrend === "up" ? (
            <TrendingUp className="w-16 h-16 text-white" />
          ) : (
            <TrendingDown className="w-16 h-16 text-white" />
          )}
        </div>
      </div>
      <div className="text-center h-8">
        {investmentStages.map((stage, index) => (
          <div
            key={stage.name}
            className={`flex items-center justify-center space-x-2 transition-opacity duration-500 absolute left-1/2 transform -translate-x-1/2 ${
              index === currentStage ? "opacity-100" : "opacity-0"
            }`}
          >
            <stage.icon className={`w-6 h-6 ${stage.color}`} />
            <p className="text-lg">{stage.sentence}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

