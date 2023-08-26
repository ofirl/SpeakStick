import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";
import { toast } from "react-toastify";

export const useGetConfigs = () => {
    return useQuery(['configs'], () => axios.get(baseUrl + "/api/configs").then(value => value.data as Record<string, string>))
};

type updateConfigParams = { key: string, value: string };
export const useUpdateConfig = () => {
    const queryClient = useQueryClient();
    return useMutation((params: updateConfigParams) =>
        axios.post(baseUrl + "/api/config", params).then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(["configs"]);
                toast.success("Config updated")
            },
            onError: () => {
                toast.error("Error updating config")
            }
        }
    )
};