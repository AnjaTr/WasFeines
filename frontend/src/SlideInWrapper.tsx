import React, { useEffect, useState } from 'react';
import { Slide, Box } from '@mui/material';
import { useLocation } from 'react-router';

const SlideInWrapper = ({ children }: { children: React.ReactNode }) => {
  const [slideIn, setSlideIn] = useState(false);

  const location = useLocation();

  useEffect(() => {
    setSlideIn(true);

    // Reset slideIn after the animation completes (this may depend on the animation duration)
    //const timer = setTimeout(() => setSlideIn(false), 300); // 300ms for slide transition

    //return () => clearTimeout(timer);
  }, [location]);

  return (
    <Slide direction="left" in={slideIn} mountOnEnter unmountOnExit>
      <Box sx={{ width: "100vw", height: "100vh", overflow: "hidden", position: "relative" }}>
        {children}
      </Box>
    </Slide>
  );
};

export default SlideInWrapper;