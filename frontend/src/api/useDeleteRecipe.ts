import { useQueryClient } from "@tanstack/react-query"
import { api } from "./client"

export const useDeleteRecipe = () => {
    const client = useQueryClient()
    return api.useMutation("delete", "/api/v1/recipes", {
        onSuccess: (data) => {
            const opts = api.queryOptions("get", "/api/v1/recipes")
            client.invalidateQueries({
                queryKey: opts.queryKey,
            })
        }
    })
}