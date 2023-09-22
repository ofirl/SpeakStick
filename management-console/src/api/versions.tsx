import { UseQueryOptions, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";
import { toast } from "react-toastify";

export const useApplicationVersions = <T extends object | string = string[]>(options: UseQueryOptions<string[], unknown, T, string[]> = {}) => {
    return useQuery(
        ['versions'],
        () => axios.get(baseUrl + "/versions").then(value => value.data as string[]),
        options
    )
};

export const useLatestVersion = () => {
    return useApplicationVersions({ select: (data) => data[0] });
};

export type ChangeLog = {
    title: string,
    description: string
}
export const useVersionsChangeLog = (options: UseQueryOptions<ChangeLog[], unknown, ChangeLog[], string[]> = {}) => {
    return useQuery(
        ['versions', 'changeLog'],
        () => axios.get(baseUrl + "/versions/change_log").then(value => value.data as ChangeLog[]),
        {
            staleTime: 1000 * 60 * 2, // 2 minutes - there is an API rate limit on this request
            ...options,
        }
    )
};

export const useApplicationCurrentVersion = (options: UseQueryOptions<string, unknown, string, string[]> = {}) => {
    return useQuery(
        ['current_version'],
        () => axios.get(baseUrl + "/versions/current").then(value => value.data as string),
        options
    )
};

type UpgradeApplicationParams = {
    version: string
}
export const useUpgradeApplication = () => {
    return useMutation((params: UpgradeApplicationParams) =>
        axios.get(baseUrl + "/upgrade", { params }).then(value => value.status === 200),
        {
            onSuccess: () => {
                toast.success("Application is upgrading, this might take a few seconds")
            },
            onError: () => {
                toast.error("Error starting application upgrade")
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