import { Check, Zap, BarChart } from "lucide-react";

const icons = [Check, Zap, BarChart];

export default function AnimatedBackground() {
  return (
    <div className="fixed inset-0 w-full h-full pointer-events-none z-0">
      <div className="absolute inset-0 flex items-center justify-center">
        {[...Array(50)].map((_, i) => {
          const Icon = icons[i % icons.length];
          const delay = Math.random() * 1;
          const duration = 20 + Math.random() * 10;
          const size = 20 + Math.random() * 30;

          return (
            <Icon
              key={i}
              className="absolute text-gray-700 opacity-5"
              style={{
                fontSize: `${size}px`,
                left: `${Math.random() * 100}%`,
                animation: `float ${duration}s ease-in-out ${0.6}s infinite`,
              }}
            />
          );
        })}
      </div>
    </div>
  );
}
