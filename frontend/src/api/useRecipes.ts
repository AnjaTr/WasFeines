import { api } from "./client"

export const useRecipes = () => {
    return api.useQuery("get", "/api/v1/recipes")
}