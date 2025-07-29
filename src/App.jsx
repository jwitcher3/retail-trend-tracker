// src/App.jsx
import RetailTrendDashboard from "./retailtrenddashboard";
import { Analytics } from "@vercel/analytics/react";

function App() {
  return (
    <>
      <RetailTrendDashboard />
      <Analytics />
    </>
  );
}

export default App;
