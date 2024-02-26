import "../App.css";
import SideBar from "../components/SideBar";
import ArticleMotif from "../components/ArticleMotif";

import {
  Box,
  Button,
  Flex,
  Heading,
  Text,
  Grid,
  GridItem,
  Badge,
  ButtonGroup,
  SimpleGrid,
} from "@chakra-ui/react";
import BaseLayout from "../layouts/BaseLayout";
import LineChart from "../components/LineChart";
import { IoIosAddCircleOutline } from "react-icons/io";
import { HiExternalLink } from "react-icons/hi";

function Company() {
  let articles = [
    "Headliner",
    "ArticleTitle",
    "NotAdmissible",
    "MoneyLaundering",
    "DidaGoodThing",
  ]; //dummy data
  return (
    <>
      <Box>
        <BaseLayout />
        <SideBar />
        <Box mx="1" as="section">
          <Box
            maxW="8xl"
            height="fit-content"
            margin="auto"
            mt="-20"
            mb="50"
            // pb="20"
            borderRadius="xl"
            overflow="auto"
            boxShadow="0px 20px 25px -5px rgba(0, 0, 0, 0.1), 0px 10px 10px -5px rgba(0, 0, 0, 0.04)"
            textAlign="center"
          >
            <Box bg="gray.50" p={["10px", "10px", "10px"]}>
              {" "}
              <Flex direction={["column", "column", "row"]}>
                <Box bg="gray.50" p={["10px", "10px", "15px"]}>
                  <Heading as="h3" fontSize={["2xl", "3xl", "5xl"]} mt="1">
                    CompanyName
                  </Heading>
                </Box>
                <Box p={["10px", "10px", "15px"]} fontSize="lg" bg="gray.50">
                  <Badge
                    colorScheme="green"
                    borderRadius="full"
                    fontSize="1.5em"
                    p="10px"
                  >
                    8.5
                  </Badge>
                </Box>
                <Box
                  bg="gray.50"
                  p={["10px", "10px", "15px"]}
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
                >
                  <Button
                    colorScheme="purple"
                    size="lg"
                    w={["auto", "282px", "282px"]}
                    // mt="6"
                    rightIcon={<IoIosAddCircleOutline size={28} />}
                  >
                    Track Company
                  </Button>
                </Box>
                <Box
                  display="flex"
                  justifyContent="center"
                  alignItems="center"
                  ml={["10px", "10px", "250px"]}
                >
                  <ButtonGroup gap="4">
                    <Button
                      colorScheme="purple"
                      variant="outline"
                      rightIcon={<HiExternalLink />}
                    >
                      Website
                    </Button>
                    <Button
                      colorScheme="purple"
                      variant="outline"
                      rightIcon={<HiExternalLink />}
                    >
                      Stock Exchange ref
                    </Button>
                  </ButtonGroup>
                </Box>
              </Flex>
            </Box>

            <Grid templateColumns="repeat(2, 1fr)" gap={1}>
              <GridItem
                w="100%"
                height="100%"
                bg="gray.50"
                p={["15px", "15px", "30px"]}
              >
                {" "}
                <Text fontSize="xl" fontWeight="bold">
                  Stock trend analysis time-series graph
                </Text>
                <Box height="60vh" mt="-20px">
                  <LineChart />
                </Box>
              </GridItem>
              <GridItem
                w="100%"
                height="100%"
                bg="gray.50"
                p={["15px", "15px", "30px"]}
              >
                <Text textAlign="left">Articles will go here</Text>
                <SimpleGrid columns={2} spacing={2}>
                  {articles.map((article) => (
                    <ArticleMotif articleName={article} />
                  ))}
                </SimpleGrid>
              </GridItem>
            </Grid>
          </Box>
        </Box>
      </Box>
    </>
  );
}

export default Company;
