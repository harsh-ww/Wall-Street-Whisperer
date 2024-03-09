import "../App.css";
import {
  Box,
  Grid,
  GridItem,
  Heading,
  Highlight,
  SimpleGrid,
} from "@chakra-ui/react";
import BaseLayout from "../layouts/BaseLayout";
import RecentArticleList from "../components/RecentArticleList";
import DataTable from "../components/DataTable";

function HomePage() {

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
                query="Followed"
                styles={{ px: "2", py: "1", rounded: "full", bg: "blue.100" }}
              >
                Your Followed Companies
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
                <DataTable />
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
                  Alerts
                </Heading>
                Notifications go here
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
