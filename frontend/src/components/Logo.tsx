import { Flex } from "@chakra-ui/react";
import { Image } from "@chakra-ui/react";

// component for the logo
function Logo() {
  return (
    <Flex justify="space-between" align="center">
      <Image
        boxSize="5em"
        src="/brandLogo.svg"
        alt="Wall Street Whisperer Logo"
      />
    </Flex>
  );
}

export default Logo;
