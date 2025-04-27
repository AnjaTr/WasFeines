import { useEffect, useMemo, useState } from "react"

import { Box, Chip, CircularProgress, Fab, ImageListItemBar, InputAdornment, Rating, Skeleton, TextField, Typography } from "@mui/material"
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { useDraftRecipe, useMutateDraftRecipe } from "./api/useDraftRecipe";
import DeleteIcon from '@mui/icons-material/Delete';
import { Create } from "@mui/icons-material";
import debounce from "lodash.debounce";
import { components } from "./api/schema";

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
    const { data: mutateData, isPending: isMutatePending, mutateAsync } = useMutateDraftRecipe();
    const [isUploadInProgress, setIsUploadInProgress] = useState<boolean>(false)
    const sortedExistingDraftMedia = data?.draft_media.filter((item) => item.exists).sort((a, b) => {
        return (b.create_timestamp ?? 0) - (a.create_timestamp ?? 0)
    })
    const isCreateRecipeEnabled = sortedExistingDraftMedia && sortedExistingDraftMedia.length > 0
    const [name, setName] = useState<string>("")
    const [description, setDescription] = useState<string>("")
    const [tags, setTags] = useState<string[]>([])
    const [rating, setRating] = useState<number>(0)
    const [inputValue, setInputValue] = useState("");
    const [comment, setComment] = useState<string>("")

    useEffect(() => {
        if (data?.name) {
            setName(data.name)
        }
        if (data?.user_content) {
            setDescription(data.user_content)
        }
        if (data?.user_tags) {
            setTags(data.user_tags)
        }
        if (data?.ratings && data.ratings.length > 0) {
            setRating(data.ratings[0].rating)
        }
        if (data?.ratings && data.ratings.length > 0 && data.ratings[0].comment) {
            setComment(data.ratings[0].comment)
        }
    }, [data?.user_content, data?.user_tags, data?.ratings, data?.name])

    const debouncedUpdate = useMemo(() =>
        debounce(async (new_: Partial<components["schemas"]["RatingRequestModel"]>) => {
            await mutateAsync({
                body: {
                    name: name ?? data?.name ?? "",
                    user_content: description ?? data?.user_content ?? null,
                    user_tags: tags ?? data?.user_tags ?? null,
                    user_rating: (data?.ratings && data?.ratings.length > 0) ? {
                        rating: data?.ratings[0].rating,
                        comment: data?.ratings[0].comment
                    } : null,
                    ...new_
                }
            })
        }, 800), [mutateAsync, name, description, tags, data?.ratings])

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && inputValue.trim() !== '') {
            e.preventDefault();
            setTags([...tags, inputValue.trim()]);
            setInputValue('');
            debouncedUpdate({ user_tags: [...tags, inputValue.trim()] })
        }
    };

    const handleDelete = (tagToDelete: string) => {
        setTags(tags.filter(tag => tag !== tagToDelete));
        debouncedUpdate({ user_tags: tags.filter(tag => tag !== tagToDelete) })
    };



    return <Box sx={{ margin: "55px 0 0 0", padding: "0 15px" }}>
        <Button
            component="label"
            sx={{ marginTop: "10px" }}
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
        <TextField
            label="Recipe Name"
            value={name}
            variant="outlined"
            sx={{ width: "100%" }}
            helperText="Leave empty for it to be generated"
            onBlur={() => {
                if (!isMutatePending) {
                    debouncedUpdate({ name: name })
                }
            }}
            onChange={(event) => {
                setName(event.target.value)
                if (!isMutatePending) {
                    debouncedUpdate({ name: event.target.value })
                }
            }}
            slotProps={{
                input: {
                    endAdornment: isMutatePending ? (<InputAdornment position="end">
                        <CircularProgress size={18} />
                    </InputAdornment>) : null,
                }
            }}
        />
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, marginTop: "20px" }}>
            {tags.map((tag, index) => (
                <Chip
                    key={index}
                    label={tag}
                    onDelete={() => handleDelete(tag)}
                />
            ))}
            <TextField
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                variant="standard"
                placeholder="Add tag"
                sx={{ minWidth: 100 }}
            />
        </Box>
        <TextField
            label="Recipe Description"
            value={description}
            variant="outlined"
            fullWidth
            multiline
            sx={{ marginTop: "20px" }}
            onBlur={() => {
                if (!isMutatePending) {
                    debouncedUpdate({ user_content: description })
                }
            }}
            onChange={(event) => {
                setDescription(event.target.value)
                if (!isMutatePending) {
                    debouncedUpdate({ user_content: event.target.value })
                }
            }}
            slotProps={{
                input: {
                    endAdornment: isMutatePending ? (<InputAdornment position="end">
                        <CircularProgress size={18} />
                    </InputAdornment>) : null,
                }
            }}
        />
        <Box sx={{ marginTop: "20px" }}>
            <TextField
                label="Comment and Rating"
                value={comment}
                variant="outlined"
                fullWidth
                multiline
                onBlur={() => {
                    if (!isMutatePending) {
                        debouncedUpdate({ user_rating: { rating: rating, comment: comment } })
                    }
                }}
                onChange={(event) => {
                    setComment(event.target.value)
                    if (!isMutatePending) {
                        debouncedUpdate({ user_rating: { rating: rating, comment: event.target.value } })
                    }
                }}
                slotProps={{
                    input: {
                        endAdornment: isMutatePending ? (<InputAdornment position="end">
                            <CircularProgress size={18} />
                        </InputAdornment>) : null,
                    }
                }}
            />
            <Rating
                name="simple-controlled"
                value={rating}
                onChange={(event, newValue) => {
                    setRating(newValue);
                    debouncedUpdate({ user_rating: { rating: newValue, comment: comment } })
                }}
                precision={0.5}
                sx={{ padding: "10px"}}
                emptyIcon={<span style={{ color: "#ddd" }}>☆</span>}
                icon={<span style={{ color: "#f39c12" }}>★</span>}
            />
        </Box>

        <Fab
            sx={{ position: "fixed", bottom: 16, right: 16 }}
            color="primary"
            onClick={async () => {
                // asd
            }}
            disabled={!isCreateRecipeEnabled || isMutatePending} variant="extended">
            <Create sx={{ mr: 1 }} />
            Create
        </Fab>
    </Box>
}