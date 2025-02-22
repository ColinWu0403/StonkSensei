
import { type NextRequest } from 'next/server'
import dbClient from '@/lib/mongodb'

export async function GET(request: NextRequest) {

  const searchParams = request.nextUrl.searchParams
  const email = searchParams.get('email')

  if (!email) {
    return new Response('Email is required', { status: 400 })
  }

  const client = await dbClient()
  const db = client.db('stonk_sensei')
  const collection = db.collection('users')

  const user = await collection.findOne({ email })

  if (!user) {
    return new Response('User not found', { status: 404 })
  }

  return new Response(JSON.stringify(user), { status: 200 })
}

export async function POST(request: NextRequest) {
  
  const body = await request.json()
  const { email } = body

  if (!email) {
    return new Response('Email, name and picture are required', { status: 400 })
  }

  const client = await dbClient()
  const db = client.db('stonk_sensei')
  const collection = db.collection('users')

  const user = await collection.findOne({ email })

  if (user) {
    return new Response('User already exists', { status: 409 })
  }

  const newUser = await collection.insertOne({ email })

  return new Response(JSON.stringify(newUser), { status: 201 })
}