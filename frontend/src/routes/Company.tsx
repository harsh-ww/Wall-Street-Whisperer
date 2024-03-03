import "../App.css";
import SideBar from "../components/SideBar";
import ArticleMotif from "../components/ArticleMotif";
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

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
import AreaChart from "../components/AreaChart";
import { IoIosAddCircleOutline } from "react-icons/io";
import { HiExternalLink } from "react-icons/hi";

const CompanyDetails = () => {
  const { exchange, ticker } = useParams();
  const [companyData, setCompanyData] = useState(null); //fill page with relevant data from server once retrieved, initially null

  useEffect(() => {
    //after rendering, fetch company data
    const fetchCompanyData = async () => {
      try {
        const response = await fetch(
          `http://server:5000/company/${ticker}` //fetch from API address
        );
        if (!response.ok) {
          throw new Error("Failed to fetch company data");
        }
        const data = await response.json(); //pass this data into the company page html...
        console.log(data);
        setCompanyData(data);
      } catch (error) {
        console.error("error has occured");
      }
    };
    fetchCompanyData();
  }, [exchange, ticker]); //optional dependencies, the page will refresh if these change, i.e. when different exchange and company identification page is chosen...

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
                      CompanyName:{" "}
                      {/*currently do not know the stae of the json formatting*/}
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
                  <Box height="60vh" mt="-20px">
                    {/* once logic done pass in ticker to AreaChart as prop */}
                    <AreaChart />
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
  return Company();
};

export default CompanyDetails;
