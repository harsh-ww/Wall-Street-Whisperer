import { Heading, Flex, Link } from "@chakra-ui/react";

interface Props {
  companyName: string;
  textSize: string;
  TickerCode: string; //ticker code to redirect to company page
}

// component suggested company alerts - will redirect to company page
function CompanyMotif({ companyName, textSize, TickerCode }: Props) {
  return (
    <Link href={`/company/${TickerCode}`}>
      <Flex
        bgGradient="linear(to-r, purple.400, purple.200)"
        justifyContent="space-around"
        alignItems="center"
        textAlign="center"
        padding="0.5em"
        boxShadow="md"
        p="5"
        rounded="xl"
        border="1px"
        borderColor="purple.300"
        _hover={{
          //on hover styling
          transform: "scale(1.015)",
          borderColor: "purple.400",
          boxShadow: "xl",
        }}
      >
        <Flex
          w="100%"
          h="100%"
          alignItems="center"
          justifyContent="center"
          whiteSpace="nowrap"
          textAlign="center"
          overflow="hidden"
        >
          <Heading size={textSize}>
            <Link href={`/company/${TickerCode}`}>{companyName}</Link>
          </Heading>
        </Flex>
      </Flex>
    </Link>
  );
}

export default CompanyMotif;
