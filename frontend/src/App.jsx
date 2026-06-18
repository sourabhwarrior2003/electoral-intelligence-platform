import React, { useState } from "react";
import axios from "axios";
import "./App.css";

import ReligionChart from "./components/ReligionChart";
import AgeChart from "./components/AgeChart";
import GenderChart from "./components/GenderChart";

export default function App() {
  const [files, setFiles] = useState([]);
  const [constituency, setConstituency] = useState("");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);

  const handleUpload = async () => {
    if (!constituency || files.length === 0) {
      alert("Please select PDF files");
      return;
    }

    const formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file);
    });

    formData.append("constituency", constituency);

    let seconds = 0;

    const timer = setInterval(() => {
      seconds++;
      setElapsedTime(seconds);
    }, 1000);

    try {
      setLoading(true);
      setElapsedTime(0);
      setReport(null);

      const response = await axios.post(
        "http://localhost:5000/api/process",
        formData
      );

      setReport(response.data);
    } catch (err) {
      console.error(err);
      alert("Backend processing failed");
    } finally {
      clearInterval(timer);
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <section className="hero">
        <div className="hero-content">

          <div className="badge">
            🇮🇳 Electoral Intelligence Platform
          </div>

          <h1 className="hero-title">
            AI Powered
            <br />
            <span className="hero-highlight">
              Demographic Analysis
            </span>
          </h1>

          <p className="hero-subtitle">
            Upload Hindi Electoral Rolls • Extract Voter Data • Generate Insights
          </p>

          <div className="upload-card">

            <div className="input-group">
              <label>Constituency Name</label>

              <input
                type="text"
                value={constituency}
                onChange={(e) => setConstituency(e.target.value)}
                placeholder="Example: Dewas"
              />
            </div>

            <div className="input-group">

              <label>Upload Electoral PDFs</label>

              <div className="file-box">

                <input
                  type="file"
                  multiple
                  accept=".pdf"
                  onChange={(e) =>
                    setFiles(
                      Array.from(e.target.files)
                    )
                  }
                />

                <p>
                  {files.length > 0
                    ? `${files.length} PDF(s) Selected`
                    : "Choose one or more PDF files"}
                </p>

              </div>

            </div>

            <button
              className="upload-btn"
              onClick={handleUpload}
              disabled={loading}
            >
              {loading
                ? `Processing... ${elapsedTime}s`
                : "Upload & Analyze"}
            </button>

            {loading && (
              <div className="processing-card">

                <h3 className="processing-title">
                  ⚙ Processing Electoral Roll
                </h3>

                <p className="processing-time">
                  Elapsed Time: {elapsedTime}s
                </p>

                <p className="processing-status">

                  {elapsedTime < 10 &&
                    "📄 Uploading PDF..."}

                  {elapsedTime >= 10 &&
                    elapsedTime < 25 &&
                    "🔍 OCR Extraction Running..."}

                  {elapsedTime >= 25 &&
                    elapsedTime < 40 &&
                    "👥 Extracting Voter Records..."}

                  {elapsedTime >= 40 &&
                    "📊 Generating Analytics..."}

                </p>

              </div>
            )}

          </div>

          {report && (
            <>
              <div className="stats">

                <div className="stat-card">
                  <div className="stat-number">
                    {report.total_voters}
                  </div>
                  <div className="stat-label">
                    Total Voters
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-number">
                    {report.booths}
                  </div>
                  <div className="stat-label">
                    Booth PDFs
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-number">
                    {
                      Object.keys(
                        report.religion_distribution || {}
                      ).length
                    }
                  </div>
                  <div className="stat-label">
                    Religions
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-number">
                    ✓
                  </div>
                  <div className="stat-label">
                    Report Ready
                  </div>
                </div>

              </div>

              <div className="charts-grid">

                <ReligionChart
                  data={
                    report.religion_distribution || {}
                  }
                />

                <AgeChart
                  data={
                    report.age_distribution || {}
                  }
                />

                <GenderChart
                  data={
                    report.gender_distribution || {}
                  }
                />

              </div>
            </>
          )}

        </div>
      </section>
    </div>
  );
}