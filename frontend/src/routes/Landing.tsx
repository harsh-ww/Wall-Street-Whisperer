import "../App.css";
import Background from "../components/Background";
import Logo from "../components/Logo";
import { Box } from "@chakra-ui/react";
import Navbar from "../components/Navbar";
import BaseLayout from "../layouts/BaseLayout";
import LineChart from "../components/LineChart";

function Landing() {
  return (
    <>
      <BaseLayout />
      {/* <Navbar />
      <Box>
        <Background>
          <Logo />
        </Background>
      </Box> */}
    </>
  );
}

export default Landing;
