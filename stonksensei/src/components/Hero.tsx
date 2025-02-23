import { Button } from "@/components/ui/button";

// primary #B2E911
// bg #1D1D1D

export default function Hero() {
  return (
    <div className="relative overflow-hidden min-h-screen flex items-center">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl tracking-tight font-extrabold text-white sm:text-5xl md:text-6xl">
            <span className="inline font-light italic">Play it</span>{" "}
            <span className="inline text-negative">Safe</span>{" "}
            <span className="inline font-light italic">or</span>{" "}
            <span className="text-positive xl:inline">YOLO</span>
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-400 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            AI-powered stock recommendations based on real-time market sentiment
            and financial data. Choose your strategy—play it safe or YOLO into
            the hype train. Stay ahead of the curve with our expert insights.
          </p>
          <div className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
            <div className="rounded-md shadow">
              <Button className="w-full flex items-center justify-center px-8 py-8 border border-transparent text-base font-medium rounded-full text-black bg-positive md:py-4 md:text-lg md:px-10">
                Get started
              </Button>
            </div>
            <div className="mt-3 sm:mt-0 sm:ml-3">
              <Button
                variant="outline"
                className="w-full flex items-center justify-center px-8 py-8 text-base font-medium rounded-full bg-neutral text-white border border-white md:py-4 md:text-lg md:px-10"
              >
                Live demo
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
