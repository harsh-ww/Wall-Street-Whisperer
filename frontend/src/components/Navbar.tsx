import React from "react";
import { NavLink } from "react-router-dom";
import Profile from "./Profile";
import {
  chakra,
  Box,
  Flex,
  useColorModeValue,
  VisuallyHidden,
  HStack,
  Button,
  useDisclosure,
  VStack,
  IconButton,
  CloseButton,
} from "@chakra-ui/react";
import Logo from "./Logo";
import {
  AiOutlineMenu,
  AiFillHome,
  AiOutlineInbox,
  AiFillBell,
} from "react-icons/ai";
import { BsFillCameraVideoFill, BsFillInboxFill } from "react-icons/bs";
import { MdOutlineBusinessCenter, MdExplore } from "react-icons/md";
import Tutorial from "../components/Tutorial";
export default function App() {
  const bg = useColorModeValue("white", "gray.800");
  const mobileNav = useDisclosure();

  return (
    <React.Fragment>
      <chakra.header
        bg={bg}
        w="full"
        px={{ base: 2, sm: 4 }}
        py={1}
        shadow="md"
      >
        <Flex alignItems="center" justifyContent="space-between" mx="auto">
          <HStack display="flex" spacing={3} alignItems="center">
            <Box display={{ base: "inline-flex", md: "none" }}>
              <IconButton
                display={{ base: "flex", md: "none" }}
                aria-label="Open menu"
                fontSize="20px"
                color="gray.800"
                _dark={{ color: "inherit" }}
                variant="ghost"
                icon={<AiOutlineMenu />}
                onClick={mobileNav.onOpen}
              />
              <VStack
                pos="absolute"
                top={0}
                left={0}
                right={0}
                display={mobileNav.isOpen ? "flex" : "none"}
                flexDirection="column"
                p={2}
                pb={4}
                m={2}
                bg={bg}
                spacing={3}
                rounded="sm"
                shadow="sm"
                zIndex={9999} // Ensure the navbar appears on top of other content
              >
                <CloseButton
                  aria-label="Close menu"
                  justifySelf="self-start"
                  onClick={mobileNav.onClose}
                />
                <NavLink to="/">
                  <Button variant="ghost" leftIcon={<AiFillHome />} size="md">
                    Home
                  </Button>
                </NavLink>
                
              </VStack>
            </Box>
            <chakra.a
              href="/"
              title="Finance App"
              display="flex"
              alignItems="center"
            >
              <Logo />
              <VisuallyHidden>Finance App</VisuallyHidden>
            </chakra.a>

            <HStack spacing={3} display={{ base: "none", md: "inline-flex" }}>
              <NavLink to="/home">
                <Button variant="ghost" leftIcon={<AiFillHome />} size="md">
                  Home
                </Button>
              </NavLink>
              <Tutorial />
            </HStack>
          </HStack>
        </Flex>
      </chakra.header>
    </React.Fragment>
  );
}
