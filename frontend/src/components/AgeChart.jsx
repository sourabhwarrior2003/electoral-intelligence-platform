import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  LabelList,
  CartesianGrid
} from "recharts";

const COLORS = [
  "#2563eb",
  "#22c55e",
  "#f59e0b",
  "#ef4444",
  "#8b5cf6",
  "#06b6d4"
];

export default function AgeChart({ data }) {

  const total = Object.values(data).reduce(
    (sum, value) => sum + value,
    0
  );

  const chartData = Object.entries(data)
    .map(([name, value]) => ({
      name,
      count: value,
      percentage: Number(
        ((value / total) * 100).toFixed(1)
      )
    }))
    .sort(
      (a, b) =>
        b.percentage - a.percentage
    );

  return (
    <div className="chart-card">

      <h2>
        Age Distribution (%)
      </h2>

      <ResponsiveContainer
        width="100%"
        height={350}
      >

        <BarChart
          data={chartData}
          layout="vertical"
          margin={{
            top: 10,
            right: 40,
            left: 20,
            bottom: 10
          }}
        >

          <CartesianGrid
            strokeDasharray="3 3"
            opacity={0.2}
          />

          <XAxis
            type="number"
            unit="%"
            domain={[0, 100]}
          />

          <YAxis
            dataKey="name"
            type="category"
            width={80}
          />

          <Tooltip
            formatter={(value, name, props) => [
              `${value}%`,
              `${props.payload.count} voters`
            ]}
          />

          <Bar
            dataKey="percentage"
            radius={[0, 8, 8, 0]}
          >

            <LabelList
              dataKey="percentage"
              position="right"
              formatter={(value) =>
                `${value}%`
              }
            />

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

          </Bar>

        </BarChart>

      </ResponsiveContainer>

    </div>
  );
}