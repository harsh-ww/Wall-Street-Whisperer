import { useState } from "react";
import {
  Button,
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverArrow,
  PopoverCloseButton,
  PopoverBody,
  Text,
  Link,
} from "@chakra-ui/react";

function App() {
  const [tutorialStarted, setTutorialStarted] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const totalSteps = 3; // Total number of tutorial steps

  const handleStartTutorial = () => {
    setTutorialStarted(true);
  };

  const handleNextStep = () => {
    //iterate through all the popovers
    if (currentStep < totalSteps - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      setTutorialStarted(false); // Reset tutorial
      setCurrentStep(0);
    }
  };

  const handleCloseTutorial = () => {
    setTutorialStarted(false);
    setCurrentStep(0);
  };

  const popoverPositions = [
    { top: "21vh", left: "-3vw" },
    { top: "37vh", left: "51vw" },
    { top: "61vh", left: "-7vw" },
  ]; // Custom positions for each popover using viewport units

  return (
    <>
      <Button
        fontStyle="italic"
        size="xs"
        fontSize="xs"
        onClick={handleStartTutorial}
      >
        Start Tutorial
      </Button>
      {/* Display popovers when tutorial is started */}
      {tutorialStarted && (
        <>
          {currentStep < totalSteps && (
            <Popover
              isOpen={true}
              onClose={handleCloseTutorial}
              placement="top" // Disable automatic placement
            >
              <PopoverTrigger>
                <Button visibility="hidden">Next</Button>
              </PopoverTrigger>
              <PopoverContent
                style={{
                  top: popoverPositions[currentStep].top,
                  left: popoverPositions[currentStep].left,
                }}
              >
                <PopoverArrow />
                <PopoverCloseButton />
                <PopoverBody>
                  {/* Text for each step of the tutorial */}
                  <Text margin="0.4em" fontStyle="italic">
                    {currentStep === 0 && (
                      <>
                        Here is the list of your{" "}
                        <strong>tracked companies</strong>. You can view a
                        summary of key information here. Companies can be added
                        via a track button on their respective pages...{" "}
                      </>
                    )}
                    {currentStep === 1 && (
                      <>
                        Here are your <strong>notifications</strong>. Any
                        articles yielding strong sentiments will appear here for
                        your tracked companies, these will also be sent to your
                        email inbox.{" "}
                      </>
                    )}
                    {currentStep === 2 && (
                      <>
                        Look here for <strong>suggested companies</strong>{" "}
                        curated according to what you currently follow!{" "}
                      </>
                    )}
                  </Text>{" "}
                  {/*Button redirects to apple company page so user can try adding*/}
                  {currentStep === 0 && (
                    <>
                      <Link href="/company/AAPL" isExternal>
                        <Button
                          padding="0.5em"
                          fontSize="sm"
                          marginRight="1em"
                          fontStyle="italic"
                        >
                          Try adding a company now
                        </Button>
                      </Link>{" "}
                    </>
                  )}
                  <Button
                    margin="5px"
                    onClick={handleNextStep}
                    colorScheme="purple"
                    bg="purple.400"
                    borderWidth="1px"
                    borderColor="purple.400"
                    _hover={{
                      transform: "scale(1.01)",
                      bgGradient: "linear(to-r, purple.600, purple.400)",
                      borderColor: "purple.600",
                    }}
                  >
                    {currentStep < totalSteps - 1 ? "Next" : "End Tutorial"}
                  </Button>
                </PopoverBody>
              </PopoverContent>
            </Popover>
          )}
        </>
      )}
    </>
  );
}

export default App;
