import { ReactNode } from "react";
import { Box } from "@chakra-ui/react";

interface Props {
  children: ReactNode;
}

function Background({ children }: Props) {
  return (
    <Box
      height="20vh"
      width="100vw"
      bg="purple.700"
      p="4"
      color="white"
      bgGradient="linear(to-b, purple.100, white)"
    >
      {children} {/*where the logo gets put */}
    </Box>
  );
}

export default Background;
