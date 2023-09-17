import { UseQueryOptions, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";
import { toast } from "react-toastify";

export const useApplicationVersions = (options: UseQueryOptions<string[], unknown, string[], string[]> = {}) => {
    return useQuery(
        ['versions'],
        () => axios.get(baseUrl + "/versions").then(value => value.data as string[]),
        options
    )
};

export const useApplicationCurrentVersion = (options: UseQueryOptions<string, unknown, string, string[]> = {}) => {
    return useQuery(
        ['current_version'],
        () => axios.get(baseUrl + "/versions/current").then(value => value.data as string),
        options
    )
};

type SwitchApplicationVersionParams = {
    version: string
}
export const useSwitchApplicationVersion = () => {
    return useMutation((params: SwitchApplicationVersionParams) =>
        axios.post(baseUrl + "/versions/switch", params).then(value => value.status === 200),
        {
            onSuccess: () => {
                toast.success("Application is switching, this might take a few minutes")
            },
            onError: () => {
                toast.error("Error switching application version")
            }
        }
    )
};

export const useUpdateApplicationVersions = () => {
    const queryClient = useQueryClient();

    return useMutation(() =>
        axios.get(baseUrl + "/versions/update").then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(['versions'])
                toast.success("Application versions were updated")
            },
            onError: () => {
                toast.error("Error switching application version")
            }
        }
    )
};