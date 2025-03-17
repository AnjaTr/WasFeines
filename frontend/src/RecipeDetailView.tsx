import { useNavigate, useParams } from "react-router";
import { useRecipeContext } from "./context/RecipeProvider";
import SlideInWrapper from "./SlideInWrapper";
import { Box, Button, Paper } from "@mui/material";
import { ArrowBackIosNew } from "@mui/icons-material";

export type RecipeDetailViewRouteParams = {
    recipeId: string;
}

export const RecipeDetailView: React.FC = ({ }) => {
    const { recipeId } = useParams<RecipeDetailViewRouteParams>();
    const { state } = useRecipeContext();
    const navigate = useNavigate();
    const recipe = state.recipes[parseInt(recipeId)];

    return (
    <SlideInWrapper>
        <Box sx={{ marginTop: "56px" }}>
            <Button startIcon={<ArrowBackIosNew />} onClick={() => navigate(-1)}>
            Back
            </Button>
            <Box>
                {recipe.name}
                test 123
            </Box>
        </Box>
    </SlideInWrapper>
    );
}
