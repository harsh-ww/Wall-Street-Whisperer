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
  CloseButton,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Link,
} from "@chakra-ui/react";
import { formatDistanceToNow, format } from "date-fns";
import { FaArrowTrendDown, FaArrowTrendUp } from "react-icons/fa6";
import { HiExternalLink } from "react-icons/hi";
import { Article } from "./ArticleCardItem";

interface ItemProps {
  article: Article;
  company?: string;
  closeButton: () => void;
}

function NotifItem({ article, company, closeButton }: ItemProps) {
  // useDisclosure hook to handle modal open and close
  const { isOpen, onOpen, onClose } = useDisclosure();
  const getRelativeDate = (str: string): string => {
    const date = new Date(str);
    return formatDistanceToNow(date, { addSuffix: true });
  };
  const getFormattedDate = (str: string): string => {
    const date = new Date(str);
    return format(date, "dd MMM yyyy");
  };

  return (
    <>
      <Card
        direction={{ base: "column", sm: "row" }}
        overflow="hidden"
        size="10rem"
        mb="10px"
        p="10px"
        _hover={{
          shadow: "sm",
          transform: "translateY(-5px)",
          transitionDuration: "0.2s",
          transitionTimingFunction: "ease-in-out",
        }}
      >
        <Stack>
          <CardBody>
            <Flex alignItems="center">
              <Box>
                <Flex align="center" mb="5px">
                  <Tag
                    size="lg"
                    borderRadius="5px"
                    colorScheme={
                      article.overallscore < 0
                        ? "red"
                        : article.overallscore >= 70
                        ? "green"
                        : "orange"
                    }
                  >
                    {company && (
                      <>
                        <TagLabel>{company}</TagLabel>
                        <TagRightIcon
                          as={
                            article.overallscore < 0
                              ? FaArrowTrendDown
                              : FaArrowTrendUp
                          }
                        />
                      </>
                    )}
                  </Tag>
                  <Text ml="10px">
                    {getRelativeDate(article.publisheddate)}
                  </Text>
                </Flex>
                <Link onClick={onOpen}>
                  <Heading size={["sm", "sm", "md"]} textAlign="left" mb="5px">
                    {article.title}
                  </Heading>
                </Link>
              </Box>
              <CloseButton
                colorScheme="pink"
                onClick={closeButton} // Call the closeButton function
              />
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
                colorScheme={
                  article.overallscore < 0
                    ? "red"
                    : article.overallscore >= 70
                    ? "green"
                    : "orange"
                }
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

export default NotifItem;
