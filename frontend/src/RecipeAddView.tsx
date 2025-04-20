import { useState } from "react"

import { Box, ImageListItemBar, Skeleton, Typography } from "@mui/material"
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { useDraftRecipe } from "./api/useDraftRecipe";
import DeleteIcon from '@mui/icons-material/Delete';

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
    const draftRecipeQuery = useDraftRecipe()
    const { data, isLoading } = draftRecipeQuery;
    const [isUploadInProgress, setIsUploadInProgress] = useState<boolean>(false)
    const sortedExistingDraftMedia = data?.draft_media.filter((item) => item.exists).sort((a, b) => {
        return (b.create_timestamp ?? 0) - (a.create_timestamp ?? 0)
    })
    return <Box sx={{ margin: "55px 0 0 0", padding: "0 15px" }}>
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
                accept="image/*"
                onChange={async (event) => {
                    try {
                        setIsUploadInProgress(true)
                        const files = event.target.files;
                        if (!files) {
                            return;
                        }
                        const fileArray = Array.from(files);
                        const fileUploadSlots = data?.draft_media.filter((value) => !value.exists)
                        if (!fileUploadSlots) {
                            return;
                        }
                        if (fileUploadSlots.length < fileArray.length) {
                            console.warn("Not enough slots to upload files")
                            return;
                        }
                        const fileUploadPromises = fileArray.map(async (file, index) => {
                            const fileContent = await file.arrayBuffer();
                            return fetch(fileUploadSlots[index].put_url, {
                                method: "PUT",
                                mode: "cors",
                                headers: {
                                    "Content-Type": file.type,
                                },
                                body: fileContent,
                            })
                        })
                        await Promise.all(fileUploadPromises)
                        draftRecipeQuery.refetch()
                    } finally {
                        setIsUploadInProgress(false)
                    }
                }}
                multiple
            />
        </Button>
        {isLoading && <>
            <Skeleton variant="rectangular" width={"100%"} height={128} sx={{ margin: "20px 0" }} />
            <Skeleton variant="rectangular" width={"100%"} height={128} sx={{ marginBottom: "20px" }} />
            <Skeleton variant="rectangular" width={"100%"} height={192} />
        </>
        }
        {
            isUploadInProgress && <Skeleton variant="rectangular" width={"100%"} height={128} sx={{ margin: "20px 0" }} />
        }
        {sortedExistingDraftMedia && <ImageList cols={1}>
            {sortedExistingDraftMedia.map((item, key) => {
                return <ImageListItem key={key}>
                        <img
                            src={item.get_url}
                            alt="An image"
                            loading="lazy"
                        />
                        <ImageListItemBar
                            sx={{ background: "transparent", padding: "10px" }}
                            position="top"
                            actionIcon={<DeleteIcon />}
                            actionPosition="right"
                            onClick={async () => {
                                if (!item.delete_url) {
                                    return
                                }
                                await fetch(item.delete_url, {
                                    method: "DELETE",
                                    mode: "cors",
                                })
                                draftRecipeQuery.refetch()
                            }}
                        />
                    </ImageListItem>
            })}
        </ImageList>
        }
    </Box>
}