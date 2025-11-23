export default function Home() {
  return (
    <main className="min-h-screen p-24">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">E-Commerce Platform</h1>
        <p className="text-lg text-gray-600 mb-4">
          Welcome to our modern e-commerce platform built with:
        </p>
        <ul className="list-disc list-inside space-y-2 text-gray-700">
          <li>Next.js 14 with App Router</li>
          <li>React 18</li>
          <li>TypeScript</li>
          <li>Tailwind CSS</li>
          <li>FastAPI Backend</li>
          <li>MongoDB Database</li>
        </ul>
        <div className="mt-8 space-x-4">
          <a 
            href="/products" 
            className="inline-block px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
          >
            Browse Products
          </a>
          <a 
            href="/login" 
            className="inline-block px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
          >
            Login
          </a>
        </div>
      </div>
    </main>
  )
}
