import { Card, Text, Button, Box, Flex } from "@chakra-ui/react";
import { ArrowLeftIcon, ArrowRightIcon } from "@chakra-ui/icons";
import { useState, useEffect } from "react";
import CompanyMotif from "./CompanyMotif";
import { API_URL } from "../config";
interface trackedDetails {
  CommonName: string;
  TickerCode: string;
}

// component contains company motif links and alert links
function MyCard() {
  const [isMoved, setIsMoved] = useState(false);
  const handleMove = () => {
    setIsMoved(!isMoved);
  };

  const [companies, setCompanies] = useState<trackedDetails[]>([]);

  useEffect(() => {
    const fetchTracked = async () => {
      try {
        const response = await fetch(`${API_URL}/tracked`);
        if (!response.ok) {
          throw new Error("Failed to fetch tracked companies");
        }
        const data = await response.json();
        setCompanies(data);
      } catch (error) {
        console.error("Error fetching companies", error);
      }
    };
    fetchTracked();
  }, []);

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
      left={isMoved ? "2em" : "-12.4em"}
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
      <Text
        fontSize="xl"
        fontWeight="semibold"
        textAlign="center"
        mt={3}
        mb={1}
      >
        Tracked Companies
      </Text>
      <Flex flexDirection="column" height="100%" overflow="auto">
        {companies.map(
          (
            company,
            index //map the retrieved json tracked companies into sections
          ) => (
            <Box transform="scale(0.8)" key={index}>
              <CompanyMotif
                companyName={company ? company.CommonName : ""}
                textSize="md"
                TickerCode={company ? company.TickerCode : ""}
              />
            </Box>
          )
        )}
      </Flex>
    </Card>
  );
}

export default MyCard;
