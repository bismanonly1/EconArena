"use client";

import { useEffect, useState } from "react";
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export default function Home() {
  const [assets, setAssets] = useState([]);
  const [portfolio, setPortfolio] = useState(null);
  const [news, setNews] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [assetId, setAssetId] = useState("");
  const [quantity, setQuantity] = useState("");

  const fetchAssets = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/market/assets`);
      setAssets(response.data);
    } catch (error) {
      console.error("FETCH ASSETS ERROR:", error);
    }
  };

  const fetchPortfolio = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/portfolio`);
      setPortfolio(response.data);
    } catch (error) {
      console.error("FETCH PORTFOLIO ERROR:", error);
    }
  };

  const simulateEvent = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/market/simulate-event`);

      setNews(response.data.news);
      setExplanation(response.data.ai_explanation);
      setAssets(response.data.updated_assets);

      await fetchPortfolio();
    } catch (error) {
      console.error("SIMULATE EVENT ERROR:", error);
    }
  };

  const buyAsset = async () => {
    try {
      if (!assetId || !quantity) {
        alert("Please enter both Asset ID and Quantity.");
        return;
      }

      await axios.post(`${API_BASE_URL}/trade/buy`, {
        asset_id: Number(assetId),
        quantity: Number(quantity),
      });

      setAssetId("");
      setQuantity("");

      await fetchAssets();
      await fetchPortfolio();
    } catch (error) {
      console.error("BUY ASSET ERROR:", error);
    }
  };

  const sellAsset = async () => {
    try {
      if (!assetId || !quantity) {
        alert("Please enter both Asset ID and Quantity.");
        return;
      }

      await axios.post(`${API_BASE_URL}/trade/sell`, {
        asset_id: Number(assetId),
        quantity: Number(quantity),
      });

      setAssetId("");
      setQuantity("");

      await fetchAssets();
      await fetchPortfolio();
    } catch (error) {
      console.error("SELL ASSET ERROR:", error);
    }
  };

  useEffect(() => {
    fetchAssets();
    fetchPortfolio();
  }, []);

  return (
    <main className="min-h-screen bg-gray-950 text-white p-8">
      <h1 className="text-4xl font-bold mb-2">EconArena AI</h1>

      <p className="text-gray-400 mb-8">
        AI-powered news-driven market simulation platform
      </p>

      <section className="mb-8">
        <button
          onClick={simulateEvent}
          className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold"
        >
          Generate Market Event
        </button>
      </section>

      {news && (
        <section className="bg-gray-900 p-6 rounded-xl mb-8 border border-gray-800">
          <h2 className="text-2xl font-semibold mb-2">Latest Market News</h2>

          <p className="text-lg">{news.title}</p>

          <p className="text-gray-400 mt-2">
            Sector: {news.sector} | Sentiment: {news.sentiment} | Severity:{" "}
            {news.severity}
          </p>
        </section>
      )}

      {explanation && (
        <section className="bg-gray-900 p-6 rounded-xl mb-8 border border-gray-800">
          <h2 className="text-2xl font-semibold mb-2">AI Explanation</h2>

          <p className="text-gray-300 mb-3">{explanation.explanation}</p>

          <p className="text-blue-300">{explanation.learning_point}</p>
        </section>
      )}

      <section className="bg-gray-900 p-6 rounded-xl mb-8 border border-gray-800">
        <h2 className="text-2xl font-semibold mb-4">Market Assets</h2>

        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="py-2">ID</th>
              <th>Name</th>
              <th>Sector</th>
              <th>Price</th>
              <th>Volatility</th>
            </tr>
          </thead>

          <tbody>
            {assets.map((asset) => (
              <tr key={asset.id} className="border-b border-gray-800">
                <td className="py-2">{asset.id}</td>
                <td>{asset.name}</td>
                <td>{asset.sector}</td>
                <td>${asset.price}</td>
                <td>{asset.volatility}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="bg-gray-900 p-6 rounded-xl mb-8 border border-gray-800">
        <h2 className="text-2xl font-semibold mb-4">Trade</h2>

        <div className="flex gap-4 mb-4">
          <input
            type="number"
            placeholder="Asset ID"
            value={assetId}
            onChange={(event) => setAssetId(event.target.value)}
            className="p-3 rounded bg-gray-800 border border-gray-700"
          />

          <input
            type="number"
            placeholder="Quantity"
            value={quantity}
            onChange={(event) => setQuantity(event.target.value)}
            className="p-3 rounded bg-gray-800 border border-gray-700"
          />
        </div>

        <div className="flex gap-4">
          <button
            onClick={buyAsset}
            className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-lg font-semibold"
          >
            Buy
          </button>

          <button
            onClick={sellAsset}
            className="bg-red-600 hover:bg-red-700 px-6 py-3 rounded-lg font-semibold"
          >
            Sell
          </button>
        </div>
      </section>

      {portfolio && (
        <section className="bg-gray-900 p-6 rounded-xl border border-gray-800">
          <h2 className="text-2xl font-semibold mb-4">Portfolio</h2>

          <p className="mb-4 text-xl">Cash: ${portfolio.cash}</p>

          <h3 className="text-lg font-semibold mb-2">Holdings</h3>

          {!portfolio.holdings || portfolio.holdings.length === 0 ? (
            <p className="text-gray-400">No assets owned yet.</p>
          ) : (
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="py-2">Asset</th>
                  <th>Quantity</th>
                  <th>Average Price</th>
                </tr>
              </thead>

              <tbody>
                {portfolio.holdings.map((holding) => (
                  <tr
                    key={holding.asset_id}
                    className="border-b border-gray-800"
                  >
                    <td className="py-2">{holding.asset_name}</td>
                    <td>{holding.quantity}</td>
                    <td>${holding.average_price}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      )}
    </main>
  );
}