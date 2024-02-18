import { Card, Text, Button, Divider } from "@chakra-ui/react";
import { useState } from "react";

function MyCard() {
  const [isMoved, setIsMoved] = useState(false);

  const handleMove = () => {
    setIsMoved(!isMoved);
  };

  return (
    <Card
      width="22vw"
      height="70vh"
      p="4"
      borderRadius="md"
      bg="white"
      boxShadow="md"
      position="absolute"
      left={isMoved ? "22vw" : "-19vw"}
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
