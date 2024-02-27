import { Flex, Input, InputGroup, InputRightElement } from "@chakra-ui/react";
import { SearchIcon } from "@chakra-ui/icons";
import {
  Fade,
  ScaleFade,
  Slide,
  SlideFade,
  Collapse,
  useDisclosure,
} from "@chakra-ui/react";
import { useState } from "react";

//search bar functionality, length dependent on container it is in
//dropdown menu needs to be added

function SearchBar() {
  const { isOpen, onToggle } = useDisclosure();
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
          />
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
