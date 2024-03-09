import { AlertIcon, Button, Spinner, Alert, Box, Flex } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import NotifItem from "./NotifItem";
import { Article } from "./ArticleCardItem";
import { API_URL } from "../config";

interface Notification extends Article {
  companyName: string;
  companyTicker: string;
}

export default function Notifications() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const fetchNotifications = async () => {
      const res = await fetch(`${API_URL}/unvisitednotifications`);
      if (!res.ok) {
        console.error(`HTTP error! status: ${res.status}`);
        return;
      }
      const data = await res.json();
      console.log(data);
      setNotifications(data);
      setLoaded(true);
    };

    fetchNotifications();
  }, []);

  const clearAllNotifications = async () => {
    const res = await fetch(`${API_URL}/visitAll`, {
      method: "POST",
    });
    if (res.ok) {
      setNotifications([]);
    }
  };

  const clearNotification = async (id: number) => {
    console.log("clearing notification", id);
    const res = await fetch(`${API_URL}/visitAll/${id}`, {
      method: "POST",
    });
    if (res.ok) {
      const notificationsWithRemoved = notifications.filter(
        (n) => n.articleid != id
      );
      setNotifications(notificationsWithRemoved);
    }
  };

  if (!loaded) {
    return (
      <Spinner
        thickness="4px"
        speed="0.65s"
        emptyColor="gray.200"
        color="blue.500"
        size="xl"
      />
    );
  }

  if (notifications.length == 0) {
    return (
      <Alert status="info">
        <AlertIcon />
        You have no new notifications!
      </Alert>
    );
  }

  return (
    <Box>
      <Button colorScheme="red" onClick={clearAllNotifications} mb="10px">
        Clear All Notifications
      </Button>
      {notifications.map((notification) => (
        <Flex justifyContent="center" alignItems="center">
          <NotifItem
            key={notification.articleid}
            article={notification}
            company={notification.companyName}
            closeButton={() => clearNotification(notification.articleid)}
          />
          {/* <CloseButton
            colorScheme="pink"
            onClick={() => clearNotification(notification.articleid)}
          /> */}
        </Flex>
      ))}
    </Box>
  );
}
