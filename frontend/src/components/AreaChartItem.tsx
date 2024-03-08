import {
  AreaChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Area,
  ResponsiveContainer,
} from "recharts";
import { useState, useEffect } from "react";
import { format, parseISO, subDays } from "date-fns";
import { Box, Text } from "@chakra-ui/react";
import { API_URL } from '../config'

interface AreaChartItemProps {
  ticker: string;
  granularity: string;
}

interface TooltipProps {
  active?: boolean;
  payload?: any[];
  label?: string;
}

export const AreaChartItem: React.FC<AreaChartItemProps> = ({
  ticker,
  granularity,
}) => {
  const [data, setData] = useState([]);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch(
        `${API_URL}/company/${ticker}/timeseries?granularity=${granularity}`
      );
      if (!response.ok) {
        console.error(`HTTP error! status: ${response.status}`);
        throw new Error("Failed to fetch data");
      }
      const stockData = await response.json();
      // stockData only contains 30 most recent data points
      setData(stockData);
      console.log(data);
      setIsLoaded(true); // Update isLoaded state after data fetching
    } catch (error) {
      console.error("Error fetching stock data:", error);
    }
  };

  // Calculate the interval to display only 5 evenly spaced ticks
  const interval = Math.ceil(data.length / 5);

  return (
    <div>
      {isLoaded ? (
        <ResponsiveContainer width="100%" height={400}>
          <AreaChart
            data={data}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id="lineColour" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#2451B7" stopOpacity={0.6} />
                <stop offset="95%" stopColor="#2451B7" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis
              dataKey="date"
              tickLine={false}
              tickFormatter={(str) => {
                const date = parseISO(str);
                if (granularity === "MONTHLY") {
                  return format(date, "MMM yy");
                } else {
                  return format(date, "dd MMM");
                }
              }}
              interval={interval}
            />
            <YAxis
              dataKey="4. close"
              tickLine={false}
              axisLine={false}
              tickCount={8}
              domain={["auto", "auto"]}
            />
            <CartesianGrid opacity={0.3} vertical={false} />
            <Tooltip content={<CustomTooltip />} />

            <Area
              dataKey="4. close"
              stroke="#2451B7"
              fillOpacity={1}
              fill="url(#lineColour)"
            />
          </AreaChart>
        </ResponsiveContainer>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

const CustomTooltip: React.FC<TooltipProps> = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    const price = payload[0].value;
    const volume = payload[0].payload["5. volume"]; // Accessing the volume value
    return (
      <Box
        p="5px"
        borderRadius="5px"
        bg="rgba(255, 255, 255, 0.5)"
        fontSize="sm"
      >
        <Text as="b">{format(parseISO(label || ""), "dd MMM yyyy")}</Text>
        <Text>{`Price: ${price}`}</Text>
        <Text>{`Volume: ${volume}`}</Text>{" "}
        {/* Include volume value in tooltip */}
      </Box>
    );
  }

  return null;
};
