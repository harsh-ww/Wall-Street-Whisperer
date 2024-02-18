import { Flex } from "@chakra-ui/react";
import { Image } from "@chakra-ui/react";

function Logo() {
  return (
    <Flex justify="space-between" align="center">
      <Image boxSize="5em" src="/logoIpsum.svg" alt="logo here" />
    </Flex>
  );
}

export default Logo;
