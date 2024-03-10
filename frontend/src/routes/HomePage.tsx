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
import Notifications from "../components/Notifications";
import SuggestionsGenerator from "../components/Suggestions";
import { useEffect, useState } from "react";
import { API_URL } from "../config";

function HomePage() {
  const [suggestions, setSuggestions] = useState([]); // State variable for suggestions

  useEffect(() => {
    // Fetch suggestions data
    const fetchSuggestions = async () => {
      try {
        const response = await fetch(`${API_URL}/suggestions`);
        if (!response.ok) {
          throw new Error('Failed to fetch suggestions');
        }
        const data = await response.json();
        setSuggestions(data);
      } catch (error) {
        console.error('Error fetching suggestions:');
      }
    };

    fetchSuggestions();
  }, []);

  return (
    <>
      <Box>
        <BaseLayout />
        {/* <SideBar /> */}
        <Box mx="1" as="section" h="fit-content">
          <Box
            h="fit-content"
            bg="whiteAlpha.900"
            maxW="80vw"
            margin="auto"
            mt="-12vh"
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
            h="200vh"
            // bg="gray.400"
            maxW="80vw"
            margin="auto"
            // mt="-20"
            mb="50"
            borderRadius="md"
            overflow="visible"
            // textAlign="center"
          >
            <Grid
              h="75vh"
              w="80vw"
              templateRows="repeat(2, 1fr)"
              // templateColumns="repeat(7, 1fr)"
              templateColumns={{
                base: "repeat(2, 1fr)",
                md: "repeat(2, 1fr)",
                lg: "repeat(7, 1fr)",
              }}
              gap={{ base: 2, md: 4, lg: 4 }}
              margin="auto"
              width="100%"
            >
              <GridItem
                colSpan={5}
                rowSpan={1}
                bg="whiteAlpha.900"
                borderRadius="md"
              >
                {" "}
                <DataTable />
              </GridItem>
              <GridItem
                colSpan={2}
                rowSpan={2}
                bg="whiteAlpha.900"
                borderRadius="md"
                p="10px"
                h="fit-content"
              >
                {" "}
                <Heading as="h4" size={["md", "lg", "lg"]} pb="10px">
                  Notifications
                </Heading>
                <Notifications />
              </GridItem>

              {/* Third item in grid: Suggested companies */}
              <GridItem
                colSpan={5}
                rowSpan={1}
                bg="whiteAlpha.900"
                borderRadius="md"
                p="10px"
              >
                {" "}
                <Heading as="h4" size={["md", "lg", "lg"]} pb="10px">
                  Suggestions
                </Heading>
                <SimpleGrid columns={{ base: 1, md: 3 }} spacing={5}> {/*column amount is reactive to viewport, set to 1 for smaller screens and UI*/}
                  {suggestions.map((company) => (
                    <SuggestionsGenerator key={company['ticker']} companyName={company['name']} ticker={company['ticker']} />
                  ))}
                </SimpleGrid>
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
