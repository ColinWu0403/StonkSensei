"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

export default function FinancialAdviceForm() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    income: "",
    expenses: "",
    goals: "",
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }))
  }

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    console.log(formData)
    // Here you would typically send the data to your backend
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <Label htmlFor="name" className="text-white">
            Name
          </Label>
          <Input
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="mt-1 bg-gray-700 text-white border-gray-600"
          />
        </div>
        <div>
          <Label htmlFor="email" className="text-white">
            Email
          </Label>
          <Input
            id="email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="mt-1 bg-gray-700 text-white border-gray-600"
          />
        </div>
        <div>
          <Label htmlFor="income" className="text-white">
            Monthly Income
          </Label>
          <Input
            id="income"
            name="income"
            type="number"
            value={formData.income}
            onChange={handleChange}
            required
            className="mt-1 bg-gray-700 text-white border-gray-600"
          />
        </div>
        <div>
          <Label htmlFor="expenses" className="text-white">
            Monthly Expenses
          </Label>
          <Input
            id="expenses"
            name="expenses"
            type="number"
            value={formData.expenses}
            onChange={handleChange}
            required
            className="mt-1 bg-gray-700 text-white border-gray-600"
          />
        </div>
      </div>
      <div>
        <Label htmlFor="goals" className="text-white">
          Financial Goals
        </Label>
        <Textarea
          id="goals"
          name="goals"
          value={formData.goals}
          onChange={handleChange}
          required
          className="mt-1 bg-gray-700 text-white border-gray-600"
          rows={4}
        />
      </div>
      <Button type="submit" className="w-full bg-positive text-black font-semibold py-3">
        Get Financial Advice
      </Button>
    </form>
  )
}

