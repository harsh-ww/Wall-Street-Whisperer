import "../App.css";
import Background from "../components/Background";
import Logo from "../components/Logo";
import { Box } from "@chakra-ui/react";
function Landing() {
  return (
    <>
      <Box>
        <Background>
          <Logo />
        </Background>
      </Box>
    </>
  );
}

export default Landing;
