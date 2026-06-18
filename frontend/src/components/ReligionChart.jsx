import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const COLORS = [
  "#2563eb",
  "#22c55e",
  "#f59e0b",
  "#ef4444"
];

export default function ReligionChart({
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
        Religion Distribution
      </h2>

      <ResponsiveContainer
        width="100%"
        height={350}
      >

        <PieChart>

          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            outerRadius={120}
            label
          >

            {chartData.map(
              (_, index) => (
                <Cell
                  key={index}
                  fill={
                    COLORS[
                      index %
                      COLORS.length
                    ]
                  }
                />
              )
            )}

          </Pie>

          <Tooltip />

        </PieChart>

      </ResponsiveContainer>

    </div>

  );
}