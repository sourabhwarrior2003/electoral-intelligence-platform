import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend
} from "recharts";

const COLORS = [
  "#2563eb",
  "#22c55e",
  "#f59e0b",
  "#ef4444",
  "#8b5cf6",
  "#06b6d4",
  "#ec4899"
];

export default function ReligionChart({ data }) {
  const chartData = Object.entries(data).map(
    ([name, value]) => ({
      name,
      value
    })
  );

  const renderLabel = ({
    name,
    percent
  }) => {
    return `${name} (${(percent * 100).toFixed(1)}%)`;
  };

  return (
    <div className="chart-card">
      <h2>Religious Demographics</h2>

      <ResponsiveContainer
        width="100%"
        height={350}
      >
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={120}
            label={renderLabel}
            labelLine={true}
          >
            {chartData.map((_, index) => (
              <Cell
                key={`cell-${index}`}
                fill={
                  COLORS[
                    index % COLORS.length
                  ]
                }
              />
            ))}
          </Pie>

          <Tooltip
            formatter={(
              value,
              name
            ) => [
              `${value} people`,
              name
            ]}
          />

          <Legend
            verticalAlign="bottom"
            align="center"
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}