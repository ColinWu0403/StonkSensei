"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";

const stocks = [
  "AAPL",
  "GOOG",
  "MSFT",
  "GME",
  "NVDA",
  "TSLA",
  "AMZN",
  "META",
  "NFLX",
  "INTC",
  "AMD",
  "UBER",
  "LYFT",
  "SNAP",
  "TWTR",
  "PINS",
  "SPOT",
  "PYPL",
  "BTC",
  "SHOP",
  "ADBE",
  "CRM",
  "DOCU",
  "OKTA",
  "WORK",
  "TEAM",
  "NOW",
  "CRWD",
  "NET",
  "DDOG",
];

const MovingColumn = ({ columnIndex }: { columnIndex: number }) => {
  const [columnStocks, setColumnStocks] = useState<string[]>([]);

  useEffect(() => {
    const shuffled = [...stocks].sort(() => 0.5 - Math.random());
    setColumnStocks(shuffled);
  }, []);

  return (
    <motion.div
      className="absolute top-0 flex flex-col items-center"
      style={{
        left: `${columnIndex * 10}%`,
        width: "10%",
      }}
      initial={{ y: "0%" }}
      animate={{ y: "-50%" }}
      transition={{
        y: {
          repeat: Number.POSITIVE_INFINITY,
          repeatType: "loop",
          duration: 35,
          ease: "linear",
        },
      }}
    >
      {columnStocks.concat(columnStocks).map((stock, index) => (
        <div
          key={`${stock}-${index}`}
          className="text-xs font-medium text-gray-300 opacity-10 whitespace-nowrap h-8 flex items-center justify-center"
        >
          {stock}
        </div>
      ))}
    </motion.div>
  );
};

export const MovingBackground = () => {
  const columns = 10;

  return (
    <div className="fixed inset-0 overflow-hidden bg-neutral">
      {Array.from({ length: columns }).map((_, columnIndex) => (
        <MovingColumn key={columnIndex} columnIndex={columnIndex} />
      ))}
    </div>
  );
};
