import { MongoClient, ServerApiVersion } from 'mongodb';

const uri = process.env.MONGODB_URI;

const client = new MongoClient(uri!, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

let clientPromise: Promise<MongoClient> | null = null;

async function dbClient() {
  if (!clientPromise) {
    clientPromise = (async () => {
      try {
        await client.connect();
        await client.db("admin").command({ ping: 1 });
        console.log("Pinged your deployment. You successfully connected to MongoDB!");
        return client; // Return the client for querying
      } catch (error) {
        console.error("Failed to connect to MongoDB", error);
        throw error;
      }
    })();
  }
  return clientPromise;
}

export default dbClient;
