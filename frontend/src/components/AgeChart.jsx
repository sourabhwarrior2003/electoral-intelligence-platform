import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function AgeChart({
  data
}) {

  const chartData =
    Object.entries(data).map(
      ([name, value]) => ({
        name,
        value
      })
    );

  return (

    <div className="chart-card">

      <h2>
        Age Distribution
      </h2>

      <ResponsiveContainer
        width="100%"
        height={350}
      >

        <BarChart
          data={chartData}
        >

          <XAxis dataKey="name" />

          <YAxis />

          <Tooltip />

          <Bar
            dataKey="value"
          />

        </BarChart>

      </ResponsiveContainer>

    </div>

  );
}