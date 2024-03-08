import "../App.css";
import {
  Box,
  Grid,
  GridItem,
  Heading,
  Highlight,
  SimpleGrid,
  Badge,
  IconButton,
} from "@chakra-ui/react";
import BaseLayout from "../layouts/BaseLayout";
import { createColumnHelper } from "@tanstack/react-table";
import { mockGridData, UnitConversion } from "../components/mockData";
import { DataGrid } from "../components/DataGrid";
import { CloseIcon } from "@chakra-ui/icons";
import RecentArticleList from "../components/RecentArticleList";
import Notifications from "../components/Notifications";

function HomePage() {
  function handleDelete(id: number) {
    console.log("delete", id);
  }

  const columnHelper = createColumnHelper<UnitConversion>();

  const columns = [
    columnHelper.accessor("Symbol", {
      cell: (info) => (
        <Badge fontSize="0.9em" bg="cyan.100">
          {info.getValue()}
        </Badge>
      ),
      header: "Symbol",
    }),
    columnHelper.accessor("Company", {
      cell: (info) => info.getValue(),
      header: "Company",
    }),
    columnHelper.accessor("LastPrice", {
      cell: (info) => info.getValue(),
      header: "Last Price",
    }),
    columnHelper.accessor("Change", {
      cell: (info) => info.getValue(),
      header: "Change",
    }),
    columnHelper.accessor("PercentChg", {
      cell: (info) => (
        <Badge
          fontSize="0.9em"
          bg={info.getValue() >= 0 ? "green.200" : "red.200"}
        >
          {info.getValue()}
        </Badge>
      ),
      header: "Change%",
      meta: {
        isNumeric: true,
      },
    }),
    columnHelper.accessor("ID", {
      cell: (info) => (
        <IconButton
          onClick={() => handleDelete(info.getValue())}
          aria-label="Delete Company"
          icon={<CloseIcon />}
        />
      ),
      header: "",
      meta: {
        isNumeric: true,
      },
    }),
  ];

  let articles = [
    "Headliner",
    "ArticleTitle",
    "NotAdmissible",
    "MoneyLaundering",
    "DidaGoodThing",
    "Headliner",
    "ArticleTitle",
    "NotAdmissible",
  ]; //dummy data

  return (
    <>
      <Box>
        <BaseLayout />
        {/* <SideBar /> */}
        <Box mx="1" as="section">
          <Box
            h="fit-content"
            bg="whiteAlpha.900"
            maxW="70vw"
            margin="auto"
            mt="-20"
            mb="10px"
            borderRadius="md"
            overflow="auto"
            p="10px"

            // textAlign="center"
          >
            <Heading lineHeight="tall">
              <Highlight
                query="Tracked"
                styles={{ px: "2", py: "1", rounded: "full", bg: "blue.100" }}
              >
                Your Tracked Companies
              </Highlight>
            </Heading>
          </Box>
          <Box
            // h="fit-content"
            h="105vh"
            // bg="gray.400"
            maxW="75vw"
            margin="auto"
            // mt="-20"
            mb="50"
            borderRadius="md"
            overflow="auto"
            // textAlign="center"
          >
            <Grid
              h="75vh"
              w="75vw"
              templateRows="repeat(2, 1fr)"
              templateColumns="repeat(7, 1fr)"
              gap={4}
              margin="auto"
              width="100%"
            >
              <GridItem colSpan={5} bg="whiteAlpha.900" borderRadius="md">
                {" "}
                <DataGrid columns={columns} data={mockGridData} />
              </GridItem>
              <GridItem
            colSpan={2}
            rowSpan={2}
            bg="whiteAlpha.900"
            borderRadius="md"
            p="10px"
        >
            {" "}
            <Heading as="h4" size={["md", "lg", "lg"]} pb="10px">
                Notifications
            </Heading>
            <Notifications />
            </GridItem>
              <GridItem
                colSpan={5}
                bg="whiteAlpha.900"
                borderRadius="md"
                p="10px"
              >
                {" "}
                <Heading as="h4" size={["md", "lg", "lg"]} pb="10px">
                  In the news
                </Heading>
                <SimpleGrid columns={1} spacing={2}>
                  <RecentArticleList />
                </SimpleGrid>
              </GridItem>
            </Grid>
          </Box>
        </Box>
      </Box>
    </>
  );
}

export default HomePage;
