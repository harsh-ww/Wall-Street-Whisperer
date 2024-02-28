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
    if (query !== "") {
      async function fetchCompanies() {
        const response = await fetch(`/company?query=${query}`);
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
      <Flex color="white" w="100vw" justifyContent="center">
        <InputGroup w="70%">
          <Input
            size="md"
            boxShadow="md"
            color="black"
            onClick={onToggle}
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
            <Fade in={!isOpen}>
              <SearchIcon color="black" />
            </Fade>
          </InputRightElement>
        </InputGroup>
      </Flex>
    </>
  );
}

export default SearchBar;
