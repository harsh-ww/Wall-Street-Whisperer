import { Flex, Input, InputGroup, InputRightElement } from "@chakra-ui/react";
import { SearchIcon } from "@chakra-ui/icons";
import {
  Fade,
  ScaleFade,
  Slide,
  SlideFade,
  Collapse,
  useDisclosure,
  Select,
  Text,
  Button
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
            placeholder="Search for Company..."
            variant="filled"
            focusBorderColor="purple.500"
            onChange={(e) => setQuery(e.target.value)}
          />
          {companyList.length > 0 && (
            <Select placeholder="Select company">
              {companyList.map((company, index) => (
                <option key={index} value={company.ticker}>
                  {company.name} ({company.ticker} - {company.exchange})
                </option>
              ))}
            </Select>
          )}

          <InputRightElement>
            <Fade in={!isFocused}>
              <SearchIcon color="black" />
            </Fade>
          </InputRightElement>
        </InputGroup>
        {isFocused && (
          <Text width="70%" bg="white" textColor="black" padding="5px">
            Hello there
          </Text>
        )}
      </Flex>
    </>
  );
}

export default SearchBar;
