"use client";

import Header from "@/components/Header";
import Advice from "@/components/advice";

export default function OutputPage() {
  return (
    <div
      className="flex flex-col justify-center items-center bg-neutral relative"
      style={{ height: "90vh" }}
    >
      <Advice />
    </div>
  );
}
