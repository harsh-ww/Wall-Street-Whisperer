import { Card, Text, Button, Divider } from "@chakra-ui/react";
import { useState } from "react";

//side bar, not located in Landing page, contains company motif links and alert links

function MyCard() {
  const [isMoved, setIsMoved] = useState(false);

  const handleMove = () => {
    setIsMoved(!isMoved);
  };

  return (
    <Card
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
        position="absolute"
        top="0"
        right="0"
        onClick={handleMove}
        zIndex="1"
      >
        {">>"}
      </Button>
      <Text fontSize="xl" fontWeight="semibold">
        Tracked Companies
      </Text>
      <Text>Individual company bubbles here</Text>
      <Divider />
      <Text fontSize="xl" fontWeight="semibold">
        Alerts
      </Text>
    </Card>
  );
}

export default MyCard;
