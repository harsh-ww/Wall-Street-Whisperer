import { Flex } from "@chakra-ui/react";
import { Image } from "@chakra-ui/react";

//reusable logo contained in its own Chakra Flex wrapper
//typically docked in top left

function Logo() {
  return (
    <Flex justify="space-between" align="center">
      <Image boxSize="5em" src="/logoIpsum.svg" alt="logo here" />
    </Flex>
  );
}

export default Logo;
