import { api } from "./client"

export const useDraftRecipe = () => {
    return api.useQuery("get", "/api/v1/draftrecipe")
}

export const useMutateDraftRecipe = () => {
    return api.useMutation("post", "/api/v1/draftrecipe")
}