import { Flex } from "@chakra-ui/react";
import { Link, Text, Box } from "@chakra-ui/react";

interface Props {
  companyName: string;
  ticker: string;
}

function SuggestionsGenerator({ companyName, ticker }: Props) {
  return (
    <Flex
      h="50%"
      bg="white"
      justifyContent="space-around"
      alignItems="center"
      boxShadow="md"
      p="5"
      borderRadius="1000px"
      border="2px"
      borderColor="purple.900"
      direction="column"
    >
      <Link href={`/company/${ticker}`}>{companyName}</Link>

    </Flex>
  );
}

export default SuggestionsGenerator;