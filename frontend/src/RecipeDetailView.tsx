import { useNavigate, useParams } from "react-router";
import { useRecipeContext } from "./context/RecipeProvider";
import SlideInWrapper from "./SlideInWrapper";
import { Box, Button } from "@mui/material";
import Skeleton from "@mui/material/Skeleton";
import { ArrowBackIosNew } from "@mui/icons-material";
import { useEffect, useState } from "react";
import { useDeleteRecipe } from "./api/useDeleteRecipe";
import { useRecipes } from "./api/useRecipes";

export type RecipeDetailViewRouteParams = {
    recipeId: string;
}

const RecipeDetailViewSkeleton: React.FC = () => <Box sx={{ padding: "0 20px" }}>
    <Skeleton variant="rectangular" height={50} />
    <Skeleton variant="text" height={30} width="60%" />
    <Skeleton variant="text" height={30} width="60%" />
    <Skeleton variant="text" height={30} width="80%" />
    <Skeleton variant="text" height={400} width="100%" />

</Box>

export const RecipeDetailView: React.FC = ({ }) => {
    const { recipeId } = useParams<RecipeDetailViewRouteParams>();
    const { data: recipes, isLoading} = useRecipes();
    const [recipeHtml, setRecipeHtml] = useState<string>("");
    const navigate = useNavigate();
    const { mutateAsync: deleteRecipe, isPending: isDeletePending } = useDeleteRecipe();
    const maybeRecipe = recipes && recipeId ? recipes[parseInt(recipeId)] : null;

    useEffect(() => {
        async function fetchRecipe() {
            const response = await fetch(maybeRecipe!.content_url);
            const html = await response.text();
            setRecipeHtml(html)
        }
        if (maybeRecipe && maybeRecipe.content_url) {
            fetchRecipe();
        }
    }, [recipeId]);

    return (
    <SlideInWrapper>
        <Box sx={{ marginTop: "56px", height: "100dvh", maxWidth: "600px" }}>
            <Box>
                <Button startIcon={<ArrowBackIosNew />} onClick={() => navigate(-1)}>
                Back
                </Button>
                { !recipeHtml && <RecipeDetailViewSkeleton />}
                { recipeHtml && <Box sx={{ padding: "0 20px", overflow: "scroll", height: "100%" }}>
                    {recipeHtml !== "" && <div dangerouslySetInnerHTML={{ __html: recipeHtml }} />}
                </Box>
                }
            </Box>
            <Box sx={{ marginTop: "10px"}}>
                {maybeRecipe && maybeRecipe.media.map((media, index) => (
                    <Box key={index}>
                        <img src={media.content_url} alt="Media" style={{ width: "100%" }} />
                    </Box>
                ))}
            </Box>
            <Box sx={{ marginTop: "10px"}}>
                {maybeRecipe && maybeRecipe.media.map((media, index) => (
                    <Box key={index}>
                        <Button variant="contained" color="error" onClick={async () => {
                            await deleteRecipe({ params: { query: { recipe_name: maybeRecipe.name } } });
                            navigate(-1);
                        }} disabled={isDeletePending}>
                            Delete Recipe
                        </Button>
                    </Box>
                ))}
            </Box>
        </Box>
    </SlideInWrapper>
    );
}
