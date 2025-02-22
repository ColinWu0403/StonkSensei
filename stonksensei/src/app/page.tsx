import Header from "@/components/Header";
import Hero from "@/components/Hero";
import Features from "@/components/Features";
import { MovingBackground } from "@/components/MovingBackground";
import FloatingPaths from "@/components/FloatingPaths";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen relative z-10">
      <MovingBackground />
      <Header />
      <main className="flex-grow relative z-10">
        <Hero />
        <div className="bg-gray-900">
          <Features />
        </div>
      </main>
    </div>
  );
}
