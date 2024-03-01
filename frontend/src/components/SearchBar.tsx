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
        throw new Error("Failed to fetch company data");
      }
      const data = await response.json();
      setSearchResults(data); //useState hook takes API json response and puts into searchResults
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
        {isLoading && ( //logic is incomplete, change && to ?? (), with default loading elements within brackets
          <Flex
            as="button"
            borderLeft="2px"
            borderRight="2px"
            borderColor="gray.300"
            width="70%"
            bg="white"
            padding="5px"
            justifyContent="flex-start"
            direction="row"
          >
            {searchResults.map(
              (
                company,
                index //response from json will stack and fill the possible search results
              ) => (
                <React.Fragment key={index}>
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
