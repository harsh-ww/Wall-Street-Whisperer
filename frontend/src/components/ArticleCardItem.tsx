//Reusable component for landing page trending articles tab, company page tab, user home page tab to reference articles
//contains article title (and possibly contents)
//hoverable fade transition popup for info on sentiment analysis
import {
  Card,
  Text,
  Stack,
  Button,
  Image,
  CardBody,
  Heading,
  Flex,
  Tag,
  TagLabel,
  TagRightIcon,
  useDisclosure,
  Badge,
  Box,
} from "@chakra-ui/react";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Link,
} from "@chakra-ui/react";
import { formatDistanceToNow, parseISO, format } from "date-fns";
import { FaArrowTrendDown, FaArrowTrendUp } from "react-icons/fa6";
import { HiExternalLink } from "react-icons/hi";

interface ItemProps {
  article: Article;
}

export interface Article {
  articleid: number;
  articleurl: string;
  authors: string;
  imageurl: string;
  keywords: string;
  overallscore: number;
  publisheddate: string;
  sentimentlabel: string;
  sentimentscore: number;
  sourceid: number;
  sourcepopularity: number;
  summary: string | null;
  title: string;
}

function ArticleCardItem({ article }: ItemProps) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const getRelativeDate = (str: string): string => {
    const date = parseISO(str);
    return formatDistanceToNow(date, { addSuffix: true });
  };
  const getFormattedDate = (str: string): string => {
    const date = parseISO(str);
    return format(date, "dd MMM yyyy");
  };

  return (
    <>
      <Card
        direction={{ base: "column", sm: "row" }}
        overflow="hidden"
        variant="outline"
        size="10rem"
        mb="10px"
        p="10px"
        borderRadius="5px"
        borderWidth="2px"
        _hover={{
          shadow: "sm",
          transform: "translateY(-5px)",
          transitionDuration: "0.2s",
          transitionTimingFunction: "ease-in-out",
        }}
        borderColor={
          article.overallscore < 0
            ? "red.100"
            : article.overallscore >= 70
            ? "green.100"
            : "orange.100"
        }
      >
        <Image
          mr="10px"
          borderRadius="10px"
          objectFit="cover"
          maxW={{ base: "100%", sm: "150px", md: "200px" }}
          src={article.imageurl}
          alt="Caffe Latte"
        />

        <Stack>
          <CardBody>
            <Flex direction="column" alignItems="flex-start">
              <Link onClick={onOpen}>
                <Heading size={["sm", "sm", "md"]} textAlign="left" mb="5px">
                  {article.title}
                </Heading>
              </Link>
              <Flex align="center">
                {article.overallscore < 0 ? (
                  <Tag size="lg" colorScheme="red" borderRadius="full">
                    <TagLabel>
                      <FaArrowTrendDown />
                    </TagLabel>
                  </Tag>
                ) : article.overallscore >= 70 ? (
                  <Tag size="lg" colorScheme="green" borderRadius="full">
                    <TagLabel>
                      <FaArrowTrendUp />
                    </TagLabel>
                  </Tag>
                ) : (
                  <Tag size="lg" colorScheme="orange" borderRadius="full">
                    <TagLabel>
                      <FaArrowTrendUp />
                    </TagLabel>
                  </Tag>
                )}
                <Text mr="10px" ml="10px">
                  {"\u2022"}
                </Text>{" "}
                {/* Bullet character */}
                <Text>{getRelativeDate(article.publisheddate)}</Text>
              </Flex>
            </Flex>
          </CardBody>
        </Stack>
      </Card>
      <Modal isOpen={isOpen} onClose={onClose} size="3xl">
        <ModalOverlay />
        <ModalContent>
          <Flex align="center">
            <ModalHeader fontSize="3xl" minW="80%">
              {article.title}
            </ModalHeader>
            <Box p="5px" fontSize="md">
              <Badge
                colorScheme="green"
                borderRadius="lg"
                fontSize="1.5em"
                p="10px"
              >
                {Math.round(article.overallscore)}
              </Badge>
            </Box>
          </Flex>

          <ModalCloseButton />
          <ModalBody>
            <Flex align="center" justify="space-between" mb="20px">
              <Flex align="center">
                <Text>{article.authors}</Text>
                <Text mr="10px" ml="10px">
                  {"\u2022"}
                </Text>{" "}
                {/* Bullet character */}
                <Text>{getFormattedDate(article.publisheddate)}</Text>
              </Flex>
              <Button
                colorScheme="purple"
                variant="outline"
                rightIcon={<HiExternalLink />}
                size="sm"
                onClick={() => window.open(article.articleurl, "_blank")}
                mr="30px"
              >
                Read Full Article
              </Button>
            </Flex>

            <Text>{article.summary}</Text>
            <Flex alignItems="center" justifyContent="center">
              <Image
                borderRadius="5px"
                objectFit="cover"
                maxW={{ base: "100%", sm: "70%", md: "70%" }}
                src={article.imageurl}
                alt="Caffe Latte"
                mt="10px"
              />
            </Flex>
          </ModalBody>

          <ModalFooter>
            <Button colorScheme="blue" mr={3} onClick={onClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}

export default ArticleCardItem;
