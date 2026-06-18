import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const COLORS = [
  "#ec4899",
  "#2563eb"
];

export default function GenderChart({
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
        Gender Distribution
      </h2>

      <ResponsiveContainer
        width="100%"
        height={350}
      >

        <PieChart>

          <Pie
            data={chartData}
            dataKey="value"
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