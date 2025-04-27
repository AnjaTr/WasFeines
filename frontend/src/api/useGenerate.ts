import { api } from "./client"

export const useGenerate = () => {
    return api.useMutation("post", "/api/v1/generate")
}