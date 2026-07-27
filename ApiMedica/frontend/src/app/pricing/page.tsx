"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

const plans = [
  {
    name: "Free",
    price: "$0",
    period: "forever",
    requests: "100 requests/day",
    features: ["All endpoints", "Production data", "Price data", "Export/Import data"],
    plan: "free",
    highlight: false,
  },
  {
    name: "Pro",
    price: "$29",
    period: "/month",
    requests: "10,000 requests/month",
    features: ["All Free features", "Priority support", "Webhook alerts", "Bulk data export"],
    plan: "pro",
    highlight: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    requests: "Unlimited requests",
    features: ["All Pro features", "Dedicated support", "Custom data feeds", "SLA guarantee"],
    plan: "enterprise",
    highlight: false,
  },
];

export default function PricingPage() {
  const router = useRouter();
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState("");

  const handleCheckout = async (plan: string) => {
    if (plan === "free") {
      router.push("/register");
      return;
    }

    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }

    setLoading(plan);
    setError("");

    try {
      const res = await fetch("http://localhost:8001/v1/billing/checkout?plan=" + plan, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to create checkout session");
      }

      const data = await res.json();
      window.location.href = data.checkout_url;
    } catch (err: any) {
      setError(err.message);
      setLoading(null);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 font-bold text-lg">
          <span>☕</span> CommodityData.io
        </Link>
        <div className="flex items-center gap-4 text-sm">
          <Link href="/login" className="text-gray-600 hover:text-gray-900">Sign In</Link>
          <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">
            Get API Key
          </Link>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-4 py-16">
        <h1 className="text-4xl font-bold text-center mb-4">Simple Pricing</h1>
        <p className="text-gray-600 text-center mb-12 text-lg">Start free. Scale as you grow. No hidden fees.</p>

        {error && (
          <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg mb-6 max-w-md mx-auto text-center">{error}</div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map((p) => (
            <div
              key={p.name}
              className={`rounded-xl p-6 border-2 ${
                p.highlight ? "border-green-600 shadow-lg" : "border-gray-200 bg-white"
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
              <button
                onClick={() => handleCheckout(p.plan)}
                disabled={loading === p.plan}
                className={`w-full py-2 rounded-lg font-medium transition ${
                  p.highlight
                    ? "bg-green-600 text-white hover:bg-green-700"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                } disabled:opacity-50`}
              >
                {loading === p.plan ? "Redirecting..." : p.plan === "free" ? "Get Started" : `Choose ${p.name}`}
              </button>
            </div>
          ))}
        </div>

        <div className="text-center mt-12 text-gray-500 text-sm">
          Questions? <a href="mailto:hello@commoditydata.io" className="text-green-600 hover:text-green-700">Contact us</a>
        </div>
      </main>
    </div>
  );
}
