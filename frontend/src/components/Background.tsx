import { ReactNode } from "react";
import { Box } from "@chakra-ui/react";

//consistent background implementing gradient effect
//considering background png for more visual design

interface Props {
  children: ReactNode;
}

function Background({ children }: Props) {
  return (
    <Box height="20vh" width="100vw" p="4">
      {children} {/*where the logo gets put */}
    </Box>
  );
}

export default Background;
