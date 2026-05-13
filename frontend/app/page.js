"use client";

import { useEffect, useMemo, useState } from "react";
import axios from "axios";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

const API_BASE_URL = "http://127.0.0.1:8000";

export default function Home() {
  const [assets, setAssets] = useState([]);
  const [portfolio, setPortfolio] = useState(null);
  const [news, setNews] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [assetId, setAssetId] = useState("");
  const [quantity, setQuantity] = useState("");
  const [marketHistory, setMarketHistory] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [newsHistory, setNewsHistory] = useState([]);
  const [selectedChartAsset, setSelectedChartAsset] = useState("");
  const [message, setMessage] = useState("");
  const [marketMovements, setMarketMovements] = useState([]);
  const [economicIndicators, setEconomicIndicators] = useState(null);
  const [marketRegime, setMarketRegime] = useState("");
  const [advisor, setAdvisor] = useState(null);

  const fetchAssets = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/market/assets`);
      setAssets(response.data);

      if (!selectedChartAsset && response.data.length > 0) {
        setSelectedChartAsset(response.data[0].name);
      }
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

  const fetchMarketHistory = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/market/history`);
      setMarketHistory(response.data);
    } catch (error) {
      console.error("FETCH MARKET HISTORY ERROR:", error);
    }
  };

  const fetchTransactions = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/transactions`);
      setTransactions(response.data);
    } catch (error) {
      console.error("FETCH TRANSACTIONS ERROR:", error);
    }
  };

  const fetchNewsHistory = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/news/history`);
      setNewsHistory(response.data);
    } catch (error) {
      console.error("FETCH NEWS HISTORY ERROR:", error);
    }
  };

  const fetchEconomicIndicators = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/economy/indicators`);
      setEconomicIndicators(response.data);
    } catch (error) {
      console.error("FETCH ECONOMIC INDICATORS ERROR:", error);
    }
  };

  const fetchAdvisor = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/advisor/portfolio`);
      setAdvisor(response.data);
    } catch (error) {
      console.error("FETCH ADVISOR ERROR:", error);
    }
  };

  const refreshAll = async () => {
    await fetchAssets();
    await fetchPortfolio();
    await fetchMarketHistory();
    await fetchTransactions();
    await fetchNewsHistory();
    await fetchEconomicIndicators();
    await fetchAdvisor();
  };

  const simulateEvent = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/market/simulate-event`);

      setNews(response.data.news);
      setExplanation(response.data.ai_explanation);
      setAssets(response.data.updated_assets);
      setMarketMovements(response.data.market_movements || []);
      setEconomicIndicators(response.data.economic_indicators);
      setMarketRegime(response.data.market_regime || "");
      setMessage("Market event generated successfully.");

      await fetchPortfolio();
      await fetchMarketHistory();
      await fetchNewsHistory();
      await fetchAdvisor();
    } catch (error) {
      console.error("SIMULATE EVENT ERROR:", error);
      setMessage("Failed to generate market event.");
    }
  };

  const buyAsset = async () => {
    try {
      if (!assetId || !quantity) {
        setMessage("Please select an asset and enter quantity.");
        return;
      }

      const response = await axios.post(`${API_BASE_URL}/trade/buy`, {
        asset_id: Number(assetId),
        quantity: Number(quantity),
      });

      if (response.data.error) {
        setMessage(response.data.error);
        return;
      }

      setAssetId("");
      setQuantity("");
      setMessage("Buy order successful.");

      await fetchAssets();
      await fetchPortfolio();
      await fetchTransactions();
      await fetchAdvisor();
    } catch (error) {
      console.error("BUY ASSET ERROR:", error);
      setMessage("Buy order failed.");
    }
  };

  const sellAsset = async () => {
    try {
      if (!assetId || !quantity) {
        setMessage("Please select an asset and enter quantity.");
        return;
      }

      const response = await axios.post(`${API_BASE_URL}/trade/sell`, {
        asset_id: Number(assetId),
        quantity: Number(quantity),
      });

      if (response.data.error) {
        setMessage(response.data.error);
        return;
      }

      setAssetId("");
      setQuantity("");
      setMessage("Sell order successful.");

      await fetchAssets();
      await fetchPortfolio();
      await fetchTransactions();
      await fetchAdvisor();
    } catch (error) {
      console.error("SELL ASSET ERROR:", error);
      setMessage("Sell order failed.");
    }
  };

  const resetSimulation = async () => {
    try {
      await axios.post(`${API_BASE_URL}/simulation/reset`);

      setNews(null);
      setExplanation(null);
      setMarketMovements([]);
      setAdvisor(null);
      setMarketRegime("");
      setMessage("Simulation reset successfully.");

      await refreshAll();
    } catch (error) {
      console.error("RESET SIMULATION ERROR:", error);
      setMessage("Simulation reset failed.");
    }
  };

  useEffect(() => {
    refreshAll();
  }, []);

  const filteredMarketHistory = useMemo(() => {
    return marketHistory
      .filter((item) => item.asset_name === selectedChartAsset)
      .map((item) => ({
        ...item,
        time: new Date(item.timestamp).toLocaleTimeString(),
      }));
  }, [marketHistory, selectedChartAsset]);

  return (
    <main className="min-h-screen bg-gray-950 text-white p-8">
      <h1 className="text-4xl font-bold mb-2">EconArena AI</h1>

      <p className="text-gray-400 mb-8">
        AI-powered news-driven market simulation platform
      </p>

      {message && (
        <section className="bg-gray-800 p-4 rounded-xl mb-6 border border-gray-700">
          <p>{message}</p>
        </section>
      )}

      <section className="mb-8 flex gap-4">
        <button
          onClick={simulateEvent}
          className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold"
        >
          Generate Market Event
        </button>

        <button
          onClick={resetSimulation}
          className="bg-gray-700 hover:bg-gray-600 px-6 py-3 rounded-lg font-semibold"
        >
          Reset Simulation
        </button>
      </section>

      {marketRegime && (
  <section className="bg-gray-900 p-6 rounded-xl mb-8 border border-gray-800">
    <h2 className="text-2xl font-semibold mb-2">Current Market Regime</h2>

    <p
      className={`text-3xl font-bold ${
        marketRegime === "Panic" || marketRegime === "Recession"
          ? "text-red-400"
          : marketRegime === "Expansion"
          ? "text-green-400"
          : marketRegime === "Inflationary"
          ? "text-yellow-400"
          : "text-blue-400"
      }`}
    >
      {marketRegime}
    </p>

    <p className="text-gray-400 mt-2">
      This regime is calculated from inflation, interest rates, GDP growth,
      unemployment, and fear conditions.
    </p>
  </section>
)}

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

      {marketMovements.length > 0 && (
        <section className="bg-gray-900 p-6 rounded-xl mb-8 border border-gray-800">
          <h2 className="text-2xl font-semibold mb-4">
            Market Movement Breakdown
          </h2>

          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="py-2">Asset</th>
                <th>Sector</th>
                <th>Old Price</th>
                <th>New Price</th>
                <th>Impact</th>
                <th>Macro Pressure</th>
                <th>Regime</th>
              </tr>
            </thead>

            <tbody>
              {marketMovements.map((movement) => (
                <tr
                  key={movement.asset_name}
                  className="border-b border-gray-800"
                >
                  <td className="py-2">{movement.asset_name}</td>
                  <td>{movement.sector}</td>
                  <td>${movement.old_price}</td>
                  <td>${movement.new_price}</td>
                  <td
                    className={
                      movement.impact_percent >= 0
                        ? "text-green-400"
                        : "text-red-400"
                    }
                  >
                    {movement.impact_percent}%
                  </td>

                  <td
                    className={
                      movement.macro_pressure_percent >= 0
                        ? "text-green-400"
                        : "text-red-400"
                    }
                    >
                    {movement.macro_pressure_percent}%
                    </td>
                  <td>{movement.market_regime}</td>
                </tr>
              ))}
            </tbody>
          </table>
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
          <select
            value={assetId}
            onChange={(event) => setAssetId(event.target.value)}
            className="p-3 rounded bg-gray-800 border border-gray-700"
          >
            <option value="">Select Asset</option>
            {assets.map((asset) => (
              <option key={asset.id} value={asset.id}>
                {asset.name} — ${asset.price}
              </option>
            ))}
          </select>

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

      <section className="bg-gray-900 p-6 rounded-xl mb-8 border border-gray-800">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold">Market Price History</h2>

          <select
            value={selectedChartAsset}
            onChange={(event) => setSelectedChartAsset(event.target.value)}
            className="p-3 rounded bg-gray-800 border border-gray-700"
          >
            {assets.map((asset) => (
              <option key={asset.id} value={asset.name}>
                {asset.name}
              </option>
            ))}
          </select>
        </div>

        <div className="w-full h-[400px] min-w-0">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={filteredMarketHistory}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="price"
                stroke="#3b82f6"
                strokeWidth={3}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="bg-gray-900 p-6 rounded-xl mb-8 border border-gray-800">
        <h2 className="text-2xl font-semibold mb-4">News History</h2>

        {newsHistory.length === 0 ? (
          <p className="text-gray-400">No news events yet.</p>
        ) : (
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="py-2">Headline</th>
                <th>Sector</th>
                <th>Sentiment</th>
                <th>Severity</th>
              </tr>
            </thead>

            <tbody>
              {newsHistory.map((event) => (
                <tr key={event.id} className="border-b border-gray-800">
                  <td className="py-2">{event.title}</td>
                  <td>{event.sector}</td>
                  <td>{event.sentiment}</td>
                  <td>{event.severity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section className="bg-gray-900 p-6 rounded-xl mb-8 border border-gray-800">
        <h2 className="text-2xl font-semibold mb-4">Transaction History</h2>

        {transactions.length === 0 ? (
          <p className="text-gray-400">No transactions yet.</p>
        ) : (
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="py-2">Type</th>
                <th>Asset</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total Value</th>
              </tr>
            </thead>

            <tbody>
              {transactions.map((transaction) => (
                <tr key={transaction.id} className="border-b border-gray-800">
                  <td className="py-2">{transaction.trade_type}</td>
                  <td>{transaction.asset_name}</td>
                  <td>{transaction.quantity}</td>
                  <td>${transaction.price}</td>
                  <td>${transaction.total_value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {portfolio && (
        <section className="bg-gray-900 p-6 rounded-xl mb-8 border border-gray-800">
          <h2 className="text-2xl font-semibold mb-4">Portfolio Analytics</h2>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-gray-800 p-4 rounded-lg">
              <p className="text-gray-400">Cash</p>
              <p className="text-2xl font-bold">${portfolio.cash}</p>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <p className="text-gray-400">Holdings Value</p>
              <p className="text-2xl font-bold">${portfolio.holdings_value}</p>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <p className="text-gray-400">Total Portfolio Value</p>
              <p className="text-2xl font-bold">
                ${portfolio.total_portfolio_value}
              </p>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <p className="text-gray-400">Unrealized P/L</p>
              <p
                className={`text-2xl font-bold ${
                  portfolio.total_unrealized_pl >= 0
                    ? "text-green-400"
                    : "text-red-400"
                }`}
              >
                ${portfolio.total_unrealized_pl}
              </p>
            </div>
          </div>

          <h3 className="text-lg font-semibold mb-2">Holdings</h3>

          {!portfolio.holdings || portfolio.holdings.length === 0 ? (
            <p className="text-gray-400">No assets owned yet.</p>
          ) : (
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="py-2">Asset</th>
                  <th>Quantity</th>
                  <th>Avg Price</th>
                  <th>Current Price</th>
                  <th>Current Value</th>
                  <th>Unrealized P/L</th>
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
                    <td>${holding.current_price}</td>
                    <td>${holding.current_value}</td>
                    <td
                      className={
                        holding.unrealized_pl >= 0
                          ? "text-green-400"
                          : "text-red-400"
                      }
                    >
                      ${holding.unrealized_pl}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      )}

      {advisor && (
  <section className="bg-gray-900 p-6 rounded-xl mb-8 border border-gray-800">
    <h2 className="text-2xl font-semibold mb-4">AI Portfolio Advisor</h2>

    <div className="bg-gray-800 p-4 rounded-lg mb-4">
      <p className="text-gray-400">Risk Level</p>

      <p
        className={`text-3xl font-bold ${
          advisor.risk_level === "High"
            ? "text-red-400"
            : advisor.risk_level === "Medium"
            ? "text-yellow-400"
            : "text-green-400"
        }`}
      >
        {advisor.risk_level}
      </p>
    </div>

    <div className="mb-4">
      <h3 className="text-lg font-semibold mb-2">Summary</h3>
      <p className="text-gray-300">{advisor.summary}</p>
    </div>

    <div className="mb-4">
      <h3 className="text-lg font-semibold mb-2">Warnings</h3>

      <ul className="list-disc list-inside text-gray-300 space-y-1">
        {advisor.warnings.map((warning, index) => (
          <li key={index}>{warning}</li>
        ))}
      </ul>
    </div>

    <div className="mb-4">
      <h3 className="text-lg font-semibold mb-2">Suggestions</h3>

      <ul className="list-disc list-inside text-gray-300 space-y-1">
        {advisor.suggestions.map((suggestion, index) => (
          <li key={index}>{suggestion}</li>
        ))}
      </ul>
    </div>

    <div>
      <h3 className="text-lg font-semibold mb-2">Sector Exposure</h3>

      {Object.keys(advisor.sector_exposure).length === 0 ? (
        <p className="text-gray-400">No sector exposure yet.</p>
      ) : (
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="py-2">Sector</th>
              <th>Exposure</th>
            </tr>
          </thead>

          <tbody>
            {Object.entries(advisor.sector_exposure).map(
              ([sector, exposure]) => (
                <tr key={sector} className="border-b border-gray-800">
                  <td className="py-2">{sector}</td>
                  <td>{exposure}%</td>
                </tr>
              )
            )}
          </tbody>
        </table>
      )}
    </div>
  </section>
)}

      {economicIndicators && (
        <section className="bg-gray-900 p-6 rounded-xl border border-gray-800">
          <h2 className="text-2xl font-semibold mb-4">Economic Indicators</h2>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <div className="bg-gray-800 p-4 rounded-lg">
              <p className="text-gray-400">Inflation</p>
              <p className="text-2xl font-bold">
                {economicIndicators.inflation}%
              </p>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <p className="text-gray-400">Interest Rate</p>
              <p className="text-2xl font-bold">
                {economicIndicators.interest_rate}%
              </p>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <p className="text-gray-400">GDP Growth</p>
              <p className="text-2xl font-bold">
                {economicIndicators.gdp_growth}%
              </p>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <p className="text-gray-400">Unemployment</p>
              <p className="text-2xl font-bold">
                {economicIndicators.unemployment}%
              </p>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <p className="text-gray-400">Fear Index</p>
              <p
                className={`text-2xl font-bold ${
                  economicIndicators.fear_index >= 50
                    ? "text-red-400"
                    : "text-green-400"
                }`}
              >
                {economicIndicators.fear_index}
              </p>
            </div>
          </div>
        </section>
      )}
    </main>
  );
}