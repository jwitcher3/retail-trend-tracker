// Retail Trend Tracker Dashboard (React + Plotly)

import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import Papa from "papaparse";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function RetailTrendDashboard() {
  const [data, setData] = useState([]);
  const [trendType, setTrendType] = useState("Sneakers");
  const [region, setRegion] = useState("US");

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

  const filteredData = data.filter(
    (d) => d.segment === trendType && d.region === region
  );

  const trends = Array.from(
    new Set(
      filteredData.flatMap((row) =>
        Object.keys(row).filter(
          (key) => !["date", "isPartial", "country", "segment", "region"].includes(key)
        )
      )
    )
  );

  const series = trends.map((trend) => {
    const x = filteredData.map((row) => row.date);
    const y = filteredData.map((row) => parseInt(row[trend]) || 0);
    return { x, y, type: "scatter", mode: "lines", name: trend };
  });

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Retail Trend Tracker</h1>
      <div className="flex gap-4">
        <Button onClick={() => setTrendType("Sneakers")}>Sneakers</Button>
        <Button onClick={() => setTrendType("Fashion")}>Fashion</Button>
        <Button onClick={() => setRegion("US")}>US</Button>
        <Button onClick={() => setRegion("CA")}>Canada</Button>
      </div>
      <Card>
        <CardContent>
          <Plot
            data={series}
            layout={{
              title: `${region} ${trendType} Trends`,
              xaxis: { title: "Date" },
              yaxis: { title: "Google Trends Interest" },
              autosize: true,
            }}
            useResizeHandler
            style={{ width: "100%", height: "500px" }}
          />
        </CardContent>
      </Card>
    </div>
  );
}
