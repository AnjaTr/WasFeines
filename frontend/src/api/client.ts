import createFetchClient from "openapi-fetch";
import createClient from "openapi-react-query";
import type { paths } from "./schema";
import { QueryClient } from "@tanstack/react-query";

const fetchClient = createFetchClient<paths>({
  baseUrl: "/",
});
export const queryClient = new QueryClient();
export const api = createClient(fetchClient);