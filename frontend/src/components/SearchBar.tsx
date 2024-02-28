import { Flex, Input, InputGroup, InputRightElement } from "@chakra-ui/react";
import { SearchIcon } from "@chakra-ui/icons";
import { Fade, Button, Text } from "@chakra-ui/react";
import { useState } from "react";

//search bar functionality, length dependent on container it is in
//dropdown menu needs to be added

function SearchBar() {
  const [isFocused, setIsFocused] = useState(false);
  const handleToggle = () => {
    setIsFocused(!isFocused);
  };

  const [companyDropDown, setCompanyDropDown] = useState(null);
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
          />
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
