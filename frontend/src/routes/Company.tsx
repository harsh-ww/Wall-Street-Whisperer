import "../App.css";
import SideBar from "../components/SideBar";
import ArticleMotif from "../components/ArticleMotif";
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  useToast,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
} from "@chakra-ui/react";

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
  Link,
  Input,
} from "@chakra-ui/react";
import { TriangleUpIcon, TriangleDownIcon } from "@chakra-ui/icons";
import BaseLayout from "../layouts/BaseLayout";
import AreaChart from "../components/AreaChart";
import {
  IoIosAddCircleOutline,
  IoIosRemoveCircleOutline,
} from "react-icons/io";
import { HiExternalLink } from "react-icons/hi";

interface CompanyDetails {
  //explicit type casting for the returned JSON
  //add necessary headers when required
  tracked: boolean;
  Name: string;
  name: string; //for non-US companies
  Symbol: string;
  symbol: string;
  Exchange: string;
  exchange: string;
  stock: {
    //stock information is the same regardless...
    change: string;
    "change percent": string;
    price: string;
  };
}

//tracking added companies

const CompanyDetails = () => {
  const [commonName, setCommonName] = useState(""); //provide database common_name insertion
  const { isOpen, onOpen, onClose } = useDisclosure(); //reactive modal dialog to be used when trying to track company
  const toastTrack = useToast();
  const { exchange, ticker, tracked } = useParams();
  const [companyData, setCompanyData] = useState<CompanyDetails>(); //fill page with relevant data from server once retrieved, initially null

  useEffect(() => {
    //after rendering, fetch company data
    const fetchCompanyData = async () => {
      try {
        const response = await fetch(
          `http://localhost:5000/company/${ticker}` //fetch from API address   (FORMAT IS DIFFERENT for US vs NON-US companies)
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
  }, [exchange, ticker, tracked]); //optional dependencies, the page will refresh if these change, i.e. when different exchange and company identification page is chosen...

  function Company() {
    //function to handle storing tracked company data for that user
    const handleTrackCompany = async () => {
      const data = {
        ticker_code: companyData
          ? companyData.Symbol || companyData.symbol || "undefined" //provide data to POST request
          : "undefined",
        common_name: commonName, //to be retrieved from a user-input
      };

      try {
        const response = await fetch(
          "http://localhost:5000/track", //calls track.py function
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
          }
        );
        if (!response.ok) {
          throw new Error("Failed to track company");
        }
        const responseData = await response.json();
        console.log(responseData);
        toastTrack({
          //usage of reactive toasts that confirm after database update whether the addition was successful
          title: "Added",
          description: "This company is now being tracked!",
          status: "success",
          duration: 3500,
          variant: "subtle",
          isClosable: true,
        });
      } catch (error) {
        toastTrack({
          //in the case that the user manages to track again, relay an error
          title: "An error has occured",
          description: "",
          status: "error",
          duration: 3500,
          variant: "subtle",
          isClosable: true,
        });
        console.error("Error, tracking try catch failed");
      }
    };

    const handleUntrackCompany = async () => {
      //insert untrack company details here
    };

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
                      {companyData
                        ? companyData.Name || companyData.name
                        : "..."}
                      {/*non-US companies json has lowercase name*/}
                    </Heading>
                    <Text fontStyle="italic">
                      {companyData
                        ? companyData.Exchange || companyData.exchange
                        : "..."}
                    </Text>
                    <Text
                      fontSize="xx-small"
                      color={
                        //colour of stock price data is dependent on whether it has recently gone down or up
                        companyData?.stock?.change &&
                        !companyData.stock.change.includes("-") //check if change is negative/positive, more straightforward than parsing as a float
                          ? "green.500"
                          : "red.500"
                      }
                    >
                      {" "}
                      {/*feel free to style as you want */}
                      {companyData ? companyData.stock.price : "..."}{" "}
                      {companyData?.stock?.change &&
                      !companyData.stock.change.includes("-") ? (
                        <TriangleUpIcon />
                      ) : (
                        <TriangleDownIcon />
                      )}
                      {companyData
                        ? companyData.stock["change percent"]
                        : "..."}
                    </Text>
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
                      colorScheme={
                        companyData && companyData.tracked ? "orange" : "purple"
                      } //change styling depending on whether company is tracked or not
                      size="lg"
                      w={["auto", "282px", "282px"]}
                      // mt="6"
                      rightIcon={
                        companyData && companyData.tracked ? (
                          <IoIosRemoveCircleOutline size={28} />
                        ) : (
                          <IoIosAddCircleOutline size={28} />
                        )
                      }
                      onClick={() => {
                        if (companyData && companyData.tracked) {
                          handleUntrackCompany();
                        } else {
                          onOpen();
                        }
                      }}
                    >
                      {companyData && companyData.tracked
                        ? "Untrack"
                        : "Track Company"}
                    </Button>
                  </Box>
                  {/* modal dialog popup to assign a new name to the tracked company */}
                  <Modal isOpen={isOpen} onClose={onClose}>
                    {" "}
                    <ModalOverlay />
                    <ModalContent paddingTop="10px">
                      <ModalBody>
                        <ModalCloseButton />
                      </ModalBody>
                      <ModalFooter>
                        {/*input acts as common name for the the database insertion */}
                        <Input
                          placeholder="Assign a name for this company"
                          w="80%"
                          mr={4}
                          value={commonName}
                          onChange={(e) => setCommonName(e.target.value)}
                          onKeyDown={(e) => {
                            if (e.key === "Enter") {
                              handleTrackCompany();
                              onClose();
                            }
                          }}
                        />
                        <Button
                          variant="ghost"
                          backgroundColor="purple.700"
                          color="white"
                          w="20%"
                          onClick={() => {
                            //function adds to database tracked company for the user
                            handleTrackCompany();
                            onClose();
                          }}
                        >
                          Confirm
                        </Button>
                      </ModalFooter>
                    </ModalContent>
                  </Modal>
                  <Box
                    display="flex"
                    justifyContent="center"
                    alignItems="center"
                    ml={["10px", "10px", "250px"]}
                  >
                    <ButtonGroup gap="4">
                      <Link
                        href={`https://www.google.com/search?q=${
                          companyData
                            ? companyData.Name || companyData.name
                            : "#"
                        }`} //straightforwardly returns the google search results page for the companies' name
                      >
                        <Button
                          colorScheme="purple"
                          variant="outline"
                          rightIcon={<HiExternalLink />}
                        >
                          Website
                        </Button>
                      </Link>
                      <Link
                        href={`https://www.nasdaq.com/market-activity/stocks/${
                          companyData
                            ? companyData.Symbol || companyData.symbol
                            : "#"
                        }`}
                        isExternal
                      >
                        <Button
                          colorScheme="purple"
                          variant="outline"
                          rightIcon={<HiExternalLink />}
                        >
                          Stock Exchange ref
                        </Button>
                      </Link>
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
                    {articles.map((article, index) => (
                      <ArticleMotif key={index} articleName={article} />
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
