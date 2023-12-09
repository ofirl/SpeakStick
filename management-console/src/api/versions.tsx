import { UseCreateMutationWrapperOptions, UseCreateQueryWrapperOptions, UseCreateQueryWrapperOptionsShort, axiosClient, useCreateMutation, useCreateQuery } from "./helpers";

export const useApplicationVersions = <T extends string[] | string = string[]>(options?: UseCreateQueryWrapperOptions<string[], T>) => {
  return useCreateQuery({
    queryKey: ['versions'],
    queryFn: () => axiosClient.get("/versions").then(value => value.data as string[]),
    errorMsg: "Error getting application version",
    ...options,
  }
  )
};

export const useLatestVersion = () => {
  return useApplicationVersions({ select: (data) => data[0], errorMsg: "Error getting latest version" });
};

export type ChangeLog = {
  title: string,
  description: string
}
export const useVersionsChangeLog = (options?: UseCreateQueryWrapperOptionsShort<ChangeLog[]>) => {
  return useCreateQuery({
    queryKey: ['versions', 'changeLog'],
    queryFn: () => axiosClient.get("/versions/change_log").then(value => value.data as ChangeLog[]),
    staleTime: 1000 * 60 * 2, // 2 minutes - there is an API rate limit on this request
    errorMsg: "Error getting change log",
    ...options,
  })
};

export const useApplicationCurrentVersion = (options?: UseCreateQueryWrapperOptionsShort<string>) => {
  return useCreateQuery({
    queryKey: ['current_version'],
    queryFn: () => axiosClient.get("/versions/current").then(value => value.data as string),
    errorMsg: "Error getting application current version",
    ...options
  })
};

type UpgradeApplicationParams = {
  version: string
}
export const useUpgradeApplication = (options?: UseCreateMutationWrapperOptions<boolean, UpgradeApplicationParams>) => {
  return useCreateMutation({
    mutationFn: (params: UpgradeApplicationParams) =>
      axiosClient.get("/upgrade", { params }).then(value => value.status === 200),
    successMsg: "Application is upgrading, this might take a few seconds",
    errorMsg: "Error starting application upgrade",
    ...options
  })
};

export const useUpgradeStatus = (options?: UseCreateQueryWrapperOptionsShort<boolean>) => {
  return useCreateQuery({
    queryKey: ["upgrade", "status"],
    queryFn: () => axiosClient.get("/upgrade/status").then(value => value.data as boolean),
    errorMsg: "", // this query has no error message on purpse, it supposed to fail (waiting for upgrade to finish)
    ...options
  })
};

export const useUpdateApplicationVersions = (options?: UseCreateMutationWrapperOptions<boolean, void>) => {
  return useCreateMutation({
    mutationFn: () =>
      axiosClient.get("/versions/update").then(value => value.status === 200),
    successMsg: "Application versions were updated",
    errorMsg: "Error upgrading application",
    invalidateQueries: ['versions'],
    ...options
  })
};