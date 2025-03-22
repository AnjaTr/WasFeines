import { useState } from "react";
import Skeleton from "@mui/material/Skeleton";
import Box from "@mui/material/Box";

interface ImageWithSkeletonProps {
  src: string;
  alt: string;
  width: number | string;
  height: number | string;
}

const ImageWithSkeleton: React.FC<ImageWithSkeletonProps> = ({ src, alt, width, height }) => {
  const [loading, setLoading] = useState(true);

  return (
    <Box position="relative" width={width} height={height}>
      {loading && <Skeleton variant="rectangular" width={width} height={height} />}
      <img
        src={src}
        alt={alt}
        width={width}
        height={height}
        onLoad={() => setLoading(false)}
        style={{
          opacity: loading ? 0 : 1,
          transition: "opacity 0.5s ease-in-out",
          display: "block",
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />
    </Box>
  );
};

export default ImageWithSkeleton;
