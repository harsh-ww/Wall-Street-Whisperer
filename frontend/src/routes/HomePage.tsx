import "../App.css";
import Background from "../components/Background";
import Logo from "../components/Logo";
import SideBar from "../components/SideBar";
import SearchBar from "../components/SearchBar";
import { Box } from "@chakra-ui/react";
import BaseLayout from "../layouts/BaseLayout";

function HomePage() {
  return (
    <>
      <Box>
        <BaseLayout />
        <SideBar />
        {/* <Background>
          <Logo />
        </Background>
        <SideBar />
        <SearchBar /> */}
      </Box>
    </>
  );
}

export default HomePage;
