import { Flex, Input, InputGroup, InputRightElement } from "@chakra-ui/react";
import { SearchIcon } from "@chakra-ui/icons";
import { Fade, Text, Image } from "@chakra-ui/react";
import { useState } from "react";
import React from "react";

interface Company {
  name: string;
}

function SearchBar() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<Company[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(
        `http://localhost:5000/company?query=${searchQuery}` //make call to server using api route search_companies()
      );
      if (!response.ok) {
        //appropriate error handling
        console.error(`HTTP error! status: ${response.status}`);
        throw new Error("Failed to fetch company data");
      }
      const data = await response.json();
      setSearchResults(data); //useState hook takes API json response and puts into searchResults
      console.log(searchResults);
    } catch (error) {
      console.error("Error fetching company data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const [isFocused, setIsFocused] = useState(false); //used specifically for styling frontend
  const handleToggle = () => {
    setIsFocused(!isFocused);
  };

  /*import {
    Fade,
    ScaleFade,
    Slide,
    SlideFade,
    Collapse,
    useDisclosure,
    Select,
    Text,
    Button,
  } from "@chakra-ui/react";
  import { useState, useEffect } from "react";

  //search bar functionality, length dependent on container it is in
  //dropdown menu needs to be added
  interface Company {
    name: string;
    ticker: string;
    exchange: string;
    tracked: boolean;
  }

  function SearchBar() {
  const { isOpen, onToggle } = useDisclosure();
  const [query, setQuery] = useState("");
  const [companyList, setCompanyList] = useState<Company[]>([]);

  useEffect(() => {
    console.log(query);
    console.log(companyList);
    if (query !== "") {
      async function fetchCompanies() {
        const response = await fetch(`/company?query=${query}`);
        if (!response.ok) {
          console.error(`HTTP error! status: ${response.status}`);
          return;
        }
        const data = await response.json();
        setCompanyList(data);
      }
      fetchCompanies();
    } else {
      setCompanyList([]);
    }
  }, [query]);
*/

  return (
    <>
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
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSearch();
              }
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
        {isLoading || ( //logic is incomplete, change && to ?? (), with default loading elements within brackets
          <Flex direction="column" zIndex="99">
            {searchResults.map(
              (
                company,
                index //response from json will stack and fill the possible search results
              ) => (
                <React.Fragment key={index}>
                  <Flex
                    as="button"
                    borderLeft="2px"
                    borderRight="2px"
                    borderBottom="1px"
                    borderColor="gray.300"
                    borderBottomColor="gray.100"
                    width="70%"
                    bg="white"
                    padding="5px"
                    justifyContent="flex-start"
                    direction="row"
                  >
                    <Image
                      src="../../public/logoIpsum.svg"
                      height="1em"
                      alignSelf="center"
                      margin="0.3em 0.5em 0.3em 0.5em"
                    />
                    <Text textColor="black" fontSize="lg" alignSelf="center">
                      {company.name}{" "}
                      {/*will additionally link to relevant page when implementation confirmed */}
                    </Text>
                  </Flex>
                </React.Fragment>
              )
            )}
          </Flex>
        )}
      </Flex>
    </>
  );
}

export default SearchBar;
