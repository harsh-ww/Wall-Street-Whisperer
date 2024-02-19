import "../App.css";
import Background from "../components/Background";
import Logo from "../components/Logo";
import SideBar from "../components/SideBar";
import { Box } from "@chakra-ui/react";

function Company() {
  return (
    <>
      <Box>
        <Background>
          <Logo />
          <SideBar />
        </Background>
      </Box>
    </>
  );
}

export default Company;
