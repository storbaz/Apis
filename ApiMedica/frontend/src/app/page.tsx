import Link from "next/link";

const features = [
  {
    title: "Production Data",
    description: "Coffee production volumes by country, year, and variety. Data from FAOSTAT and USDA spanning 1961-present.",
    icon: "🌾",
    endpoint: "GET /v1/production",
  },
  {
    title: "Price Tracking",
    description: "Monthly Arabica and Robusta prices from FRED/IMF. Historical data with daily updates.",
    icon: "📈",
    endpoint: "GET /v1/prices",
  },
  {
    title: "Export Statistics",
    description: "Global coffee export flows with origin, destination, HS codes, and trade values in USD.",
    icon: "🚢",
    endpoint: "GET /v1/exports",
  },
  {
    title: "Import Data",
    description: "Track coffee imports by destination country with detailed trade breakdowns.",
    icon: "📦",
    endpoint: "GET /v1/imports",
  },
  {
    title: "Country Profiles",
    description: "40+ coffee producing and consuming countries with regional classifications.",
    icon: "🌍",
    endpoint: "GET /v1/countries",
  },
  {
    title: "Market Overview",
    description: "Quick summary: total production, top producers, and key market metrics.",
    icon: "📊",
    endpoint: "GET /v1/overview",
  },
];

const codeExample = `// Fetch latest Arabica price
const res = await fetch("https://api.commoditydata.io/v1/prices/latest?variety=arabica", {
  headers: { "X-API-Key": "cd_your_api_key_here" }
});
const { data } = await res.json();
// → { date: "2025-06-15", variety: "arabica", price_usd_cents_per_lb: 385.4 }`;

const plans = [
  {
    name: "Free",
    price: "$0",
    period: "forever",
    requests: "100 requests/day",
    features: ["All endpoints", "Production data", "Price data", "Export/Import data"],
    cta: "Get API Key",
    ctaLink: "/register",
    highlight: false,
  },
  {
    name: "Pro",
    price: "$29",
    period: "/month",
    requests: "10,000 requests/month",
    features: ["All Free features", "Priority support", "Webhook alerts", "Bulk data export"],
    cta: "Start Pro Trial",
    ctaLink: "/register",
    highlight: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    requests: "Unlimited requests",
    features: ["All Pro features", "Dedicated support", "Custom data feeds", "SLA guarantee"],
    cta: "Contact Sales",
    ctaLink: "/register",
    highlight: false,
  },
];

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Nav */}
      <nav className="border-b border-gray-100 bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">☕</span>
            <span className="font-bold text-lg">CommodityData.io</span>
          </div>
          <div className="flex items-center gap-6 text-sm">
            <a href="#features" className="text-gray-600 hover:text-gray-900">Features</a>
            <a href="#pricing" className="text-gray-600 hover:text-gray-900">Pricing</a>
            <a href="#docs" className="text-gray-600 hover:text-gray-900">Docs</a>
            <Link href="/login" className="text-gray-600 hover:text-gray-900">Sign In</Link>
            <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">
              Get API Key
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-block bg-green-50 text-green-700 text-sm font-medium px-3 py-1 rounded-full mb-6">
            Coffee Market Data API
          </div>
          <h1 className="text-5xl font-bold mb-6 leading-tight">
            Global Coffee Commodity<br />Data in One API
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Production volumes, export/import flows, and price data from FAO, USDA, and FRED.
            The only API that gives you production data alongside prices.
          </p>
          <div className="flex items-center justify-center gap-4">
            <Link
              href="/register"
              className="bg-green-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-700 transition text-lg"
            >
              Get Free API Key
            </Link>
            <a
              href="#docs"
              className="border border-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-50 transition text-lg"
            >
              View Docs
            </a>
          </div>
          <p className="text-sm text-gray-400 mt-4">No credit card required · Free tier available</p>
        </div>
      </section>

      {/* Stats */}
      <section className="py-12 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 grid grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-3xl font-bold text-green-600">40+</div>
            <div className="text-sm text-gray-500 mt-1">Countries</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-green-600">60+</div>
            <div className="text-sm text-gray-500 mt-1">Years of Data</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-green-600">7</div>
            <div className="text-sm text-gray-500 mt-1">Endpoints</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-green-600">Free</div>
            <div className="text-sm text-gray-500 mt-1">Tier Available</div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">Everything You Need</h2>
          <p className="text-gray-600 text-center mb-12 max-w-xl mx-auto">
            The only coffee API that covers production, trade, and prices in a single integration.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f) => (
              <div key={f.title} className="border border-gray-200 rounded-xl p-6 hover:shadow-md transition">
                <div className="text-3xl mb-3">{f.icon}</div>
                <h3 className="font-semibold text-lg mb-2">{f.title}</h3>
                <p className="text-gray-600 text-sm mb-3">{f.description}</p>
                <code className="text-xs bg-gray-50 text-green-700 px-2 py-1 rounded">{f.endpoint}</code>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Code Example */}
      <section id="docs" className="py-20 px-4 bg-gray-900 text-white">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">Simple Integration</h2>
          <p className="text-gray-400 text-center mb-8">One API key. Clean REST responses. Ready in minutes.</p>
          <div className="bg-gray-800 rounded-xl p-6 font-mono text-sm overflow-x-auto">
            <pre className="text-green-400">{codeExample}</pre>
          </div>
          <div className="text-center mt-8">
            <Link href="/register" className="bg-green-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-700 transition">
              Try It Free →
            </Link>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-20 px-4">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">Simple Pricing</h2>
          <p className="text-gray-600 text-center mb-12">Start free. Scale as you grow.</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {plans.map((p) => (
              <div
                key={p.name}
                className={`rounded-xl p-6 border-2 ${
                  p.highlight
                    ? "border-green-600 shadow-lg"
                    : "border-gray-200"
                }`}
              >
                {p.highlight && (
                  <div className="text-green-600 text-xs font-semibold mb-2 uppercase">Most Popular</div>
                )}
                <h3 className="text-xl font-bold">{p.name}</h3>
                <div className="my-4">
                  <span className="text-4xl font-bold">{p.price}</span>
                  <span className="text-gray-500">{p.period}</span>
                </div>
                <p className="text-sm text-gray-500 mb-4">{p.requests}</p>
                <ul className="space-y-2 mb-6">
                  {p.features.map((f) => (
                    <li key={f} className="text-sm text-gray-600 flex items-center gap-2">
                      <span className="text-green-600">✓</span> {f}
                    </li>
                  ))}
                </ul>
                <Link
                  href={p.ctaLink}
                  className={`block text-center py-2 rounded-lg font-medium transition ${
                    p.highlight
                      ? "bg-green-600 text-white hover:bg-green-700"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  {p.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Data Sources */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-6">
            Powered by Trusted Sources
          </h2>
          <div className="flex items-center justify-center gap-12 text-gray-400">
            <div className="text-lg font-medium">FAOSTAT</div>
            <div className="text-lg font-medium">USDA FAS</div>
            <div className="text-lg font-medium">FRED / IMF</div>
            <div className="text-lg font-medium">ICO</div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 border-t">
        <div className="max-w-6xl mx-auto flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center gap-2">
            <span>☕</span>
            <span>© 2025 CommodityData.io</span>
          </div>
          <div className="flex gap-6">
            <a href="#features">Features</a>
            <a href="#pricing">Pricing</a>
            <a href="#docs">Docs</a>
            <a href="mailto:hello@commoditydata.io">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
