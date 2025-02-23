"use client";

import FinancialAdviceForm from "@/components/financial-advice-form";

import { ReactNode } from "react";
import { useState } from "react";

export default function FormLayout({ children }: { children: ReactNode }) {
    return(
        <div>
            {children}
        </div>
    );
}