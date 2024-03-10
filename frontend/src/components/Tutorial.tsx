import { useState } from "react";
import { Button, Popover, PopoverTrigger, PopoverContent, PopoverArrow, PopoverCloseButton, PopoverHeader, PopoverBody, Text, Box } from "@chakra-ui/react";

function App() {
  const [tutorialStarted, setTutorialStarted] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const totalSteps = 3; // Total number of tutorial steps 

  const handleStartTutorial = () => {
    setTutorialStarted(true);
  };

  const handleNextStep = () => { //iterate through all the popovers
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
    { top: "10vh", left: "10vw" },
    { top: "40vh", left: "50vw" },
    { top: "70vh", left: "20vw" }
  ]; // Custom positions for each popover using viewport units

  return (
    <>
      <Button fontStyle="italic" size="xs" fontSize="xs" onClick={handleStartTutorial}>Start Tutorial</Button>
      {tutorialStarted && (
        <>
          {/* Background overlay to blur the content */}
          <Box
            position="fixed"
            top="0"
            left="0"
            width="100%"
            height="100%"
          />

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
                  <Text>
                    {currentStep === 0 && "This is step 1 of the tutorial. Click the button to continue."}
                    {currentStep === 1 && "This is step 2 of the tutorial. Click the button to continue."}
                    {currentStep === 2 && "This is step 3 of the tutorial. Click the button to end the tutorial."}
                  </Text>
                  <Button onClick={handleNextStep}>{currentStep < totalSteps - 1 ? "Next" : "End Tutorial"}</Button>
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