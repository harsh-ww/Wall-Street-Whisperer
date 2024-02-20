import "../App.css";
import Background from "../components/Background";
import Logo from "../components/Logo";
import SideBar from "../components/SideBar";
import { Box } from "@chakra-ui/react";
import BaseLayout from "../layouts/BaseLayout";
import NavBar from "../components/Navbar";
import LineChart from "../components/LineChart";

function Company() {
  return (
    <>
      <Box>
        <BaseLayout />
        <SideBar />
        {/* <Background>
          <Logo />
          <SideBar />
        </Background> */}
      </Box>
    </>
  );
}

export default Company;
