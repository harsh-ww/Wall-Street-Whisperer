import { Card, Text, Button, Divider, Box, Flex } from "@chakra-ui/react";
import { ArrowLeftIcon, ArrowRightIcon, BellIcon } from "@chakra-ui/icons";
import { useState } from "react";
import CompanyMotif from "./CompanyMotif";

//side bar, not located in Landing page, contains company motif links and alert links

function MyCard() {
  const [isMoved, setIsMoved] = useState(false);
  const handleMove = () => {
    setIsMoved(!isMoved);
  };

  let trackedCompanies = [
    "Company1",
    "NotaCompany",
    "ShellCorp",
    "LemonadeStand",
    "EvenBiggerCompany",
    "ehgeg",
    "gwggwg",
  ]; //dummy data

  return (
    <Card
      marginY="-50px"
      width="15em"
      height="70vh"
      p="4"
      borderRadius="md"
      bg="white"
      boxShadow="md"
      position="absolute"
      zIndex="100"
      left={isMoved ? "2em" : "-10em"}
      transition="left 0.3s ease"
    >
      <Button
        bg="white"
        position="absolute"
        top="0"
        right="0"
        onClick={handleMove}
        zIndex="1"
        transform="scaleY(0.8)"
      >
        {isMoved ? <ArrowLeftIcon /> : <ArrowRightIcon />}
      </Button>
      <Text fontSize="xl" fontWeight="semibold">
        Tracked Companies
      </Text>
      <Flex flexDirection="column" height="55%" overflow="auto">
        {trackedCompanies.map((company) => (
          <Box transform="scale(0.8)">
            <CompanyMotif companyName={company} textSize="xs" />
          </Box>
        ))}
      </Flex>
      <Divider />
      <Text fontSize="xl" fontWeight="semibold">
        Alerts
        <BellIcon float="right" margin="5px" />
      </Text>
    </Card>
  );
}

export default MyCard;
