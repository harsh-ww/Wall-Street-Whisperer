import { Flex, Link, Text, Box, Fade} from "@chakra-ui/react";

interface Props {
  companyName: string;
  ticker: string;
}

function SuggestionsGenerator({ companyName, ticker }: Props) {
  return (
    <Fade in={true}>
      <Flex
        bgGradient="linear(to-r, purple.300, purple.100)"
        h="auto"
        justifyContent="center"
        alignItems="center"
        boxShadow="lg"
        p="3"
        rounded="xl"
        border="2px"
        borderColor="purple.300"
        overflow="hidden"
        maxW="300px"
        maxH="120px"
        flexDirection="column" 
        textAlign="center"
        transition="all 0.3s"
        _hover={{ //on hover styling
          transform: "scale(1.015)",
          borderColor: "purple.400",
          boxShadow: "xl",
        }}
      >
        <Link href={`/company/${ticker}`} textDecoration="none" _hover={{ textDecoration: 'none' }}>
          <Text fontWeight="bold" fontSize="lg" mb="2" color="gray.800">{companyName}</Text>
        </Link>
        <Box mt="auto"> {/* Pushes ticker to bottom */}
          <Text fontStyle="italic" color="gray.600" fontSize="sm" lineHeight="1.2">Ticker: {ticker}</Text>
        </Box>
      </Flex>
    </Fade>
  );
}

export default SuggestionsGenerator;

