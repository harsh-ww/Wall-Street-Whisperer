//Reusable component for landing page trending articles tab, company page tab, user home page tab to reference articles
//contains article title (and possibly contents)
//hoverable fade transition popup for info on sentiment analysis
import { Heading, Flex } from "@chakra-ui/react";
import {
  Link,
  Image,
  Text,
  Card,
  CardHeader,
  CardBody,
  Box,
} from "@chakra-ui/react";

interface Props {
  articleName: string;
}

function ArticleMotif({ articleName }: Props) {
  return (
    <Flex
      bg="purple.100"
      justifyContent="space-around"
      alignItems="center"
      boxShadow="md"
      p="6"
      rounded="xl"
    >
      <Link href="">{articleName}</Link>
      <Box>
        <Text fontSize="xs">Hi here is the text woah</Text>
      </Box>
    </Flex>
  );
}

export default ArticleMotif;
