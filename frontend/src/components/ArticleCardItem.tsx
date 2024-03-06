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
import { formatDistanceToNow, parseISO, parse } from "date-fns";
import { FaArrowTrendDown, FaArrowTrendUp } from "react-icons/fa6";

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
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Modal Title</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <p>jfnlsrnjerglongtjkrdgtnjdkrgrnthjktrnhjkrt</p>
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
