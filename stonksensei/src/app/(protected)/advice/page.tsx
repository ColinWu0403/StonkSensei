"use client"

import Header from "@/components/Header"
import Advice from "@/components/advice"

export default function OutputPage() {
  return (
    <div className="flex flex-col min-h-screen relative">
      <Header />
      <main className="flex-grow relative z-10 bg-gradient-to-b from-gray-900 to-neutral">
        <div className="container mx-auto px-4 py-12 md:py-24 lg:py-32 xl:py-48 flex flex-col items-center">
          <div className="text-center mb-12 max-w-3xl w-full">
            <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none text-white mb-6">
              Your Investment Strategy
            </h1>
            <div className="flex justify-center">
              <p className="max-w-[600px] text-muted-foreground text-white/70 md:text-xl">
                Based on your preferences, here's our AI-powered investment advice tailored just for you.
              </p>
            </div>
          </div>
          <div className="w-full max-w-2xl bg-gray-800 p-8 rounded-lg shadow-lg">
            <Advice />
          </div>
        </div>
      </main>
    </div>
  )
}

