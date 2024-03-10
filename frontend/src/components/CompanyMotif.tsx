//Reusable component primarily for side bar navigation and suggested company alerts
//functionally similar to article motif except for companies and will redirect to company page
import { Heading, Flex } from "@chakra-ui/react";
import { Link, Image } from "@chakra-ui/react";

interface Props {
  companyName: string;
  textSize: string;
  TickerCode: string; //ticker code to redirect to company page
}

function CompanyMotif({ companyName, textSize, TickerCode }: Props) {
  return (
    <Flex
      bgGradient="linear(to-r, purple.400, purple.200)"
      justifyContent="space-around"
      alignItems="center"
      padding="0.5em"
      boxShadow="md"
      p="5"
      rounded="xl"
      border="1px"
      borderColor="purple.300"
      _hover={{ //on hover styling
        transform: "scale(1.015)",
        borderColor: "purple.400",
        boxShadow: "xl",
      }}
    >
      <Image src="../../public/logoIpsum.svg" w="25%" />{" "}
      {/*image will also be replaced from prop*/}
      <Flex
        w="65%"
        h="100%"
        alignItems="center"
        whiteSpace="nowrap"
        overflow="hidden"

      >
        <Heading size={textSize}>
          <Link href={`/company/${TickerCode}`}>
            {companyName}
          </Link>
        </Heading>
      </Flex>
    </Flex>
  );
}

export default CompanyMotif;
