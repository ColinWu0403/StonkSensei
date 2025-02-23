"use client";

import Header from "@/components/Header";
import Hero from "@/components/Hero";
import Features from "@/components/Features";
import { MovingBackground } from "@/components/MovingBackground";

export default function Home() {
  return (
    <div className="flex flex-col min-h-[90vh] relative z-10">
      <MovingBackground />
      <Header />
      <main className="flex-grow h-[90vh] relative z-10">
        <Hero />
      </main>
    </div>
  );
}
