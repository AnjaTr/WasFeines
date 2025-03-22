import { useState } from "react"

import { Box } from "@mui/material"
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});


type RecipeAddViewProps = {
}

export const RecipeAddView: React.FC<RecipeAddViewProps> = () => {
    const [itemData, setItemData] = useState([])
    return <Box sx={{ margin: "55px 0 0 0", padding: "0 20px" }}>
        <Button
            component="label"
            role={undefined}
            variant="contained"
            tabIndex={-1}
            startIcon={<CloudUploadIcon />}
        >
            Upload files
            <VisuallyHiddenInput
                type="file"
                onChange={(event) => setItemData([...event.target.files])}
                multiple
            />
        </Button>
        <ImageList sx={{ width: 500, height: 450 }} cols={3} rowHeight={164}>
            {itemData.map((item, key) => {
                const src = URL.createObjectURL(item)
                return (
                <ImageListItem key={key}>
                    <img
                        src={src}
                        alt="An image"
                        loading="lazy"
                    />
                </ImageListItem>
            )})}
        </ImageList>
    </Box>
}