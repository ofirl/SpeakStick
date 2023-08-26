import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

export const useGetWords = () => {
    return useQuery(['words'], () => axios.get(baseUrl + "/api/words").then(value => value.data as Record<string, string>))
};

type updateWordParams = { position: string, word: string };
export const useUpdateWord = () => {
    const queryClient = useQueryClient();
    return useMutation((params: updateWordParams) =>
        axios.post(baseUrl + "/api/word", params).then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(["words"]);
            }
        }
    )
};