import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "CommodityData.io - Coffee Market Data API | Production, Prices & Trade",
    template: "%s | CommodityData.io",
  },
  description:
    "REST API for global coffee commodity data. Production volumes, export/import statistics, and real-time price data from FAO, USDA, and FRED. Free tier available.",
  keywords: [
    "coffee API",
    "commodity data",
    "coffee production",
    "coffee prices",
    "FAOSTAT API",
    "USDA coffee",
    "coffee exports",
    "coffee imports",
    "market data API",
    "agricultural data",
  ],
  authors: [{ name: "CommodityData.io" }],
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://commoditydata.io",
    siteName: "CommodityData.io",
    title: "CommodityData.io - Coffee Market Data API",
    description:
      "REST API for global coffee commodity data. Production, trade, and price data.",
  },
  twitter: {
    card: "summary_large_image",
    title: "CommodityData.io - Coffee Market Data API",
    description:
      "REST API for global coffee commodity data. Production, trade, and price data.",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="canonical" href="https://commoditydata.io" />
      </head>
      <body className="antialiased">{children}</body>
    </html>
  );
}
