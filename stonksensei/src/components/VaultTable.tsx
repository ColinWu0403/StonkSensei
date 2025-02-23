import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

export interface Advice {
  ticker: string;
  category: string;
  risk: number;
  hype: number;
  sentiment: number;
  reasoning: string;
  links: string[];
  final_score: number;
}

const categoryColors: Record<string, string> = {
  Yolo: "bg-red-100 text-red-800",
  "Good trade": "bg-green-100 text-green-800",
  "Bad trade": "bg-yellow-100 text-yellow-800",
};

function getGradientColor(value: number) {
  const red = Math.max(255 - value * 2.55, 0);
  const green = Math.min(value * 2.55, 255);
  return `rgb(${red}, ${green}, 100)`;
}

export function VaultTable({ advice }: { advice: Advice[] }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Ticker</TableHead>
          <TableHead>Category</TableHead>
          <TableHead>Risk</TableHead>
          <TableHead>Hype</TableHead>
          <TableHead>Sentiment</TableHead>
          <TableHead>Links</TableHead>
          <TableHead>Reason</TableHead>
          <TableHead>Final Score</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {advice.map((a) => (
          <TableRow key={a.ticker}>
            <TableCell className="font-medium">{a.ticker}</TableCell>
            <TableCell>
              <span
                className={cn(
                  "px-2 py-1 rounded-md text-sm font-semibold text-center",
                  categoryColors[a.category] || "bg-gray-100 text-gray-800"
                )}
              >
                {a.category}
              </span>
            </TableCell>
            <TableCell className="text-center">{a.risk}</TableCell>
            <TableCell className="text-center">{a.hype}</TableCell>
            <TableCell
              style={{ color: getGradientColor(a.sentiment) }}
              className="font-bold text-md text-center"
            >
              {a.sentiment}
            </TableCell>
            <TableCell>
              <div className="flex gap-1 max-w-xs overflow-x-auto">
                {a.links.map((link) => (
                  <a
                    href={link}
                    target="_blank"
                    rel="noopener noreferrer"
                    key={link}
                    className="text-blue-400 italic underline text-sm"
                  >
                    {new URL(link).hostname}
                  </a>
                ))}
              </div>
            </TableCell>
            <TableCell className="text-gray-500 text-sm italic max-w-xs overflow-x-auto">
              {a.reasoning}
            </TableCell>
            <TableCell
              style={{ color: getGradientColor(a.final_score) }}
              className="font-bold text-md text-center"
            >
              {a.final_score}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
