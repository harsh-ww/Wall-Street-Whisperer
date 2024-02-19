import "../App.css";
import Background from "../components/Background";
import Logo from "../components/Logo";
import SideBar from "../components/SideBar";
import SearchBar from "../components/SearchBar";
import { Box } from "@chakra-ui/react";

function HomePage() {
  return (
    <>
      <Box>
        <Background>
          <Logo />
        </Background>
        <SideBar />
        <SearchBar />
      </Box>
    </>
  );
}

export default HomePage;
