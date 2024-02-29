//Reusable component for landing page trending articles tab, company page tab, user home page tab to reference articles
//contains article title (and possibly contents)
//hoverable fade transition popup for info on sentiment analysis
import { Flex } from "@chakra-ui/react";
import { Link, Text, Box } from "@chakra-ui/react";

interface Props {
  articleName: string;
}

function ArticleMotif({ articleName }: Props) {
  return (
    <Flex
      h="60%"
      bg="white"
      justifyContent="space-around"
      alignItems="left"
      boxShadow="md"
      p="5"
      borderRadius="1000px"
      border="2px"
      borderColor="purple.900"
      direction="column"
    >
      <Link href="">{articleName}</Link>
      <Box>
        <Text fontSize="xs" overflow="hidden">
          Hi here is the text woah lore ipsum dolorem Caecilius est in horto
        </Text>
      </Box>
    </Flex>
  );
}

export default ArticleMotif;
