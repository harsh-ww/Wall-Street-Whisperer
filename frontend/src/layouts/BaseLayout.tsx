import React from "react";
import Background from "../components/Background";
import { Box } from "@chakra-ui/react";
import Navbar from "../components/Navbar";
import SearchBar from "../components/SearchBar";

export default function BaseLayout() {
  return (
    <>
      <Box>
        <Navbar />
        <Background>
          <SearchBar />
        </Background>
      </Box>
    </>
  );
}
