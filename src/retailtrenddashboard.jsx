import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import Papa from "papaparse";

export default function RetailTrendDashboard() {
  // 🔧 State for data, filters, theme, and metric toggle
  const [data, setData] = useState([]);
  const [trendType, setTrendType] = useState("Sneakers");
  const [region, setRegion] = useState("US");
  const [theme, setTheme] = useState("dark");
  const isDark = theme === "dark";
  const [changeType, setChangeType] = useState("percent"); // or "delta"

  // 📥 Load CSV data on mount
  useEffect(() => {
    fetch("/trends.csv")
      .then((res) => res.text())
      .then((csv) => {
        Papa.parse(csv, {
          header: true,
          complete: (results) => setData(results.data),
        });
      });
  }, []);
  // 🔍 Filter data by segment and region
  const filteredData = data.filter(
    (d) => d.segment === trendType && d.region === region
  );
  // 🏷️ Identify all unique trend columns
  const trends = Array.from(
    new Set(
      filteredData.flatMap((row) =>
        Object.keys(row).filter(
          (key) =>
            !["date", "isPartial", "country", "segment", "region"].includes(key)
        )
      )
    )
  );

  // 🎨 Utility for dynamic button styling
  const getButtonStyle = (selected, value) => ({
    padding: "8px 12px",
    border: "1px solid",
    borderColor: selected === value ? "#fff" : "#444",
    borderRadius: "4px",
    backgroundColor: selected === value ? "#646cff" : "#1a1a1a",
    color: selected === value ? "#fff" : "#ccc",
    fontWeight: selected === value ? "600" : "400",
    cursor: "pointer",
    transition: "all 0.2s ease",
});
  // 📈 Prepare trend data for Plotly chart
  const series = trends.map((trend) => {
    const x = filteredData.map((row) => row.date);
    const y = filteredData.map((row) => parseFloat(row[trend]) || 0);
    return { x, y, type: "scatter", mode: "lines", name: trend };
  });

  // 📊 Calculate top 5 movers by percent or absolute delta
 const getTopMovers = () => {
    return trends
      .map((trend) => {
        const y = filteredData.map((row) => parseFloat(row[trend]) || 0);
        if (y.length < 2) return null;
        const latest = y[y.length - 1];
        const previous = y[y.length - 2];
        const delta = latest - previous;
        const percentChange = previous !== 0 ? (delta / previous) * 100 : 0;
        return { name: trend, latest, previous, delta, percentChange };
      })
      .filter(Boolean)
      .sort((a, b) =>
        changeType === "percent"
          ? Math.abs(b.percentChange) - Math.abs(a.percentChange)
          : Math.abs(b.delta) - Math.abs(a.delta)
      )
      .slice(0, 5);
  };

  const topMovers = getTopMovers();

   // 📋 Optional fixed button style (currently unused)
  const buttonStyle = {
    padding: "8px 12px",
    border: "1px solid #888",
    borderRadius: "4px",
    backgroundColor: "#222",
    color: "#fff",
    cursor: "pointer",
  };

// 🎨 JSX Layout
  return (
    <div
      style={{
        padding: "24px",
        fontFamily: "Arial, sans-serif",
        backgroundColor: isDark ? "#121212" : "#f4f4f4",
        color: isDark ? "#fff" : "#111",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column", // ✅ stack content + footer vertically
      }}
    >
         {/* Main Content Wrapper */}
      <div style={{ flex: 1, display: "flex", justifyContent: "center", padding: "24px" }}>
      <div style={{ width: "100%", maxWidth: "1400px" }}>
        {/* 🏷️ Header */}
        <h1 style={{ fontSize: "28px", fontWeight: "bold", marginBottom: "16px" }}>
          Retail Trend Tracker
        </h1>

        {/* 🌗 Theme Toggle */}
        <div style={{ marginBottom: "12px" }}>
          <button
            onClick={() => setTheme(isDark ? "light" : "dark")}
            style={{
              marginBottom: "16px",
              padding: "6px 10px",
              borderRadius: "4px",
              backgroundColor: isDark ? "#444" : "#ddd",
              color: isDark ? "#fff" : "#000",
              border: "1px solid #888",
              cursor: "pointer",
            }}
          >
            Toggle {isDark ? "Light" : "Dark"} Mode
          </button>
        </div>

        {/* 🎛️ Filter Buttons */}
        <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "16px" }}>
          <button style={getButtonStyle(trendType, "Sneakers")} onClick={() => setTrendType("Sneakers")}>Sneakers</button>
          <button style={getButtonStyle(trendType, "Fashion")} onClick={() => setTrendType("Fashion")}>Fashion</button>
          <button style={getButtonStyle(region, "US")} onClick={() => setRegion("US")}>US</button>
          <button style={getButtonStyle(region, "CA")} onClick={() => setRegion("CA")}>Canada</button>
        </div>

        {/* 📊 Top Movers Panel */}
        <div
          style={{
            backgroundColor: isDark ? "#1e1e1e" : "#f0f0f0",
            padding: "12px",
            borderRadius: "8px",
            marginBottom: "16px",
            maxWidth: "100%",
          }}
        >
          {/* 🔁 Metric Toggle */}
          <h3 style={{ marginBottom: "8px" }}>
            📈 Top Movers ({changeType === "percent" ? "WoW % Change" : "WoW Δ Points"})
          </h3>
          <div style={{ marginBottom: "8px" }}>
            <button
              onClick={() =>
                setChangeType(changeType === "percent" ? "delta" : "percent")
              }
              style={{
                backgroundColor: "#333",
                color: "#fff",
                border: "1px solid #666",
                padding: "4px 8px",
                borderRadius: "4px",
                fontSize: "0.85rem",
                cursor: "pointer",
              }}
            >
              Show {changeType === "percent" ? "Absolute Change" : "Percent Change"}
            </button>
          </div>

          {/* 📝 List of Movers */}
          <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
            {topMovers.map((mover) => {
              const isPositive = mover.delta >= 0;
              const arrow = isPositive ? "🔺" : "🔻";
              const color = isPositive ? "#4ade80" : "#f87171";
              const value = changeType === "percent"
                ? `${Math.abs(mover.percentChange).toFixed(1)}%`
                : `${Math.abs(mover.delta).toFixed(1)}`;
              return (
                <li
                  key={mover.name}
                  style={{
                    marginBottom: "6px",
                    display: "flex",
                    justifyContent: "space-between",
                  }}
                >
                  <span><strong>{mover.name}</strong></span>
                  <span style={{ color }}>{arrow} {value}</span>
                </li>
              );
            })}
          </ul>
        </div>

        {/* 📉 Main Plotly Chart */}
        <div
          style={{
            backgroundColor: isDark ? "#1e1e1e" : "#fff",
            padding: "16px",
            borderRadius: "8px",
            width: "100%",
          }}
        >
          <Plot
            data={series}
            layout={{
              title: `${region} ${trendType} Trends`,
              xaxis: { title: "Date" },
              yaxis: { title: "Google Trends Interest" },
              autosize: true,
              margin: { l: 40, r: 40, t: 50, b: 50 },
              paper_bgcolor: isDark ? "#1e1e1e" : "#fff",
              plot_bgcolor: isDark ? "#1e1e1e" : "#fff",
              font: { color: isDark ? "#fff" : "#111" },
            }}
            useResizeHandler
            style={{ width: "100%", height: "600px" }}
            config={{ responsive: true }}
          />
        </div>
      </div>
    </div>
    <footer
      style={{
        padding: "20px",
        borderTop: `1px solid ${isDark ? "#444" : "#ccc"}`,
        fontSize: "0.85rem",
        color: isDark ? "#aaa" : "#444",
        textAlign: "center",
      }}
    >
      © {new Date().getFullYear()} James Witcher ·{" "}
      <a
        href="https://github.com/jwitcher3"
        target="_blank"
        rel="noopener noreferrer"
        style={{ color: isDark ? "#aaa" : "#444" }}
      >
        GitHub
      </a>{" "}
      ·{" "}
      <a
        href="https://www.linkedin.com/in/james-witcher/"
        target="_blank"
        rel="noopener noreferrer"
        style={{ color: isDark ? "#aaa" : "#444" }}
      >
        LinkedIn
      </a>
    </footer>
  </div>
);
}