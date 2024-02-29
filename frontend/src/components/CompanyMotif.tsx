//Reusable component primarily for side bar navigation and suggested company alerts
//functionally similar to article motif except for companies and will redirect to company page
import { Heading, Flex } from "@chakra-ui/react";
import { Link, Image } from "@chakra-ui/react";

interface Props {
  companyName: string;
  textSize: string;
}

function CompanyMotif({ companyName, textSize }: Props) {
  return (
    <Flex
      bg="purple.100"
      justifyContent="space-around"
      alignItems="center"
      padding="0.5em"
      boxShadow="md"
      p="5"
      rounded="xl"
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
          <Link href="">{companyName}</Link>
        </Heading>
      </Flex>
    </Flex>
  );
}

export default CompanyMotif;
