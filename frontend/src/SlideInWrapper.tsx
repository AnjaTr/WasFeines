import React, { useEffect, useState } from 'react';
import { Slide, Box } from '@mui/material';
import { useLocation } from 'react-router';

const SlideInWrapper = ({ children }: { children: React.ReactNode }) => {
  const [slideIn, setSlideIn] = useState(false);

  const location = useLocation();

  useEffect(() => {
    setSlideIn(true);
  }, [location]);

  return (
    <Slide direction="left" in={slideIn} mountOnEnter unmountOnExit>
      <Box position="absolute" top={0} sx={{ background: "white" }}>
        {children}
      </Box>
    </Slide>
  );
};

export default SlideInWrapper;