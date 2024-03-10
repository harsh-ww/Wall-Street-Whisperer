import {
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Text,
} from "@chakra-ui/react";
import { AreaChartItem } from "./AreaChartItem";

// variable for ticker symbol - will pass in as a prop later
// const ticker: string = "IBM";

const AreaChart = ({ ticker }: { ticker: string }) => {
  return (
    <>
      <Text fontSize="lg">Stock price over time</Text>
      <Tabs variant="soft-rounded">
        <TabList>
          <Tab>Daily</Tab>
          <Tab>Weekly</Tab>
          <Tab>Monthly</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <AreaChartItem ticker={ticker} granularity="DAILY" />
          </TabPanel>
          <TabPanel>
            <AreaChartItem ticker={ticker} granularity="WEEKLY" />
          </TabPanel>
          <TabPanel>
            <AreaChartItem ticker={ticker} granularity="MONTHLY" />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </>
  );
};
export default AreaChart;
