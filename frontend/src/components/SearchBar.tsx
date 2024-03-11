import {
  Flex,
  Input,
  InputGroup,
  InputRightElement,
  Card,
  CardBody,
  Stack,
  StackDivider,
  Heading,
  Badge,
  Spacer,
  Fade,
  Text,
} from "@chakra-ui/react";
import { SearchIcon } from "@chakra-ui/icons";
import { useEffect, useState } from "react";
import React from "react";
import { NavLink } from "react-router-dom";
import { API_URL } from "../config";

interface Company {
  exchange: string; //region
  name: string;
  symbol?: string;
  ticker?: string;
  tracked: boolean;
  link: string;
}

function SearchBar() {
  // states for search query, search results, and loading status
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<Company[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // triggers search when search query changes
  useEffect(() => {
    if (searchQuery.length > 1) {
      handleSearch();
    } else {
      setSearchResults([]);
    }
  }, [searchQuery]);

  const handleNavigate = () => {
    setSearchQuery("");
  };

  const handleSearch = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`${API_URL}/company?query=${searchQuery}`);
      if (!response.ok) {
        //appropriate error handling
        console.error(`HTTP error! status: ${response.status}`);
        throw new Error("Failed to fetch company data");
      }
      const data = await response.json();
      setSearchResults(data); // stores API json response in searchResults
    } catch (error) {
      console.error("Error fetching company data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // State to manage focus state for styling
  const [isFocused, setIsFocused] = useState(false);
  const handleToggle = () => {
    setIsFocused(!isFocused);
  };

  // State to track hovered company
  const [hoveredCompany, setHoveredCompany] = useState<number | null>(null);
  // handles mouse enter event
  const handleMouseEnter = (index: number) => {
    setHoveredCompany(index);
  };
  // handles mouse leave event
  const handleMouseLeave = () => {
    setHoveredCompany(null);
  };

  return (
    <>
      {/* Flex container for search bar and search results */}
      <Flex
        color="white"
        w="100vw"
        justifyContent="center"
        direction="column"
        marginLeft="14vw"
      >
        <InputGroup w="70%">
          <Input
            size="md"
            boxShadow="md"
            color="black"
            onFocus={handleToggle}
            onBlur={handleToggle}
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
            }}
            placeholder="Search for Company..."
            variant="filled"
            focusBorderColor="purple.500"
          />
          <InputRightElement>
            <Fade in={!isFocused}>
              <SearchIcon color="black" />
            </Fade>
          </InputRightElement>
        </InputGroup>
        {/* Conditional rendering of search results */}
        {isLoading || searchResults.length === 0 ? null : (
          //logic is incomplete, change && to ?? (), with default loading elements within brackets
          <Flex direction="column" zIndex="99">
            <Card
              borderColor="gray.300"
              borderBottomColor="gray.100"
              maxWidth="70%"
              // padding="5px"
            >
              <CardBody width="100%">
                <Stack divider={<StackDivider />} spacing="2" width="100%">
                  {searchResults.map(
                    (
                      company,
                      index //response from json will stack and fill the possible search results
                    ) => (
                      <React.Fragment key={index}>
                        {/* <NavLink to={`/company/${company.symbol}`}> */}{" "}
                        {/*commented out until company page logic is complete*/}
                        <NavLink
                          to={`/company/${company.symbol || company.ticker}`}
                        >
                          <Flex
                            color={company.tracked ? "pink.500" : "black"}
                            p="5px"
                            width="100%"
                            alignItems="center"
                            as="button"
                            bg={
                              hoveredCompany === index
                                ? "gray.200"
                                : "transparent"
                            } // change bg color based on hoveredCompany
                            onMouseEnter={() => handleMouseEnter(index)}
                            onMouseLeave={handleMouseLeave}
                            onClick={handleNavigate}
                          >
                            <Badge
                              fontSize="0.8em"
                              mr="3"
                              // variant="subtle"
                              colorScheme={company.tracked ? "pink" : "gray"}
                              borderRadius="5px"
                            >
                              {company.symbol || company.ticker}
                            </Badge>
                            <Heading size="xs" textTransform="uppercase">
                              {company.name}{" "}
                            </Heading>
                            <Spacer />
                            {company.tracked && (
                              <Badge
                                fontSize="0.8em"
                                mr="3"
                                variant="outline"
                                colorScheme="pink"
                                borderRadius="5px"
                              >
                                Following
                              </Badge>
                            )}
                            <Text fontSize="sm">{company.exchange}</Text>
                          </Flex>
                        </NavLink>
                      </React.Fragment>
                    )
                  )}
                </Stack>
              </CardBody>
            </Card>
          </Flex>
        )}
      </Flex>
    </>
  );
}

export default SearchBar;
