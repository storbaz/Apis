"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api, User, ApiKeyItem } from "@/lib/api";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [keys, setKeys] = useState<ApiKeyItem[]>([]);
  const [newKeyName, setNewKeyName] = useState("");
  const [newKey, setNewKey] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [creatingKey, setCreatingKey] = useState(false);
  const [error, setError] = useState("");

  const loadData = useCallback(async (token: string) => {
    try {
      const [userData, keysData] = await Promise.all([
        api.auth.me(token),
        api.apiKeys.list(token),
      ]);
      setUser(userData);
      setKeys(keysData.keys);
    } catch {
      localStorage.removeItem("token");
      router.push("/login");
    } finally {
      setLoading(false);
    }
  }, [router]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }
    loadData(token);
  }, [router, loadData]);

  const createKey = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    if (!token || !newKeyName.trim()) return;
    setCreatingKey(true);
    try {
      const key = await api.apiKeys.create(token, newKeyName.trim());
      setNewKey(key.key);
      setNewKeyName("");
      await loadData(token);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setCreatingKey(false);
    }
  };

  const revokeKey = async (id: number) => {
    const token = localStorage.getItem("token");
    if (!token || !confirm("Revoke this API key? This cannot be undone.")) return;
    try {
      await api.apiKeys.revoke(token, id);
      await loadData(token);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_id");
    router.push("/");
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-400">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 font-bold text-lg">
          <span>☕</span> CommodityData.io
        </Link>
        <div className="flex items-center gap-4 text-sm">
          <span className="text-gray-500">{user?.email}</span>
          <span className="bg-green-50 text-green-700 px-2 py-1 rounded text-xs font-medium uppercase">
            {user?.plan}
          </span>
          <button onClick={logout} className="text-gray-400 hover:text-gray-600">
            Sign out
          </button>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

        {error && (
          <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg mb-4">{error}</div>
        )}

        {newKey && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
            <div className="text-sm font-medium text-green-800 mb-2">
              Your new API key (copy it now, it won&apos;t be shown again):
            </div>
            <code className="bg-white border rounded px-3 py-2 text-sm block break-all">{newKey}</code>
            <button
              onClick={() => {
                navigator.clipboard.writeText(newKey);
              }}
              className="mt-2 text-sm text-green-700 hover:text-green-800 underline"
            >
              Copy to clipboard
            </button>
          </div>
        )}

        <div className="bg-white rounded-xl border p-6 mb-6">
          <h2 className="font-semibold mb-3">Quick Start</h2>
          <div className="bg-gray-900 text-green-400 rounded-lg p-4 font-mono text-sm overflow-x-auto">
            <pre>{`curl -H "X-API-Key: cd_your_key_here" \\
  http://localhost:8001/v1/overview`}</pre>
          </div>
          <p className="text-sm text-gray-500 mt-3">
            Base URL: <code className="bg-gray-100 px-1 rounded">http://localhost:8001</code> (dev)
          </p>
        </div>

        {user?.plan === "free" && (
          <div className="bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-xl p-6 mb-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-green-800">Upgrade to Pro</h3>
                <p className="text-sm text-green-700 mt-1">Get 10,000 requests/month, priority support, and webhook alerts.</p>
              </div>
              <a
                href="/pricing"
                className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition whitespace-nowrap"
              >
                View Plans →
              </a>
            </div>
          </div>
        )}

        <div className="bg-white rounded-xl border p-6">
          <h2 className="font-semibold mb-4">API Keys</h2>

          <form onSubmit={createKey} className="flex gap-2 mb-4">
            <input
              type="text"
              value={newKeyName}
              onChange={(e) => setNewKeyName(e.target.value)}
              placeholder="Key name (e.g. 'dev', 'production')"
              className="flex-1 border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
            />
            <button
              type="submit"
              disabled={creatingKey || !newKeyName.trim()}
              className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50"
            >
              {creatingKey ? "Creating..." : "Create Key"}
            </button>
          </form>

          {keys.length === 0 ? (
            <p className="text-gray-400 text-sm py-4 text-center">
              No API keys yet. Create one above to get started.
            </p>
          ) : (
            <div className="space-y-3">
              {keys.map((k) => (
                <div key={k.id} className="flex items-center justify-between border rounded-lg px-4 py-3">
                  <div>
                    <div className="font-medium text-sm">{k.name}</div>
                    <div className="text-xs text-gray-400 font-mono">{k.key.slice(0, 20)}...</div>
                    <div className="text-xs text-gray-400 mt-1">
                      Created: {new Date(k.created_at).toLocaleDateString()}
                      {k.last_used_at && ` · Last used: ${new Date(k.last_used_at).toLocaleDateString()}`}
                      {` · Limit: ${k.rate_limit}/day`}
                    </div>
                  </div>
                  <button
                    onClick={() => revokeKey(k.id)}
                    className="text-red-500 hover:text-red-700 text-sm"
                  >
                    Revoke
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
