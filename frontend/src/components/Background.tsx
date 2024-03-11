import { Box } from "@chakra-ui/react";
import React from "react";

interface Props {
  children: React.ReactNode;
}

function Background({ children }: Props) {
  return (
    <Box
      height="20vh"
      width="100vw"
      p="4"
      bgGradient="linear(to-b, purple.300, purple.100)"
    >
      {children}
    </Box>
  );
}

export default Background;
