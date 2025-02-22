import FinancialAdviceForm from "@/components/financial-advice-form";
import Header from "@/components/Header";
import Hero from "@/components/Hero";
import Features from "@/components/Features";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen relative">
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
